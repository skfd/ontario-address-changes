"""A homogeneous sweep is flagged and held; heterogeneous city activity is not.

The signatures replay the fabricated stories this project actually published:
Brant's replayed 1,000-row batch (2026-08-16, +5.2% in a day), Renfrew's
1,104-row address restyle (2026-06-13), and the single-field recodes that mass
collapsing was built for. Each must flag; ordinary daily churn must not; and a
verdict in the ledger must control exactly what a render shows.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import flags
from src.registry import Dataset


def _ds(**kw):
    return Dataset(slug="_test", provider="Test", data_url="x", access="static",
                   format="geojson", **kw)


def _mod(i, field_changes):
    return {"identity_key": f"k{i}",
            "changes": [{"field": f, "old": o, "new": n}
                        for f, o, n in field_changes]}


def _diff(added=0, removed=0, modified=()):
    return {"added": [{"identity_key": f"a{i}"} for i in range(added)],
            "removed": [{"identity_key": f"r{i}"} for i in range(removed)],
            "modified": list(modified)}


CITY = 20_000  # denominator: previous snapshot's row count


def test_a_replayed_batch_flags_and_ordinary_growth_does_not():
    # brant 2026-08-16: +1,000 on 19,335
    found = flags.detect(_ds(), _diff(added=1000), CITY)
    assert [f["signature"] for f in found] == ["mass-added"], found
    assert "5.0%" in found[0]["scope"]
    # a genuine subdivision: 120 adds on 20k (0.6%) stays quiet
    assert flags.detect(_ds(), _diff(added=120), CITY) == []
    # small city, small absolute count: 30 adds on 400 is 7.5% but under the floor
    assert flags.detect(_ds(), _diff(added=30), 400) == []


def test_a_mass_removal_flags():
    found = flags.detect(_ds(), _diff(removed=800), CITY)
    assert [f["signature"] for f in found] == ["mass-removed"]


def test_a_single_field_sweep_flags_with_transition_evidence():
    mods = [_mod(i, [("ZONING", "R", "RES")]) for i in range(60)]
    found = flags.detect(_ds(), _diff(modified=mods), CITY)
    assert [f["signature"] for f in found] == ["mass-modified"]
    assert found[0]["fields"] == ["ZONING"]
    assert "'R' -> 'RES' (60)" in found[0]["detail"]


def test_a_restyle_sweep_is_called_out():
    # renfrew 2026-06-13: "17883 Highway 60" -> "17883 60 Highway"
    mods = [_mod(i, [("full", f"{i} Highway 60", f"{i} 60 Highway")])
            for i in range(1104)]
    found = flags.detect(_ds(), _diff(modified=mods), CITY)
    assert len(found) == 1 and "restyle" in found[0]["detail"]


def test_heterogeneous_modifications_stay_quiet():
    # 120 rows, 3 different field-sets of 40 each: no set clears the 50-row floor
    mods = ([_mod(i, [("street", "A", "B")]) for i in range(40)]
            + [_mod(100 + i, [("unit", "1", "2")]) for i in range(40)]
            + [_mod(200 + i, [("ZONING", "R", "C")]) for i in range(40)])
    assert flags.detect(_ds(), _diff(modified=mods), CITY) == []


def test_a_configured_class_sweep_is_exempt():
    ds = _ds(classes={"status": ["LIFECYCLE"]})
    mods = [_mod(i, [("LIFECYCLE", "PLANNED", "ACTIVE")]) for i in range(500)]
    assert flags.detect(ds, _diff(modified=mods), CITY) == []
    # ...but only for the configured fields; the same sweep elsewhere flags
    assert flags.detect(_ds(), _diff(modified=mods), CITY) != []


def test_lat_lon_collapse_to_one_location_fieldset():
    mods = [_mod(i, [("latitude", 45.0, 45.1), ("longitude", -75.0, -75.1)])
            for i in range(60)]
    found = flags.detect(_ds(), _diff(modified=mods), CITY)
    assert len(found) == 1 and found[0]["fields"] == ["location"]
    assert found[0]["detail"] == "", "no old->new listing for coordinates"


def test_ledger_append_is_idempotent_and_survives_tomllib():
    import tomllib
    fd, path = tempfile.mkstemp(suffix=".toml")
    os.close(fd)
    os.remove(path)  # record() must create it, header included
    try:
        fl = {"slug": "brant", "date": "2026-08-16", "signature": "mass-added",
              "scope": '1,000 added ("replay")', "detail": "",
              "detected": "2026-08-18"}
        assert len(flags.record([fl], path)) == 1
        assert flags.record([fl, dict(fl)], path) == [], "same key never re-appends"
        with open(path, "rb") as f:
            back = tomllib.load(f)["flag"]
        assert back[0]["scope"] == '1,000 added ("replay")', "quotes must survive"
        assert back[0]["status"] == "open"
    finally:
        os.remove(path)


def test_holds_follow_the_verdict():
    mods = [_mod(i, [("ZONING", "R", "RES")]) for i in range(60)] \
        + [_mod(900, [("street", "Old", "New")])]
    d = _diff(added=1000, modified=mods)
    base = [{"slug": "x", "date": "2026-01-02", "signature": "mass-added",
             "scope": "", "detected": "2026-01-02", "status": "open"},
            {"slug": "x", "date": "2026-01-02", "signature": "mass-modified",
             "fields": ["ZONING"], "scope": "", "detected": "2026-01-02",
             "status": "open"}]

    # open flags hold; the untouched street rename still publishes
    held = flags.holds_for(base, "x", "2026-01-02")
    d2, notes = flags.apply_holds(d, held)
    assert d2["added"] == [] and len(d2["modified"]) == 1
    assert d2["modified"][0]["identity_key"] == "k900"
    assert len(notes) == 2
    assert d["added"], "apply_holds must not mutate the original diff"

    # a business verdict releases its event; the other stays held
    base[0] |= {"status": "reviewed", "verdict": "business"}
    d3, _ = flags.apply_holds(d, flags.holds_for(base, "x", "2026-01-02"))
    assert len(d3["added"]) == 1000 and len(d3["modified"]) == 1

    # technical and bug verdicts hold forever
    base[0] |= {"verdict": "technical"}
    d4, _ = flags.apply_holds(d, flags.holds_for(base, "x", "2026-01-02"))
    assert d4["added"] == []

    # other cities and days are untouched
    assert flags.holds_for(base, "y", "2026-01-02") == []
    assert flags.holds_for(base, "x", "2026-01-03") == []


if __name__ == "__main__":
    test_a_replayed_batch_flags_and_ordinary_growth_does_not()
    test_a_mass_removal_flags()
    test_a_single_field_sweep_flags_with_transition_evidence()
    test_a_restyle_sweep_is_called_out()
    test_heterogeneous_modifications_stay_quiet()
    test_a_configured_class_sweep_is_exempt()
    test_lat_lon_collapse_to_one_location_fieldset()
    test_ledger_append_is_idempotent_and_survives_tomllib()
    test_holds_follow_the_verdict()
    print("\nALL ASSERTIONS PASSED")
