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
