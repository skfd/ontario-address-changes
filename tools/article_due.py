"""Is a city's monthly article due?  The decision behind monthly-article.ps1.

    python tools/article_due.py --city toronto [--month YYYY-MM]

The target month defaults to the previous calendar month.  Prints one JSON
object and exits with:

  0  due      the month is complete, no open flag is dated inside it, and at
              least one of the three article files is missing ("missing" lists
              which of offline / research / researched)
  2  done     all three files exist
  3  waiting  the month is not complete yet, or an open flag is dated inside it
              ("reason" says which); try again tomorrow
  1  error    unknown city, or publish_reports = false (no article allowed)

Completeness is month_digest.complete_months: the month opens where the
previous one closed and at least one snapshot follows it.  Flags are matched
on the event's `date` (the day the change happened), not `detected`.
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

VARIANTS = ("offline", "research", "researched")


def previous_month(today=None):
    today = today or dt.date.today()
    first = today.replace(day=1)
    last = first - dt.timedelta(days=1)
    return f"{last.year}-{last.month:02d}"


def article_paths(slug, month):
    return {v: os.path.join(ROOT, "articles", v, f"{slug}-{month}.md") for v in VARIANTS}


def open_flags_in(slug, month):
    return [f for f in flags.load_ledger()
            if f.get("slug") == slug
            and f.get("status", "open") != "reviewed"
            and str(f.get("date", ""))[:7] == month]


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--city", default="toronto")
    p.add_argument("--month", help="YYYY-MM (default: previous calendar month)")
    a = p.parse_args()
    month = a.month or previous_month()
    out = {"city": a.city, "month": month}

    def finish(code, **kw):
        out.update(kw)
        print(json.dumps(out))
        sys.exit(code)

    try:
        ds = registry.load(a.city)
    except Exception as e:                # unknown slug, bad TOML
        finish(1, status="error", reason=f"cannot load city: {e}")
    if not ds.publish_reports:
        finish(1, status="error",
               reason="publish_reports = false: licence forbids republication, no article")

    paths = article_paths(a.city, month)
    missing = [v for v, path in paths.items() if not os.path.exists(path)]
    out["missing"] = missing
    if not missing:
        finish(2, status="done")

    if month not in month_digest.complete_months(ds):
        finish(3, status="waiting", reason=f"{month} is not a complete month yet")
    held = open_flags_in(a.city, month)
    if held:
        finish(3, status="waiting",
               reason=f"{len(held)} open flag(s) dated inside {month}",
               flags=[f"{f['date']} {f['signature']}" for f in held])

    finish(0, status="due")


if __name__ == "__main__":
    main()
