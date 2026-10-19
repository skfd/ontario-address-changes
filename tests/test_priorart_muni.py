"""priorart/muni.py: the municipality key every comparison joins on.

Names arrive from four spellings (LIO shortform, StatCan CSD English name,
Overture postal municipality, ODA csdname); these are the shapes that broke
the first run: bilingual "X / Y", a trailing "County", the Hamilton city /
township collision, slash spacing, and a StatCan name LIO no longer uses.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "priorart"))

import muni  # noqa: E402


def test_norm_name_strips_accents_periods_and_slash_spacing():
    assert muni.norm_name("Sault Ste. Marie") == "SAULT STE MARIE"
    assert muni.norm_name("Rivière des Français") == "RIVIERE DES FRANCAIS"
    assert muni.norm_name("Gordon / Barrie Island") == muni.norm_name("Gordon/Barrie Island")
    assert muni.norm_name("  ") is None and muni.norm_name(None) is None


def test_type_word_from_official_name():
    assert muni.type_word("CITY OF HAMILTON") == "CITY"
    assert muni.type_word("TOWNSHIP OF HAMILTON") == "TOWNSHIP"
    assert muni.type_word("UNITED TOWNSHIPS OF HEAD, CLARA AND MARIA") == "UNITED TOWNSHIPS"
    assert muni.type_word(None) == "MUNICIPALITY"


@pytest.fixture
def munis(tmp_path, monkeypatch):
    """A tiny LIO-shaped layer: Hamilton twice, a bilingual county, a slash name."""
    def sq(x, y):
        return {"type": "Polygon", "coordinates": [[[x, y], [x + 1, y], [x + 1, y + 1], [x, y + 1], [x, y]]]}

    def feat(short, official, mtype, upper, x, y):
        return {"type": "Feature", "geometry": sq(x, y), "properties": {
            "MUNID": f"{x}{y}", "MUNICIPAL_NAME_SHORTFORM": short, "MUNICIPAL_NAME": official,
            "MUNICIPAL_TYPE": mtype, "UPPER_TIER_MUNICIPALITY": upper, "MUNICIPAL_AREA_EXTENT_TYPE": "Mainland"}}

    fc = {"type": "FeatureCollection", "features": [
        feat("HAMILTON", "CITY OF HAMILTON", "Single Tier Municipality", None, 0, 0),
        feat("HAMILTON", "TOWNSHIP OF HAMILTON", "Lower Tier Municipality", "COUNTY OF NORTHUMBERLAND", 2, 0),
        feat("GREATER SUDBURY", "CITY OF GREATER SUDBURY", "Single Tier Municipality", None, 4, 0),
        feat("NORFOLK COUNTY", "NORFOLK COUNTY", "Single Tier Municipality", None, 6, 0),
        feat("PRINCE EDWARD", "COUNTY OF PRINCE EDWARD", "Single Tier Municipality", None, 8, 0),
        feat("GORDON / BARRIE ISLAND", "MUNICIPALITY OF GORDON / BARRIE ISLAND", "Single Tier Municipality", None, 10, 0),
        feat("TARBUTT", "TOWNSHIP OF TARBUTT", "Single Tier Municipality", None, 12, 0),
    ]}
    import json
    p = tmp_path / "lio.geojson"
    p.write_text(json.dumps(fc), encoding="utf-8")
    aliases = tmp_path / "aliases.csv"
    aliases.write_text("alias,municipality,note\nTarbutt and Tarbutt Additional,Tarbutt,\n", encoding="utf-8")
    monkeypatch.setattr(muni, "ALIASES_PATH", str(aliases))
    return muni.Municipalities(str(p))


def test_shared_short_name_gets_type_keys(munis):
    assert "HAMILTON (CITY)" in munis.info and "HAMILTON (TOWNSHIP)" in munis.info
    assert "HAMILTON" not in munis.info
    assert munis.resolve("Hamilton", "CY") == "HAMILTON (CITY)"
    assert munis.resolve("Hamilton", "TP") == "HAMILTON (TOWNSHIP)"
    assert munis.resolve("Hamilton") == "HAMILTON (CITY)", "without a type the city wins"
    assert [r["name_collision"] for r in munis.table() if r["municipality"].startswith("HAMILTON")] == [True, True]


def test_resolve_bilingual_county_suffix_and_alias(munis):
    assert munis.resolve("Greater Sudbury / Grand Sudbury") == "GREATER SUDBURY"
    assert munis.resolve("Norfolk") == "NORFOLK COUNTY"
    assert munis.resolve("Prince Edward County") == "PRINCE EDWARD"
    assert munis.resolve("Gordon/Barrie Island") == "GORDON/BARRIE ISLAND"
    assert munis.resolve("Tarbutt and Tarbutt Additional") == "TARBUTT"
    assert munis.resolve("City of Greater Sudbury") == "GREATER SUDBURY"
    assert munis.resolve("Saugeen 29") is None


def test_assign_bins_points_and_leaves_outsiders_none(munis):
    names = munis.assign([0.5, 2.5, 4.5, 50.0], [0.5, 0.5, 0.5, 50.0])
    assert names == ["HAMILTON (CITY)", "HAMILTON (TOWNSHIP)", "GREATER SUDBURY", None]
    assert munis.assign([], []) == []
