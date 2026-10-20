"""db.merge_touching_spans: fold the span pairs the importer would have kept as one."""

import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db
from src.registry import Dataset


@pytest.fixture
def conn():
    ds = Dataset(slug="_test_merge", provider="Test", data_url="x", access="static",
                 format="geojson")
    shutil.rmtree(ds.data_dir, ignore_errors=True)
    c = db.init_db(ds)
    # snapshots 1..6; 3 is a skipped pull
    for sid in range(1, 7):
        c.execute("INSERT INTO snapshots (id, filename, downloaded, row_count, "
                  "content_hash, skipped) VALUES (?, ?, '', 0, '', ?)",
                  (sid, f"x-2026-01-0{sid}.geojson", int(sid == 3)))
    yield c
    c.close()
    shutil.rmtree(ds.data_dir, ignore_errors=True)


def _span(c, key, lo, hi, h):
    c.execute("INSERT INTO addresses (identity_key, min_snapshot_id, max_snapshot_id, "
              "payload_hash, props) VALUES (?, ?, ?, ?, '{}')", (key, lo, hi, h))


def _spans(c):
    return c.execute("SELECT identity_key, min_snapshot_id, max_snapshot_id, payload_hash "
                     "FROM addresses ORDER BY identity_key, min_snapshot_id").fetchall()


def _active(c, sid):
    return sorted(c.execute("SELECT identity_key, payload_hash FROM addresses "
                            "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?",
                            (sid, sid)).fetchall())


def test_folds_adjacent_and_across_a_skipped_pull(conn):
    _span(conn, "a", 1, 1, "h")
    _span(conn, "a", 2, 2, "h")       # adjacent
    _span(conn, "a", 4, 6, "h")       # only the skipped 3 between
    before = {sid: _active(conn, sid) for sid in (1, 2, 4, 5, 6)}
    assert db.merge_touching_spans(conn) == (1, 2)
    assert [tuple(r) for r in _spans(conn)] == [("a", 1, 6, "h")]
    assert {sid: _active(conn, sid) for sid in (1, 2, 4, 5, 6)} == before


def test_keeps_real_changes_and_real_gaps(conn):
    _span(conn, "b", 1, 2, "h1")
    _span(conn, "b", 4, 6, "h2")      # modified: different hash
    _span(conn, "c", 1, 2, "h")
    _span(conn, "c", 5, 6, "h")       # live snapshot 4 between: removed, re-added
    assert db.merge_touching_spans(conn) == (0, 0)
    assert len(_spans(conn)) == 4


def test_folds_only_the_equal_run(conn):
    _span(conn, "d", 1, 1, "h1")
    _span(conn, "d", 2, 2, "h2")
    _span(conn, "d", 4, 4, "h2")
    _span(conn, "d", 5, 6, "h1")
    assert db.merge_touching_spans(conn) == (1, 1)
    assert [tuple(r)[1:] for r in _spans(conn)] == [(1, 1, "h1"), (2, 4, "h2"),
                                                     (5, 6, "h1")]


def test_dry_run_writes_nothing_and_rerun_is_a_noop(conn):
    _span(conn, "e", 1, 1, "h")
    _span(conn, "e", 2, 6, "h")
    assert db.merge_touching_spans(conn, dry_run=True) == (1, 1)
    assert len(_spans(conn)) == 2
    db.merge_touching_spans(conn)
    assert db.merge_touching_spans(conn) == (0, 0)
