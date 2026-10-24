"""Which row a duplicate identity_key keeps: a fixed rule, not the file's order.

db._records used to keep the first row per key in file order. Exports that reorder
between pulls then swapped the stored row back and forth - greater-sudbury key
105696 alternated between two addresses, muskoka coordinates flipped, brampton
stored SECONDARY / FRONTDOOR points for its ADDRESS_ID - each swap a fake event.
"""

import json
import os
import random
import shutil
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize
from src.registry import Dataset, _parse


def _ds(**kw):
    kw.setdefault("key_field", "ID")
    return Dataset(slug="_test_tiebreak", provider="T", data_url="x", access="static",
                   format="geojson",
                   fields={"number": "NUM", "street": "ST", "full": "FULL"}, **kw)


def _feat(id_, num, st, lon=-80.9, lat=46.5, **props):
    return {"type": "Feature",
            "properties": {"ID": id_, "NUM": num, "ST": st, "FULL": f"{num} {st}", **props},
            "geometry": {"type": "Point", "coordinates": [lon, lat]}}


def _kept(ds, feats):
    return {r["identity_key"]: (r["full"], r["longitude"]) for r in db._records(ds, feats)}


def test_the_kept_row_does_not_depend_on_file_order(capsys):
    ds = _ds()
    feats = [_feat("105696", "1545", "Redfern Street"),
             _feat("105696", "119", "Vaillancourt Crescent"),
             _feat("7", "1", "Main St", lon=-80.1),
             _feat("7", "1", "Main St", lon=-80.2),
             _feat("8", "2", "Main St")]
    want = _kept(ds, feats)
    assert want == {"105696": ("119 Vaillancourt Crescent", -80.9),   # content order
                    "7": ("1 Main St", -80.2),                          # westernmost
                    "8": ("2 Main St", -80.9)}
    rng = random.Random(1)
    for _ in range(20):
        rng.shuffle(feats)
        assert _kept(ds, feats) == want
    assert "2 duplicate identity_key rows dropped" in capsys.readouterr().out


def test_prefer_beats_content_order():
    ds = _ds(prefer=("ADDRESS_TYPE", "PRIMARY"))
    feats = [_feat("1", "10", "Main St", lon=-80.3, ADDRESS_TYPE="FRONTDOOR"),
             _feat("1", "10", "Main St", lon=-80.1, ADDRESS_TYPE=" PRIMARY "),
             _feat("1", "10", "Main St", lon=-80.2, ADDRESS_TYPE="SECONDARY")]
    for order in (feats, feats[::-1], feats[1:] + feats[:1]):
        assert _kept(ds, order) == {"1": ("10 Main St", -80.1)}


def test_prefer_falls_back_to_content_order():
    ds = _ds(prefer=("ADDRESS_TYPE", "PRIMARY"))
    feats = [_feat("1", "10", "Main St", lon=-80.1, ADDRESS_TYPE="SECONDARY"),
             _feat("1", "10", "Main St", lon=-80.2, ADDRESS_TYPE="FRONTDOOR")]
    assert _kept(ds, feats) == {"1": ("10 Main St", -80.2)}
    assert _kept(ds, feats[::-1]) == {"1": ("10 Main St", -80.2)}
    both = [_feat("1", "10", "Main St", lon=-80.1, ADDRESS_TYPE="PRIMARY"),
            _feat("1", "10", "Main St", lon=-80.2, ADDRESS_TYPE="PRIMARY")]
    assert _kept(ds, both) == _kept(ds, both[::-1]) == {"1": ("10 Main St", -80.2)}


def test_rows_differing_only_in_props_are_ordered_too():
    """Equal canonical columns and point: the stored props break the tie."""
    ds = _ds()
    a = _feat("1", "10", "Main St", POSTAL="N0B 1A0")
    b = _feat("1", "10", "Main St", POSTAL="N0B 1A1")
    assert db._records(ds, [a, b])[0]["props"] == db._records(ds, [b, a])[0]["props"]


def test_a_reordered_pull_is_a_skip(tmp_path, monkeypatch):
    """The point of it: the same rows in another order record no change."""
    ds = _ds()
    monkeypatch.setattr(Dataset, "data_dir", property(lambda self: str(tmp_path)))
    feats = [_feat("105696", "1545", "Redfern Street"),
             _feat("105696", "119", "Vaillancourt Crescent")]
    db.import_snapshot(ds, "s-2026-01-01.geojson", feats)
    db.import_snapshot(ds, "s-2026-01-02.geojson", feats[::-1])
    conn = sqlite3.connect(ds.db_path)
    assert conn.execute("SELECT skipped FROM snapshots ORDER BY id").fetchall() == [(0,), (1,)]
    conn.close()


def _write(tmp_path, identity):
    p = tmp_path / "x.toml"
    p.write_text('slug = "x"\nprovider = "X"\ndata_url = "u"\naccess = "static"\n'
                 'format = "geojson"\nignore_fields = ["WARD"]\n[identity]\n' + identity,
                 encoding="utf-8")
    return str(p)


def test_registry_parses_prefer(tmp_path):
    ds = _parse(_write(tmp_path, 'key_field = "ADDRESS_ID"\n'
                                 'prefer = {field = "ADDRESS_TYPE", value = "PRIMARY"}\n'))
    assert ds.prefer == ("ADDRESS_TYPE", "PRIMARY")
    assert _parse(_write(tmp_path, 'key_field = "ADDRESS_ID"\n')).prefer == ()


@pytest.mark.parametrize("prefer", [
    '"PRIMARY"',
    '{field = "ADDRESS_TYPE"}',
    '{field = "ADDRESS_TYPE", value = ""}',
    '{field = "ADDRESS_TYPE", value = 1}',
    '{field = "ADDRESS_TYPE", value = "PRIMARY", case = "any"}',
    '{field = "ward", value = "1"}',                   # an ignored field
])
def test_registry_rejects_bad_prefer(tmp_path, prefer):
    with pytest.raises(ValueError, match="identity.prefer"):
        _parse(_write(tmp_path, f"prefer = {prefer}\n"))


def test_brampton_prefers_its_primary_point():
    from src import registry
    assert registry.load("brampton").prefer == ("ADDRESS_TYPE", "PRIMARY")


def test_synth_props_null_literal_is_absent():
    """A synth prop holding "<Null>" keys as if absent - what the stored props hold,
    so recanonicalize can recompute it (muskoka StreetQual)."""
    ds = Dataset(slug="_t", provider="T", data_url="x", access="static", format="geojson",
                 key_field="", synth_fields=["number", "street"],
                 synth_props=["ROLL", "QUAL"], use_geometry=False,
                 fields={"number": "NUM", "street": "ST"})
    f = lambda q: {"type": "Feature",
                   "properties": {"NUM": "149", "ST": "MUSKOKA RD", "ROLL": "44", "QUAL": q},
                   "geometry": {"type": "Point", "coordinates": [-79.3, 45.0]}}
    keys = {q: normalize.canonical(ds, f(q))["identity_key"]
            for q in ("<Null>", None, "", " ", "None", "A")}
    assert keys["<Null>"] == keys[None] == keys[""] == keys[" "] == keys["None"]
    assert keys["A"] != keys[None]


# --- tools/rebuild_from_pulls.py --tiebreak ------------------------------------------

def _store(tmp_path, monkeypatch, days, gap=None, **kw):
    """Build the 'old' store under the file-order dedupe from `days` (lists of
    features), written as pulls into the dataset dir; drop the `gap` day's file."""
    import json
    from tools import rebuild_from_pulls

    def local_only(ds, filename, dump_dir=None):
        p = os.path.join(ds.data_dir, filename)
        return p if os.path.exists(p) else None
    monkeypatch.setattr(rebuild_from_pulls, "raw_path", local_only)
    monkeypatch.setattr(Dataset, "data_dir",
                        property(lambda self: str(tmp_path / self.slug)))
    ds = _ds(**kw)
    os.makedirs(ds.data_dir)
    names = []
    for i, feats in enumerate(days, 1):
        name = f"t-2026-01-{i:02d}.geojson"
        with open(os.path.join(ds.data_dir, name), "w", encoding="utf-8") as f:
            json.dump({"type": "FeatureCollection", "features": feats}, f)
        names.append(name)
    with monkeypatch.context() as m:
        m.setattr(db, "_rank", lambda pref, rec: 0)            # never displaces: file order
        for name, feats in zip(names, days):
            db.import_snapshot(ds, name, feats)
    if gap:
        os.remove(os.path.join(ds.data_dir, names[gap - 1]))
    return ds, rebuild_from_pulls


def _history(path):
    conn = sqlite3.connect(path)
    out = (conn.execute("SELECT id, skipped FROM snapshots ORDER BY id").fetchall(),
           conn.execute("SELECT identity_key, min_snapshot_id, max_snapshot_id, full "
                        "FROM addresses ORDER BY identity_key, min_snapshot_id").fetchall())
    conn.close()
    return out


_A = _feat("105696", "1545", "Redfern Street")
_B = _feat("105696", "119", "Vaillancourt Crescent")
_C = _feat("8", "2", "Main St")


def test_rebuild_tiebreak_rewrites_the_flip_flop(tmp_path, monkeypatch, capsys):
    ds, rb = _store(tmp_path, monkeypatch, [[_A, _B, _C], [_B, _A, _C], [_A, _B, _C]])
    snaps, rows = _history(ds.db_path)
    assert snaps == [(1, 0), (2, 0), (3, 0)]                 # two fake modifications
    assert [r[3] for r in rows if r[0] == "105696"] == [
        "1545 Redfern Street", "119 Vaillancourt Crescent", "1545 Redfern Street"]
    with pytest.raises(SystemExit, match="snapshot list differs"):
        rb.rebuild(ds, ds)                                   # the plain checks refuse
    tmp = rb.rebuild(ds, ds, tiebreak=True)
    snaps, rows = _history(tmp.db_path)
    assert snaps == [(1, 0), (2, 1), (3, 1)]                 # nothing ever changed
    assert [r[1:] for r in rows if r[0] == "105696"] == [(1, 1, "119 Vaillancourt Crescent")]
    out = capsys.readouterr().out
    assert "snapshot 2 (t-2026-01-02.geojson): change -> skip" in out
    assert "1 keys store another of their rows" in out


def test_rebuild_tiebreak_refuses_anything_but_a_lost_tie(tmp_path, monkeypatch):
    """A row that was not a candidate of its group in the pull is still refused."""
    ds, rb = _store(tmp_path, monkeypatch, [[_A, _B, _C]])
    conn = sqlite3.connect(ds.db_path)
    conn.execute("UPDATE addresses SET payload_hash = 'x' WHERE identity_key = '8'")
    conn.commit()
    conn.close()
    with pytest.raises(SystemExit, match="1 stored"):
        rb.rebuild(ds, ds, tiebreak=True)


def test_rebuild_tiebreak_infers_a_gap_day_from_its_brackets(tmp_path, monkeypatch):
    moved = _feat("8", "2", "Main St", lon=-80.0)
    ds, rb = _store(tmp_path, monkeypatch,
                    [[_A, _B, _C], [_B, _A, moved], [_A, _B, moved]], gap=2)
    tmp = rb.rebuild(ds, ds, tiebreak=True)
    snaps, rows = _history(tmp.db_path)
    assert snaps == [(1, 0), (2, 0), (3, 1)]
    assert [r[1:] for r in rows if r[0] == "105696"] == [(1, 2, "119 Vaillancourt Crescent")]


def test_rebuild_tiebreak_gap_assumes_only_rows_on_both_sides(tmp_path, monkeypatch, capsys):
    """Only A is on both sides of the gap, so only A is assumed present on the gap day
    beside the stored B (present by definition); "0 Zero Street", which would win, is
    on one side only and is not."""
    other = _feat("105696", "7", "Elm Street")
    a0 = _feat("105696", "0", "Zero Street")
    ds, rb = _store(tmp_path, monkeypatch,
                    [[_A, _B, a0, _C], [_B, _A, _C], [_A, other, _C]], gap=2)
    tmp = rb.rebuild(ds, ds, tiebreak=True)
    assert "1 tie candidates on both sides, 1 keys' candidates differ" in capsys.readouterr().out
    _, rows = _history(tmp.db_path)
    assert [r[1:] for r in rows if r[0] == "105696"] == [
        (1, 1, "0 Zero Street"), (2, 2, "119 Vaillancourt Crescent"),
        (3, 3, "1545 Redfern Street")]


def test_rebuild_gap_day_restores_ignored_mapped_and_volatile_columns(tmp_path, monkeypatch):
    """renfrew ignores Full_Address, the source of `full`, so its stored props cannot
    rebuild a gap day on their own; neither can a GlobalID key, which is volatile."""
    ds, rb = _store(tmp_path, monkeypatch,
                    [[_C], [_feat("8", "2", "Main St", lon=-80.0)],
                     [_feat("8", "2", "Main St", lon=-80.1)]],
                    gap=2, ignore_fields=["FULL"])
    tmp = rb.rebuild(ds, ds)
    assert _history(tmp.db_path) == _history(ds.db_path)
    gid = dict(key_field="GlobalID")
    g = lambda lon: {**_feat("x", "2", "Main St", lon=lon),
                     "properties": {**_feat("x", "2", "Main St")["properties"],
                                    "GlobalID": "{A-1}"}}
    shutil.rmtree(tmp_path / "_test_tiebreak")
    ds, rb = _store(tmp_path, monkeypatch, [[g(-80.9)], [g(-80.0)], [g(-80.1)]], gap=2, **gid)
    tmp = rb.rebuild(ds, ds)
    assert _history(tmp.db_path) == _history(ds.db_path)


def test_rebuild_keeps_a_hole_in_the_snapshot_ids(tmp_path, monkeypatch):
    """muskoka's table has no id 18 (a dropped degraded pull); the replay must not
    renumber everything after it."""
    moved = _feat("8", "2", "Main St", lon=-80.0)
    ds, rb = _store(tmp_path, monkeypatch, [[_C], [_C], [moved]])
    conn = sqlite3.connect(ds.db_path)
    conn.execute("DELETE FROM snapshots WHERE id = 2")         # a skip: no row spans it
    conn.commit()
    conn.close()
    tmp = rb.rebuild(ds, ds)
    assert _history(tmp.db_path) == _history(ds.db_path)
    assert _history(tmp.db_path)[0] == [(1, 0), (3, 0)]


def test_rebuild_stored_day_keeps_what_the_store_imported(tmp_path, monkeypatch):
    """frontenac 07-16: the vault holds a later re-fetch than the pull the store
    imported. --stored-day rebuilds that day from the store, not from the file."""
    moved = _feat("8", "2", "Main St", lon=-80.0)
    ds, rb = _store(tmp_path, monkeypatch, [[_C], [moved], [moved]])
    refetch = os.path.join(ds.data_dir, "t-2026-01-02.geojson")
    with open(refetch, "w", encoding="utf-8") as f:            # the vault's later copy
        json.dump({"type": "FeatureCollection", "features": [_C]}, f)
    with pytest.raises(SystemExit, match="snapshot list differs"):
        rb.rebuild(ds, ds)
    tmp = rb.rebuild(ds, ds, stored_days=["t-2026-01-02.geojson"])
    assert _history(tmp.db_path) == _history(ds.db_path)
    with pytest.raises(SystemExit, match="names no recorded snapshot"):
        rb.rebuild(ds, ds, stored_days=["t-2026-01-03.geojson"])  # a skip: not recorded
