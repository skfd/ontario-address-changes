"""Drop corrupt snapshots from a city's store and rebuild its SCD-2 history.

    python tools/repair_bad_snapshots.py --city muskoka \\
        --drop muskoka-2026-06-28.geojson [--rekey] [--dry-run]

Use when a snapshot that is not an observation of the city got recorded anyway --
a degraded pull small enough to slip past the import guards. Reports are rebuilt
from the store on every run, so until the store is repaired the bad day keeps
producing its fake event. See .claude/skills/data-integrity/references/repair.md
for when this is the right answer.

Rebuilds `addresses` from the active set of each surviving non-skipped snapshot,
so range boundaries land exactly where a clean import would have put them, and
recomputes each snapshot's content_hash (it gates the "no changes -> record a
skip" fast path in src/db.py).

The dropped day is not re-fetched: the services serve current data only, so the
true state of a past date is usually unrecoverable. SCD-2 already means "the last
observation holds until the next one", which is the correct reading of a day we
failed to observe.

`--rekey` additionally rewrites every identity_key from the city's *current*
config. Only for a store whose [identity] was wrong, and only together with the
TOML change -- it is the one operation here that rewrites history rather than
removing something from it.

Not part of the daily run. Safe to re-run: once a snapshot is gone it is a no-op.
Take a copy of data/<slug>/<slug>.db first; nothing here can be undone.

Originally a one-shot for the three snapshots found on 2026-08-08, all since
refused at fetch/import time rather than recorded:

  kitchener-2026-07-28  102,000 of 131,912 features (exactly 51 pages of 2000)
  huron-2026-07-28       20,000 of  38,300 features (exactly 10 pages of 2000)
  muskoka-2026-06-28     every attribute null except PropertyNum

The first two were truncated pulls, whose missing rows were recorded as removed
and re-added days later, splitting ~48k identity keys across redundant SCD-2
ranges. Muskoka's was attribute-stripped, and because muskoka synthesizes
identity, every key in the city changed. Muskoka was also the one --rekey to
date: its coordinates jitter up to 1.36 m between republishes, crossing the 5 dp
(~1.1 m) rounding in normalize._identity and minting a new key for ~43% of the
city on any republish, so the store carried 157,666 keys for a 66k-row city.
"""

import argparse
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize, registry

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


def repair(ds, drop=(), rekey=False, dry_run=False):
    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row

    snaps = [dict(r) for r in conn.execute("SELECT * FROM snapshots ORDER BY id")]
    bad_ids = {s["id"] for s in snaps if s["filename"] in drop}
    absent = sorted(set(drop) - {s["filename"] for s in snaps})
    if absent and not bad_ids:
        conn.close()
        return {"absent": absent}

    order = [s["id"] for s in snaps if not s["skipped"] and s["id"] not in bad_ids]

    # active set of each surviving snapshot, keyed by the identity it will carry
    collisions = 0
    by_sid = {}
    for sid in order:
        keyed = {}
        for row in _active(conn, sid):
            key = _rekey(ds, row) if rekey else row["identity_key"]
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
        conn.executemany("DELETE FROM snapshots WHERE id = ?",
                         [(i,) for i in sorted(bad_ids)])

        # content_hash gates the "no changes -> record a skip" fast path
        # (src/db.py:125). Recompute it for each surviving non-skipped snapshot;
        # a skipped snapshot's hash is by definition the preceding one's.
        carry = None
        for s in snaps:
            if s["id"] in bad_ids:
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
    return {"dropped": sorted(bad_ids), "absent": absent,
            "rows_before": before, "rows_after": len(out),
            "keys_before": keys_before, "keys_after": keys_after,
            "collisions": collisions, "rekeyed": rekey}


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--city", required=True, help="dataset slug")
    ap.add_argument("--drop", action="append", default=[], metavar="FILENAME",
                    help="snapshot filename to remove; repeatable")
    ap.add_argument("--rekey", action="store_true",
                    help="also recompute every identity_key from the current config")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change, write nothing")
    args = ap.parse_args()

    if not args.drop and not args.rekey:
        ap.error("nothing to do: pass --drop and/or --rekey")

    ds = registry.load(args.city)
    res = repair(ds, args.drop, args.rekey, args.dry_run)
    if res.get("absent") and not res.get("dropped"):
        print(f"  {ds.slug:<12} nothing to drop - not in this store: "
              f"{', '.join(res['absent'])}")
        return
    if res["absent"]:
        print(f"  {ds.slug:<12} not in this store, ignored: {', '.join(res['absent'])}")
    print(f"  {ds.slug:<12} drop {len(res['dropped'])} snapshot(s) "
          f"{res['dropped'] or ''}{'  + rekey' if res['rekeyed'] else ''}")
    print(f"  {'':12} rows {res['rows_before']:>9,} -> {res['rows_after']:>9,}"
          f"   keys {res['keys_before']:>9,} -> {res['keys_after']:>9,}"
          f"   collisions {res['collisions']:,}")
    if args.dry_run:
        print("\ndry run - nothing written")
    else:
        print(f"\n  regenerate the reports:  python run.py report --city {ds.slug}")


if __name__ == "__main__":
    main()
