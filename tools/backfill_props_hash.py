"""One-shot migration: re-clean stored props and recompute payload_hash in place.

Run once, after the two normalize.py fixes (globalid_1 -> _VOLATILE_KEYS, and
_clean_props dropping whitespace-only values). Without it those fixes would
re-hash ~670k rows across 28 cities on the next import, opening a redundant SCD-2
range for each and reporting every one as modified.

Every row is rewritten, not just the active ones: report.generate_all rebuilds
each historical diff from the stored rows, so a partial backfill would invent a
change at the boundary between migrated and unmigrated snapshots.

Only the delta from the two fixes is applied. ignore_fields/keep_fields are NOT
re-applied -- those were resolved at import time against the config as it stood
then, and re-applying today's config would rewrite history beyond these fixes.

Not part of the daily run. Safe to re-run: it is idempotent.
"""

import argparse
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize, registry

_HASH_COLS = ("number", "street", "unit", "full", "longitude", "latitude")


def _reclean(props):
    """Apply exactly the two fixes to an already-stored props dict."""
    out = {}
    for k, v in props.items():
        if k.lower() == "globalid_1":
            continue
        if isinstance(v, str) and not v.strip():
            continue
        out[k] = v
    return out


def migrate(ds, dry_run=False):
    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row
    keep = {k.lower() for k in ds.keep_fields}

    updates = []
    for r in conn.execute(
            "SELECT identity_key, min_snapshot_id, number, street, unit, full, "
            "longitude, latitude, props, payload_hash FROM addresses"):
        old_props = r["props"] or "{}"
        cleaned = _reclean(json.loads(old_props))
        # must match normalize.canonical's dump exactly (src/normalize.py:141)
        new_props = json.dumps(cleaned, sort_keys=True, ensure_ascii=False, default=str)
        hash_props = {k: v for k, v in cleaned.items() if k.lower() not in keep}
        rec = {c: r[c] for c in _HASH_COLS}
        new_hash = normalize._payload_hash(rec, hash_props)
        if new_props != old_props or new_hash != r["payload_hash"]:
            updates.append((new_props, new_hash, r["identity_key"], r["min_snapshot_id"]))

    if not dry_run and updates:
        conn.executemany(
            "UPDATE addresses SET props = ?, payload_hash = ? "
            "WHERE identity_key = ? AND min_snapshot_id = ?", updates)

    # content_hash is only ever compared against the latest non-skipped snapshot
    # (src/db.py:125), so only that one needs recomputing; leaving the rest is
    # deliberate -- recomputing every snapshot means a full scan per snapshot.
    sid = conn.execute(
        "SELECT MAX(id) FROM snapshots WHERE skipped = 0").fetchone()[0]
    rehashed = False
    if sid is not None and not dry_run:
        rows = conn.execute(
            "SELECT identity_key, payload_hash FROM addresses "
            "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchall()
        ch = db._content_hash([dict(x) for x in rows])
        conn.execute("UPDATE snapshots SET content_hash = ? WHERE id = ?", (ch, sid))
        rehashed = True

    if not dry_run:
        conn.commit()
    conn.close()
    return len(updates), rehashed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change, write nothing")
    ap.add_argument("--city", help="single dataset slug (default: all)")
    args = ap.parse_args()

    datasets = [registry.load(args.city)] if args.city else registry.load_all()
    total = 0
    for ds in datasets:
        if not os.path.exists(ds.db_path):
            continue
        n, rehashed = migrate(ds, args.dry_run)
        total += n
        if n:
            note = "" if args.dry_run else f", content_hash {'rewritten' if rehashed else 'skipped'}"
            print(f"  {ds.slug:<22} {n:>9,} rows{note}")
    verb = "would rewrite" if args.dry_run else "rewrote"
    print(f"\n{verb} {total:,} rows")


if __name__ == "__main__":
    main()
