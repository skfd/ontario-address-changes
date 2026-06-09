"""Diff two snapshots of a dataset's SCD-2 store into added / removed / modified."""

from src import db

_FIELDS = ("identity_key", "number", "street", "unit", "full",
           "longitude", "latitude", "payload_hash")


def _active(conn, snapshot_id):
    """Rows valid at a given snapshot id, keyed by identity_key."""
    rows = conn.execute(
        f"SELECT {', '.join(_FIELDS)} FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?",
        (snapshot_id, snapshot_id)).fetchall()
    return {r["identity_key"]: dict(r) for r in rows}


def compute_diff(ds, old_id, new_id):
    conn = db.init_db(ds)
    old = _active(conn, old_id)
    new = _active(conn, new_id)
    conn.close()

    added = [new[k] for k in new.keys() - old.keys()]
    removed = [old[k] for k in old.keys() - new.keys()]
    modified = [{"old": old[k], "new": new[k]} for k in old.keys() & new.keys()
                if old[k]["payload_hash"] != new[k]["payload_hash"]]
    return {"added": added, "removed": removed, "modified": modified}


def latest_two(ds):
    """The two most recent non-skipped snapshot rows (old, new), or None."""
    snaps = [s for s in db.get_snapshots(ds) if not s["skipped"]]
    if len(snaps) < 2:
        return None
    return snaps[-2], snaps[-1]


def report_latest_silent(ds):
    """Latest-pair diff dict, or None if fewer than two snapshots. No output."""
    pair = latest_two(ds)
    if pair is None:
        return None
    old, new = pair
    return compute_diff(ds, old["id"], new["id"])


def report_latest(ds):
    """Print a one-line delta for the latest pair; returns the diff dict or None."""
    pair = latest_two(ds)
    if pair is None:
        n = len([s for s in db.get_snapshots(ds) if not s["skipped"]])
        print(f"  only {n} snapshot(s) — need 2 to diff")
        return None
    old, new = pair
    d = compute_diff(ds, old["id"], new["id"])
    print(f"  diff {old['id']}->{new['id']}: "
          f"+{len(d['added']):,} added, -{len(d['removed']):,} removed, "
          f"~{len(d['modified']):,} modified")
    return d
