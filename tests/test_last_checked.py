"""The index leads with the newest check, and keeps no empty days behind it.

The vault keeps no copy of an unchanged day, so the tracker once recorded nothing
for one and Guelph's reports read "last snapshot 2026-09-17" while the City was
being pulled daily -- a quiet source and a stopped updater looked the same. And
a snapshot whose only movement was in a field since ignored rendered as an empty
"No changes" day in the middle of the history, which says nothing.
"""

import json
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, flags, report
from src.registry import Dataset

SLUG = "_test_checked"


def _ds(ignore=()):
    return Dataset(slug=SLUG, provider="Test", data_url="x", access="static",
                   format="geojson", key_field="ID", ignore_fields=list(ignore),
                   fields={"number": "NUM", "street": "ST", "full": "FULL"})


def _feats(n, note="a"):
    return [{"type": "Feature",
             "properties": {"ID": str(i), "NUM": str(i), "ST": "Main St",
                            "FULL": f"{i} Main St", "NOTE": note},
             "geometry": {"type": "Point", "coordinates": [-75.1 + i / 1e4, 45.1]}}
            for i in range(n)]


def test_an_unchanged_pull_is_recorded_once_under_its_own_date():
    ds = _ds()
    if os.path.isdir(ds.data_dir):
        shutil.rmtree(ds.data_dir)
    try:
        db.import_snapshot(ds, "snap-2026-01-01.geojson", _feats(3))
        for _ in range(2):  # a rerun of the same day adds nothing
            db.record_check(ds, "snap-2026-01-01.geojson", "2026-01-09", "2026-01-09T12:00:00")
        snaps = db.get_snapshots(ds)
        assert [(s["filename"], s["skipped"]) for s in snaps] == [
            ("snap-2026-01-01.geojson", 0), (f"{SLUG}-2026-01-09.geojson", 1)], snaps
        assert snaps[1]["content_hash"] == snaps[0]["content_hash"]
        assert snaps[1]["downloaded"] == "2026-01-09T12:00:00"
    finally:
        shutil.rmtree(ds.data_dir)


def test_the_index_leads_with_the_check_and_drops_empty_days():
    ds = _ds()
    if os.path.isdir(ds.data_dir):
        shutil.rmtree(ds.data_dir)
    db.import_snapshot(ds, "snap-2026-01-01.geojson", _feats(3))
    db.import_snapshot(ds, "snap-2026-01-02.geojson", _feats(4))            # +1
    db.import_snapshot(ds, "snap-2026-01-03.geojson", _feats(4, note="b"))  # NOTE only
    db.record_check(ds, "snap-2026-01-03.geojson", "2026-01-09", "2026-01-09T12:00:00")

    docs = tempfile.mkdtemp()
    os.makedirs(os.path.join(docs, SLUG))
    orphan = os.path.join(docs, SLUG, "report-2025-12-31.html")
    open(orphan, "w").close()
    real = flags.record, report.generate_flags_page, report.DOCS_DIR
    flags.record = lambda new, *a, **kw: []
    report.generate_flags_page = lambda: None
    report.DOCS_DIR = docs
    try:
        # NOTE is ignored only now: the reprocessing that empties 01-03.
        report.generate_all([_ds(ignore=["NOTE"])])
        city = os.path.join(docs, SLUG)
        assert sorted(f for f in os.listdir(city) if f.startswith("report-")) == [
            "report-2026-01-01.html", "report-2026-01-02.html"]

        with open(os.path.join(city, "index.html"), encoding="utf-8") as f:
            index = f.read()
        dates = re.findall(r'class="date">([^<]+)<', index)
        assert dates[0].endswith("Jan 09, 2026"), dates
        assert len(dates) == 3, dates                   # check, 01-02, baseline
        assert index.count("No changes") == 1

        with open(os.path.join(city, "_card.json"), encoding="utf-8") as f:
            assert json.load(f)["last_checked"] == "2026-01-09"
    finally:
        flags.record, report.generate_flags_page, report.DOCS_DIR = real
        shutil.rmtree(docs)
        shutil.rmtree(ds.data_dir)


if __name__ == "__main__":
    test_an_unchanged_pull_is_recorded_once_under_its_own_date()
    test_the_index_leads_with_the_check_and_drops_empty_days()
