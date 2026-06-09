"""SCD-2 import/skip/modify logic against synthetic features (no network)."""

import os
import shutil
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, diff
from src.registry import Dataset

SLUG = "_test"


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


def _active_keys(ds):
    conn = sqlite3.connect(ds.db_path)
    sid = conn.execute("SELECT MAX(id) FROM snapshots WHERE skipped=0").fetchone()[0]
    rows = conn.execute(
        "SELECT full FROM addresses WHERE max_snapshot_id=?", (sid,)).fetchall()
    conn.close()
    return sorted(r[0] for r in rows)


def main():
    ds = _ds()
    if os.path.isdir(ds.data_dir):
        shutil.rmtree(ds.data_dir)

    base = [_feat("1", "Main St", -75.1, 45.1),
            _feat("2", "Main St", -75.2, 45.2),
            _feat("3", "Oak Ave", -75.3, 45.3)]

    # 1. baseline import
    db.import_snapshot(ds, "snap-2026-01-01.geojson", base)
    assert _active_keys(ds) == ["1 Main St", "2 Main St", "3 Oak Ave"], "baseline active set"

    # 2. re-import identical content (new filename) -> recorded as skip, active unchanged
    db.import_snapshot(ds, "snap-2026-01-02.geojson", list(base))
    snaps = db.get_snapshots(ds)
    assert sum(s["skipped"] for s in snaps) == 1, "identical re-import should skip"
    assert _active_keys(ds) == ["1 Main St", "2 Main St", "3 Oak Ave"], "skip keeps active set"

    # 3. mutate: remove '3 Oak Ave', add '4 Elm Rd', modify '2 Main St' (new prop)
    mutated = [base[0],
               _feat("2", "Main St", -75.2, 45.2, extra={"NOTE": "changed"}),
               _feat("4", "Elm Rd", -75.4, 45.4)]
    db.import_snapshot(ds, "snap-2026-01-03.geojson", mutated)
    assert _active_keys(ds) == ["1 Main St", "2 Main St", "4 Elm Rd"], "mutated active set"

    # verify history preserved: '3 Oak Ave' still in table but not active
    conn = sqlite3.connect(ds.db_path)
    total = conn.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]
    oak = conn.execute(
        "SELECT min_snapshot_id, max_snapshot_id FROM addresses WHERE full='3 Oak Ave'"
    ).fetchall()
    conn.close()
    # snapshot 2 was a skip (identical) so it never extends validity. Rows:
    # 1Main(1->3 unchanged), 2Main(v1: 1->1), 2Main(v2: 3->3), 3Oak(1->1), 4Elm(3->3)
    assert total == 5, f"expected 5 history rows, got {total}"
    assert oak == [(1, 1)], f"Oak Ave last seen at snapshot 1, got {oak}"

    # 4. diff between the two real snapshots (1 and 3): +1 added, -1 removed, 1 modified
    d = diff.report_latest_silent(ds)
    assert sorted(r["full"] for r in d["added"]) == ["4 Elm Rd"], d["added"]
    assert sorted(r["full"] for r in d["removed"]) == ["3 Oak Ave"], d["removed"]
    assert sorted(m["new"]["full"] for m in d["modified"]) == ["2 Main St"], d["modified"]

    shutil.rmtree(ds.data_dir)
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
