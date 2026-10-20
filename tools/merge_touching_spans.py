r"""Migration: fold the span pairs the importer would have kept as one span.

A key's two spans touch when no non-skipped snapshot lies between them; with the same
payload_hash they are one unchanged address split in two. The importer never leaves
such a pair - it extends a span whenever the hash matches - but the tools that rewrite
hashes in place did (backfill_props_hash.py --reapply-ignore above all), until they
started calling db.merge_touching_spans themselves on 2026-10-20. This runs that
function over stores rewritten before then. See db.merge_touching_spans.

Nothing a report reads changes: compute_diff only counts a key as modified when the
hash differs, histories only look at presence at non-skipped snapshots, and the
active set at every non-skipped snapshot is the same before and after. Check with a
full `run.py report --all` - the pages must come out byte-identical.

A consistent backup of each store that has pairs is taken first into --backup-dir.

Run so far:
  2026-10-20  20 stores, before: guelph 53,849 keys / 270,430 pairs, chatham-kent
              56,147, huron 17,344, renfrew 4,834 / 5,591, brampton 2,742 / 4,687,
              kingston 1,091 / 1,094, kitchener 1,067, durham 957, simcoe 402 / 781,
              york 261, toronto 191 / 346, hastings 163, thunder-bay 129, barrie 7,
              cornwall 2, milton 2, bruce, hamilton, kawartha-lakes, quinte-west 1.

Not part of the daily run. Safe to re-run: it is idempotent.
"""

import argparse
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, registry


def backup(ds, backup_dir):
    os.makedirs(backup_dir, exist_ok=True)
    path = os.path.join(backup_dir, f"{ds.slug}.db")
    if os.path.exists(path):
        sys.exit(f"backup already exists: {path} - move it aside first")
    src = sqlite3.connect(ds.db_path)
    dst = sqlite3.connect(path)
    src.backup(dst)
    dst.close()
    src.close()
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--city", help="single dataset slug (default: all)")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("--backup-dir", help="directory for the pre-merge copies")
    ap.add_argument("--no-backup", action="store_true")
    args = ap.parse_args()
    if not args.dry_run and not args.no_backup and not args.backup_dir:
        sys.exit("--backup-dir is required unless --no-backup or --dry-run")

    datasets = [registry.load(args.city)] if args.city else registry.load_all()
    verb = "would merge" if args.dry_run else "merged"
    total = 0
    for ds in datasets:
        if not os.path.exists(ds.db_path):
            continue
        conn = sqlite3.connect(ds.db_path)
        keys, rows = db.merge_touching_spans(conn, dry_run=True)
        if rows and not args.dry_run:
            if not args.no_backup:
                backup(ds, args.backup_dir)
            keys, rows = db.merge_touching_spans(conn)
            conn.commit()
        conn.close()
        if rows:
            total += rows
            print(f"  {ds.slug:<22} {verb} {keys:>7,} keys, {rows:>8,} rows folded")
    print(f"\n{verb} {total:,} rows")


if __name__ == "__main__":
    main()
