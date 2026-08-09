"""Migration: re-clean stored props and recompute payload_hash in place.

Run after any change to the *global* prop rules in normalize._clean_props.
Without it, the change re-hashes every affected row on the next import, opening a
redundant SCD-2 range for each and reporting every one as modified. Run so far:

  2026-08-08  globalid_1 -> _VOLATILE_KEYS; whitespace-only values dropped.
              884,765 rows.
  2026-08-09  numbered objectid/fid spellings matched by pattern; string values
              stripped rather than only dropped when entirely whitespace.

Every row is rewritten, not just the active ones: report.generate_all rebuilds
each historical diff from the stored rows, so a partial backfill would invent a
change at the boundary between migrated and unmigrated snapshots.

Scope, and the asymmetry in it. keep_fields ARE re-applied by default, because they
define the hash basis and the stored hash has to match what the next import will
compute. That is not a nicety -- a keep_fields entry added since the last run leaves
every active row hashed on the old basis, and the next import re-hashes the whole
city and opens a fresh SCD-2 range for every row in it (measured 2026-08-09:
kitchener 132,057 active rows, renfrew 27,486, burlington 10,188, all at 100%).

ignore_fields are NOT re-applied by default: props holds only what survived them at
import time, so re-applying today's list rewrites history, and the values leave the
stores for good -- recoverable only by re-importing the vault's snapshots. Pass
--reapply-ignore to do it anyway, which is the fix for the same problem on the
ignore side. Same failure, no default remedy: an ignore_fields entry added since the
row was written still sits in props, and the next import drops it and re-hashes the
city. Used 2026-08-09 on the five cities the 08-08 city-tune passes had left in that
state (282,583 active rows, 100% of each: kitchener, burlington, renfrew, hastings,
quinte-west). Prefer it over letting the churn land, but run it per city and only
when you mean to rewrite that city's history.

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


def _reclean(props, drop=frozenset(), zero_keep=frozenset()):
    """Re-apply the importer's prop rules to an already-stored props dict.

    Empty args are what make this the global delta and nothing more: the per-city
    config was already applied when the row was written, and props holds only what
    survived it. Calling the importer rather than restating its rules means this
    cannot drift from what the next import would produce.

    Under --reapply-ignore the caller passes the same two arguments
    normalize.canonical does, so the result is what a fresh import would store.
    """
    return normalize._clean_props(props, drop, zero_keep)


def migrate(ds, dry_run=False, reapply_ignore=False):
    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row
    keep = {k.lower() for k in ds.keep_fields}

    # mirror normalize.canonical's two arguments exactly (src/normalize.py:158),
    # or pass nothing and stay on the global rules
    drop = zero_keep = frozenset()
    if reapply_ignore:
        drop = ({k.lower() for k in ds.ignore_fields}
                | normalize.EDIT_METADATA_FIELDS) - keep
        zero_keep = keep

    updates = []
    for r in conn.execute(
            "SELECT identity_key, min_snapshot_id, number, street, unit, full, "
            "longitude, latitude, props, payload_hash FROM addresses"):
        old_props = r["props"] or "{}"
        cleaned = _reclean(json.loads(old_props), drop, zero_keep)
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
    ap.add_argument("--reapply-ignore", action="store_true",
                    help="also strip today's ignore_fields from historical rows "
                         "(rewrites history; the values leave the store)")
    args = ap.parse_args()

    datasets = [registry.load(args.city)] if args.city else registry.load_all()
    total = 0
    for ds in datasets:
        if not os.path.exists(ds.db_path):
            continue
        n, rehashed = migrate(ds, args.dry_run, args.reapply_ignore)
        total += n
        if n:
            note = "" if args.dry_run else f", content_hash {'rewritten' if rehashed else 'skipped'}"
            print(f"  {ds.slug:<22} {n:>9,} rows{note}")
    verb = "would rewrite" if args.dry_run else "rewrote"
    print(f"\n{verb} {total:,} rows")


if __name__ == "__main__":
    main()
