"""Review brief for flagged events.

    python .claude/skills/review-flags/brief.py                 # open flags, oldest first
    python .claude/skills/review-flags/brief.py <slug> <date>   # full brief for that day

The brief is everything a verdict needs in one place: the flag entries, sample
rows with their old->new values from the SCD-2 store, the full value-transition
distribution, this city's past flags with the same signature, and the vault's
own day verdict when addressvault is reachable. Read it, decide
business / technical / bug, and file the verdict in flags.toml (see SKILL.md).
"""

import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, date as date_t

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT)

from src import db, diff, flags, registry  # noqa: E402

SAMPLES = 10


def _addr(r):
    if r.get("full"):
        return r["full"]
    return " ".join(p for p in (r.get("number"), r.get("street")) if p).strip() \
        or r.get("identity_key", "")


def _list_open():
    ledger = flags.load_ledger()
    open_flags = sorted((f for f in ledger if f.get("status", "open") != "reviewed"),
                        key=lambda f: (f.get("detected", ""), f.get("slug", "")))
    if not open_flags:
        print("No open flags. Nothing to review.")
        return
    print(f"{len(open_flags)} open flag(s), oldest first:\n")
    for f in open_flags:
        fields = f": {', '.join(f['fields'])}" if f.get("fields") else ""
        print(f"  {f['slug']} {f['date']}  {f['signature']}{fields}")
        print(f"      {f['scope']}")
        if f.get("detail"):
            print(f"      {f['detail']}")
    print("\nNext: brief.py <slug> <date> for each, oldest first.")


def _find_pair(ds, date):
    snaps = diff.nonskipped(ds)
    for i in range(1, len(snaps)):
        if diff.snap_date(snaps[i]) == date:
            return snaps[i - 1], snaps[i]
    return None, None


def _sample_modified(rows, fs):
    for m in rows[:SAMPLES]:
        chs = "; ".join(f"{c['field']}: {c['old']!r} -> {c['new']!r}"
                        for c in m["changes"])
        print(f"    {_addr(m)}  |  {chs}")
    if len(rows) > SAMPLES:
        print(f"    ... and {len(rows) - SAMPLES:,} more")
    for field in fs:
        if field == "location":
            continue
        pairs = Counter((str(c["old"]), str(c["new"])) for m in rows
                        for c in m["changes"] if c["field"] == field)
        print(f"\n  All {field} transitions ({len(pairs)} distinct):")
        for (old, new), n in pairs.most_common(10):
            print(f"    {old!r} -> {new!r}  x{n:,}")
        if len(pairs) > 10:
            print(f"    ... and {len(pairs) - 10} more distinct transitions")


def _sample_plain(rows, label):
    for r in rows[:SAMPLES]:
        print(f"    {_addr(r)}  ({r.get('identity_key', '')})")
    if len(rows) > SAMPLES:
        print(f"    ... and {len(rows) - SAMPLES:,} more")
    streets = Counter(r.get("street") or "?" for r in rows)
    print(f"\n  {label} rows spread over {len(streets)} street(s); top:")
    for s, n in streets.most_common(8):
        print(f"    {s}  x{n:,}")
    print("  (many streets at low counts reads like a sweep/replay; few streets"
          " at high counts reads like a subdivision or a real removal)")


def _vault_verdict(slug, date):
    days = max((date_t.today() - datetime.strptime(date, "%Y-%m-%d").date()).days + 5, 14)
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "addressvault.cli", "report", "--json",
             "--days", str(days)],
            capture_output=True, text=True, encoding="utf-8", timeout=120)
        data = json.loads(proc.stdout)
    except Exception as e:
        print(f"  (vault unreachable: {e})")
        return
    hits = [c for c in data.get("changes", [])
            if c.get("slug") == slug and c.get("date") == date]
    if not hits:
        print(f"  vault has no anomaly row for {slug} {date} within {days} days "
              "(the pull itself looked ordinary at the wire)")
    for c in hits:
        print(f"  vault: verdict={c.get('verdict') or 'null (unreviewed)'}  "
              f"why={c.get('why', '')}")
        if c.get("note"):
            print(f"         note: {c['note']}")


def _brief(slug, date):
    ds = registry.load(slug)
    ledger = flags.load_ledger()
    day_flags = [f for f in ledger if f.get("slug") == slug and f.get("date") == date]
    if not day_flags:
        sys.exit(f"no ledger entries for {slug} {date}")

    old, new = _find_pair(ds, date)
    if not new:
        sys.exit(f"{slug}: no non-skipped snapshot dated {date} "
                 "(repaired store? check data/ and the ledger entry)")
    d = diff.compute_diff(ds, old["id"], new["id"])
    print(f"=== {slug} {date}  ({diff.snap_date(old)} -> {date}, "
          f"{old['row_count']:,} -> {new['row_count']:,} rows) ===")

    for fl in day_flags:
        fields = f" [{', '.join(fl['fields'])}]" if fl.get("fields") else ""
        print(f"\n--- {fl['signature']}{fields}  "
              f"(status: {fl.get('status', 'open')}"
              + (f", verdict: {fl['verdict']}" if fl.get("verdict") else "") + ") ---")
        print(f"  {fl['scope']}")
        if fl.get("detail"):
            print(f"  {fl['detail']}")
        print()
        if fl["signature"] == "mass-added":
            _sample_plain(d["added"], "Added")
        elif fl["signature"] == "mass-removed":
            _sample_plain(d["removed"], "Removed")
        elif fl["signature"] == "mass-modified":
            fs = tuple(sorted(fl.get("fields", [])))
            rows = [m for m in d["modified"] if flags._fieldset(m) == fs]
            _sample_modified(rows, fs)

        same = [f for f in ledger
                if f.get("slug") == slug and f.get("signature") == fl["signature"]
                and f.get("fields", []) == fl.get("fields", [])
                and f.get("date") != date]
        if same:
            print(f"\n  This city has {len(same)} other {fl['signature']} flag(s):")
            for f in same:
                v = f.get("verdict") or f.get("status", "open")
                print(f"    {f['date']}: {v}"
                      + (f" — {f['note']}" if f.get("note") else ""))

    print("\n--- vault day verdict ---")
    _vault_verdict(slug, date)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        _list_open()
    elif len(sys.argv) == 3:
        _brief(sys.argv[1], sys.argv[2])
    else:
        sys.exit(__doc__)
