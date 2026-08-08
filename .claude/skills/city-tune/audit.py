"""Audit one city's DB for every datasets/<slug>.toml decision, from its full history.

    python .claude/skills/city-tune/audit.py <slug> [--tags] [--identity]
                                                    [--fields] [--classes]

With no flags, runs everything. Sections:

  tags      Every prop key ever stored, with the snapshot range it covers (catches a
            field the source dropped, added, or carried intermittently), plus a churn
            tally: rows each field touched vs rows where it was the ONLY change.
  identity  Whether key_field / the synthesized key is actually stable and unique.
  fields    Coverage of the mapped canonical fields, and candidates for unmapped ones.
  classes   Low-cardinality props that could drive a [classes] entry.

Read-only. `--tags` runs one compute_diff per consecutive snapshot pair, which
dominates runtime (seconds for a mid-size city, minutes for toronto); the other
sections are single passes over the latest snapshot.
"""

import json
import os
import sys
from collections import Counter, defaultdict
from itertools import groupby

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

from src import db, diff, registry

VALUE_CAP = 30          # distinct values kept per prop before calling it high-cardinality
CLASS_MAX = 25          # at most this many distinct values to suggest as a class


# ---- helpers ----

def _ordinals(snaps):
    """{snapshot_id: position} over non-skipped snapshots.

    Skipped snapshots never appear in addresses (import_snapshot leaves the table
    alone), so a row that persists across one keeps a single unbroken range. Gaps
    must therefore be measured in this ordinal space, not in raw snapshot ids.
    """
    return {s["id"]: i for i, s in enumerate(snaps)}


def _merge(intervals, pos):
    """Merge (min_id, max_id) pairs into contiguous ordinal spans."""
    spans = []
    for lo, hi in sorted((pos[a], pos[b]) for a, b in intervals):
        if spans and lo <= spans[-1][1] + 1:
            spans[-1][1] = max(spans[-1][1], hi)
        else:
            spans.append([lo, hi])
    return spans


_VALUE_CACHE = {}


def _prop_values(ds, sid):
    """One pass over the latest snapshot: {key: (fill_count, values|None)}.

    `values` is None once a key passes VALUE_CAP distinct values (high cardinality).
    Cached: the fields and classes sections both want it.
    """
    if (ds.slug, sid) in _VALUE_CACHE:
        return _VALUE_CACHE[ds.slug, sid]
    conn = db.init_db(ds)
    rows = conn.execute(
        "SELECT je.key AS k, je.value AS v FROM addresses, json_each(addresses.props) AS je "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid))
    fill, vals = Counter(), {}
    for k, v in rows:
        fill[k] += 1
        seen = vals.get(k, set())
        if seen is not None and len(seen) <= VALUE_CAP:
            seen.add(str(v))
            vals[k] = None if len(seen) > VALUE_CAP else seen
    conn.close()
    _VALUE_CACHE[ds.slug, sid] = {k: (fill[k], vals.get(k)) for k in fill}
    return _VALUE_CACHE[ds.slug, sid]


# ---- sections ----

def tags(ds, snaps):
    pos = _ordinals(snaps)
    date = [diff.snap_date(s) for s in snaps]
    conn = db.init_db(ds)
    ivals, count = defaultdict(list), Counter()
    for mn, mx, props in conn.execute(
            "SELECT min_snapshot_id, max_snapshot_id, props FROM addresses"):
        for k in json.loads(props):
            count[k] += 1
            ivals[k].append((mn, mx))
    conn.close()

    print(f"=== tags: {len(count)} keys ever stored ===")
    print("A key already in ignore_fields is absent from every snapshot imported after")
    print("that config landed, and is filtered out of the churn tally below.\n")
    last = len(snaps) - 1
    for k, n in sorted(count.items(), key=lambda kv: -kv[1]):
        spans = _merge(ivals[k], pos)
        text = ", ".join(date[a] if a == b else f"{date[a]}..{date[b]}" for a, b in spans)
        note = ""
        if spans[-1][1] < last:
            note += "  <- GONE from the source"
        if spans[0][0] > 0:
            note += "  <- appeared mid-history"
        if len(spans) > 1:
            note += "  <- intermittent"
        print(f"  {k:26} rows={n:8}  {text}{note}")

    ids = [s["id"] for s in snaps]
    date_of = {s["id"]: diff.snap_date(s) for s in snaps}
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
                per_day[date_of[b]][f] += 1
            if len(fs) == 1:
                solo[fs[0]] += 1
        print(f"  {date_of[a]} -> {date_of[b]}: "
              f"+{len(d['added'])} -{len(d['removed'])} ~{len(d['modified'])}", flush=True)

    print("\n=== churn (rows touched / rows where it was the only change) ===")
    for f, n in touched.most_common():
        print(f"  {f:26} touched={n:8}  solo={solo.get(f, 0)}")
    print("\n=== top change combos (co-movement reveals derived echoes) ===")
    for fs, n in combo.most_common(25):
        print(f"  {n:8}  {', '.join(fs)}")
    print("\n=== per-day field tallies ===")
    for d in sorted(per_day):
        print(f"  {d} {dict(per_day[d].most_common(12))}")
    return solo


def identity(ds, snaps):
    pos = _ordinals(snaps)
    sid = snaps[-1]["id"]
    conn = db.init_db(ds)
    total, distinct, synth = conn.execute(
        "SELECT COUNT(*), COUNT(DISTINCT identity_key), "
        "SUM(identity_key LIKE 'syn:%') FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchone()

    # Stream every key's ranges in PK order to find keys that vanished and came back:
    # a flapping key reports as retired-then-new instead of modified.
    rows = conn.execute("SELECT identity_key, min_snapshot_id, max_snapshot_id FROM addresses "
                        "ORDER BY identity_key, min_snapshot_id")
    flapped = versions = keys = 0
    for _, grp in groupby(rows, key=lambda r: r[0]):
        ivals = [(a, b) for _, a, b in grp]
        keys += 1
        versions += len(ivals)
        if len(_merge(ivals, pos)) > 1:
            flapped += 1
    conn.close()

    print("\n=== identity ===")
    print(f"  key_field    = {ds.key_field or '(synthesized)'}")
    print(f"  synth_fields = {ds.synth_fields}  synth_props = {ds.synth_props}  "
          f"use_geometry = {ds.use_geometry}")
    print(f"  latest snapshot: {total:,} rows, {distinct:,} distinct keys "
          f"({total - distinct:,} collisions), {synth or 0:,} synthesized")
    print(f"  whole history:   {keys:,} keys, {versions:,} versions "
          f"({versions / keys:.2f} per key)")
    print(f"  flapped (absent then present again): {flapped:,} "
          f"({flapped / keys:.2%} of keys)")
    print("  A high flap rate or a versions-per-key far above the number of real edits")
    print("  means the key is not stable - see references/identity.md.")


def field_map(ds, snaps):
    sid = snaps[-1]["id"]
    conn = db.init_db(ds)
    total = conn.execute("SELECT COUNT(*) FROM addresses WHERE min_snapshot_id <= ? "
                         "AND max_snapshot_id >= ?", (sid, sid)).fetchone()[0]
    filled = conn.execute(
        "SELECT COUNT(number), COUNT(street), COUNT(unit), COUNT(full) FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchone()
    conn.close()

    print("\n=== field map (latest snapshot) ===")
    unmapped = []
    for name, n in zip(("number", "street", "unit", "full"), filled):
        src = ds.fields.get(name)
        if src:
            print(f"  {name:7} <- {src:22} {n:8,} / {total:,} filled ({n / total:.0%})")
        else:
            unmapped.append(name)
            print(f"  {name:7} <- (unmapped)")
    if not unmapped:
        return
    print(f"\n  candidates for {', '.join(unmapped)} - every prop with its fill rate:")
    for k, (n, vals) in sorted(_prop_values(ds, sid).items(), key=lambda kv: -kv[1][0]):
        sample = "high cardinality" if vals is None else ", ".join(sorted(vals)[:3])
        print(f"    {k:26} {n:8,} ({n / total:.0%})  {sample[:60]}")


def classes(ds, snaps, solo=None):
    sid = snaps[-1]["id"]
    conn = db.init_db(ds)
    total = conn.execute("SELECT COUNT(*) FROM addresses WHERE min_snapshot_id <= ? "
                         "AND max_snapshot_id >= ?", (sid, sid)).fetchone()[0]
    conn.close()
    classed = {f: cls for cls, srcs in ds.classes.items() for f in srcs}

    print("\n=== class candidates (low-cardinality props) ===")
    print("  A [classes] entry only fires when the row's ENTIRE changed set fits it,")
    print("  so pair this with the churn tally: a field that never changes alone is")
    print("  an echo to ignore, not a class.\n")
    for k, (n, vals) in sorted(_prop_values(ds, sid).items(), key=lambda kv: -kv[1][0]):
        if vals is None or len(vals) > CLASS_MAX:
            continue
        mark = f"  [in classes.{classed[k]}]" if k in classed else ""
        churn = f"  solo changes={solo[k]}" if solo and k in solo else ""
        print(f"  {k:26} {len(vals):3} values, {n:,} rows ({n / total:.1%}){mark}{churn}")
        print(f"    {', '.join(sorted(vals)[:12])}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a[2:] for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 1 or flags - {"tags", "identity", "fields", "classes"}:
        sys.exit(__doc__)
    if not flags:
        flags = {"tags", "identity", "fields", "classes"}

    ds = registry.load(args[0])
    snaps = diff.nonskipped(ds)
    if len(snaps) < 2:
        sys.exit(f"{ds.slug}: only {len(snaps)} non-skipped snapshot(s)")
    print(f"{ds.slug}: {len(snaps)} non-skipped snapshots, "
          f"{diff.snap_date(snaps[0])} .. {diff.snap_date(snaps[-1])}")
    print(f"ignore_fields = {ds.ignore_fields}")
    print(f"keep_fields   = {ds.keep_fields}")
    print(f"classes       = {ds.classes}\n")

    solo = tags(ds, snaps) if "tags" in flags else None
    if "identity" in flags:
        identity(ds, snaps)
    if "fields" in flags:
        field_map(ds, snaps)
    if "classes" in flags:
        classes(ds, snaps, solo)


if __name__ == "__main__":
    main()
