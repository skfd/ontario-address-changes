"""Audit one city's source fields across its whole snapshot history.

    python .claude/skills/field-audit/audit.py <slug>

Prints three sections:
  1. Tag inventory  - every prop key ever stored, with the snapshot span it covers.
                      Keys whose span ends early are fields the source dropped;
                      keys spanning a single snapshot appeared and vanished.
  2. Churn tally    - per field, how many modified rows it touched and how many it
                      was the ONLY change on ("solo"). Solo rows are what a field
                      costs the reports on its own.
  3. Change combos  - which fields move together, which reveals derived echoes.

Read-only. Runtime is dominated by one compute_diff per consecutive snapshot pair
(seconds for a mid-size city, a few minutes for Toronto).
"""

import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

from src import db, diff, registry


def _spans(intervals):
    """Merge (min,max) snapshot intervals into '1-14,16-36' form."""
    out = []
    for lo, hi in sorted(intervals):
        if out and lo <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], hi)
        else:
            out.append([lo, hi])
    return ",".join(f"{a}" if a == b else f"{a}-{b}" for a, b in out), out


def inventory(ds, snaps):
    """Prop key -> stored row-versions + the snapshot spans it appears in."""
    import json
    conn = db.init_db(ds)
    rows = conn.execute("SELECT min_snapshot_id, max_snapshot_id, props FROM addresses")
    ivals = defaultdict(list)
    count = Counter()
    for mn, mx, props in rows:
        for k in json.loads(props):
            count[k] += 1
            ivals[k].append((mn, mx))
    conn.close()

    first, last = snaps[0]["id"], snaps[-1]["id"]
    date = {s["id"]: diff.snap_date(s) for s in snaps}
    print(f"=== tag inventory ({len(count)} keys ever stored) ===")
    print("Keys already in ignore_fields are absent from snapshots imported after "
          "that config landed.\n")
    for k, n in sorted(count.items(), key=lambda kv: -kv[1]):
        text, merged = _spans(ivals[k])
        note = ""
        if merged[-1][1] < last:
            note = f"  <- GONE after {date.get(merged[-1][1], merged[-1][1])}"
        elif merged[0][0] > first:
            note = f"  <- appeared {date.get(merged[0][0], merged[0][0])}"
        if len(merged) > 1:
            note += "  <- intermittent"
        print(f"  {k:26} rows={n:8}  snapshots={text}{note}")


def churn(ds, snaps):
    """Field-level change tally across every consecutive non-skipped pair."""
    ids = [s["id"] for s in snaps]
    date = {s["id"]: diff.snap_date(s) for s in snaps}
    touched, solo, combo = Counter(), Counter(), Counter()
    per_day = defaultdict(Counter)

    print("\n=== per-diff summary ===")
    for a, b in zip(ids, ids[1:]):
        d = diff.compute_diff(ds, a, b)
        for m in d["modified"]:
            fs = tuple(sorted(c["field"] for c in m["changes"]))
            combo[fs] += 1
            for f in fs:
                touched[f] += 1
                per_day[date[b]][f] += 1
            if len(fs) == 1:
                solo[fs[0]] += 1
        print(f"  {date[a]} -> {date[b]}: +{len(d['added'])} -{len(d['removed'])} "
              f"~{len(d['modified'])}", flush=True)

    print("\n=== churn tally (rows touched / rows where it was the only change) ===")
    for f, n in touched.most_common():
        print(f"  {f:26} touched={n:8}  solo={solo.get(f, 0)}")

    print("\n=== top change combos ===")
    for fs, n in combo.most_common(25):
        print(f"  {n:8}  {', '.join(fs)}")

    print("\n=== per-day field tallies ===")
    for d in sorted(per_day):
        print(f"  {d} {dict(per_day[d].most_common(12))}")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    ds = registry.load(sys.argv[1])
    snaps = diff.nonskipped(ds)
    if len(snaps) < 2:
        sys.exit(f"{ds.slug}: only {len(snaps)} non-skipped snapshot(s)")
    print(f"{ds.slug}: {len(snaps)} non-skipped snapshots, "
          f"{diff.snap_date(snaps[0])} .. {diff.snap_date(snaps[-1])}")
    print(f"ignore_fields = {ds.ignore_fields}\nkeep_fields   = {ds.keep_fields}\n")
    inventory(ds, snaps)
    churn(ds, snaps)


if __name__ == "__main__":
    main()
