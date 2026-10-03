"""Migration: derive canonical street from full minus the number, across all history.

For turning on `street_from_full = true` in datasets/<slug>.toml (a source with no
street column). Without it the next import computes a street for every row while the
store still holds NULL, diffing the whole city as "modified" (street is a
payload_hash column) - a phantom mass event. Rewriting the whole history first means
store and import already agree: no event, no flag entry, and new-street debuts
(diff.new_streets_by_snapshot) read as if the street had always been there.

Sibling of tools/remap_canonical_from_prop.py, whose --prop contract does not fit:
street here comes from two stored canonical columns (number, full) through
normalize.street_from_full, the very function the importer calls, so the two cannot
disagree. Every row is rewritten, not just active ones (report.generate_all rebuilds
each historical diff from the stored rows). The latest non-skipped snapshot's
content_hash is recomputed so an unchanged re-pull still registers as a skip.

Preconditions, checked here:
  - The TOML already says street_from_full = true (edit it first, same commit as
    the code), so the importer and this tool are reading the same config.
  - street is not part of the identity basis (key_field city, or synth_fields
    without it): only street and payload_hash move, no row re-keys.

A consistent backup is taken first (sqlite3 backup API - the store is WAL mode) to
data/<slug>/<slug>.pre-street-from-full-<date>.db unless --no-backup.

Run so far:
  2026-10-03  lennox-addington: 26,168 of 26,182 rows (all history) got a street;
              14 stay None (12 bare numbers / no number in ADDRESS, 2 no ADDRESS).
              Only street + payload_hash moved, no row re-keyed; snapshot 38's
              content_hash rewritten and re-verified against the 2026-09-25 raw
              pull (0 diffs). Backup: lennox-addington.pre-street-from-full-2026-10-03.db.
  2026-10-03  perth-county: 18,726 of 18,735 rows got a street (the trailing unit cut
              off via the new unit argument); 9 with no Full_Add stay None. No row
              re-keyed; snapshot 2's content_hash rewritten and re-verified against
              the 2026-09-08 raw pull (0 diffs). Debuts: AREND STREET and ROSE LANE
              (28 each) at snapshot 2. Backup:
              perth-county.pre-street-from-full-2026-10-03.db.

Not part of the daily run. Safe to re-run: it is idempotent.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize, registry

_HASH_COLS = ("number", "street", "unit", "full", "longitude", "latitude")


def backup(ds):
    path = os.path.join(ds.data_dir,
                        f"{ds.slug}.pre-street-from-full-{date.today().isoformat()}.db")
    if os.path.exists(path):
        sys.exit(f"backup already exists: {path} - move it aside first")
    src = sqlite3.connect(ds.db_path)
    dst = sqlite3.connect(path)
    src.backup(dst)
    dst.close()
    src.close()
    return path


def migrate(ds, dry_run=False):
    if not ds.street_from_full:
        sys.exit(f"{ds.slug}.toml does not set street_from_full = true - edit it first, "
                 "or the next import undoes this migration")
    if not ds.key_field and "street" in ds.synth_fields:
        sys.exit(f"{ds.slug}: 'street' is in the synthesized identity basis - "
                 "rewriting it needs an identity migration, refusing")

    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row
    keep = {k.lower() for k in ds.keep_fields}

    updates = []
    total = with_street = 0
    for r in conn.execute(
            "SELECT identity_key, min_snapshot_id, number, street, unit, full, "
            "longitude, latitude, props, payload_hash FROM addresses"):
        total += 1
        new_street = normalize.street_from_full(r["full"], r["number"], r["unit"])
        with_street += new_street is not None
        rec = {c: r[c] for c in _HASH_COLS}
        rec["street"] = new_street
        props = json.loads(r["props"] or "{}")
        hash_props = {k: v for k, v in props.items() if k.lower() not in keep}
        new_hash = normalize._payload_hash(rec, hash_props)
        if new_street == r["street"] and new_hash == r["payload_hash"]:
            continue
        updates.append((new_street, new_hash, r["identity_key"], r["min_snapshot_id"]))

    if not dry_run and updates:
        conn.executemany(
            "UPDATE addresses SET street = ?, payload_hash = ? "
            "WHERE identity_key = ? AND min_snapshot_id = ?", updates)

    # cf. backfill_props_hash: content_hash is only compared against the latest
    # non-skipped snapshot (db._last_snapshot), so only that one needs recomputing.
    sid = conn.execute(
        "SELECT MAX(id) FROM snapshots WHERE skipped = 0").fetchone()[0]
    rehashed = False
    if sid is not None and not dry_run and updates:
        rows = conn.execute(
            "SELECT identity_key, payload_hash FROM addresses "
            "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchall()
        ch = db._content_hash([dict(x) for x in rows])
        conn.execute("UPDATE snapshots SET content_hash = ? WHERE id = ?", (ch, sid))
        rehashed = True

    if not dry_run:
        conn.commit()
    conn.close()
    return len(updates), total, with_street, rehashed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--city", required=True, help="dataset slug")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change, write nothing")
    ap.add_argument("--no-backup", action="store_true",
                    help="skip the pre-migration backup copy")
    args = ap.parse_args()

    ds = registry.load(args.city)
    if not os.path.exists(ds.db_path):
        sys.exit(f"no store at {ds.db_path}")
    if not args.dry_run and not args.no_backup:
        print(f"backup: {backup(ds)}")

    n, total, with_street, rehashed = migrate(ds, args.dry_run)
    verb = "would rewrite" if args.dry_run else "rewrote"
    note = "" if args.dry_run or not n else \
        f", content_hash {'rewritten' if rehashed else 'skipped'}"
    print(f"{verb} {n:,} of {total:,} rows{note}; {with_street:,} have a street, "
          f"{total - with_street:,} stay None")


if __name__ == "__main__":
    main()
