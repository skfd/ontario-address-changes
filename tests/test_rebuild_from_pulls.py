"""tools/rebuild_from_pulls.py --gap-dates: dating hidden rows across a no-pull gap.

The shape is sdg's (2026-10-24): an old key that is a bare prefix on some rows, so the
importer kept one row per prefix and never stored the rest; days with no raw pull in
the middle of the history; and a hidden set that differs on the raw days either side.
The override must date every difference row, and nothing else.
"""

import dataclasses
import gc
import os
import shutil
import sqlite3
import sys
import json

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize
from src.registry import Dataset
from tools import rebuild_from_pulls as rb
from tools import recanonicalize

OLD = Dataset(slug="_test_gapdates", provider="Test", data_url="x", access="static",
              format="geojson", key_field="UID", synth_fields=["number", "street", "unit"],
              fields={"number": "NUM", "street": "ST", "unit": "U", "full": "FULL"})
NEW = dataclasses.replace(OLD, key_field="")


def _f(uid, num):
    return {"type": "Feature",
            "properties": {"UID": uid, "NUM": num, "ST": "Main St", "U": None,
                           "FULL": f"{num} Main St"},
            "geometry": {"type": "Point", "coordinates": [-75.0 - int(num) / 1000, 45.0]}}


A1, P2, H3, G4, N5, B9, C10 = (_f("T_1", "1"), _f("T_", "2"), _f("T_", "3"), _f("T_", "4"),
                               _f("T_", "5"), _f("T_9", "9"), _f("T_10", "10"))
# "T_" is the bare prefix: the old rule keeps 2 and hides 3 and 4 on day 1, 3 and 5 on
# day 4 - 4 goes and 5 appears somewhere in the two days with no raw pull.
DAYS = [("snap-2026-01-01.geojson", [A1, P2, H3, G4], True),
        ("snap-2026-01-02.geojson", [A1, P2, H3, G4, B9], False),
        ("snap-2026-01-03.geojson", [A1, P2, H3, G4, B9, C10], False),
        ("snap-2026-01-04.geojson", [A1, P2, H3, B9, C10, N5], True)]   # a skip, old rule


def key(f):
    return normalize.canonical(NEW, f)["identity_key"]


def _build(monkeypatch, days):
    """The old store, built under OLD from `days`, then re-keyed under NEW - the real
    sequence: recanonicalize first, so old and new keys compare. Raw days get a file."""
    tmp = dataclasses.replace(NEW, slug=f"_rebuild_{NEW.slug}")
    for d in (NEW.data_dir, tmp.data_dir):
        shutil.rmtree(d, ignore_errors=True)
        assert not os.path.exists(d), f"left over from an earlier run: {d}"
    for fn, feats, raw in days:
        db.import_snapshot(OLD, fn, feats)
        if raw:
            with open(os.path.join(OLD.data_dir, fn), "w", encoding="utf-8") as f:
                json.dump({"type": "FeatureCollection", "features": feats}, f)
    conn = sqlite3.connect(NEW.db_path)
    conn.row_factory = sqlite3.Row
    recanonicalize.apply(conn, recanonicalize.plan(NEW, conn, OLD)[0])
    conn.commit()
    conn.close()

    def local_only(ds, filename):
        p = os.path.join(ds.data_dir, filename)
        return p if os.path.exists(p) else None
    monkeypatch.setattr(rb, "raw_path", local_only)
    return tmp


@pytest.fixture
def clean():
    yield
    gc.collect()        # a refusal leaves the tool's read-only connection to the store open
    for d in (NEW.data_dir, os.path.join(os.path.dirname(NEW.data_dir), f"_rebuild_{NEW.slug}")):
        shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def store(monkeypatch, clean):
    tmp = _build(monkeypatch, DAYS)
    assert _spans(NEW)[1] == [0, 0, 0, 1]
    return tmp


def _gap_file(tmp_path, added, gone):
    p = tmp_path / "gap.toml"
    p.write_text("[added]\n" + "".join(f'"{k}" = "{d}"\n' for k, d in added.items())
                 + "[gone]\n" + "".join(f'"{k}" = "{d}"\n' for k, d in gone.items()),
                 encoding="utf-8")
    return rb.load_gap_dates(str(p))


def _spans(tmp):
    conn = sqlite3.connect(tmp.db_path)
    spans = {k: (lo, hi) for k, lo, hi in conn.execute(
        "SELECT identity_key, min_snapshot_id, max_snapshot_id FROM addresses")}
    skipped = [s for (s,) in conn.execute("SELECT skipped FROM snapshots ORDER BY id")]
    conn.close()
    return spans, skipped


def test_refuses_a_changing_hidden_set_without_the_override(store):
    with pytest.raises(SystemExit, match=r"1 added, 1 gone.*--gap-dates"):
        rb.rebuild(NEW, OLD)


@pytest.mark.parametrize("added, gone, spans5, spans4, last, skipped", [
    # both inside the gap: day 4 stays a skip (which extends no span)
    ("2026-01-02", "2026-01-03", (2, 3), (1, 2), 3, [0, 0, 0, 1]),
    # no evidence, dated to the first raw pull that shows it: day 4 records both
    ("2026-01-04", "2026-01-04", (4, 4), (1, 3), 4, [0, 0, 0, 0]),
])
def test_override_dates_each_difference_row(store, tmp_path, added, gone, spans5, spans4,
                                            last, skipped):
    rb.rebuild(NEW, OLD, _gap_file(tmp_path, {key(N5): added}, {key(G4): gone}))
    spans, flags = _spans(store)
    assert flags == skipped
    assert spans[key(N5)] == spans5
    assert spans[key(G4)] == spans4
    assert spans[key(H3)] == (1, last), "hidden on both sides: present all through"
    assert spans[key(P2)] == (1, last) and spans[key(B9)] == (2, last)


def test_refuses_an_undated_difference_row(store, tmp_path):
    with pytest.raises(SystemExit, match="does not date 1 hidden-set difference rows"):
        rb.rebuild(NEW, OLD, _gap_file(tmp_path, {key(N5): "2026-01-02"}, {}))


def test_refuses_a_key_that_is_no_difference(store, tmp_path):
    gap = _gap_file(tmp_path, {key(N5): "2026-01-02", key(H3): "2026-01-02"},
                    {key(G4): "2026-01-03"})
    with pytest.raises(SystemExit, match="1 keys that are no hidden-set difference"):
        rb.rebuild(NEW, OLD, gap)


@pytest.mark.parametrize("date", ["2026-01-01", "2026-01-05", "2026-01-06"])
def test_refuses_a_date_outside_the_gap(store, tmp_path, date):
    gap = _gap_file(tmp_path, {key(N5): date}, {key(G4): "2026-01-03"})
    with pytest.raises(SystemExit, match="neither a non-skipped snapshot in the gap"):
        rb.rebuild(NEW, OLD, gap)


def test_refuses_the_wrong_side(store, tmp_path):
    gap = _gap_file(tmp_path, {key(N5): "2026-01-02", key(G4): "2026-01-03"}, {})
    with pytest.raises(SystemExit, match=r"is under \[added\] but is gone"):
        rb.rebuild(NEW, OLD, gap)


def test_gap_file_rejects_other_tables_and_bad_dates(tmp_path):
    p = tmp_path / "gap.toml"
    p.write_text('[changed]\n"syn:x" = "2026-01-02"\n', encoding="utf-8")
    with pytest.raises(SystemExit, match="only \\[added\\] and \\[gone\\]"):
        rb.load_gap_dates(str(p))
    p.write_text('[added]\n"syn:x" = "Jan 2"\n', encoding="utf-8")
    with pytest.raises(SystemExit, match="not a YYYY-MM-DD date"):
        rb.load_gap_dates(str(p))


def test_a_raw_skip_may_become_a_change_when_only_a_hidden_row_changed(monkeypatch, clean):
    """No gap at all: on day 2 only a row the old rule hid changes. The old store saw a
    skip; the replay records the change, and that flip is accepted."""
    h3b = _f("T_", "3")
    h3b["properties"]["FULL"] = "3 Main Street"
    tmp = _build(monkeypatch, [("snap-2026-01-01.geojson", [A1, P2, H3], True),
                               ("snap-2026-01-02.geojson", [A1, P2, h3b], True)])
    assert _spans(NEW)[1] == [0, 1]
    rb.rebuild(NEW, OLD)
    spans, flags = _spans(tmp)
    assert flags == [0, 0]
    assert spans[key(H3)] == (2, 2), "modified on day 2: the key stays, a new version"
    assert spans[key(P2)] == (1, 2)
