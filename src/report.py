"""Render the static HTML site: per-city dated reports, per-city index, and a
cross-city landing page (docs/index.html) for GitHub Pages.

Layout:
    docs/index.html              cross-city landing
    docs/<slug>/index.html       per-city report list
    docs/<slug>/report-<date>.html
"""

import glob
import json
import math
import os
import re
import statistics
import tomllib
from collections import Counter
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from shapely import MultiPoint, concave_hull
from shapely.geometry import mapping, shape

from src import db, diff, flags

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
SKIPPED_PATH = os.path.join(ROOT_DIR, "skipped.toml")

MAX_RENDER = 1000          # cap rows rendered per table (true counts still shown)
MASS_MIN_ROWS = 50         # a same-shaped sweep must cover this many rows...
MASS_MIN_SHARE = 0.25      # ...and this share of its section to collapse to a summary
SPARK_KEYS = ("added", "removed", "modified", "modified_location",
              "renumbered", "renamed", "place_name", "status", "boundary")

# Ontario bounding box (lon_min, lat_min, lon_max, lat_max): drops stray
# geocodes / leftover projected coords that would otherwise distort a hull.
ONT_BBOX = (-96.0, 41.0, -73.0, 57.0)
HULL_MAX_POINTS = 6000     # sample cap: a hull from this many points is visually identical
HULL_RATIO = 0.4           # concave_hull ratio: 0=most detailed, 1=convex
HULL_SIMPLIFY = 0.0008     # ~80m, trims the embedded coordinate count

_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)


def _friendly_date(d):
    try:
        return datetime.strptime(d[:10], "%Y-%m-%d").strftime("%A, %b %d, %Y")
    except (ValueError, TypeError):
        return d


def _addr(r):
    if r.get("full"):
        return r["full"]
    parts = " ".join(p for p in (r.get("number"), r.get("street")) if p).strip()
    return parts or r.get("identity_key", "")


def _bearing_arrow(dx, dy):
    if dx == 0 and dy == 0:
        return ""
    angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
    return ["→", "↗", "↑", "↖", "←", "↙", "↓", "↘"][int((angle + 22.5) // 45) % 8]


def _combine_location(m):
    """Fold latitude/longitude changes into one 'location' change with arrow+distance."""
    changes = m["changes"]
    lat_c = next((c for c in changes if c["field"] == "latitude"), None)
    lon_c = next((c for c in changes if c["field"] == "longitude"), None)
    if not (lat_c or lon_c):
        return
    new_lat, new_lon = m.get("latitude"), m.get("longitude")
    old_lat = lat_c["old"] if lat_c else new_lat
    old_lon = lon_c["old"] if lon_c else new_lon

    def _is_deg(lat, lon):
        return lat is not None and lon is not None and abs(lat) <= 90 and abs(lon) <= 180

    arrow = ""
    dist_m = None
    # Distance only makes sense between two geographic points; some imported
    # snapshots stored projected (metre) coordinates, where degree math explodes.
    if _is_deg(old_lat, old_lon) and _is_deg(new_lat, new_lon):
        mid = math.radians((old_lat + new_lat) / 2)
        dy = new_lat - old_lat
        dx = (new_lon - old_lon) * math.cos(mid)
        if abs(dy) > 1e-6 or abs(dx) > 1e-6:
            dy_m = dy * 111_320
            dx_m = (new_lon - old_lon) * 111_320 * math.cos(mid)
            dist_m = math.hypot(dx_m, dy_m)
            arrow = f"{_bearing_arrow(dx, dy)} {dist_m:.1f}m"

    def fmt(lat, lon):
        return "—" if lat is None or lon is None else f"{lat:.5f}, {lon:.5f}"

    changes = [c for c in changes if c["field"] not in ("latitude", "longitude")]
    changes.append({"field": "location", "display_field": "Location",
                    "old": fmt(old_lat, old_lon), "new": fmt(new_lat, new_lon),
                    "arrow": arrow, "dist_m": dist_m,
                    "old_pt": None if None in (old_lat, old_lon) else (old_lat, old_lon),
                    "new_pt": None if None in (new_lat, new_lon) else (new_lat, new_lon)})
    m["changes"] = changes


def _stats(d):
    street_added, street_removed, field_changes = Counter(), Counter(), Counter()
    for r in d["added"]:
        if r.get("street"):
            street_added[r["street"]] += 1
    for r in d["removed"]:
        if r.get("street"):
            street_removed[r["street"]] += 1
    for m in d["modified"]:
        for ch in m["changes"]:
            field_changes[ch.get("display_field") or ch["field"]] += 1
    MIN = 3

    def top(counter, min_count=1):
        # count desc, then name A-Z so ties are deterministic across runs
        items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
        return {k: v for k, v in items if v >= min_count}

    return {
        "top_streets_added": top(street_added, MIN),
        "top_streets_removed": top(street_removed, MIN),
        "field_changes": top(field_changes),
    }


def _sparkline_svg(values, color, width=110, height=20, pad=2):
    if not values:
        return ""
    n = len(values)
    vmax = max(values) or 1
    iw, ih = width - 2 * pad, height - 2 * pad
    xs = [pad + iw] if n == 1 else [pad + i * iw / (n - 1) for i in range(n)]
    ys = [pad + ih - (v / vmax) * ih for v in values]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return (f'<svg class="sparkline" viewBox="0 0 {width} {height}" width="{width}" '
            f'height="{height}" preserveAspectRatio="none" aria-hidden="true">'
            f'<polyline fill="none" stroke="{color}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" points="{pts}"/>'
            f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="2" fill="{color}"/></svg>')


_env.globals["sparkline_svg"] = _sparkline_svg


def _category(m, classes=None, has_number=False, has_street=False):
    """Classify a modified row by its changed-field set.

    Works both before and after _combine_location (raw latitude/longitude or the
    combined 'location' pseudo-field). 'full' is derived from number+street, so it
    rides along with either; number takes precedence (matches the sibling Toronto
    tracker's renumbered category).

    'full' changing *alone* is read against what the dataset actually maps
    (`has_number` / `has_street`). Where a component is unmapped, a real edit to it can
    only ever surface in the assembled string - waterloo publishes no number column, so
    a renumber there is a full-only change. Where both are mapped, neither moved, and
    the row is the publisher restyling the string: renfrew reformatted 1,104 highway
    addresses from "17883 Highway 60" to "17883 60 Highway" on 2026-06-13, with
    Add_Number and St_Name untouched.

    `classes` is Dataset.classes: per-city class -> source prop names. A row whose
    changes all fall inside one class lands in that class; any mix stays significant.
    """
    fields = {c["field"] for c in m["changes"]}
    if fields <= {"latitude", "longitude", "location"}:
        return "location"
    if fields == {"full"}:
        if not has_number:
            return "renumbered"
        if not has_street:
            return "renamed"
    elif fields <= {"number", "full"}:
        return "renumbered"
    elif fields <= {"street", "full"}:
        return "renamed"
    for cls, srcs in (classes or {}).items():
        if fields <= set(srcs):
            return cls
    return "significant"


def _group_renames(renamed):
    """Group street renames by (old, new) street: one upstream rename event covers
    every address on the street, so present it once with a count."""
    groups = {}
    for m in renamed:
        ch = next(c for c in m["changes"] if c["field"] == "street")
        groups.setdefault((ch["old"] or "—", ch["new"] or "—"), []).append(m)
    out = [{"old": o, "new": n, "count": len(rows), "rows": rows[:MAX_RENDER]}
           for (o, n), rows in groups.items()]
    out.sort(key=lambda g: (-g["count"], g["old"]))
    return out


# A child of a split: the base civic number plus a short letter suffix ("127A",
# "127 B", "12AA") or the Ontario half-number ("127 1/2").
_SPLIT_SUFFIX_RE = re.compile(r"^(\d+)\s*([A-Za-z]{1,2}|1/2)$")


def _unit_sort_key(r):
    u = str(r.get("unit") or "")
    return (0, int(u), u) if u.isdigit() else (1, 0, u)


def _split_children_label(kind, rows):
    if kind == "suffix":
        nums = [str(r.get("number") or "") for r in rows]
        return ", ".join(nums[:8]) + (", …" if len(nums) > 8 else "")
    units = [str(r.get("unit") or "") for r in sorted(rows, key=_unit_sort_key)]
    ints = sorted(int(u) for u in units) if all(u.isdigit() for u in units) else None
    if ints and len(ints) > 2 and ints == list(range(ints[0], ints[-1] + 1)):
        return f"{len(units)} units ({ints[0]}–{ints[-1]})"
    listed = ", ".join(units[:8]) + (", …" if len(units) > 8 else "")
    return f"{len(units)} units ({listed})"


def _group_splits(added, removed, bases_active_fn):
    """Group added rows into address-split events: one base address turning into
    suffixed siblings (127 -> 127A + 127B) or into units (127 -> units 1-30).

    Display-level only, like _category: the rows keep their place in the added
    count, they just render as one event instead of N disconnected table rows.
    `bases_active_fn(pairs)` reports which (number, street) bases still exist in
    the new snapshot, so the event can say whether the original address was
    retired (subdivision), remains (infill/severance), or was never on record
    (new multi-unit building).
    """
    suffix, units, rest = {}, {}, []
    for r in added:
        number = str(r.get("number") or "").strip()
        if r.get("unit") and number:
            units.setdefault((number, r.get("street")), []).append(r)
            continue
        m = _SPLIT_SUFFIX_RE.match(number)
        if m and r.get("street"):
            suffix.setdefault((m.group(1), r.get("street")), []).append(r)
        else:
            rest.append(r)

    cands = []
    for (base, street), rows in suffix.items():
        if len(rows) >= 2:
            cands.append(("suffix", base, street, sorted(rows, key=diff.addr_sort_key)))
        else:
            rest.extend(rows)
    for (base, street), rows in units.items():
        if len({r.get("unit") for r in rows}) >= 2:
            cands.append(("unit", base, street, sorted(rows, key=_unit_sort_key)))
        else:
            rest.extend(rows)

    removed_bases = {(str(r.get("number") or "").strip(), r.get("street"))
                     for r in removed if not r.get("unit")}
    pending = [(b, s) for _, b, s, _ in cands if (b, s) not in removed_bases]
    still_active = bases_active_fn(pending) if pending else set()

    groups = []
    for kind, base, street, rows in cands:
        parent = ("retired" if (base, street) in removed_bases
                  else "remains" if (base, street) in still_active else "none")
        groups.append({"kind": kind, "base_addr": f"{base} {street or ''}".strip(),
                       "count": len(rows), "rows": rows, "parent": parent,
                       "children_label": _split_children_label(kind, rows)})
    groups.sort(key=lambda g: (-g["count"], g["base_addr"]))
    rest.sort(key=diff.addr_sort_key)
    return groups, rest


def _group_transitions(mods):
    """Group status/boundary modifications by their exact change signature: one
    upstream decision (redistricting, lifecycle stage flip) covers many addresses,
    so present each distinct old->new transition once with a count."""
    groups = {}
    for m in mods:
        key = tuple(sorted((c["field"], str(c["old"]), str(c["new"]))
                           for c in m["changes"]))
        groups.setdefault(key, []).append(m)
    out = [{"changes": rows[0]["changes"], "count": len(rows), "rows": rows[:MAX_RENDER]}
           for rows in groups.values()]
    out.sort(key=lambda g: (-g["count"],
                            [(c["field"], str(c["old"])) for c in g["changes"]]))
    return out


def _collapse_mass(mods):
    """Split a section into mass events and the remaining one-off rows.

    One upstream sweep (field recode, bulk renumbering) shows up as the same
    changed-field-set on a large share of a section; row by row in a capped
    table it reads as noise, so present each such sweep once with a count."""
    groups = {}
    for m in mods:
        key = tuple(sorted(c.get("display_field") or c["field"] for c in m["changes"]))
        groups.setdefault(key, []).append(m)
    mass, rest = [], []
    for key, rows in groups.items():
        if len(rows) > MASS_MIN_ROWS and len(rows) > len(mods) * MASS_MIN_SHARE:
            mass.append({"fields": list(key), "count": len(rows),
                         "rows": rows[:MAX_RENDER]})
        else:
            rest.extend(rows)
    mass.sort(key=lambda g: (-g["count"], g["fields"]))
    rest.sort(key=diff.addr_sort_key)
    return mass, rest


def _location_mass(rows):
    """Summary stats when a bulk re-geocode moved a large share of the city.
    The section is homogeneous (every row is one location change), so the
    mass trigger reduces to the row-count threshold."""
    if len(rows) <= MASS_MIN_ROWS:
        return None
    dists = [c["dist_m"] for m in rows for c in m["changes"]
             if c["field"] == "location" and c.get("dist_m") is not None]
    return {"count": len(rows),
            "median_m": statistics.median(dists) if dists else None,
            "max_m": max(dists) if dists else None}


def _prepare(ds, d, new_id, is_baseline=False):
    """Cap rows, attach addr + history, split modifications into categories."""
    for r in d["added"] + d["removed"]:
        r["addr"] = _addr(r)

    # Split events (127 -> 127A + 127B, or 127 -> 30 units) are meaningless on a
    # baseline, where every suffixed address that ever existed arrives at once.
    if is_baseline:
        split_groups, added_rest = [], d["added"]
    else:
        split_groups, added_rest = _group_splits(
            d["added"], d["removed"],
            lambda pairs: diff.bases_active(ds, pairs, new_id))
    for m in d["modified"]:
        m["addr"] = _addr(m)
        _combine_location(m)

    cats = {"significant": [], "location": [], "renumbered": [], "renamed": [],
            "place_name": [], "status": [], "boundary": []}
    for m in d["modified"]:
        cats[_category(m, ds.classes, bool(ds.fields.get("number")),
                       bool(ds.fields.get("street")))].append(m)

    counts = {"added": len(d["added"]), "removed": len(d["removed"]),
              "modified": len(cats["significant"]),
              "modified_location": len(cats["location"]),
              "renumbered": len(cats["renumbered"]),
              "renamed": len(cats["renamed"]),
              "place_name": len(cats["place_name"]),
              "status": len(cats["status"]),
              "boundary": len(cats["boundary"]),
              "split": len(split_groups)}

    added = added_rest[:MAX_RENDER]
    removed = d["removed"][:MAX_RENDER]
    modified_mass, modified_rest = _collapse_mass(cats["significant"])
    modified = modified_rest[:MAX_RENDER]
    location_mass = _location_mass(cats["location"])
    location_only = cats["location"][:MAX_RENDER]
    renumbered_mass, renumbered_rest = _collapse_mass(cats["renumbered"])
    renumbered = renumbered_rest[:MAX_RENDER]
    renamed_groups = _group_renames(cats["renamed"])
    place_name = cats["place_name"][:MAX_RENDER]
    status_groups = _group_transitions(cats["status"])
    boundary_groups = _group_transitions(cats["boundary"])

    # history only for the rows we actually render
    split_children = [r for g in split_groups for r in g["rows"]]
    keys = [r["identity_key"] for r in added + removed + split_children]
    hist = diff.compute_histories(ds, keys, new_id)
    for r in added + removed + split_children:
        r["history"] = hist.get(r["identity_key"], [])

    return {"added": added, "removed": removed, "modified": modified,
            "split_groups": split_groups, "added_rest_count": len(added_rest),
            "modified_mass": modified_mass, "modified_rest_count": len(modified_rest),
            "location": location_only, "location_mass": location_mass,
            "renumbered": renumbered, "renumbered_mass": renumbered_mass,
            "renumbered_rest_count": len(renumbered_rest),
            "renamed_groups": renamed_groups, "place_name": place_name,
            "status_groups": status_groups, "boundary_groups": boundary_groups,
            "counts": counts}


_CANON_LABEL = {"number": "Street number", "street": "Street name",
                "unit": "Unit", "full": "Full address"}

# Humanized index labels for the category counts, in display priority order.
# "split" counts events (one base address -> N children), not rows; the child
# rows are already inside the added count, so it never feeds the changed sum.
_CAT_LABELS = (
    ("split", "address split", "address splits"),
    ("renamed", "street rename", "street renames"),
    ("place_name", "place rename", "place renames"),
    ("boundary", "boundary change", "boundary changes"),
    ("status", "status change", "status changes"),
    ("renumbered", "renumbered", "renumbered"),
    ("modified_location", "moved", "moved"),
)


def _cat_phrases(counts):
    """['2 place renames', '19 status changes', ...] for the nonzero categories."""
    out = []
    for key, sing, plur in _CAT_LABELS:
        n = counts.get(key, 0)
        if n:
            out.append(f"{n:,} {sing if n == 1 else plur}")
    return out


def _compared_fields(ds, prop_keys):
    """Exact list of the fields change detection compares, for the info popup.

    Canonical mapped fields first (labelled, with source name), then every
    remaining source prop key seen in the latest snapshot, minus ignored.
    """
    out = [f"{_CANON_LABEL[k]} ({src})"
           for k in ("number", "street", "unit", "full") if (src := ds.fields.get(k))]
    out.append("Coordinates (latitude, longitude)")
    seen = {src.lower() for src in ds.fields.values() if src}
    seen |= {f.lower() for f in ds.ignore_fields}
    seen |= diff.EDIT_METADATA_FIELDS
    out += [k for k in prop_keys if k.lower() not in seen]
    return out


def _render_report(ds, snap, d, is_baseline, spark, source_url, compared, ignored):
    p = _prepare(ds, d, snap["id"], is_baseline)
    counts = p["counts"]
    date = diff.snap_date(snap)
    ctx = {
        "compared_fields": compared, "ignored_fields": ignored,
        "provider": ds.provider, "license_name": ds.license_name,
        "generated": datetime.now().strftime("%b %d, %Y at %I:%M %p"),
        "new_snapshot": snap, "new_date_friendly": _friendly_date(date),
        "old_date_friendly": "", "is_baseline": is_baseline,
        "added": p["added"], "removed": p["removed"], "modified": p["modified"],
        "split_groups": p["split_groups"], "added_rest_count": p["added_rest_count"],
        "modified_mass": p["modified_mass"], "modified_rest_count": p["modified_rest_count"],
        "modified_location": p["location"], "location_mass": p["location_mass"],
        "renumbered": p["renumbered"], "renumbered_mass": p["renumbered_mass"],
        "renumbered_rest_count": p["renumbered_rest_count"],
        "renamed_groups": p["renamed_groups"],
        "place_name": p["place_name"], "status_groups": p["status_groups"],
        "boundary_groups": p["boundary_groups"],
        "configured_classes": set(ds.classes),
        "added_count": counts["added"], "removed_count": counts["removed"],
        "modified_count": counts["modified"], "modified_location_count": counts["modified_location"],
        "renumbered_count": counts["renumbered"], "renamed_count": counts["renamed"],
        "place_name_count": counts["place_name"], "status_count": counts["status"],
        "boundary_count": counts["boundary"],
        "stats": _stats(d), "sparklines": spark, "source_url": source_url,
    }
    html = _env.get_template("report.html").render(**ctx)
    out = os.path.join(DOCS_DIR, ds.slug, f"report-{date}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return counts


def _spark_series(history, idx):
    """Trailing 7 values for each key ending at report index idx."""
    lo = max(0, idx - 6)
    return {k: [history[k][j] for j in range(lo, idx + 1)] for k in SPARK_KEYS}


def generate_all(datasets):
    os.makedirs(DOCS_DIR, exist_ok=True)
    open(os.path.join(DOCS_DIR, ".nojekyll"), "w").close()
    cities = []
    ledger = flags.load_ledger()

    for ds in datasets:
        snaps = diff.nonskipped(ds)
        if not snaps:
            continue
        os.makedirs(os.path.join(DOCS_DIR, ds.slug), exist_ok=True)
        source_url = _source_url(ds)

        # chronological diffs: baseline first, then each consecutive pair
        diffs = [(snaps[0], diff.compute_baseline(ds, snaps[0]["id"]), True)]
        for i in range(len(snaps) - 1):
            diffs.append((snaps[i + 1],
                          diff.compute_diff(ds, snaps[i]["id"], snaps[i + 1]["id"]), False))

        # Flag suspicious events (idempotent by key, so a full re-render also
        # retro-flags history), then hold flagged events off the public pages.
        # Holds run before series/counts so sparklines match what is shown.
        detected = []
        for i in range(len(snaps) - 1):
            found = flags.detect(ds, diffs[i + 1][1], snaps[i]["row_count"])
            detected += flags.stamp(found, ds.slug, diff.snap_date(snaps[i + 1]))
        appended = flags.record(detected)
        if appended:
            ledger = flags.load_ledger()
            for fl in appended:
                print(f"  FLAGGED {fl['slug']} {fl['date']}: "
                      f"{fl['signature']} — {fl['scope']}")

        added_held_sids = set()
        held_diffs = [diffs[0]]
        for snap, d, _ in diffs[1:]:
            held = flags.holds_for(ledger, ds.slug, diff.snap_date(snap))
            d, notes = flags.apply_holds(d, held)
            for sig, text in notes:
                print(f"  {ds.slug} {diff.snap_date(snap)}: {text}")
                if sig == "mass-added":
                    added_held_sids.add(snap["id"])
            held_diffs.append((snap, d, False))
        diffs = held_diffs

        new_by_snap = diff.new_streets_by_snapshot(ds)
        # Street debuts come from the store, not the diff, so a held mass-add
        # would still leak its streets into the city index without this.
        for sid in added_held_sids:
            new_by_snap.pop(sid, None)
        pkeys = diff.prop_keys(ds, snaps[-1]["id"])
        compared = _compared_fields(ds, pkeys)
        # A mapped source column can be ignored as a prop (renfrew's Full_Address churns
        # on padding the canonical strips) while the canonical field it feeds is still
        # compared. Listing it as ignored would contradict the compared list above it.
        mapped = {src.lower() for src in ds.fields.values() if src}
        ignored = sorted({f for f in ds.ignore_fields if f.lower() not in mapped} |
                         {k for k in pkeys if k.lower() in diff.EDIT_METADATA_FIELDS})

        series = {k: [] for k in SPARK_KEYS}  # filled as we render, for sparklines
        meta = []
        for idx, (snap, d, is_base) in enumerate(diffs):
            cat = Counter(_category(m, ds.classes, bool(ds.fields.get("number")),
                                    bool(ds.fields.get("street")))
                          for m in d["modified"])
            series["added"].append(len(d["added"]))
            series["removed"].append(len(d["removed"]))
            series["modified"].append(cat["significant"])
            series["modified_location"].append(cat["location"])
            for k in ("renumbered", "renamed", "place_name", "status", "boundary"):
                series[k].append(cat[k])

        for idx, (snap, d, is_base) in enumerate(diffs):
            counts = _render_report(ds, snap, d, is_base, _spark_series(series, idx), source_url,
                                    compared, ignored)
            date = diff.snap_date(snap)
            changed = (counts["modified"] + counts["modified_location"]
                       + counts["renumbered"] + counts["renamed"]
                       + counts["place_name"] + counts["status"] + counts["boundary"])
            meta.append({
                "date": date, "friendly_date": _friendly_date(date),
                "filename": f"report-{date}.html", "is_baseline": is_base,
                "added": counts["added"], "removed": counts["removed"],
                "modified": counts["modified"], "changed": changed,
                "phrases": _cat_phrases(counts),
                "new_streets": new_by_snap.get(snap["id"], []),
            })

        meta.reverse()                       # newest first
        if meta:
            meta[0]["is_latest"] = not meta[0]["is_baseline"]

        # The most recent run may have found no changes (a skipped snapshot newer
        # than the latest real report). Surface that check date as an inactive
        # "No changes" row, matching the sibling Toronto tracker's index.
        all_snaps = db.get_snapshots(ds)
        if all_snaps:
            last_date = diff.snap_date(all_snaps[-1])
            if last_date > meta[0]["date"]:
                meta.insert(0, {
                    "date": last_date, "friendly_date": _friendly_date(last_date),
                    "filename": None, "is_baseline": False,
                    "added": 0, "removed": 0, "modified": 0, "changed": 0,
                    "phrases": [], "new_streets": [],
                })

        # flatten new-street debuts across reports, newest first, cap at 15
        recent_new_streets = [
            {"street": s["street"], "count": s["count"],
             "filename": m["filename"], "friendly_date": m["friendly_date"]}
            for m in meta for s in m["new_streets"]
        ][:15]

        with open(os.path.join(DOCS_DIR, ds.slug, "index.html"), "w", encoding="utf-8") as f:
            f.write(_env.get_template("city_index.html").render(
                provider=ds.provider, license_name=ds.license_name,
                source_url=source_url, reports=meta,
                recent_new_streets=recent_new_streets,
                compared_fields=compared, ignored_fields=ignored))

        latest = meta[0]
        # "No changes ever observed": no non-baseline report found any add/remove/
        # change (baseline-only cities qualify — they have no non-baseline reports).
        no_changes = sum(m["added"] + m["removed"] + m["changed"]
                         for m in meta if not m["is_baseline"]) == 0
        card = {
            "slug": ds.slug, "provider": ds.provider, "license_name": ds.license_name,
            "row_count": snaps[-1]["row_count"], "last_date": diff.snap_date(snaps[-1]),
            "added": latest["added"], "removed": latest["removed"], "modified": latest["changed"],
            "highlight": "" if latest["is_baseline"] else " · ".join(latest["phrases"][:2]),
            "has_changes": not latest["is_baseline"],
            "report_count": sum(1 for m in meta if m["filename"]),
            "compared_fields": compared, "ignored_fields": ignored,
            "no_changes": no_changes, "hull": _hull_geometry(ds),
        }
        cities.append(card)
        # Persist the landing card so a single-city update still leaves the
        # cross-city landing complete (it's rebuilt from every city's card below).
        with open(os.path.join(DOCS_DIR, ds.slug, "_card.json"), "w", encoding="utf-8") as f:
            json.dump(card, f)

    # Landing lists every city that has a persisted card, not just the ones
    # rendered this run, so `update --city X` doesn't clobber it to one city.
    rendered = {c["slug"] for c in cities}
    for path in glob.glob(os.path.join(DOCS_DIR, "*", "_card.json")):
        if os.path.basename(os.path.dirname(path)) not in rendered:
            with open(path, encoding="utf-8") as f:
                cities.append(json.load(f))

    cities.sort(key=lambda c: c["provider"])
    total_addresses = sum(c["row_count"] for c in cities)
    map_features = _map_features(cities)
    with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(_env.get_template("cities.html").render(
            cities=cities, skipped=_load_skipped(),
            total_addresses=total_addresses, map_features=map_features))
    print(f"\nwrote site for {len(cities)} dataset(s) to {DOCS_DIR}")
    generate_flags_page()


def generate_flags_page():
    """Back-office flags page (logs/flags.html): open flags oldest-first, then
    reviewed history. Deliberately outside docs/ — suspicions are the
    operator's, the public site carries only verified claims (same line the
    vault report and refusal blocks live behind)."""
    ledger = flags.load_ledger()
    today = datetime.now().date()

    def age(fl):
        try:
            return (today - datetime.strptime(fl.get("detected", ""), "%Y-%m-%d").date()).days
        except ValueError:
            return None

    open_flags = sorted((f for f in ledger if f.get("status", "open") != "reviewed"),
                        key=lambda f: (f.get("detected", ""), f.get("slug", "")))
    for f in open_flags:
        f["age_days"] = age(f)
    reviewed = sorted((f for f in ledger if f.get("status") == "reviewed"),
                      key=lambda f: (f.get("reviewed", ""), f.get("slug", "")),
                      reverse=True)
    by_city = Counter(f["slug"] for f in ledger)
    verdicts = Counter(f.get("verdict", "") for f in reviewed)

    os.makedirs(LOGS_DIR, exist_ok=True)
    out = os.path.join(LOGS_DIR, "flags.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(_env.get_template("flags.html").render(
            open_flags=open_flags, reviewed=reviewed,
            by_city=by_city.most_common(), verdicts=verdicts,
            generated=datetime.now().strftime("%b %d, %Y at %I:%M %p")))
    if open_flags:
        print(f"{len(open_flags)} open flag(s) awaiting review -> {out}")
    return len(open_flags)


def _map_features(cities):
    """FeatureCollection of city hulls, smaller polygons drawn last (on top).

    Regional/county datasets geographically swallow a city inside them (e.g.
    Wellington over Guelph, Peel over Brampton). Drawn as raw overlapping
    polygons the larger one sits on top and intercepts every click, leaving the
    inner city unreachable. Emitting features largest-area-first puts the
    smaller, more specific city on top so it stays clickable, while the
    container stays clickable everywhere it doesn't overlap. We deliberately do
    not cut holes: a hull can't tell a separated city excluded from its county
    (a true gap, e.g. Guelph) from a two-tier region that does include the city
    (Peel/Brampton), so carving would misrepresent the latter's coverage.
    """
    feats = [(shape(c["hull"]).area,
              {"type": "Feature", "geometry": c["hull"],
               "properties": {"name": c["provider"], "slug": c["slug"],
                              "no_changes": bool(c.get("no_changes"))}})
             for c in cities if c.get("hull")]
    feats.sort(key=lambda t: -t[0])     # largest first => smaller drawn on top & clickable
    return {"type": "FeatureCollection", "features": [f for _, f in feats]}


def _load_skipped():
    """Sources probed but not added, for the landing page. Empty if no file."""
    if not os.path.exists(SKIPPED_PATH):
        return []
    with open(SKIPPED_PATH, "rb") as f:
        return tomllib.load(f).get("skipped", [])


def _source_url(ds):
    # ArcGIS layers have a browsable HTML page at their REST URL.
    return ds.data_url if ds.access == "arcgis" else ""


def _round_coords(obj, ndigits=5):
    """Round every coordinate float in a GeoJSON geometry to trim payload."""
    if isinstance(obj, float):
        return round(obj, ndigits)
    if isinstance(obj, (list, tuple)):
        return [_round_coords(x, ndigits) for x in obj]
    return obj


def _hull_geometry(ds):
    """Concave-hull GeoJSON geometry around a city's active address points.

    We track points, not municipal boundaries, so the observed coverage area is
    derived as a concave hull of the latest snapshot's points. Returns a GeoJSON
    geometry dict, or None when there are too few usable points.
    """
    lo_lon, lo_lat, hi_lon, hi_lat = ONT_BBOX
    pts = [(x, y) for (x, y) in db.active_points(ds)
           if lo_lon <= x <= hi_lon and lo_lat <= y <= hi_lat]
    if len(pts) < 3:
        return None
    if len(pts) > HULL_MAX_POINTS:           # even stride = spatially uniform sample
        step = len(pts) / HULL_MAX_POINTS
        pts = [pts[int(i * step)] for i in range(HULL_MAX_POINTS)]
    hull = concave_hull(MultiPoint(pts), ratio=HULL_RATIO).simplify(HULL_SIMPLIFY)
    if hull.is_empty or hull.geom_type not in ("Polygon", "MultiPolygon"):
        return None
    geom = mapping(hull)
    geom["coordinates"] = _round_coords(geom["coordinates"])
    return geom
