"""Diff two snapshots of a dataset's SCD-2 store into added / removed / modified.

Provides both a one-line console summary (report_latest) and the detailed,
field-level diff + per-identity history that the HTML reports consume.
"""

import json
import re

from src import db

_FULL_COLS = ("identity_key", "number", "street", "unit", "full",
              "longitude", "latitude", "props", "payload_hash")

_CANONICAL_DISPLAY = {
    "number": "Address Number", "street": "Street", "unit": "Unit",
    "full": "Full Address", "longitude": "Location (longitude)",
    "latitude": "Location (latitude)", "location": "Location",
}

_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

# Edit-metadata props ignored in every dataset (case-insensitive): timestamps and
# editor names that change alongside any real edit (or on their own) and carry no
# address information. Curated from a scan of all tracked sources; meaningful date
# fields (OCCUPANCY_DATE, VERIFIED_DATE, ...) are deliberately not listed.
EDIT_METADATA_FIELDS = frozenset({
    "created_date", "create_date", "createdate", "created_user",
    "edit_date", "edited_date", "editdate", "dateedit", "dateupdate",
    "update_date", "updated", "lastupdate", "lasteditdate",
    "last_edited_date", "last_edited_user", "modified_date", "moddate", "adddate",
})


# ---- snapshot helpers ----

def nonskipped(ds):
    return [s for s in db.get_snapshots(ds) if not s["skipped"]]


def snap_date(s):
    m = _DATE_RE.search(s["filename"] or "")
    return m.group(1) if m else (s["downloaded"] or "")[:10]


# ---- active set ----

def _active(conn, snapshot_id):
    rows = conn.execute(
        f"SELECT {', '.join(_FULL_COLS)} FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?",
        (snapshot_id, snapshot_id)).fetchall()
    return {r["identity_key"]: dict(r) for r in rows}


def prop_keys(ds, snapshot_id):
    """Sorted distinct source-prop keys across the active rows of a snapshot."""
    conn = db.init_db(ds)
    rows = conn.execute(
        "SELECT DISTINCT je.key FROM addresses, json_each(addresses.props) AS je "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?",
        (snapshot_id, snapshot_id)).fetchall()
    conn.close()
    return sorted(r[0] for r in rows)


# ---- field-level change detection ----

def field_changes(old, new, ignore=(), field_map=None):
    """List of {field, old, new, display_field} between two row dicts.

    `ignore` is a set of source prop names (case-insensitive) whose changes are
    not counted — used to silence per-dataset noise fields (see Dataset.ignore_fields).
    Edit-metadata props (EDIT_METADATA_FIELDS) are always ignored.

    `field_map` is the dataset's canonical->source mapping (Dataset.fields). The
    canonical columns are copies of mapped source props, so when a canonical field
    changed, the matching source-prop change is dropped as a duplicate echo.
    """
    ignore = {k.lower() for k in ignore} | EDIT_METADATA_FIELDS
    out = []
    changed_canon = set()
    for f in ("number", "street", "unit", "full", "latitude", "longitude"):
        if (old.get(f) if old.get(f) != "" else None) != (new.get(f) if new.get(f) != "" else None):
            out.append({"field": f, "old": old.get(f), "new": new.get(f),
                        "display_field": _CANONICAL_DISPLAY.get(f, f)})
            changed_canon.add(f)
    echoes = {src.lower() for canon, src in (field_map or {}).items()
              if src and canon in changed_canon}
    oldp = json.loads(old.get("props") or "{}")
    newp = json.loads(new.get("props") or "{}")
    for k in sorted(set(oldp) | set(newp)):
        if k.lower() in ignore or k.lower() in echoes:
            continue
        if oldp.get(k) != newp.get(k):
            out.append({"field": k, "old": oldp.get(k), "new": newp.get(k),
                        "display_field": k})
    return out


# ---- diffs ----

def addr_sort_key(r):
    """Canonical row order: street A-Z, number numerically, unit, identity_key.

    Every list of address rows we present (added/removed/modified/baseline) is
    sorted with this key so output is deterministic across runs.
    """
    num = str(r.get("number") or "")
    m = re.match(r"\d+", num)
    return (r.get("street") or "", int(m.group()) if m else 0, num,
            r.get("unit") or "", r["identity_key"])


def compute_diff(ds, old_id, new_id):
    """Detailed diff: added / removed / modified (with per-row `changes`)."""
    conn = db.init_db(ds)
    old = _active(conn, old_id)
    new = _active(conn, new_id)
    conn.close()

    added = sorted((new[k] for k in new.keys() - old.keys()), key=addr_sort_key)
    removed = sorted((old[k] for k in old.keys() - new.keys()), key=addr_sort_key)
    modified = []
    for k in old.keys() & new.keys():
        if old[k]["payload_hash"] != new[k]["payload_hash"]:
            ch = field_changes(old[k], new[k], ds.ignore_fields, ds.fields)
            if ch:
                m = dict(new[k])
                m["changes"] = ch
                modified.append(m)
    modified.sort(key=addr_sort_key)
    return {"added": added, "removed": removed, "modified": modified}


def compute_baseline(ds, snapshot_id):
    """First snapshot: every active row counts as added."""
    conn = db.init_db(ds)
    new = _active(conn, snapshot_id)
    conn.close()
    return {"added": sorted(new.values(), key=addr_sort_key), "removed": [], "modified": []}


# ---- history ----

def compute_histories(ds, keys, before_id):
    """For each identity_key, prior add/remove events at snapshots before `before_id`.

    Returns {key: [{date, kind}]} ordered by snapshot. Empty list => first appearance.
    """
    if not keys:
        return {}
    snaps = nonskipped(ds)
    order = [s["id"] for s in snaps]
    date_of = {s["id"]: snap_date(s) for s in snaps}

    conn = db.init_db(ds)
    placeholders = ",".join("?" * len(keys))
    rows = conn.execute(
        f"SELECT identity_key, min_snapshot_id, max_snapshot_id FROM addresses "
        f"WHERE identity_key IN ({placeholders})", tuple(keys)).fetchall()
    conn.close()

    ranges = {k: [] for k in keys}
    for r in rows:
        ranges[r["identity_key"]].append((r["min_snapshot_id"], r["max_snapshot_id"]))

    # Walk the timeline and emit an event only on a presence transition, so that a
    # modification (one span closing and another opening with no gap in coverage)
    # is NOT mistaken for a remove-then-add. "added" = coverage starts here;
    # "removed" = coverage ends here.
    hist = {}
    for k, rngs in ranges.items():
        events = []
        prev = False
        for sid in order:
            if sid >= before_id:
                break
            present = any(mn <= sid <= mx for mn, mx in rngs)
            if present and not prev:
                events.append({"date": date_of.get(sid, ""), "kind": "added"})
            elif not present and prev:
                events.append({"date": date_of.get(sid, ""), "kind": "removed"})
            prev = present
        hist[k] = events
    return hist


# ---- new streets ----

def new_streets_by_snapshot(ds):
    """{snapshot_id: [{street, count}]} of streets debuting at each snapshot.

    A street "debuts" at the earliest non-skipped snapshot in which any address
    on it appears; `count` is how many addresses it debuts with. The baseline
    snapshot is excluded (every street is "new" on first import). Lists are
    ordered by count desc, then street asc.
    """
    snaps = nonskipped(ds)
    if len(snaps) < 2:
        return {}
    baseline_id = snaps[0]["id"]

    conn = db.init_db(ds)
    rows = conn.execute("""
        WITH first_seen AS (
            SELECT street, MIN(min_snapshot_id) AS first_sid
            FROM addresses
            WHERE street IS NOT NULL AND street != ''
            GROUP BY street
        )
        SELECT f.street AS street, f.first_sid AS sid, COUNT(*) AS count
        FROM first_seen f
        JOIN addresses a ON a.street = f.street AND a.min_snapshot_id = f.first_sid
        GROUP BY f.street, f.first_sid
        ORDER BY count DESC, street ASC
    """).fetchall()
    conn.close()

    out = {}
    for r in rows:
        if r["sid"] == baseline_id:
            continue
        out.setdefault(r["sid"], []).append({"street": r["street"], "count": r["count"]})
    return out


# ---- console summary (CLI) ----

def report_latest(ds):
    snaps = nonskipped(ds)
    if len(snaps) < 2:
        print(f"  only {len(snaps)} snapshot(s) — need 2 to diff")
        return None
    old, new = snaps[-2], snaps[-1]
    d = compute_diff(ds, old["id"], new["id"])
    print(f"  diff {old['id']}->{new['id']}: "
          f"+{len(d['added']):,} added, -{len(d['removed']):,} removed, "
          f"~{len(d['modified']):,} modified")
    return d
