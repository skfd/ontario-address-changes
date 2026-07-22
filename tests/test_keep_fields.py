"""keep_fields: stored in props, ignored for change detection, out of payload_hash.

Guards the toronto-2-address-import migration — see
toronto-addresses-import/docs/migration/MIGRATION_PLAN.md. A kept field that
leaked into payload_hash would reopen an SCD-2 span on every churn (the bloat
fixed in 363e435); a kept field missing from props would silently disable the
importer's Land Entrance skip.
"""

import json
import os
import shutil
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize
from src.registry import Dataset, _parse


def _ds(**kw):
    return Dataset(slug="_test_keep", provider="Test", data_url="x", access="static",
                   format="geojson", key_field="", synth_fields=["full"],
                   fields={"number": "NUM", "street": "ST", "full": "FULL"}, **kw)


def _feat(cls="Land", note="a"):
    return {"type": "Feature",
            "properties": {"NUM": "1", "ST": "Main St", "FULL": "1 Main St",
                           "CLS": cls, "NOISE": note},
            "geometry": {"type": "Point", "coordinates": [-75.1, 45.1]}}


def test_kept_field_stored_but_not_hashed():
    kept = _ds(ignore_fields=["CLS", "NOISE"], keep_fields=["CLS"])
    plain = _ds(ignore_fields=["CLS", "NOISE"])

    a = normalize.canonical(kept, _feat())
    b = normalize.canonical(plain, _feat())

    assert json.loads(a["props"])["CLS"] == "Land", "kept field must reach props"
    assert "CLS" not in json.loads(b["props"])
    assert "NOISE" not in json.loads(a["props"]), "non-kept ignore_fields still stripped"
    assert a["payload_hash"] == b["payload_hash"], "keep_fields must not alter the hash"


def test_kept_field_churn_does_not_split_span():
    """The whole point: the value can change without opening a new SCD-2 span."""
    ds = _ds(ignore_fields=["CLS", "NOISE"], keep_fields=["CLS"])
    if os.path.isdir(ds.data_dir):
        shutil.rmtree(ds.data_dir)

    db.import_snapshot(ds, "snap-2026-01-01.geojson", [_feat(cls="Land")])
    db.import_snapshot(ds, "snap-2026-01-02.geojson", [_feat(cls="Structure")])

    conn = sqlite3.connect(ds.db_path)
    spans = conn.execute("SELECT min_snapshot_id, max_snapshot_id FROM addresses").fetchall()
    conn.close()
    assert len(spans) == 1, f"kept-field churn must not split the span, got {spans}"

    shutil.rmtree(ds.data_dir)


def test_keep_fields_must_be_ignored(tmp_path):
    """A keep_fields entry that isn't ignored would be dropped from the hash
    while still being stored — a live field silently leaving change detection."""
    cfg = tmp_path / "bad.toml"
    cfg.write_text(
        'slug="bad"\nprovider="p"\ndata_url="u"\naccess="static"\nformat="geojson"\n'
        'ignore_fields=["A"]\nkeep_fields=["B"]\n', encoding="utf-8")
    with pytest.raises(ValueError, match="keep_fields not in ignore_fields"):
        _parse(str(cfg))


def test_real_toronto_config_keeps_importer_fields():
    ds = {d.slug: d for d in __import__("src.registry", fromlist=["x"]).load_all()}["toronto"]
    assert "ADDRESS_CLASS_DESC" in ds.keep_fields
    assert set(ds.keep_fields) <= set(ds.ignore_fields)
