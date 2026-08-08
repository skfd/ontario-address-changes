"""A degraded pull must be refused, not recorded.

Both signatures come from real days: a short pull (kitchener/huron 2026-07-28,
where an ArcGIS paging loop ended on a transient blank page) and an
attribute-stripped pull (muskoka 2026-06-28, york 2026-07-31, where the rows
arrived but a mapped column came back empty). Each was published as a mass event
and had to be undone by rebuilding the store by hand, so the import must reject
them while the store is still untouched.
"""

import os
import shutil
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db
from src.registry import Dataset


def _ds(slug):
    return Dataset(slug=slug, provider="Test", data_url="x", access="static",
                   format="geojson", key_field="ID", synth_fields=["full"],
                   fields={"number": "NUM", "street": "ST", "unit": "UNIT",
                           "full": "FULL"})


def _feat(i, street="Main St", unit=None):
    props = {"ID": str(i), "NUM": str(i), "ST": street, "FULL": f"{i} {street}"}
    if unit:
        props["UNIT"] = unit
    return {"type": "Feature", "properties": props,
            "geometry": {"type": "Point", "coordinates": [-75.0 - i / 1e4, 45.0]}}


def _fresh(slug, features):
    """A store holding one baseline snapshot of `features`."""
    ds = _ds(slug)
    if os.path.isdir(ds.data_dir):
        shutil.rmtree(ds.data_dir)
    db.import_snapshot(ds, f"{slug}-2026-01-01.geojson", features)
    return ds


def _state(ds):
    conn = sqlite3.connect(ds.db_path)
    snaps = conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0]
    addrs = conn.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]
    conn.close()
    return snaps, addrs


def _rejects(ds, features, day, match):
    before = _state(ds)
    try:
        db.import_snapshot(ds, f"{ds.slug}-{day}.geojson", features)
    except db.DegradedPull as e:
        assert match in str(e), f"unexpected reason: {e}"
    else:
        raise AssertionError(f"{ds.slug}: degraded pull was imported")
    assert _state(ds) == before, "a refused pull must leave the store untouched"
    # ...but the refusal itself is recorded, or the city would silently stall
    block = db.active_block(ds)
    assert block and match in block["reason"], block


def test_a_short_pull_is_refused():
    base = [_feat(i) for i in range(200)]
    ds = _fresh("_test_short", base)
    _rejects(ds, base[:100], "2026-01-02", "below snapshot 1")
    shutil.rmtree(ds.data_dir)


def test_a_stripped_field_is_refused():
    base = [_feat(i) for i in range(200)]
    ds = _fresh("_test_stripped", base)
    # every row still arrives; the street column comes back empty
    stripped = [_feat(i, street="") for i in range(200)]
    _rejects(ds, stripped, "2026-01-02", "'street' (ST) populated on 0 rows")
    shutil.rmtree(ds.data_dir)


def test_ordinary_churn_still_imports():
    # 2.5% of rows gone and a street renamed: the largest real day-over-day row
    # loss on record is 0.63%, so this is already generous, and must not trip.
    base = [_feat(i) for i in range(200)]
    ds = _fresh("_test_churn", base)
    churned = [_feat(i, street="Oak Ave" if i < 20 else "Main St")
               for i in range(195)]
    db.import_snapshot(ds, "_test_churn-2026-01-02.geojson", churned)
    assert _state(ds)[0] == 2, "a normal day must be recorded"
    shutil.rmtree(ds.data_dir)


def test_a_sparse_field_emptying_is_not_treated_as_damage():
    # Below the guarded-rows floor a field's coverage is too small to judge, and
    # wedging a city daily over a handful of rows would be worse than the noise.
    base = [_feat(i, unit=("A" if i < 50 else None)) for i in range(200)]
    ds = _fresh("_test_sparse", base)
    db.import_snapshot(ds, "_test_sparse-2026-01-02.geojson",
                       [_feat(i) for i in range(200)])
    assert _state(ds)[0] == 2, "sparse unit loss must not block the import"
    shutil.rmtree(ds.data_dir)


def test_a_recovered_source_clears_its_own_block():
    # The refusal has to stop asking for attention on its own, or every transient
    # bad day would need a human to dismiss it.
    base = [_feat(i) for i in range(200)]
    ds = _fresh("_test_recover", base)
    _rejects(ds, base[:100], "2026-01-02", "below snapshot 1")
    _rejects(ds, base[:100], "2026-01-03", "below snapshot 1")
    assert db.active_block(ds)["attempts"] == 2, "each refusal counts"
    assert db.active_block(ds)["since"] == db.active_block(ds)["detected"][:10]

    db.import_snapshot(ds, "_test_recover-2026-01-04.geojson",
                       [_feat(i) for i in range(201)])
    assert db.active_block(ds) is None, "a good pull clears the block"
    shutil.rmtree(ds.data_dir)


def test_an_unchanged_republish_also_clears_a_block():
    # The recovery pull is often byte-identical to the last good one, which takes
    # the content-hash skip path and never reaches the guards.
    base = [_feat(i) for i in range(200)]
    ds = _fresh("_test_recover_skip", base)
    _rejects(ds, base[:100], "2026-01-02", "below snapshot 1")
    db.import_snapshot(ds, "_test_recover_skip-2026-01-03.geojson", list(base))
    assert db.active_block(ds) is None, "an unchanged republish is still a good pull"
    shutil.rmtree(ds.data_dir)


if __name__ == "__main__":
    test_a_short_pull_is_refused()
    test_a_stripped_field_is_refused()
    test_ordinary_churn_still_imports()
    test_a_sparse_field_emptying_is_not_treated_as_damage()
    test_a_recovered_source_clears_its_own_block()
    test_an_unchanged_republish_also_clears_a_block()
    print("\nALL ASSERTIONS PASSED")
