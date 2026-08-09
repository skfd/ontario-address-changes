"""Triage the daily run: what has gone stale, what was refused, what failed.

    python .claude/skills/data-integrity/health.py [--stale] [--blocks]
                                                   [--runs] [--drift] [--city SLUG]

With no flags: stale + blocks + runs, all of which read local state only. `--drift` is
the one section that goes to the network, so it is never in the default set.

  stale   Days since each city's last snapshot, judged against that city's own gap
          history rather than a flat threshold. This is the ONLY place the frozen-vault
          failure is visible: run.py checks the filename before db.already_imported, so
          a vault serving the same dated file every day writes no snapshot row at all -
          not even a skip - and logs/runs.csv reports the day a success.
  blocks  Pulls the import guards refused (the `blocks` table). `attempts` - how many
          days running - is what separates a transient degraded pull from a source that
          really changed and now needs a config edit.
  runs    logs/runs.csv outcomes, days with no run at all, and per-city ERROR lines
          from logs/update.log.
  drift   Each arcgis layer's current field roster and copyright text against what we
          actually store. Catches URL rot, a source adding or dropping a column, and a
          licence rewrite.

Read-only, and never edits a dataset. Deciding what to do about what it finds is the
skill's job, not this script's.
"""

import argparse
import csv
import datetime
import json
import os
import re
import sys
import urllib.request
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

from src import db, normalize, registry

LOGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))), "logs")

# A city is only called stale once it is past BOTH its own p90 gap and this floor.
# Without the floor, every city that normally updates daily reports stale the moment
# a source takes a weekend off.
STALE_MIN_DAYS = 3
RUNS_SHOWN = 14
DRIFT_TIMEOUT = 60

_DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def _pct(xs, p):
    """The p-th percentile of a sorted-able list, nearest-rank."""
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))]


def _snapshot_dates(ds):
    """Every distinct date this city has a snapshot for, oldest first.

    Read from the filename, which carries the date the vault stamped the pull; the
    `downloaded` column would instead date a backfill to the day it was run.
    """
    if not os.path.exists(ds.db_path):
        return []
    conn = db.init_db(ds)
    names = [r[0] for r in conn.execute("SELECT filename FROM snapshots ORDER BY id")]
    conn.close()
    out = set()
    for n in names:
        m = _DATE.search(n)
        if m:
            out.add(datetime.date(*map(int, m.groups())))
    return sorted(out)


def stale(datasets, today):
    rows = []
    for ds in datasets:
        dates = _snapshot_dates(ds)
        if not dates:
            rows.append((float("inf"), ds.slug, None, 0, 0, 0, 0))
            continue
        age = (today - dates[-1]).days
        gaps = [(b - a).days for a, b in zip(dates, dates[1:])]
        # p90 of the city's own gaps, so an irregular publisher is judged by its own
        # rhythm: toronto runs 1-6 days between snapshots and is fine at 5, while a
        # city that has never missed a day is not fine at 5.
        p90 = _pct(gaps, 0.9) if gaps else 0
        rows.append((age / max(p90, 1), ds.slug, dates[-1], age, p90,
                     max(gaps or [0]), len(dates)))

    print("=== stale (days since last snapshot, vs the city's own gap history) ===")
    print("  A frozen vault leaves no other trace: no snapshot row, no skip row, and a")
    print("  clean exit in runs.csv. Nothing here proves the source stopped publishing -")
    print("  only that we stopped recording it. Confirm on the vault side.\n")
    print(f"  {'':22} {'last':>11} {'age':>5} {'p90':>5} {'max':>5} {'dates':>6}")
    flagged = 0
    for ratio, slug, last, age, p90, mx, n in sorted(rows, reverse=True):
        if last is None:
            print(f"  {slug:22} {'no snapshots at all':>11}")
            flagged += 1
            continue
        bad = age > p90 and age >= STALE_MIN_DAYS
        flagged += bad
        print(f"  {slug:22} {last.isoformat():>11} {age:4}d {p90:4}d {mx:4}d {n:6}"
              f"{'   <- STALE' if bad else ''}")
    print(f"\n  {flagged} of {len(rows)} cities past their own p90 gap.")


def blocks(datasets):
    print("\n=== refused pulls (blocks table, unresolved) ===")
    print("  A refusal already shows on the site as a red 'needs a look' badge. What it")
    print("  cannot decide is whether the source is degraded or genuinely different -")
    print("  read `attempts`, then references/corrupt-pulls.md.\n")
    any_block = False
    for ds in datasets:
        b = db.active_block(ds)
        if not b:
            continue
        any_block = True
        print(f"  {ds.slug:22} since {b['since']}  {b['attempts']} attempt(s)")
        print(f"  {'':22} {b['filename']}")
        print(f"  {'':22} {b['reason']}")
    if not any_block:
        print("  none.")


def runs(today):
    path = os.path.join(LOGS, "runs.csv")
    print("\n=== runs.csv ===")
    if not os.path.exists(path):
        print(f"  {path} not found.")
        return
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("  empty.")
        return

    seen = {}
    for r in rows:
        d = _DATE.search(r["started"])
        if d:
            seen[datetime.date(*map(int, d.groups()))] = r
    tally = Counter(r["exit"] for r in rows)
    print(f"  {len(rows)} runs, {min(seen)} .. {max(seen)}   outcomes: "
          f"{dict(tally.most_common())}")
    print("  'offline' and 'metered' are deliberate skips, not failures; a numeric exit")
    print("  is the real one. attempts > 1 means daily-update.ps1 retried itself.\n")
    for d in sorted(seen)[-RUNS_SHOWN:]:
        r = seen[d]
        note = ("" if r["exit"] == "0"
                else "   <- deliberate skip, not a failure"
                if r["exit"] in ("offline", "metered")
                else "   <- FAILED, needs a look")
        print(f"  {d} exit={r['exit']:<14} attempts={r['attempts']}{note}")

    missing = [str(min(seen) + datetime.timedelta(days=i))
               for i in range((today - min(seen)).days + 1)
               if (min(seen) + datetime.timedelta(days=i)) not in seen]
    print(f"\n  days with no run at all: {len(missing)}"
          + (f" ({', '.join(missing[-10:])})" if missing else ""))

    log = os.path.join(LOGS, "update.log")
    if os.path.exists(log):
        with open(log, encoding="utf-8", errors="replace") as f:
            errs = Counter(m.group(1) for m in
                           re.finditer(r"ERROR \(([^)]+)\)", f.read()))
        print(f"  update.log ERROR lines: {dict(errs.most_common(10)) or 'none'}"
              " (last run only - the file is rewritten each time)")


def _layer_json(url):
    with urllib.request.urlopen(f"{url}?f=json", timeout=DRIFT_TIMEOUT) as r:
        return json.load(r)


def drift(datasets):
    print("\n=== source drift (live schema vs what we store) ===")
    print("  Feeds city-tune rather than deciding anything: a field that appeared or")
    print("  vanished is a config question, not an integrity one.\n")
    for ds in datasets:
        if ds.access != "arcgis":
            print(f"  {ds.slug:22} static {ds.format} - not probed")
            continue
        try:
            meta = _layer_json(ds.data_url)
        except Exception as e:                              # URL rot lands here
            print(f"  {ds.slug:22} UNREACHABLE: {type(e).__name__}: {e}")
            continue
        if "fields" not in meta:
            print(f"  {ds.slug:22} no field list in the layer json "
                  f"({meta.get('error', {}).get('message', 'unknown')})")
            continue

        live = {f["name"] for f in meta["fields"]}
        stored = set()
        if os.path.exists(ds.db_path):
            conn = db.init_db(ds)
            # The last NON-SKIPPED snapshot: a skip writes a snapshots row but leaves
            # `addresses` alone, so querying the skipped id back returns no active rows
            # at all and every field in the layer would read as new.
            sid = conn.execute(
                "SELECT MAX(id) FROM snapshots WHERE skipped = 0").fetchone()[0]
            stored = {r[0] for r in conn.execute(
                "SELECT DISTINCT je.key FROM addresses, json_each(addresses.props) AS je "
                "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid))}
            conn.close()
        # Only fields we could have stored count either way: ignore_fields, the
        # volatile ESRI ids and the edit-metadata timestamps never reach props, so
        # neither their absence nor their presence is news.
        never = (normalize.EDIT_METADATA_FIELDS
                 | {f.lower() for f in ds.ignore_fields})
        gone = sorted((stored | set(ds.fields.values())) - live)
        new = sorted(f for f in live - stored - set(ds.fields.values())
                     if f.lower() not in never and not normalize.is_volatile(f))
        note = f"{len(live)} fields"
        if gone:
            note += f"  DROPPED: {', '.join(gone)}"
        if new:
            note += (f"  new ({len(new)}): {', '.join(new[:8])}"
                     + (" ..." if len(new) > 8 else ""))
        print(f"  {ds.slug:22} {note}")
        rights = (meta.get("copyrightText") or "").strip()
        if rights and rights.lower() not in ds.license_name.lower():
            print(f"  {'':22} copyrightText: {rights[:100]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    for name in ("stale", "blocks", "runs", "drift"):
        ap.add_argument(f"--{name}", action="store_true")
    ap.add_argument("--city", help="restrict the per-city sections to one slug")
    args = ap.parse_args()

    picked = {n for n in ("stale", "blocks", "runs", "drift") if getattr(args, n)}
    if not picked:
        picked = {"stale", "blocks", "runs"}

    datasets = [registry.load(args.city)] if args.city else registry.load_all()
    today = datetime.date.today()

    if "stale" in picked:
        stale(datasets, today)
    if "blocks" in picked:
        blocks(datasets)
    if "runs" in picked:
        runs(today)
    if "drift" in picked:
        drift(datasets)


if __name__ == "__main__":
    main()
