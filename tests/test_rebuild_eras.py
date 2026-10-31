"""tools/rebuild_from_pulls.py --map-rev / --map-until: replaying a column rename.

The shape is lambton's (2026-09-15): the publisher renamed every column mid-history
(STNUM/STNAME/ADDRESS -> Add_Number/St_Name/full_add), the TOML was remapped the same
day, and the key basis (synth number|street + point) is the same in both eras. Under
today's map a pre-switch pull maps nothing, so the replay must hand each snapshot the
TOML of its own era.
"""

import dataclasses
import gc
import json
import os
import shutil
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize
from src.registry import Dataset
from tools import rebuild_from_pulls as rb

PRE = Dataset(slug="_test_eras", provider="Test", data_url="x", access="static",
              format="geojson", synth_fields=["number", "street"],
              fields={"number": "STNUM", "street": "STNAME", "full": "ADDRESS"},
              classes={"boundary": ["MUNICIPALITY"]})
POST = dataclasses.replace(PRE, fields={"number": "Add_Number", "street": "St_Name",
                                        "unit": "Unit", "full": "full_add"},
                           classes={"boundary": ["MUNICIPALITY", "Inc_Muni"]})
OLD = POST     # --old-rev: no rule change, today's TOML is the old rule too


def _pre(num, street, muni="Warwick"):
    return {"type": "Feature",
            "properties": {"STNUM": num, "STNAME": street, "ADDRESS": f"{num} {street}",
                           "MUNICIPALITY": muni},
            "geometry": {"type": "Point", "coordinates": [-82.0 - int(num) / 1000, 43.0]}}


def _post(num, street, muni="Warwick"):
    return {"type": "Feature",
            "properties": {"Add_Number": int(num), "St_Name": street, "Unit": None,
                           "full_add": f"{num} {street} Township of {muni} ON",
                           "Inc_Muni": muni},
            "geometry": {"type": "Point", "coordinates": [-82.0 - int(num) / 1000, 43.0]}}


# day 1 baseline, day 2 unchanged (a skip), day 3 one row edited; then the switch:
# day 4 re-hashes every row (props roster), retires 7 and adds 9; day 5 unchanged.
DAYS = [("snap-2026-01-01.geojson", PRE, [_pre("1", "Main St"), _pre("3", "Main St"),
                                          _pre("7", "Elm Rd")]),
        ("snap-2026-01-02.geojson", PRE, [_pre("1", "Main St"), _pre("3", "Main St"),
                                          _pre("7", "Elm Rd")]),
        ("snap-2026-01-03.geojson", PRE, [_pre("1", "Main St"), _pre("3", "Main St", "Brooke"),
                                          _pre("7", "Elm Rd")]),
        ("snap-2026-01-04.geojson", POST, [_post("1", "Main St"), _post("3", "Main St", "Brooke"),
                                           _post("9", "Elm Rd")]),
        ("snap-2026-01-05.geojson", POST, [_post("1", "Main St"), _post("3", "Main St", "Brooke"),
                                           _post("9", "Elm Rd")])]
SWITCH = "snap-2026-01-03.geojson"          # the last pre-switch pull


def _active(path):
    conn = sqlite3.connect(path)
    snaps = conn.execute("SELECT id, filename, skipped FROM snapshots ORDER BY id").fetchall()
    live = {sid: set(conn.execute(
        "SELECT identity_key, payload_hash, number, street, full, props FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchall())
        for sid, _, _ in snaps}
    conn.close()
    return snaps, live


@pytest.fixture
def store(monkeypatch):
    """The live store as the daily run built it: each day imported under the TOML of
    its day, every pull kept as a raw file."""
    tmp = dataclasses.replace(POST, slug=f"_rebuild_{POST.slug}")
    for d in (POST.data_dir, tmp.data_dir):
        shutil.rmtree(d, ignore_errors=True)
        assert not os.path.exists(d), f"left over from an earlier run: {d}"
    for fn, ds, feats in DAYS:
        db.import_snapshot(ds, fn, feats)
        with open(os.path.join(POST.data_dir, fn), "w", encoding="utf-8") as f:
            json.dump({"type": "FeatureCollection", "features": feats}, f)

    def local_only(ds, filename):
        p = os.path.join(ds.data_dir, filename)
        return p if os.path.exists(p) else None
    monkeypatch.setattr(rb, "raw_path", local_only)
    yield tmp
    gc.collect()        # a refusal leaves the tool's read-only connection to the store open
    for d in (POST.data_dir, tmp.data_dir):
        shutil.rmtree(d, ignore_errors=True)


def test_store_has_the_lambton_shape(store):
    snaps, live = _active(POST.db_path)
    assert [sk for _, _, sk in snaps] == [0, 1, 0, 0, 1]
    keys = {sid: {k for k, *_ in rows} for sid, rows in live.items()}
    assert len(keys[1] & keys[4]) == 2, "number|street keys survive the switch"
    assert live[1] != live[4], "the switch re-hashes every row"


def test_era_dataset_picks_the_earliest_era_the_filename_sorts_into():
    eras = [("snap-2026-01-06.geojson", "B"), (SWITCH, "A")]      # unsorted on purpose
    pick = lambda fn: rb.era_dataset(eras, "today", fn)
    assert pick("snap-2026-01-01.geojson") == "A"
    assert pick(SWITCH) == "A", "inclusive"
    assert pick("snap-2026-01-04.geojson") == "B"
    assert pick("snap-2026-01-06.geojson") == "B"
    assert pick("snap-2026-01-07.geojson") == "today"
    assert rb.era_dataset([], "today", "snap-2026-01-01.geojson") == "today"


def test_without_eras_the_pre_switch_days_do_not_replay(store):
    # today's map names no pre-switch column: number and street are null, the synth
    # key degrades to the point alone, and no stored (key, hash) pair comes back
    with pytest.raises(SystemExit, match=r"snapshot 1: 3 stored \(key, hash\) pairs missing"):
        rb.rebuild(POST, OLD)


def test_era_replay_rebuilds_the_store_row_for_row(store, capsys):
    rb.rebuild(POST, OLD, eras=[(SWITCH, PRE)])
    out = capsys.readouterr().out
    assert "eras: 1-3 -> --map-rev #1 (until snap-2026-01-03.geojson); 4-5 -> today's TOML" in out
    old_snaps, old_live = _active(POST.db_path)
    new_snaps, new_live = _active(store.db_path)
    assert new_snaps == old_snaps
    assert new_live == old_live, "every active row, canonical columns and props included"
    assert "the rebuild adds up to 0 keys per snapshot; 7 -> 7 rows" in out


def test_era_boundary_is_the_filename_not_the_schema(store):
    # one day too early: day 3 (still pre-switch) replays under today's map
    with pytest.raises(SystemExit, match=r"snapshot 3: 3 stored \(key, hash\) pairs missing"):
        rb.rebuild(POST, OLD, eras=[("snap-2026-01-02.geojson", PRE)])


def test_main_pairs_the_flags(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["rebuild_from_pulls.py", "--city", "x", "--old-rev",
                                      "HEAD", "--map-rev", "abc"])
    with pytest.raises(SystemExit):
        rb.main()
