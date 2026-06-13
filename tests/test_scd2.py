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
    snaps = diff.nonskipped(ds)
    d = diff.compute_diff(ds, snaps[0]["id"], snaps[-1]["id"])
    assert sorted(r["full"] for r in d["added"]) == ["4 Elm Rd"], d["added"]
    assert sorted(r["full"] for r in d["removed"]) == ["3 Oak Ave"], d["removed"]
    assert sorted(m["full"] for m in d["modified"]) == ["2 Main St"], d["modified"]
    # the modification carries a field-level change (the added NOTE prop)
    assert any(c["field"] == "NOTE" for m in d["modified"] for c in m["changes"]), d["modified"]

    shutil.rmtree(ds.data_dir)

    test_field_changes()
    test_categories()
    print("\nALL ASSERTIONS PASSED")


def test_field_changes():
    """Echo dedup + always-ignored edit metadata in diff.field_changes."""
    fmap = {"number": "NUM", "street": "ST", "full": "FULL"}
    old = {"number": "93", "street": "Main St", "full": "93 Main St",
           "props": '{"NUM": "93", "FULL": "93 Main St", "EDIT_DATE": 1, "NOTE": "x"}'}
    new = {"number": "97", "street": "Main St", "full": "97 Main St",
           "props": '{"NUM": "97", "FULL": "97 Main St", "EDIT_DATE": 2, "NOTE": "x"}'}
    ch = diff.field_changes(old, new, field_map=fmap)
    fields = {c["field"] for c in ch}
    # NUM/FULL props are echoes of the changed canonical columns; EDIT_DATE is metadata
    assert fields == {"number", "full"}, fields

    # a mapped prop change with NO canonical change is not an echo and must survive
    old = {"street": "McCaul St", "props": '{"ST": "Mc Caul St"}'}
    new = {"street": "McCaul St", "props": '{"ST": "McCaul St"}'}
    ch = diff.field_changes(old, new, field_map=fmap)
    assert {c["field"] for c in ch} == {"ST"}, ch


def test_categories():
    """Report-level classification of modified rows by changed-field set."""
    from src import report

    def m(*fields):
        return {"changes": [{"field": f} for f in fields]}

    assert report._category(m("latitude", "longitude")) == "location"
    assert report._category(m("location")) == "location"      # after _combine_location
    assert report._category(m("number", "full")) == "renumbered"
    assert report._category(m("number")) == "renumbered"
    assert report._category(m("street", "full")) == "renamed"
    assert report._category(m("street")) == "renamed"
    assert report._category(m("street", "number", "full")) == "significant"
    assert report._category(m("location", "PLACE_NAME")) == "significant"
    assert report._category(m("NOTE")) == "significant"

    # per-dataset classes (Dataset.classes): all changed fields inside ONE class
    classes = {"place_name": ["PLACE_NAME", "PLACE_NAME_ALL"],
               "status": ["MAINT_STAGE"], "boundary": ["WARD", "WARD_NAME"]}
    assert report._category(m("PLACE_NAME"), classes) == "place_name"
    assert report._category(m("PLACE_NAME", "PLACE_NAME_ALL"), classes) == "place_name"
    assert report._category(m("MAINT_STAGE"), classes) == "status"
    assert report._category(m("WARD", "WARD_NAME"), classes) == "boundary"
    assert report._category(m("MAINT_STAGE", "WARD"), classes) == "significant"   # cross-class mix
    assert report._category(m("PLACE_NAME", "location"), classes) == "significant"
    assert report._category(m("street"), classes) == "renamed"  # built-ins win

    # transition grouping: same old->new signature collapses into one group
    a = {"changes": [{"field": "WARD", "old": "06", "new": "18"}], "addr": "1 A St"}
    b = {"changes": [{"field": "WARD", "old": "06", "new": "18"}], "addr": "2 A St"}
    c = {"changes": [{"field": "WARD", "old": "18", "new": "06"}], "addr": "3 A St"}
    groups = report._group_transitions([a, b, c])
    assert [(g["count"], g["changes"][0]["old"]) for g in groups] == [(2, "06"), (1, "18")], groups


def test_history_coverage():
    """A modification splits the SCD-2 span, but the history must report a single
    'added' (a coverage transition) rather than a spurious remove-then-add."""
    ds = _ds()
    ds.slug = "_test_hist"
    if os.path.isdir(ds.data_dir):
        shutil.rmtree(ds.data_dir)

    db.import_snapshot(ds, "snap-2026-01-01.geojson",
                       [_feat("1", "Main St", -75.1, 45.1)])
    # modify (extra prop) -> splits into spans (1,1)+(2,2), still continuously present
    db.import_snapshot(ds, "snap-2026-01-02.geojson",
                       [_feat("1", "Main St", -75.1, 45.1, extra={"NOTE": "x"})])

    conn = sqlite3.connect(ds.db_path)
    key = conn.execute("SELECT identity_key FROM addresses LIMIT 1").fetchone()[0]
    spans = conn.execute(
        "SELECT min_snapshot_id, max_snapshot_id FROM addresses").fetchall()
    conn.close()
    assert len(spans) == 2, f"modification should split into two spans, got {spans}"

    hist = diff.compute_histories(ds, [key], before_id=999)
    kinds = [e["kind"] for e in hist[key]]
    assert kinds == ["added"], f"continuous coverage = one 'added', got {kinds}"

    shutil.rmtree(ds.data_dir)


if __name__ == "__main__":
    main()
    test_history_coverage()
