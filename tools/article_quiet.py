"""Write the monthly piece for a city-month in which nothing changed.

    python tools/article_quiet.py --city windsor --month 2026-09

A month the vault watched end to end whose every pull came back as the file
already on record has no story to research and no numbers to interpret, so
no headless Claude run is spent on it: this writes the article, a one-line
research note (so article_due reads the month as done) and the README row
from a fixed shape, saying plainly that nothing changed and on what evidence.

Refuses (exit 4) when the month is not quiet - any net or gross change goes
through the monthly-article skill instead - and (exit 3) when the vault did
not watch the month end to end, because "nothing changed" is only true of
the days somebody looked.
"""

import argparse
import datetime as dt
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

from src import registry                 # noqa: E402
import month_digest                      # noqa: E402

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def month_label(month):
    return f"{MONTHS[int(month[5:]) - 1]} {month[:4]}"


def day_label(date):
    d = dt.date.fromisoformat(date)
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def article_text(ds, g):
    m = g["meta"]
    obs = m["observation"]
    label = month_label(m["month"])
    since = day_label(m["opening_snapshot"])
    days = obs["pull_days"]
    total = f"{m['row_count_close']:,}"
    failed = obs["failed_days"]
    read_line = (f"The tracker read {ds.provider}'s address file on {days} days in {label}"
                 + (f" ({failed} further attempt{'s' if failed != 1 else ''} failed)" if failed else "")
                 + f", and every read came back as the same file: the one first seen on {since}.")
    return f"""# Nothing changed in {ds.provider}'s address file in {label}

{read_line} No address was added, retired, renumbered or renamed, and no street name
moved. The file holds {total} records, the same {total} it held at the end of the month before.

## By the numbers

| | |
|---|---|
| New addresses | 0 |
| Retired | 0 |
| Renumbered | 0 |
| Street renames | 0 |
| Address splits | 0 |
| Total on file at month end | {total} |

## What a quiet month means

The file is the municipality's own record of which addresses exist, and this tracker
only ever sees what the municipality publishes. A month in which nothing changed is
a month in which the published file was not updated. It does not say whether no
address was assigned in {label}, or whether addresses were assigned and the
publication is waiting on a batch, a quarter-end, or a person. The file does not
record which, and this piece does not guess.

The month to watch is the one in which the file next moves: a long stretch of
identical reads tends to end with everything that happened in between arriving in
one day.

---
*How this is measured* — The tracker pulls the published file daily and keeps a
snapshot whenever its contents differ from the last one kept. {label} produced no
new snapshot; the diff from the last snapshot before the month to the last one in
it is therefore empty on every count. The {days} reads are recorded in the
tracker's pull calendar, which is what separates a quiet month from an unobserved
one. Daily reports for this city: [{m['site_url']}]({m['site_url']}).

{m['attribution']} · Daily reports: [ontario-address-changes]({m['site_url']})
"""


def research_text(ds, g):
    m = g["meta"]
    return f"""# Research notes — {ds.provider}, {m['month']}

Nothing to research: the month produced no change in the file ({m['observation']['pull_days']}
reads, all identical to the snapshot of {m['opening_snapshot']}), so there are no named
things to look up. Written by `tools/article_quiet.py`.
"""


README = os.path.join(ROOT, "articles", "README.md")
ROW_RE = re.compile(r"^\| (\d{4}-\d{2}) \| ([a-z0-9-]+) \| ")


def add_readme_row(month, slug, lead, net="0"):
    """Insert `| month | slug | net | lead |` into the months table of
    articles/README.md, keeping the table ordered by month then city.
    A row already there for the pair is replaced."""
    with open(README, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    head = next(i for i, l in enumerate(lines) if l.startswith("| Month | City |"))
    i = head + 2
    rows = []
    while i < len(lines) and lines[i].startswith("|"):
        rows.append(lines[i])
        i += 1
    new = f"| {month} | {slug} | {net} | {lead} |"
    rows = [r for r in rows if not (ROW_RE.match(r) and ROW_RE.match(r).groups() == (month, slug))]
    rows.append(new)

    def key(r):
        mm = ROW_RE.match(r)
        return (mm.group(1), mm.group(2)) if mm else ("", r)
    rows.sort(key=key)
    lines[head + 2:i] = rows
    with open(README, "w", encoding="utf-8", newline="") as f:
        f.write(nl.join(lines))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--city", required=True)
    p.add_argument("--month", required=True, help="YYYY-MM")
    p.add_argument("--force", action="store_true", help="overwrite existing files")
    a = p.parse_args()

    ds = registry.load(a.city)
    if not ds.publish_reports:
        sys.exit("publish_reports = false: no article for this city")
    g = month_digest.digest(ds, a.month)
    m = g["meta"]
    if not (m["observation"] and m["observation"]["watched"]):
        print(f"{a.city} {a.month}: not watched end to end, nothing can be said")
        sys.exit(3)
    if not m["quiet"]:
        print(f"{a.city} {a.month}: not quiet (net {g['net']}, gross {g['gross']}); "
              "use the monthly-article skill")
        sys.exit(4)

    paths = {
        "researched": os.path.join(ROOT, "articles", "researched", f"{a.city}-{a.month}.md"),
        "research": os.path.join(ROOT, "articles", "research", f"{a.city}-{a.month}.md"),
    }
    if not a.force and any(os.path.exists(x) for x in paths.values()):
        sys.exit(f"{a.city} {a.month}: article files already exist (use --force)")
    texts = {"researched": article_text(ds, g), "research": research_text(ds, g)}
    for k, path in paths.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(texts[k])
        print(f"wrote {os.path.relpath(path, ROOT)}")
    obs = m["observation"]
    add_readme_row(a.month, a.city,
                   f"Nothing changed: {obs['pull_days']} reads, the file unchanged since "
                   f"{day_label(m['opening_snapshot'])}")
    print("updated articles/README.md")


if __name__ == "__main__":
    main()
