r"""Migration: re-derive the canonical columns, identity and hash of every stored row
under the current normalize rules, across all history.

For a change to how normalize.canonical computes the canonical columns that would
otherwise land as a phantom mass event on the next import: a new null literal in
_CANONICAL_NULL_LITERALS, or a derivation switched on in the TOML
(number_unit_from_full, street_from_full). Rewriting the whole history first means
store and import already agree - no event, no flag entry, and old reports re-render
as if the rule had always held.

Unlike its siblings (remap_canonical_from_prop.py, derive_street_from_full.py) this
one may move a column in the synthesized identity basis, so it re-keys rows. That is
the heavier surgery, and the tool proves each step before trusting it:

  1. Faithful derivation: a row whose canonical columns change has its stored
     identity_key recomputed from its stored columns and props with
     normalize._identity, and it must match exactly, or the city is refused (a
     synth_props or key_field prop the store cleaned away would make new keys
     unreliable). Rows that do not change keep their key and are only counted:
     newmarket keys on GLOBALID, which is_volatile strips from stored props, so
     none of its keys recompute - and nothing there moves.
  2. One chain, one key: every version of a chain must map to the same new key.
  3. No collision: a new key must not already belong to another chain anywhere in
     history. Two real addresses merging is refused, never stitched.
  4. Versions the rewrite makes equal, on spans that touch, are folded into one
     span by db.merge_touching_spans, as the importer would have kept them.

The values come from the stored canonical columns, not raw features: a stored mapped
column is _clean(raw) under the old rules, and _clean is idempotent, so applying the
current _clean to it gives what the importer computes now. Derived columns are then
recomputed from those, in the importer's order.

The latest non-skipped snapshot's content_hash is recomputed so an unchanged re-pull
still registers as a skip. --verify re-normalizes the vault's latest pull with the
current code and compares it with the stored active set: zero differences and an
equal content_hash mean the next import is a no-op.

A consistent backup is taken first (sqlite3 backup API - the store is WAL mode) into
--backup-dir unless --no-backup.

Run so far:
  2026-10-20  "None" / "<Null>" dropped from the canonical columns: windsor 696 rows
              re-keyed, norfolk 12 re-keyed, durham 5, leeds-grenville 2.
              waterloo number_unit_from_full: 55,845 rows, none re-keyed.
              All five verified against the latest vault pull (0/0/0, content_hash
              equal). Backups: C:\Users\kk\ontario-db-backup-2026-10-20-recanonicalize\

Not part of the daily run. Safe to re-run: it is idempotent.
"""

import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize, registry

_CANONICAL = ("number", "street", "unit", "full")


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


def derive(ds, row):
    """The canonical columns the importer would compute today for a stored row."""
    rec = {c: normalize._clean(row[c]) for c in _CANONICAL}
    if ds.number_unit_from_full:
        rec["number"], rec["unit"] = normalize.number_unit_from_full(rec["full"], rec["street"])
    if ds.street_from_full:
        rec["street"] = normalize.street_from_full(rec["full"], rec["number"], rec["unit"])
    return rec


def plan(ds, conn):
    """Return (updates, stats) or exit with the reason the city is refused."""
    keep = {k.lower() for k in ds.keep_fields}
    rows = conn.execute(
        "SELECT identity_key, min_snapshot_id, max_snapshot_id, number, street, unit, "
        "full, longitude, latitude, props, payload_hash FROM addresses").fetchall()

    unfaithful = []
    unfaithful_untouched = 0
    new_key_of = {}            # old key -> new key, per chain
    split_chains = set()
    updates = []
    for r in rows:
        props = json.loads(r["props"] or "{}")
        lon, lat = r["longitude"], r["latitude"]
        old = {c: r[c] for c in _CANONICAL}
        rec = derive(ds, r)
        if normalize._identity(ds, old, props, lon, lat) != r["identity_key"]:
            if any(rec[c] != old[c] for c in _CANONICAL):
                unfaithful.append(r["identity_key"])
                continue
            unfaithful_untouched += 1
            key = r["identity_key"]
        else:
            key = normalize._identity(ds, rec, props, lon, lat)
        if new_key_of.setdefault(r["identity_key"], key) != key:
            split_chains.add(r["identity_key"])
        rec["longitude"], rec["latitude"] = lon, lat
        hash_props = {k: v for k, v in props.items() if k.lower() not in keep}
        h = normalize._payload_hash(rec, hash_props)
        if key != r["identity_key"] or h != r["payload_hash"] or \
                any(rec[c] != r[c] for c in _CANONICAL):
            updates.append((key, rec["number"], rec["street"], rec["unit"], rec["full"],
                            h, r["identity_key"], r["min_snapshot_id"]))

    if unfaithful:
        sys.exit(f"{ds.slug}: {len(unfaithful):,} stored keys do not recompute from the "
                 f"stored row (e.g. {unfaithful[:3]}) - refusing to re-key")
    if split_chains:
        sys.exit(f"{ds.slug}: {len(split_chains):,} chains would split across new keys "
                 f"(e.g. {sorted(split_chains)[:3]}) - refusing")

    owners = defaultdict(set)
    for old, new in new_key_of.items():
        owners[new].add(old)
    collisions = {new: olds for new, olds in owners.items() if len(olds) > 1}
    if collisions:
        sample = list(collisions.items())[:3]
        sys.exit(f"{ds.slug}: {len(collisions):,} new keys would merge distinct chains "
                 f"(e.g. {sample}) - refusing")


    rekeyed = sum(1 for old, new in new_key_of.items() if old != new)
    return updates, {"rows": len(rows), "chains_rekeyed": rekeyed,
                     "unfaithful_untouched": unfaithful_untouched}


def apply(conn, updates):
    # two passes: a re-key could otherwise collide on the primary key with a row
    # later in the same batch (refused above for distinct chains, but a chain's own
    # versions move together)
    conn.executemany(
        "UPDATE addresses SET identity_key = '~mig~' || ?, number = ?, street = ?, "
        "unit = ?, full = ?, payload_hash = ? "
        "WHERE identity_key = ? AND min_snapshot_id = ?", updates)
    conn.execute("UPDATE addresses SET identity_key = substr(identity_key, 6) "
                 "WHERE identity_key LIKE '~mig~%'")
    db.merge_touching_spans(conn)
    sid = conn.execute("SELECT MAX(id) FROM snapshots WHERE skipped = 0").fetchone()[0]
    if sid is not None:
        rows = conn.execute(
            "SELECT identity_key, payload_hash FROM addresses "
            "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchall()
        conn.execute("UPDATE snapshots SET content_hash = ? WHERE id = ?",
                     (db._content_hash([dict(x) for x in rows]), sid))


def verify(ds):
    """Re-normalize the vault's latest pull; compare with the stored active set."""
    from addressvault import Archived, Vault
    v = Vault(link_wait=False)
    try:
        path = v.path(ds.slug, "latest")
    except Archived:
        v.thaw(ds.slug, v.snapshot(ds.slug, "latest").date, wait=True)
        path = v.path(ds.slug, "latest")
    from src.fetch import load_features
    pulled = {r["identity_key"]: r["payload_hash"]
              for r in db._records(ds, load_features(path))}
    conn = sqlite3.connect(f"file:{ds.db_path}?mode=ro", uri=True)
    sid, ch = conn.execute("SELECT id, content_hash FROM snapshots WHERE skipped = 0 "
                           "ORDER BY id DESC LIMIT 1").fetchone()
    stored = dict(conn.execute(
        "SELECT identity_key, payload_hash FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchall())
    conn.close()
    added = pulled.keys() - stored.keys()
    removed = stored.keys() - pulled.keys()
    modified = [k for k in pulled.keys() & stored.keys() if pulled[k] != stored[k]]
    pulled_ch = db._content_hash([{"identity_key": k, "payload_hash": h}
                                  for k, h in pulled.items()])
    print(f"verify {ds.slug} against {os.path.basename(path)}: "
          f"{len(added)} added, {len(removed)} removed, {len(modified)} modified; "
          f"content_hash {'equal' if pulled_ch == ch else 'DIFFERS'}")
    return not (added or removed or modified) and pulled_ch == ch


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--city", required=True, help="dataset slug")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("--verify", action="store_true",
                    help="after (or instead of, with --dry-run) the rewrite, compare "
                         "the store with the vault's latest pull")
    ap.add_argument("--backup-dir", help="directory for the pre-migration copy")
    ap.add_argument("--no-backup", action="store_true")
    args = ap.parse_args()

    ds = registry.load(args.city)
    if not os.path.exists(ds.db_path):
        sys.exit(f"no store at {ds.db_path}")

    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row
    updates, stats = plan(ds, conn)
    verb = "would rewrite" if args.dry_run else "rewrote"
    if updates and not args.dry_run:
        if not args.no_backup:
            if not args.backup_dir:
                sys.exit("--backup-dir is required unless --no-backup")
            print(f"backup: {backup(ds, args.backup_dir)}")
        apply(conn, updates)
        conn.commit()
    conn.close()
    print(f"{ds.slug}: {verb} {len(updates):,} of {stats['rows']:,} rows, "
          f"{stats['chains_rekeyed']:,} chains re-keyed"
          + (f"; {stats['unfaithful_untouched']:,} unchanged rows whose key does not "
             "recompute, left alone" if stats["unfaithful_untouched"] else ""))
    if args.verify and not verify(ds):
        sys.exit(1)


if __name__ == "__main__":
    main()
