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


def test_literal_null_strings_dropped():
    """A publisher whose ETL writes str(None) means null, not the word "None".

    toronto ships it on ~525k rows (ADDRESS_STATUS, PLACE_NAME, ...), windsor on
    Ward; ArcGIS writes "<Null>" for the same thing. Both must hash as absent, so
    the day either export is fixed the city does not re-hash in one go.
    """
    ds = _ds()
    leaked = normalize.canonical(ds, _feat(STATUS="None", WARD=" <Null> "))
    absent = normalize.canonical(ds, _feat())

    props = json.loads(leaked["props"])
    assert "STATUS" not in props
    assert "WARD" not in props
    assert leaked["payload_hash"] == absent["payload_hash"]


def test_real_words_that_only_look_null_are_kept():
    """Only the exact-case serializer spellings go.

    "Unknown" is a coded-domain value on 541,943 stored props (toronto GENERAL_USE,
    kitchener UNIT_TYPE); "NA", "?" and an uppercase "NONE" are things a person
    typed. Dropping any of them would delete meaning, not noise.
    """
    ds = _ds()
    props = json.loads(normalize.canonical(ds, _feat(
        USE="Unknown", TYPE="UNKNOWN", POSTAL="NA", UNIT="?", LOT="NONE",
        NOTE="None of the above"))["props"])
    assert props == {"ID": "1", "NUM": "1", "ST": "Main St", "FULL": "1 Main St",
                     "USE": "Unknown", "TYPE": "UNKNOWN", "POSTAL": "NA",
                     "UNIT": "?", "LOT": "NONE", "NOTE": "None of the above"}


def test_esri_editor_tracking_spellings_ignored():
    """CreationDate/ModificationDate are the newer esri editor-tracking columns
    (west-parry-sound); they churn with every edit and carry no address content."""
    ds = _ds()
    a = normalize.canonical(ds, _feat(CreationDate="2026-01-01", ModificationDate="2026-01-02"))
    b = normalize.canonical(ds, _feat(CreationDate="2020-05-05", ModificationDate="2026-08-21"))
    assert "CreationDate" not in json.loads(a["props"])
    assert "ModificationDate" not in json.loads(a["props"])
    assert a["payload_hash"] == b["payload_hash"]


def test_globalid_1_is_volatile():
    ds = _ds()
    a = normalize.canonical(ds, _feat(GlobalID_1="{AAA}"))
    b = normalize.canonical(ds, _feat(GlobalID_1="{BBB}"))
    assert "GlobalID_1" not in json.loads(a["props"])
    assert a["payload_hash"] == b["payload_hash"]


def test_padded_values_are_stripped():
    """A source that re-pads a real value must not churn the prop.

    renfrew's Full_Address did it on 1,060 rows, while the canonical `full` sat
    still because _clean already strips it.
    """
    ds = _ds()
    padded = normalize.canonical(ds, _feat(ADDR="2502 Calabogie Road "))
    tight = normalize.canonical(ds, _feat(ADDR="2502 Calabogie Road"))

    assert json.loads(padded["props"])["ADDR"] == "2502 Calabogie Road"
    assert padded["payload_hash"] == tight["payload_hash"]


def test_objectid_spellings_are_volatile():
    """Numbered ESRI id spellings churn like the unnumbered ones.

    hastings publishes OBJECTID_12 (its alias is literally "OBJECTID_1"); listing
    the spellings one by one missed it until 2026-08-08.
    """
    ds = _ds()
    for key in ("OBJECTID_12", "FID_1", "fid_003"):
        a = normalize.canonical(ds, _feat(**{key: 1}))
        b = normalize.canonical(ds, _feat(**{key: 2}))
        assert key not in json.loads(a["props"]), key
        assert a["payload_hash"] == b["payload_hash"], key


def test_objectid_pattern_is_anchored():
    """Only the id spellings go; a real column that merely starts that way stays."""
    ds = _ds()
    props = json.loads(normalize.canonical(
        ds, _feat(OBJECTID_SOURCE="MPAC", FIDUCIARY="Y", FID_A="x"))["props"])
    assert props["OBJECTID_SOURCE"] == "MPAC"
    assert props["FIDUCIARY"] == "Y"
    assert props["FID_A"] == "x"


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
