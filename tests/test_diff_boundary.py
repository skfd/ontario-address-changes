"""compute_diff reads only the spans that end or start between two snapshots.

The reference is the full-active-set comparison it replaced: every pair of
real snapshots, consecutive or not, must diff the same both ways, across a
skipped pull, a modification, a removal and a re-add of identical content.
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, diff
from src.registry import Dataset

SLUG = "_test_boundary"


def _ds():
    return Dataset(slug=SLUG, provider="Test", data_url="x", access="static",
                   format="geojson", key_field="", synth_fields=["full"],
                   fields={"number": "NUM", "street": "ST", "full": "FULL"})


def _feat(num, st, lon, lat, extra=None):
    props = {"NUM": num, "ST": st, "FULL": f"{num} {st}"}
    if extra:
        props.update(extra)
    return {"type": "Feature", "properties": props,
            "geometry": {"type": "Point", "coordinates": [lon, lat]}}


def _reference_diff(ds, old_id, new_id):
    """The pre-2026-10-19 compute_diff: both whole active sets, compared."""
    conn = db.init_db(ds)
    old = diff._active(conn, old_id)
    new = diff._active(conn, new_id)
    conn.close()
    added = sorted((new[k] for k in new.keys() - old.keys()), key=diff.addr_sort_key)
    removed = sorted((old[k] for k in old.keys() - new.keys()), key=diff.addr_sort_key)
    modified = []
    for k in old.keys() & new.keys():
        if old[k]["payload_hash"] != new[k]["payload_hash"]:
            ch = diff.field_changes(old[k], new[k], ds.ignore_fields, ds.fields)
            if ch and not diff._below_location_floor(ds, old[k], new[k], ch):
                m = dict(new[k])
                m["changes"] = ch
                modified.append(m)
    modified.sort(key=diff.addr_sort_key)
    return {"added": added, "removed": removed, "modified": modified}


def test_boundary_diff_matches_full_active_sets():
    ds = _ds()
    if os.path.isdir(ds.data_dir):
        shutil.rmtree(ds.data_dir)
    a = _feat("1", "Main St", -75.1, 45.1)
    b = _feat("2", "Main St", -75.2, 45.2)
    b2 = _feat("2", "Main St", -75.2, 45.2, extra={"NOTE": "changed"})
    c = _feat("3", "Oak Ave", -75.3, 45.3)
    d = _feat("4", "Elm Rd", -75.4, 45.4)
    e = _feat("5", "Elm Rd", -75.5, 45.5)
    f = _feat("6", "Elm Rd", -75.6, 45.6)
    days = [
        [a, b, c, d],
        [a, b, c, d],          # identical -> a skipped pull between real ones
        [a, b2, d, e],         # b modified, c removed, e added
        [a, b2, c, d, e],      # c back with identical content
        [a, b2, c, e, f],      # d removed, f added
    ]
    try:
        for i, feats in enumerate(days, 1):
            db.import_snapshot(ds, f"snap-2026-01-{i:02d}.geojson", list(feats))
        assert sum(s["skipped"] for s in db.get_snapshots(ds)) == 1, "day 2 should skip"

        ids = [s["id"] for s in diff.nonskipped(ds)]
        assert len(ids) == 4
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                got = diff.compute_diff(ds, ids[i], ids[j])
                want = _reference_diff(ds, ids[i], ids[j])
                assert got == want, f"pair {ids[i]}->{ids[j]}: {got} != {want}"

        # Spot-check the content, so the two cannot agree on being wrong.
        first, after_skip = ids[0], ids[1]
        dd = diff.compute_diff(ds, first, after_skip)
        assert [r["full"] for r in dd["added"]] == ["5 Elm Rd"]
        assert [r["full"] for r in dd["removed"]] == ["3 Oak Ave"]
        assert [m["full"] for m in dd["modified"]] == ["2 Main St"]
        back = diff.compute_diff(ds, ids[1], ids[2])
        assert [r["full"] for r in back["added"]] == ["3 Oak Ave"], back
        span = diff.compute_diff(ds, ids[0], ids[3])
        assert [r["full"] for r in span["added"]] == ["5 Elm Rd", "6 Elm Rd"], span
        assert [r["full"] for r in span["removed"]] == ["4 Elm Rd"], span

        # The start index must serve the diff and nothing else: a plain index on
        # min_snapshot_id took over every "active at S" query and turned each into
        # a scan of all history (the 2026-10-19 render that ran past an hour).
        conn = db.init_db(ds)
        def plan(sql, args):
            return " ".join(r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + sql, args))
        active = plan("SELECT * FROM addresses WHERE min_snapshot_id <= ? "
                      "AND max_snapshot_id >= ?", (ids[-1], ids[-1]))
        started = plan("SELECT * FROM addresses WHERE min_snapshot_id + 0 > ? "
                       "AND min_snapshot_id + 0 <= ? AND max_snapshot_id >= ?",
                       (ids[0], ids[1], ids[1]))
        conn.close()
        assert "idx_addr_active" in active, active
        assert "idx_addr_start" in started, started
    finally:
        shutil.rmtree(ds.data_dir, ignore_errors=True)


if __name__ == "__main__":
    test_boundary_diff_matches_full_active_sets()
    print("ALL ASSERTIONS PASSED")
