"""A licence-blocked city is still flagged, and still publishes nothing.

publish_reports = false means the licence forbids republication: the city keeps
tracking and the site carries only a card saying why there is no link. Flag
detection used to sit below that gate, so the four blocked cities were
structurally invisible to it -- renfrew could have taken a 45k-row sweep and
flags.toml would have stayed silent. Detection now runs for every dataset;
holding is what stays gated (there is nothing to hold back).
"""

import glob
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, flags, report
from src.registry import Dataset


def _ds(slug, publish):
    return Dataset(slug=slug, provider="Test", data_url="x", access="static",
                   format="geojson", publish_reports=publish, key_field="ID",
                   license_name="Restrictive test licence",
                   fields={"number": "NUM", "street": "ST", "full": "FULL"})


def _feats(n):
    return [{"type": "Feature",
             "properties": {"ID": str(i), "NUM": str(i), "ST": "Main St",
                            "FULL": f"{i} Main St"},
             "geometry": {"type": "Point", "coordinates": [-75.1 + i / 1e5, 45.1]}}
            for i in range(n)]


def _run(slug, publish):
    """Import a baseline then a mass add; render; return (recorded, docs_dir)."""
    ds = _ds(slug, publish)
    if os.path.isdir(ds.data_dir):
        shutil.rmtree(ds.data_dir)
    db.import_snapshot(ds, "snap-2026-01-01.geojson", _feats(2_000))
    db.import_snapshot(ds, "snap-2026-01-02.geojson", _feats(3_000))  # +50%

    recorded = []
    real_record, real_docs = flags.record, report.DOCS_DIR
    docs = tempfile.mkdtemp()
    flags.record = lambda new, *a, **kw: (recorded.extend(new), [])[1]
    report.DOCS_DIR = docs
    try:
        report.generate_all([ds])
    finally:
        flags.record, report.DOCS_DIR = real_record, real_docs
        shutil.rmtree(ds.data_dir)
    return recorded, docs


def test_a_blocked_city_is_flagged_but_publishes_nothing():
    recorded, docs = _run("_test_blocked", publish=False)
    try:
        assert [f["signature"] for f in recorded] == ["mass-added"], recorded
        assert recorded[0]["slug"] == "_test_blocked"

        city_dir = os.path.join(docs, "_test_blocked")
        assert glob.glob(os.path.join(city_dir, "report-*.html")) == []
        assert not os.path.exists(os.path.join(city_dir, "index.html"))
        with open(os.path.join(city_dir, "_card.json"), encoding="utf-8") as f:
            card = json.load(f)
        assert card["license_blocked"] is True
        assert card["added"] == 0, "a blocked card states no change counts"
    finally:
        shutil.rmtree(docs)


def test_a_published_city_still_flags_the_same_event():
    """The move must not have changed what a normal city records."""
    recorded, docs = _run("_test_published", publish=True)
    try:
        assert [f["signature"] for f in recorded] == ["mass-added"], recorded
        assert glob.glob(os.path.join(docs, "_test_published", "report-*.html"))
    finally:
        shutil.rmtree(docs)
