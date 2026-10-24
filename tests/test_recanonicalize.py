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
    ("70", "MAIN ST", "70", None),
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


# --- number_from_full / unit_from_number (hastings, thunder-bay, brantford) -------

@pytest.mark.parametrize("full, number", [
    ("152B JAMIESON LN", "152B"),
    ("963 1/2 HOLT PL", "963 1/2"),
    ("1320A HIGHWAY 61", "1320A"),                 # the street's own digits stay
    ("108 5th Concession Road", "108"),            # ordinal stops the run
    ("171", "171"),                                # number-only full is that number
    ("BACK ST", None),
    ("   ", None),
    (None, None),
])
def test_number_from_full(full, number):
    assert normalize.number_from_full(normalize._clean(full)) == number


@pytest.mark.parametrize("number, out", [
    ("12-73", ("73", "12")),
    ("46-17", ("17", "46")),
    ("A-23", ("23", "A")),
    ("197E", ("197E", None)),
    ("73", ("73", None)),
    ("2-2-30", ("2-2-30", None)),                   # not one unit token
    ("12-", ("12-", None)),
    (None, (None, None)),
])
def test_unit_from_number(number, out):
    assert normalize.unit_from_number(number) == out


@pytest.mark.parametrize("body, msg", [
    ('number_from_full = true\n[fields]\nnumber = "N"\nfull = "F"\n', "pick one"),
    ('number_from_full = true\n[fields]\nstreet = "S"\n', "needs a mapped"),
    ('unit_from_number = true\n[fields]\nnumber = "N"\nunit = "U"\n', "pick one"),
    ('unit_from_number = true\n[fields]\nfull = "F"\n', "needs a number"),
])
def test_registry_rejects_bad_derivations(tmp_path, body, msg):
    with pytest.raises(ValueError, match=msg):
        _parse(_write(tmp_path, body))


def test_canonical_number_from_full_then_unit_from_number():
    ds = Dataset(slug="_t", provider="T", data_url="x", access="static", format="geojson",
                 fields={"number": "N", "full": "F"}, unit_from_number=True)
    rec = normalize.canonical(ds, {"properties": {"N": "12-73", "F": "12-73 MORTON AVE W"},
                                   "geometry": {"type": "Point", "coordinates": [-80, 43]}})
    assert (rec["number"], rec["unit"]) == ("73", "12")


def _chain_store(synth, rows):
    """A store with rows (number, full, min, max) at one point, under `synth`."""
    ds = Dataset(slug="_test_recanon", provider="Test", data_url="x", access="static",
                 format="geojson", key_field="", synth_fields=synth,
                 fields={"street": "ST", "full": "FULL"}, number_from_full=True)
    shutil.rmtree(ds.data_dir, ignore_errors=True)
    conn = db.init_db(ds)
    for sid in range(1, 5):
        conn.execute("INSERT INTO snapshots (id, filename, downloaded, row_count, "
                     "content_hash, skipped) VALUES (?, ?, '', 0, '', 0)",
                     (sid, f"x-2026-01-0{sid}.geojson"))
    for number, full, lo, hi in rows:
        rec = {"number": number, "street": "MAIN ST", "unit": None, "full": full,
               "longitude": -80.0, "latitude": 43.0}
        conn.execute(
            "INSERT INTO addresses (identity_key, min_snapshot_id, max_snapshot_id, number, "
            "street, unit, full, longitude, latitude, props, payload_hash) "
            "VALUES (?, ?, ?, ?, 'MAIN ST', NULL, ?, -80.0, 43.0, '{}', ?)",
            (normalize._identity(ds, rec, {}, -80.0, 43.0), lo, hi, number, full,
             normalize._payload_hash(rec, {})))
    conn.commit()
    return ds, conn


def test_a_chain_splits_where_the_new_rule_sees_a_renumber():
    # House_No stayed 11 while the full address went 11 -> 11A: one chain before,
    # a retire + add under number_from_full
    ds, conn = _chain_store(["number", "street"], [("11", "11 MAIN ST", 1, 2),
                                                   ("11", "11A MAIN ST", 3, 4)])
    try:
        updates, stats = recanonicalize.plan(ds, conn)
        assert len(stats["split"]) == 1
        recanonicalize.apply(conn, updates)
        assert len({r[0] for r in conn.execute("SELECT identity_key FROM addresses")}) == 2
    finally:
        conn.close()
        shutil.rmtree(ds.data_dir, ignore_errors=True)


def test_time_disjoint_chains_join_but_overlapping_ones_are_refused():
    # number missing on snapshot 1, back from 3: one address under the new rule
    ds, conn = _chain_store(["number", "street"], [(None, "660 MAIN ST", 1, 1),
                                                   ("660", "660 MAIN ST", 3, 4)])
    try:
        updates, stats = recanonicalize.plan(ds, conn)
        assert stats["joined"] == 1
        recanonicalize.apply(conn, updates)
        assert [tuple(r) for r in conn.execute(
            "SELECT min_snapshot_id, max_snapshot_id FROM addresses ORDER BY 1")] == \
            [(1, 1), (3, 4)]
        assert len({r[0] for r in conn.execute("SELECT identity_key FROM addresses")}) == 1
    finally:
        conn.close()
        shutil.rmtree(ds.data_dir, ignore_errors=True)
    ds, conn = _chain_store(["number", "street"], [(None, "660 MAIN ST", 1, 3),
                                                   ("660", "660 MAIN ST", 3, 4)])
    try:
        with pytest.raises(SystemExit, match="merge distinct chains"):
            recanonicalize.plan(ds, conn)
    finally:
        conn.close()
        shutil.rmtree(ds.data_dir, ignore_errors=True)


def test_unit_from_number_rewrite_is_idempotent():
    """A stored number is already split ("73" + unit "12"): a re-run must leave it."""
    ds = Dataset(slug="_test_recanon", provider="Test", data_url="x", access="static",
                 format="geojson", key_field="", synth_fields=["number", "street"],
                 fields={"number": "N", "street": "ST", "full": "F"})
    shutil.rmtree(ds.data_dir, ignore_errors=True)
    feats = [{"type": "Feature",
              "properties": {"N": f"{u}-73", "ST": "MORTON AVE W", "F": f"{u}-73 MORTON AVE W"},
              "geometry": {"type": "Point", "coordinates": [-80.2, 43.1]}} for u in (12, 13)]
    try:
        db.import_snapshot(ds, "snap-2026-01-01.geojson", feats)
        ds.unit_from_number = True
        ds.synth_fields = ["number", "street", "unit"]
        conn = sqlite3.connect(ds.db_path)
        conn.row_factory = sqlite3.Row
        old = Dataset(slug=ds.slug, provider="Test", data_url="x", access="static",
                      format="geojson", key_field="", synth_fields=["number", "street"])
        recanonicalize.apply(conn, recanonicalize.plan(ds, conn, old)[0])
        conn.commit()
        assert sorted(tuple(r) for r in conn.execute("SELECT number, unit FROM addresses")) \
            == [("73", "12"), ("73", "13")]
        assert recanonicalize.plan(ds, conn)[0] == []
        conn.close()
        db.import_snapshot(ds, "snap-2026-01-02.geojson", feats)
        assert _snapshot_rows(ds)[1][-1][1] == 1
    finally:
        shutil.rmtree(ds.data_dir, ignore_errors=True)


# --- unit_from_full (leamington: the unit between the number and the street) -------

@pytest.mark.parametrize("full, number, street, unit", [
    # real leamington shapes
    ("24 UNIT 300 SEACLIFF DRIVE EAST", "24", "SEACLIFF DRIVE EAST", "UNIT 300"),
    ("1217 FLR 01 MERSEA RD 2", "1217", "MERSEA RD 2", "FLR 01"),   # the 2 is the street's
    ("20 APT 3 FOUNDRY STREET", "20", "FOUNDRY STREET", "APT 3"),
    ("10B SUITE 101 MAIN STREET", "10B", "MAIN STREET", "SUITE 101"),
    ("3 BLDG 2 IROQUOIS ROAD", "3", "IROQUOIS ROAD", "BLDG 2"),
    ("437 LOWER OAK STREET EAST", "437", "OAK STREET EAST", "LOWER"),
    ("1327 REAR MERSEA RD 6", "1327", "MERSEA RD 6", "REAR"),
    ("20 apt b foundry st", "20", "FOUNDRY ST", "apt b"),          # case kept as published
    # no unit
    ("259 MERSEA RD 15", "259", "MERSEA RD 15", None),
    ("4 LOWER ROAD", "4", "LOWER ROAD", None),                      # LOWER is the street's
    # after the street: a pair designator and its token only
    ("7 CHERRY LANE UNIT 1", "7", "CHERRY LANE", "UNIT 1"),
    ("109 ROBSON ROAD UNIT 904", "109", "ROBSON ROAD", "UNIT 904"),
    ("3 IROQUOIS ROAD  BLD 2", "3", "IROQUOIS ROAD", "BLD 2"),      # doubled space
    ("1217 MERSEA RD 2 APT 3", "1217", "MERSEA RD 2", "APT 3"),
    ("7 CHERRY LANE REAR", "7", "CHERRY LANE", None),               # lone word: street's?
    ("7 CHERRY LANE UNIT", "7", "CHERRY LANE", None),
    ("7 CHERRY LANE UNIT 1 2", "7", "CHERRY LANE", None),
    ("7 OLD CHERRY LANE UNIT 1", "7", "CHERRY LANE", None),         # street not next
    ("8 CHERRY LANE UNIT 1", "7", "CHERRY LANE", None),             # number mismatch
    # left unparsed rather than guessed
    ("17 APT B CLARK STREET EAST APT B", "17", "CLARK STREET EAST", None),   # doubled
    ("44 APT 2 CLARK STREET WEST APT 2", "44", "CLARK STREET WEST", None),
    ("5 ERIE STREET NORTH", "5-15", "ERIE STREET NORTH", None),     # number mismatch
    ("717 HIGHWAY 77", "717", "MERSEA RD 7", None),                 # street mismatch
    ("12 OLD MAIN ST", "12", "MAIN ST", None),                      # not a designator
    ("12 UNIT MAIN ST", "12", "MAIN ST", None),                     # pair word, no token
    ("12 UPPER 2 MAIN ST", "12", "MAIN ST", None),                  # lone word with a token
    ("12 UNIT 3 4 MAIN ST", "12", "MAIN ST", None),
    (None, "12", "MAIN ST", None),
    ("12 UNIT 3 MAIN ST", None, "MAIN ST", None),
    ("12 UNIT 3 MAIN ST", "12", None, None),
])
def test_unit_from_full(full, number, street, unit):
    assert normalize.unit_from_full(full, number, street) == unit


def test_registry_parses_unit_from_full(tmp_path):
    ds = _parse(_write(tmp_path, 'unit_from_full = true\n'
                                 '[fields]\nnumber = "N"\nstreet = "S"\nfull = "F"\n'))
    assert ds.unit_from_full and "unit" not in ds.fields


@pytest.mark.parametrize("body, msg", [
    ('unit_from_full = true\n[fields]\nnumber = "N"\nstreet = "S"\nfull = "F"\nunit = "U"\n',
     "pick one"),
    ('unit_from_full = true\n[fields]\nstreet = "S"\nfull = "F"\n', "needs mapped"),
    ('unit_from_full = true\n[fields]\nnumber = "N"\nfull = "F"\n', "needs mapped"),
    ('unit_from_full = true\n[fields]\nnumber = "N"\nstreet = "S"\n', "needs mapped"),
    ('unit_from_full = true\nunit_from_number = true\n'
     '[fields]\nnumber = "N"\nstreet = "S"\nfull = "F"\n', "pick one"),
    ('unit_from_full = "yes"\n[fields]\nnumber = "N"\nstreet = "S"\nfull = "F"\n',
     "true or false"),
])
def test_registry_rejects_bad_unit_from_full(tmp_path, body, msg):
    with pytest.raises(ValueError, match=msg):
        _parse(_write(tmp_path, body))


def _leamington_feat(gid, num, st, full, lon):
    return {"type": "Feature",
            "properties": {"GlobalID": gid, "N": num, "ST": st, "F": full},
            "geometry": {"type": "Point", "coordinates": [lon, 42.05]}}


def test_canonical_unit_from_full_leaves_unaffected_rows_alone():
    ds = Dataset(slug="_t", provider="T", data_url="x", access="static", format="geojson",
                 key_field="GlobalID", fields={"number": "N", "street": "ST", "full": "F"})
    feats = [_leamington_feat("a", "24", "SEACLIFF DRIVE EAST",
                              "24 UNIT 300 SEACLIFF DRIVE EAST", -82.6),
             _leamington_feat("b", "259", "MERSEA RD 15", "259 MERSEA RD 15", -82.5),
             _leamington_feat("c", "7", "CHERRY LANE", "7 CHERRY LANE UNIT 1", -82.4),
             _leamington_feat("d", "17", "CLARK STREET EAST",
                              "17 APT B CLARK STREET EAST APT B", -82.3)]
    before = [normalize.canonical(ds, f) for f in feats]
    ds.unit_from_full = True
    after = [normalize.canonical(ds, f) for f in feats]
    assert [r["unit"] for r in after] == ["UNIT 300", None, "UNIT 1", None]
    assert [r["identity_key"] for r in after] == ["a", "b", "c", "d"]
    assert after[0]["payload_hash"] != before[0]["payload_hash"]
    assert after[2]["payload_hash"] != before[2]["payload_hash"]
    assert (after[1], after[3]) == (before[1], before[3])


def test_unit_from_full_rewrite_keeps_globalid_keys():
    """GlobalID is volatile, so the stored props cannot recompute the key; the key comes
    from the source id, not the canonical columns, so it is kept - and the next import
    of the same pull is a skip."""
    ds = Dataset(slug="_test_recanon", provider="Test", data_url="x", access="static",
                 format="geojson", key_field="GlobalID",
                 fields={"number": "N", "street": "ST", "full": "F"})
    shutil.rmtree(ds.data_dir, ignore_errors=True)
    feats = [_leamington_feat("{A}", "24", "SEACLIFF DRIVE EAST",
                              "24 UNIT 300 SEACLIFF DRIVE EAST", -82.6),
             _leamington_feat("{B}", "24", "SEACLIFF DRIVE EAST",
                              "24 UNIT 301 SEACLIFF DRIVE EAST", -82.6),
             _leamington_feat("{C}", "259", "MERSEA RD 15", "259 MERSEA RD 15", -82.5)]
    try:
        db.import_snapshot(ds, "snap-2026-01-01.geojson", feats)
        ds.unit_from_full = True
        conn = sqlite3.connect(ds.db_path)
        conn.row_factory = sqlite3.Row
        updates, stats = recanonicalize.plan(ds, conn)
        assert len(updates) == 2 and stats["chains_rekeyed"] == 0
        recanonicalize.apply(conn, updates)
        conn.commit()
        assert sorted(tuple(r) for r in conn.execute(
            "SELECT identity_key, unit FROM addresses")) == \
            [("{A}", "UNIT 300"), ("{B}", "UNIT 301"), ("{C}", None)]
        assert recanonicalize.plan(ds, conn)[0] == []
        conn.close()
        db.import_snapshot(ds, "snap-2026-01-02.geojson", feats)
        assert _snapshot_rows(ds)[1][-1][1] == 1
    finally:
        shutil.rmtree(ds.data_dir, ignore_errors=True)


@pytest.mark.parametrize("slug", ["perth-county", "lennox-addington", "waterloo"])
def test_unit_from_full_stays_off_the_other_full_address_parsers(slug):
    """perth-county / lennox-addington (street_from_full) and waterloo
    (number_unit_from_full) parse their own vocabularies; the trailing-unit extension
    of unit_from_full must not reach them."""
    from src import registry
    ds = registry.load(slug)
    assert not ds.unit_from_full
    assert normalize._DESIGNATOR_WORDS == {"site", "unit", "apt", "suite"}
