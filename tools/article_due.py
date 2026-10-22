"""Which monthly articles are due?  The decision behind monthly-article.ps1.

    python tools/article_due.py --city toronto [--month YYYY-MM]     one city
    python tools/article_due.py --all [--since YYYY-MM]              every city

One city, one month (defaults to the previous calendar month): prints one JSON
object and exits with

  0  due      the month is complete, no open flag is dated inside it, and at
              least one of the two article files is missing ("missing" lists
              which of research / researched; "quiet" says whether nothing
              changed, so tools/article_quiet.py can write it without Claude)
  2  done     both files exist
  3  waiting  the month is not complete yet, or an open flag is dated inside it
              ("reason" says which); try again tomorrow
  1  error    unknown city, or publish_reports = false (no article allowed)

--all: every dataset, every complete month from --since (default 2026-09, the
first month written for all cities) to the previous calendar month, as a JSON
list of the same objects (status due / done / waiting), oldest month first and
cities alphabetical within it. Exit 0. Licence-gated cities and months a city
cannot write (not watched end to end, first observed month) are not listed.

Completeness is month_digest.complete_months: the store's own rule, or the
vault's pull calendar watching the month end to end. Flags are matched on the
event's `date` (the day the change happened), not `detected`.
"""

import argparse
import datetime as dt
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

from src import flags, registry          # noqa: E402
import month_digest                      # noqa: E402

VARIANTS = ("research", "researched")
ALL_SINCE = "2026-09"


def previous_month(today=None):
    today = today or dt.date.today()
    first = today.replace(day=1)
    last = first - dt.timedelta(days=1)
    return f"{last.year}-{last.month:02d}"


def article_paths(slug, month):
    return {v: os.path.join(ROOT, "articles", v, f"{slug}-{month}.md") for v in VARIANTS}


def open_flags_in(ledger, slug, month):
    return [f for f in ledger
            if f.get("slug") == slug
            and f.get("status", "open") != "reviewed"
            and str(f.get("date", ""))[:7] == month]


def decide(ds, month, ledger, complete=None):
    """The status object for one city-month. `complete` is the city's complete
    month list when the caller already has it."""
    out = {"city": ds.slug, "month": month}
    if not ds.publish_reports:
        return dict(out, status="error",
                    reason="publish_reports = false: licence forbids republication, no article")
    paths = article_paths(ds.slug, month)
    missing = [v for v, path in paths.items() if not os.path.exists(path)]
    out["missing"] = missing
    if not missing:
        return dict(out, status="done")
    if complete is None:
        complete = month_digest.complete_months(ds)
    if month not in complete:
        return dict(out, status="waiting", reason=f"{month} is not a complete month yet")
    held = open_flags_in(ledger, ds.slug, month)
    if held:
        return dict(out, status="waiting",
                    reason=f"{len(held)} open flag(s) dated inside {month}",
                    flags=[f"{f['date']} {f['signature']}" for f in held])
    g = month_digest.digest(ds, month)
    return dict(out, status="due", quiet=g["meta"]["quiet"],
                net=g["net"], observed=g["meta"]["observation"])


EXIT = {"due": 0, "error": 1, "done": 2, "waiting": 3}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--city", help="dataset slug (default toronto unless --all)")
    p.add_argument("--month", help="YYYY-MM (default: previous calendar month)")
    p.add_argument("--all", action="store_true", help="every city, every month since --since")
    p.add_argument("--since", default=ALL_SINCE, help=f"with --all: first month (default {ALL_SINCE})")
    a = p.parse_args()
    ledger = flags.load_ledger()
    last = previous_month()

    if a.all:
        out = []
        for ds in registry.load_all():
            if not ds.publish_reports:
                continue
            for month in month_digest.complete_months(ds):
                if a.since <= month <= (a.month or last):
                    out.append(decide(ds, month, ledger, complete=[month]))
        out.sort(key=lambda d: (d["month"], d["city"]))
        print(json.dumps(out))
        return

    month = a.month or last
    city = a.city or "toronto"
    try:
        ds = registry.load(city)
    except Exception as e:                # unknown slug, bad TOML
        print(json.dumps({"city": city, "month": month, "status": "error",
                          "reason": f"cannot load city: {e}"}))
        sys.exit(1)
    out = decide(ds, month, ledger)
    print(json.dumps(out))
    sys.exit(EXIT[out["status"]])


if __name__ == "__main__":
    main()
