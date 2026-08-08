"""One-shot repair: drop corrupt snapshots and rebuild their stores' SCD-2 history.

Three snapshots were recorded from degraded upstream responses and are not
observations of the cities they claim to describe:

  kitchener-2026-07-28  102,000 of 131,912 features (exactly 51 pages of 2000)
  huron-2026-07-28       20,000 of  38,300 features (exactly 10 pages of 2000)
  muskoka-2026-06-28     every attribute null except PropertyNum

The first two are truncated pulls: addressvault's ArcGIS paging loop ends on a
mid-stream empty page, so a transient blank page reads as end-of-layer. The
missing rows were recorded as removed and re-added days later, splitting ~48k
identity keys across redundant SCD-2 ranges. Muskoka's is an attribute-stripped
pull; because muskoka synthesizes identity, every key in the city changed.

The true state of those dates is unrecoverable (the services serve current data
only, and the vault's history starts after two of them), so the snapshots are
deleted rather than re-fetched. SCD-2 already means "the last observation holds
until the next one", which is the correct reading of a day we failed to observe.

Muskoka additionally gets a new identity basis. Its coordinates jitter by up to
1.36 m between republishes, which crosses the 5 dp (~1.1 m) rounding in
normalize._identity and mints a new key for ~43% of the city on any republish --
so the store carried 157,666 keys for a 66k-row city. datasets/muskoka.toml now
synthesizes from address + PropertyNum with use_geometry = false; this script
rewrites the existing rows onto that basis. It is muskoka-only: every other city
has a distinct-key-to-active-row ratio of 1.01 or less.

Rebuilds `addresses` from the active set of each surviving non-skipped snapshot,
so range boundaries land exactly where a clean import would have put them.

Not part of the daily run. Safe to re-run: once a snapshot is gone it is a no-op.
"""

import argparse
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize, registry

# slug -> filename of the snapshot to drop
DROP = {
    "kitchener": "kitchener-2026-07-28.geojson",
    "huron": "huron-2026-07-28.geojson",
    "muskoka": "muskoka-2026-06-28.geojson",
}
# slugs whose identity_key is recomputed from the current config
REKEY = {"muskoka"}

_ROW_COLS = ("identity_key", "number", "street", "unit", "full",
             "longitude", "latitude", "props", "payload_hash")


def _active(conn, sid):
    rows = conn.execute(
        f"SELECT {', '.join(_ROW_COLS)} FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid))
    return [dict(r) for r in rows]


def _rekey(ds, row):
    """The identity this row would get from today's config."""
    props = json.loads(row["props"] or "{}")
    return normalize._identity(ds, row, props, row["longitude"], row["latitude"])


def repair(ds, dry_run=False):
    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row

    snaps = [dict(r) for r in conn.execute("SELECT * FROM snapshots ORDER BY id")]
    bad = next((s for s in snaps if s["filename"] == DROP[ds.slug]), None)
    if bad is None:
        conn.close()
        return None

    order = [s["id"] for s in snaps if not s["skipped"] and s["id"] != bad["id"]]

    # active set of each surviving snapshot, keyed by the identity it will carry
    collisions = 0
    by_sid = {}
    for sid in order:
        keyed = {}
        for row in _active(conn, sid):
            key = _rekey(ds, row) if ds.slug in REKEY else row["identity_key"]
            prev = keyed.get(key)
            # Two source rows collapsing onto one key: import keeps whichever it
            # saw first (db._records). Row order is not preserved here, so pick
            # deterministically instead.
            if prev is None or row["identity_key"] < prev["identity_key"]:
                if prev is not None:
                    collisions += 1
                keyed[key] = row
            else:
                collisions += 1
        by_sid[sid] = keyed

    # SCD-2 rebuild: a range runs while the key is present with the same
    # payload_hash, and carries the values from the snapshot that opened it.
    out = []
    for key in {k for keyed in by_sid.values() for k in keyed}:
        open_at = last = None
        row = None
        for sid in order:
            r = by_sid[sid].get(key)
            if r is None:
                if open_at is not None:
                    out.append((open_at, last, key, row))
                    open_at = None
                continue
            if open_at is not None and row["payload_hash"] == r["payload_hash"]:
                last = sid
                continue
            if open_at is not None:
                out.append((open_at, last, key, row))
            open_at, last, row = sid, sid, r
        if open_at is not None:
            out.append((open_at, last, key, row))

    before = conn.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]
    keys_before = conn.execute(
        "SELECT COUNT(DISTINCT identity_key) FROM addresses").fetchone()[0]
    keys_after = len({k for _, _, k, _ in out})

    if not dry_run:
        cols = ", ".join(_ROW_COLS[1:])          # identity_key supplied separately
        conn.execute("DELETE FROM addresses")
        conn.executemany(
            f"INSERT INTO addresses (min_snapshot_id, max_snapshot_id, identity_key, {cols}) "
            f"VALUES ({', '.join('?' * (3 + len(_ROW_COLS) - 1))})",
            [(mn, mx, key, *(row[c] for c in _ROW_COLS[1:])) for mn, mx, key, row in out])
        conn.execute("DELETE FROM snapshots WHERE id = ?", (bad["id"],))

        # content_hash gates the "no changes -> record a skip" fast path
        # (src/db.py:125). Recompute it for each surviving non-skipped snapshot;
        # a skipped snapshot's hash is by definition the preceding one's.
        carry = None
        for s in snaps:
            if s["id"] == bad["id"]:
                continue
            if s["skipped"]:
                if carry is not None:
                    conn.execute("UPDATE snapshots SET content_hash = ? WHERE id = ?",
                                 (carry, s["id"]))
                continue
            carry = db._content_hash(
                [{"identity_key": k, "payload_hash": r["payload_hash"]}
                 for k, r in by_sid[s["id"]].items()])
            conn.execute("UPDATE snapshots SET content_hash = ? WHERE id = ?",
                         (carry, s["id"]))
        conn.commit()

    conn.close()
    return {"snapshot": bad["filename"], "snapshot_id": bad["id"],
            "rows_before": before, "rows_after": len(out),
            "keys_before": keys_before, "keys_after": keys_after,
            "collisions": collisions, "rekeyed": ds.slug in REKEY}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change, write nothing")
    ap.add_argument("--city", help="single dataset slug (default: all three)")
    args = ap.parse_args()

    slugs = [args.city] if args.city else sorted(DROP)
    for slug in slugs:
        ds = registry.load(slug)
        res = repair(ds, args.dry_run)
        if res is None:
            print(f"  {slug:<12} already repaired ({DROP[slug]} not present)")
            continue
        print(f"  {slug:<12} drop snapshot {res['snapshot_id']} ({res['snapshot']})"
              f"{'  + rekey' if res['rekeyed'] else ''}")
        print(f"  {'':12} rows {res['rows_before']:>9,} -> {res['rows_after']:>9,}"
              f"   keys {res['keys_before']:>9,} -> {res['keys_after']:>9,}"
              f"   collisions {res['collisions']:,}")
    if args.dry_run:
        print("\ndry run - nothing written")


if __name__ == "__main__":
    main()
