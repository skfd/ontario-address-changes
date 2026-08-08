"""Blank source values must not reach props or payload_hash.

Many sources pad unused columns with " " instead of leaving them empty (london
StreetDirection, windsor Legal2, oakville SUFFIX, ...). Those blanks used to be
stored and hashed, so a source that stopped padding a field reported every
affected row as modified with a "' ' -> -" change that shows nothing.
Same for GlobalID_1, an ESRI housekeeping key reassigned on republish.
"""

import json
import os
import shutil
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize
from src.registry import Dataset


def _ds(slug="_test_blank"):
    return Dataset(slug=slug, provider="Test", data_url="x", access="static",
                   format="geojson", key_field="ID", synth_fields=["full"],
                   fields={"number": "NUM", "street": "ST", "full": "FULL"})


def _feat(**extra):
    props = {"ID": "1", "NUM": "1", "ST": "Main St", "FULL": "1 Main St"}
    props.update(extra)
    return {"type": "Feature", "properties": props,
            "geometry": {"type": "Point", "coordinates": [-75.1, 45.1]}}


def test_whitespace_only_values_dropped():
    ds = _ds()
    padded = normalize.canonical(ds, _feat(PAD=" ", TABBED="\t"))
    absent = normalize.canonical(ds, _feat())

    assert "PAD" not in json.loads(padded["props"])
    assert "TABBED" not in json.loads(padded["props"])
    assert padded["payload_hash"] == absent["payload_hash"]


def test_non_string_falsy_values_kept():
    """Only whitespace strings go; a real 0 or False is data."""
    ds = _ds()
    props = json.loads(normalize.canonical(ds, _feat(ZERO=0, FLAG=False))["props"])
    assert props["ZERO"] == 0
    assert props["FLAG"] is False


def test_globalid_1_is_volatile():
    ds = _ds()
    a = normalize.canonical(ds, _feat(GlobalID_1="{AAA}"))
    b = normalize.canonical(ds, _feat(GlobalID_1="{BBB}"))
    assert "GlobalID_1" not in json.loads(a["props"])
    assert a["payload_hash"] == b["payload_hash"]


def test_dropped_padding_does_not_open_a_new_span():
    """The regression: source stops padding a column -> must not read as modified."""
    ds = _ds("_test_blank_scd2")
    if os.path.isdir(ds.data_dir):
        shutil.rmtree(ds.data_dir)

    db.import_snapshot(ds, "snap-2026-01-01.geojson", [_feat(PAD=" ")])
    db.import_snapshot(ds, "snap-2026-01-02.geojson", [_feat()])

    conn = sqlite3.connect(ds.db_path)
    spans = conn.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]
    conn.close()
    shutil.rmtree(ds.data_dir)
    assert spans == 1, "padding change must not open a second SCD-2 span"
