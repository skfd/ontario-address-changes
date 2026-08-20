"""Migration: re-derive one canonical column from a stored prop, across all history.

For a field-map remap (datasets/<slug>.toml [fields]) that would otherwise land as a
phantom mass event: the next import would compute the canonical value from the new
source column while the store still holds the old one, diffing every affected row as
"modified" even though the source changed nothing. Rewriting the whole history to the
new standard first means store and import already agree - no event, no flag entry,
and old reports re-render as if the mapping had always been this way.

House rule (2026-08-20): prefer this full-history migration over letting the phantom
event land and reviewing it as a technical flag.

Preconditions, checked here or by you:
  - The prop must be stored for the row being rewritten (put it in keep_fields if it
    is ignored; values already stripped from props are only recoverable from backup).
  - The canonical field must NOT be part of the city's identity (a key_field city, or
    a synth basis that omits it). Rewriting a key component would need an identity
    migration too - out of scope, this tool refuses.
  - Edit the TOML [fields] mapping in the same session, or the next import undoes it.

Every row is rewritten, not just active ones: report.generate_all rebuilds each
historical diff from the stored rows, so a partial rewrite would invent a change at
the migrated/unmigrated boundary. Rows without the prop get canonical None - exactly
what the next import will compute. The latest snapshot's content_hash is recomputed
(cf. tools/backfill_props_hash.py) so an unchanged re-pull still registers as a skip.

Run so far:
  2026-08-20  lennox-addington number: Number -> ADD_LABEL (house suffix carrier).

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
_CANONICAL = ("number", "street", "unit", "full")


def migrate(ds, canonical, prop, dry_run=False):
    if not ds.key_field and canonical in ds.synth_fields:
        sys.exit(f"{ds.slug}: '{canonical}' is in the synthesized identity basis - "
                 "rewriting it needs an identity migration, refusing")

    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row
    keep = {k.lower() for k in ds.keep_fields}

    updates = []
    missing_prop = 0
    for r in conn.execute(
            "SELECT identity_key, min_snapshot_id, number, street, unit, full, "
            "longitude, latitude, props, payload_hash FROM addresses"):
        props = json.loads(r["props"] or "{}")
        # what normalize.canonical computes for the new mapping (src/normalize.py:153)
        new_val = normalize._clean(props.get(prop))
        if prop not in props:
            missing_prop += 1
        if new_val == r[canonical]:
            continue
        rec = {c: r[c] for c in _HASH_COLS}
        rec[canonical] = new_val
        hash_props = {k: v for k, v in props.items() if k.lower() not in keep}
        new_hash = normalize._payload_hash(rec, hash_props)
        updates.append((new_val, new_hash, r["identity_key"], r["min_snapshot_id"]))

    if not dry_run and updates:
        conn.executemany(
            f"UPDATE addresses SET {canonical} = ?, payload_hash = ? "
            "WHERE identity_key = ? AND min_snapshot_id = ?", updates)

    # cf. backfill_props_hash: content_hash is only compared against the latest
    # non-skipped snapshot, so only that one needs recomputing.
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
    return len(updates), missing_prop, rehashed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--city", required=True, help="dataset slug")
    ap.add_argument("--canonical", required=True, choices=_CANONICAL,
                    help="canonical column to rewrite")
    ap.add_argument("--prop", required=True,
                    help="stored prop to derive it from (the new [fields] source)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change, write nothing")
    args = ap.parse_args()

    ds = registry.load(args.city)
    if not os.path.exists(ds.db_path):
        sys.exit(f"no store at {ds.db_path}")
    mapped = ds.fields.get(args.canonical)
    if mapped != args.prop:
        print(f"note: {args.city}.toml currently maps {args.canonical} = "
              f"{mapped!r}, not {args.prop!r} - edit the TOML in this session "
              "or the next import undoes this migration")

    n, missing, rehashed = migrate(ds, args.canonical, args.prop, args.dry_run)
    verb = "would rewrite" if args.dry_run else "rewrote"
    note = "" if args.dry_run or not n else \
        f", content_hash {'rewritten' if rehashed else 'skipped'}"
    print(f"{verb} {n:,} rows ({args.canonical} <- {args.prop}){note}; "
          f"{missing:,} rows lack the prop (canonical becomes None if set)")


if __name__ == "__main__":
    main()
