"""street_from_full: derive canonical street from full minus the number.

lennox-addington publishes only a full ADDRESS and a number (ADD_LABEL), so its
street was NULL on every row and street-level features (new-street debuts,
renames) could never fire; perth-county likewise publishes only Full_Add, with
the unit trailing it. The shapes below are real rows from their stores.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import normalize
from src.normalize import street_from_full
from src.registry import Dataset, _parse


@pytest.mark.parametrize("full, number, street", [
    # 1. the number as published leads the address
    ("137A Main Street", "137A", "Main Street"),
    ("137a Main Street", "137A", "Main Street"),             # case-insensitive match
    ("A-23 Manitou Crescent West", "A-23", "Manitou Crescent West"),
    ("C01 Unit A 310 Bridge Street West", "C01 Unit A 310", "Bridge Street West"),
    ("Site N/A Bass Cove Family Campground", "Site N/A", "Bass Cove Family Campground"),
    ("108 5th Concession Road South", "108", "5th Concession Road South"),  # ordinal kept
    ("12  Erie   Court", "12", "Erie Court"),                 # whitespace collapsed
    # 2. number absent or disagreeing: strip leading civic material instead
    ("336 Precambrian Lane", "363", "Precambrian Lane"),
    ("70A Cranberry Lane", "70", "Cranberry Lane"),
    ("12 Erie Court", None, "Erie Court"),
    ("Site 14 Pickerel Park Rv Resort", None, "Pickerel Park Rv Resort"),
    ("Unit 4-140 Industrial Boulevard", "4-140", "Industrial Boulevard"),
    ("Unit 8 140 Industrial Boulevard", "8-140", "Industrial Boulevard"),
    ("2-2- 30 Dundas Street East", "2-30", "Dundas Street East"),
    ("6248 County Road 4", "6248 County Road 4", "County Road 4"),  # number == full
    ("12 Unit Street East", "12", "Unit Street East"),        # not a designator here
])
def test_derives_street(full, number, street):
    assert street_from_full(full, number) == street


@pytest.mark.parametrize("full, number, unit, street", [
    # perth-county: 3. the unit as published trails the address
    ("11 MADDISON STREET EAST UNIT 3E", "11", "UNIT 3E", "MADDISON STREET EAST"),
    ("195 ST. DAVID STREET SUITE 101", "195", "SUITE 101", "ST. DAVID STREET"),
    ("9A MAPLE STREET UNIT 1", "9A", "UNIT 1", "MAPLE STREET"),
    ("596 ALBERT AVENUE NORTH UNIT 1, BUILDING A", "596", "UNIT 1",
     "ALBERT AVENUE NORTH"),                                  # trailer after the unit
    ("11 Maddison Street East Unit 3e", "11", "UNIT 3E", "Maddison Street East"),
    ("11 MADDISON STREET EAST", "11", "UNIT 3E", "MADDISON STREET EAST"),  # not found
    ("12 UNIT 3E", "12", "UNIT 3E", None),                    # nothing left before it
    # perth-county shapes with no unit
    ("1874 PERTH ROAD 120A", "1874", None, "PERTH ROAD 120A"),  # street's own digits kept
    ("5083B LINE 2", "5083B", None, "LINE 2"),
    ("6379-6389 APPLE BLOSSOM WAY", "6379-6389", None, "APPLE BLOSSOM WAY"),
    ("984035 PERTH-OXFORD ROAD", "984035", None, "PERTH-OXFORD ROAD"),
    ("59 N.D. WALT LANE", "59", None, "N.D. WALT LANE"),
    ("290 O'LOANE AVENUE", "290", None, "O'LOANE AVENUE"),
    ("61636 FISCHER ROAD", "6136", None, "FISCHER ROAD"),     # number typo in source
])
def test_derives_street_with_unit(full, number, unit, street):
    assert street_from_full(full, number, unit) == street


@pytest.mark.parametrize("full, number", [
    (None, "1653"),
    ("", "1"),
    ("70", "70"),                         # nothing but the number
    ("Windermere Boulevard", "119"),      # no number to anchor on: not guessed
    ("Unassigned Nugent Road", "Unknown"),
])
def test_unparseable_stays_none(full, number):
    assert street_from_full(full, number) is None


def _ds(**kw):
    return Dataset(slug="_test_sff", provider="Test", data_url="x", access="static",
                   format="geojson", key_field="", synth_fields=["full"],
                   fields={"number": "NUM", "full": "ADDR"}, **kw)


def _feat(addr="137A Main Street", num="137A"):
    return {"type": "Feature", "properties": {"NUM": num, "ADDR": addr},
            "geometry": {"type": "Point", "coordinates": [-77.0, 44.2]}}


def test_canonical_derives_when_on():
    rec = normalize.canonical(_ds(street_from_full=True), _feat())
    assert rec["street"] == "Main Street"


def test_canonical_default_off():
    """Every other city keeps exactly the street (and hash) it had."""
    rec = normalize.canonical(_ds(), _feat())
    assert rec["street"] is None


def test_street_moves_the_hash_but_not_the_key():
    """Why turning it on needs tools/derive_street_from_full.py: payload_hash
    covers street, identity (synthesized from full) does not."""
    off = normalize.canonical(_ds(), _feat())
    on = normalize.canonical(_ds(street_from_full=True), _feat())
    assert on["identity_key"] == off["identity_key"]
    assert on["payload_hash"] != off["payload_hash"]


def _write(tmp_path, body):
    p = tmp_path / "x.toml"
    p.write_text('slug = "x"\nprovider = "P"\ndata_url = "u"\naccess = "static"\n'
                 'format = "geojson"\n' + body, encoding="utf-8")
    return str(p)


def test_registry_parses_option(tmp_path):
    ds = _parse(_write(tmp_path, 'street_from_full = true\n'
                                 '[fields]\nnumber = "N"\nfull = "F"\n'))
    assert ds.street_from_full and ds.has_street


def test_registry_default_off(tmp_path):
    ds = _parse(_write(tmp_path, '[fields]\nstreet = "S"\nfull = "F"\n'))
    assert not ds.street_from_full and ds.has_street


def test_registry_rejects_mapped_street(tmp_path):
    with pytest.raises(ValueError, match="street_from_full"):
        _parse(_write(tmp_path, 'street_from_full = true\n'
                                '[fields]\nstreet = "S"\nfull = "F"\n'))


def test_registry_requires_full(tmp_path):
    with pytest.raises(ValueError, match="full"):
        _parse(_write(tmp_path, 'street_from_full = true\n[fields]\nnumber = "N"\n'))


def test_registry_rejects_non_bool(tmp_path):
    with pytest.raises(ValueError, match="true or false"):
        _parse(_write(tmp_path, 'street_from_full = "yes"\n[fields]\nfull = "F"\n'))
