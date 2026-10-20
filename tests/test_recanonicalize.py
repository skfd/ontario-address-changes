"""Canonical null literals, number_unit_from_full, and tools/recanonicalize.py.

The migration's promise is that the next import after it is a no-op: a store built
under the old rules, rewritten, then fed the same pull again must record nothing.
"""

import os
import shutil
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize
from src.normalize import number_unit_from_full
from src.registry import Dataset, _parse
from tools import recanonicalize


@pytest.mark.parametrize("full, street, number, unit", [
    # real waterloo shapes
    ("29 BARREL YARDS BLVD 1205", "BARREL YARDS BLVD", "29", "1205"),
    ("300 REGINA ST N 2 204", "REGINA ST N", "300", "2 204"),
    ("25 WESTMOUNT RD N PH B", "WESTMOUNT RD N", "25", "PH B"),
    ("345-347 ERB ST W", "ERB ST W", "345-347", None),
    ("653 albert st a", "ALBERT ST", "653", "a"),            # case-insensitive anchor
    # the street not in the address: leading number only, no unit guessed
    ("526B BROOKMILL CRES", "BEAVER CREEK RD", "526B", None),
    ("526B BROOKMILL CRES", None, "526B", None),
    ("BROOKMILL CRES", "BROOKMILL CRES", None, None),          # nothing in front
    ("70", "MAIN ST", None, None),
    (None, "MAIN ST", None, None),
])
def test_number_unit_from_full(full, street, number, unit):
    assert number_unit_from_full(full, street) == (number, unit)


@pytest.mark.parametrize("val", ["None", "<Null>", "N/A", " None ", "", "  "])
def test_clean_drops_null_literals(val):
    assert normalize._clean(val) is None


@pytest.mark.parametrize("val", ["NONE", "Unknown", "NA", "?", "0"])
def test_clean_keeps_real_values(val):
    assert normalize._clean(val) == val


def _write(tmp_path, body):
    p = tmp_path / "x.toml"
    p.write_text('slug = "x"\nprovider = "P"\ndata_url = "u"\naccess = "static"\n'
                 'format = "geojson"\n' + body, encoding="utf-8")
    return str(p)


def test_registry_parses_number_unit_from_full(tmp_path):
    ds = _parse(_write(tmp_path, 'number_unit_from_full = true\n'
                                 '[fields]\nstreet = "S"\nfull = "F"\n'))
    assert ds.number_unit_from_full


@pytest.mark.parametrize("fields", ['number = "N"\nstreet = "S"\nfull = "F"\n',
                                    'unit = "U"\nstreet = "S"\nfull = "F"\n',
                                    'full = "F"\n',
                                    'street = "S"\n'])
def test_registry_rejects_bad_number_unit_from_full(tmp_path, fields):
    with pytest.raises(ValueError, match="number_unit_from_full"):
        _parse(_write(tmp_path, 'number_unit_from_full = true\n[fields]\n' + fields))


# --- the migration, end to end on a throwaway store -------------------------------

def _ds(**kw):
    return Dataset(slug="_test_recanon", provider="Test", data_url="x", access="static",
                   format="geojson", key_field="",
                   fields={"number": "NUM", "street": "ST", "unit": "U", "full": "FULL"},
                   **kw)


def _feat(num, st, unit, lon, lat):
    return {"type": "Feature",
            "properties": {"NUM": num, "ST": st, "U": unit, "FULL": f"{num} {st}"},
            "geometry": {"type": "Point", "coordinates": [lon, lat]}}


def _snapshot_rows(ds):
    conn = sqlite3.connect(ds.db_path)
    rows = conn.execute("SELECT identity_key, number, unit, min_snapshot_id, "
                        "max_snapshot_id FROM addresses ORDER BY full").fetchall()
    snaps = conn.execute("SELECT id, skipped FROM snapshots ORDER BY id").fetchall()
    conn.close()
    return rows, snaps


@pytest.fixture
def store(monkeypatch):
    ds = _ds(synth_fields=["number", "street", "unit"])
    shutil.rmtree(ds.data_dir, ignore_errors=True)
    feats = [_feat("1", "Main St", "None", -75.1, 45.1),
             _feat("2", "Main St", "<Null>", -75.2, 45.2),
             _feat("3", "Main St", "4B", -75.3, 45.3)]
    # build the history under the old rule, which kept the literals
    with monkeypatch.context() as m:
        m.setattr(normalize, "_CANONICAL_NULL_LITERALS", frozenset({"N/A"}))
        db.import_snapshot(ds, "snap-2026-01-01.geojson", feats)
    yield ds, feats
    shutil.rmtree(ds.data_dir, ignore_errors=True)


def test_rewrite_rekeys_and_next_import_is_a_skip(store):
    ds, feats = store
    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row
    updates, stats = recanonicalize.plan(ds, conn)
    assert len(updates) == 2 and stats["chains_rekeyed"] == 2
    recanonicalize.apply(conn, updates)
    conn.commit()
    conn.close()

    rows, _ = _snapshot_rows(ds)
    assert [r[2] for r in rows] == [None, None, "4B"]
    assert not any(r[0].startswith("~mig~") for r in rows)

    db.import_snapshot(ds, "snap-2026-01-02.geojson", feats)
    rows2, snaps = _snapshot_rows(ds)
    assert snaps[-1][1] == 1, "the same pull must register as a skip"
    assert [r[0] for r in rows2] == [r[0] for r in rows]


def test_rewrite_is_idempotent(store):
    ds, _ = store
    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row
    recanonicalize.apply(conn, recanonicalize.plan(ds, conn)[0])
    conn.commit()
    assert recanonicalize.plan(ds, conn)[0] == []
    conn.close()


def test_rewrite_refuses_a_collision(store):
    """A "None" unit and a real null unit at the same point and number are two chains
    under the old rule and one under the new: refused, never stitched."""
    ds, _ = store
    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("UPDATE addresses SET longitude = -75.1, latitude = 45.1, number = '1', "
                 "full = '1 Main St'")
    conn.execute("UPDATE addresses SET unit = NULL WHERE unit = '<Null>'")
    # re-key the doctored rows as the old rule would have, so they pass faithfulness
    for r in conn.execute("SELECT * FROM addresses").fetchall():
        rec = {c: r[c] for c in ("number", "street", "unit", "full")}
        conn.execute("UPDATE addresses SET identity_key = ? WHERE identity_key = ?",
                     (normalize._identity(ds, rec, {}, -75.1, 45.1), r["identity_key"]))
    with pytest.raises(SystemExit, match="merge distinct chains"):
        recanonicalize.plan(ds, conn)
    conn.close()


def test_number_unit_from_full_rewrite_keeps_keys(monkeypatch):
    ds = Dataset(slug="_test_recanon", provider="Test", data_url="x", access="static",
                 format="geojson", key_field="", synth_fields=["full"],
                 fields={"street": "ST", "full": "FULL"})
    shutil.rmtree(ds.data_dir, ignore_errors=True)
    feats = [{"type": "Feature", "properties": {"ST": "REGINA ST N",
                                                "FULL": "300 REGINA ST N 2 204"},
              "geometry": {"type": "Point", "coordinates": [-80.5, 43.4]}}]
    try:
        db.import_snapshot(ds, "snap-2026-01-01.geojson", feats)
        ds.number_unit_from_full = True
        conn = sqlite3.connect(ds.db_path)
        conn.row_factory = sqlite3.Row
        updates, stats = recanonicalize.plan(ds, conn)
        assert len(updates) == 1 and stats["chains_rekeyed"] == 0
        recanonicalize.apply(conn, updates)
        conn.commit()
        conn.close()
        rows, _ = _snapshot_rows(ds)
        assert rows[0][1:3] == ("300", "2 204")
        db.import_snapshot(ds, "snap-2026-01-02.geojson", feats)
        assert _snapshot_rows(ds)[1][-1][1] == 1
    finally:
        shutil.rmtree(ds.data_dir, ignore_errors=True)
