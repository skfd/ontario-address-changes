"""Synthesized identity: geometry is the default disambiguator, not the only one.

Muskoka's service re-emits coordinates that differ by up to 1.36 m between
republishes. That crosses the 5 dp (~1.1 m) rounding in _identity, so a key
built on geometry changed for 43% of the city on a republish where nothing
about the addresses changed, and the store grew to 157,666 keys for 66k rows.
`synth_props` supplies a stable disambiguator instead; `use_geometry = false`
takes the jittering coordinates back out of the basis.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import normalize
from src.registry import Dataset, _parse, load_all


def _ds(**kw):
    kw.setdefault("synth_fields", ["number", "street"])
    return Dataset(slug="_test_synth", provider="Test", data_url="x", access="static",
                   format="geojson", key_field="",
                   fields={"number": "NUM", "street": "ST"}, **kw)


def _feat(lon=-79.37, lat=45.03, roll="4402-001"):
    return {"type": "Feature",
            "properties": {"NUM": "1", "ST": "Main St", "ROLL": roll},
            "geometry": {"type": "Point", "coordinates": [lon, lat]}}


# a shift below the 5th decimal — well under the observed 1.36 m jitter
_JITTERED = dict(lon=-79.37001, lat=45.03001)


def test_geometry_jitter_changes_the_default_key():
    """The behaviour every other city relies on, and muskoka's problem."""
    ds = _ds()
    assert (normalize.canonical(ds, _feat())["identity_key"]
            != normalize.canonical(ds, _feat(**_JITTERED))["identity_key"])


def test_synth_props_without_geometry_survives_jitter():
    ds = _ds(synth_props=["ROLL"], use_geometry=False)
    assert (normalize.canonical(ds, _feat())["identity_key"]
            == normalize.canonical(ds, _feat(**_JITTERED))["identity_key"])


def test_synth_props_still_separate_distinct_rows():
    """Dropping geometry must not collapse two rows that differ by roll number."""
    ds = _ds(synth_props=["ROLL"], use_geometry=False)
    assert (normalize.canonical(ds, _feat(roll="4402-001"))["identity_key"]
            != normalize.canonical(ds, _feat(roll="4402-002"))["identity_key"])


def test_synth_props_default_off():
    """Adding the knobs must not move any existing city's keys."""
    ds = _ds()
    assert ds.synth_props == [] and ds.use_geometry is True
    parts = ["1", "MAIN ST", f"{-79.37:.5f}", f"{45.03:.5f}"]
    import hashlib
    expected = "syn:" + hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()
    assert normalize.canonical(ds, _feat())["identity_key"] == expected


def test_dropping_geometry_needs_a_replacement(tmp_path):
    """Without synth_props, use_geometry = false collapses every same-address
    row in the city onto one key."""
    cfg = tmp_path / "bad.toml"
    cfg.write_text(
        'slug="bad"\nprovider="p"\ndata_url="u"\naccess="static"\nformat="geojson"\n'
        '[identity]\nuse_geometry=false\n', encoding="utf-8")
    with pytest.raises(ValueError, match="use_geometry = false needs synth_props"):
        _parse(str(cfg))


def test_only_muskoka_opts_out_of_geometry():
    off = [d.slug for d in load_all() if not d.use_geometry]
    assert off == ["muskoka"], f"unexpected datasets without geometry identity: {off}"
