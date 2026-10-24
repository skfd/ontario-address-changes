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
     normalize._identity - under the identity config the store was built with,
     --old-rev's TOML when the change edits [identity] (brantford gaining unit,
     2026-10-20) - and it must match exactly, or the city is refused (a
     synth_props or key_field prop the store cleaned away would make new keys
     unreliable). Rows that do not change keep their key and are only counted:
     newmarket keys on GLOBALID, which is_volatile strips from stored props, so
     none of its keys recompute - and nothing there moves. A source-id key under an
     unchanged key_field is kept without the check, changed row or not: it comes
     from a raw prop, not the canonical columns, so no derivation can move it
     (leamington unit_from_full on GlobalID, 2026-10-23).
  2. A chain may split: versions whose identity-basis columns differ under the new
     rule get different keys (hastings "11 WANNAMAKER LN" -> "11A ..." while
     House_No stayed 11: a modification under the old rule, a retire + add under
     the new one, as the importer would have recorded it). Splits are counted and
     printed, never refused, since that is the rule taking effect.
  3. No collision: chains that land on one new key must never be active at the same
     snapshot - that would be two real addresses folding into one, refused, never
     stitched. Chains that land on one key at different times are joined, as the
     importer would have recorded a re-appearance (thunder-bay "660 VICTORIA AVE E":
     no ADDRESS_NUMBER on 06-11, back with one from 07-24 - one address under the new
     rule). Joins are counted and printed.
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
  2026-10-20  suffix fixes: thunder-bay number_from_full (359 rows, 356 chains re-keyed,
              1 split, 1 join); brantford unit_from_number + unit in the synth basis
              (--old-rev HEAD, all 39,510 rows re-keyed); hastings number_from_full
              (2,811 rows, 16 splits) - then rebuilt by rebuild_from_pulls.py, since
              its verify showed 417 rows the old key had collapsed.
              All five verified against the latest vault pull (0/0/0, content_hash
              equal). Backups: C:\Users\kk\ontario-db-backup-2026-10-20-recanonicalize\
  2026-10-23  prince-edward-county key_field "" -> "NGUID" (--old-rev HEAD): 27,436
              rows, 27,430 chains re-keyed, 11 joins (real edits the synth key had
              split). Verify showed 182 added only - suffix siblings - so rebuilt.
              Backup: C:\Users\kk\ontario-db-backup-2026-10-23-pec-nguid\
  2026-10-23  leamington unit_from_full: 488 of 11,423 rows, none re-keyed (GlobalID).
              Verify 0/0/0. Backup: C:\Users\kk\ontario-db-backup-2026-10-23-leamington-unit\
  2026-10-24  sdg key_field "Unique_ID" -> "" (--old-rev HEAD): 32,060 of 32,072 rows,
              31,877 chains re-keyed, 177 splits (52 on 06-12, the 30-70 m structure
              snap, now retire + add; 47 on 06-18, Saphire -> Sapphire Dr), 13 joins.
              Then rebuilt by rebuild_from_pulls.py --gap-dates: the bare-prefix and
              duplicated Unique_IDs had hidden 1,863-2,020 addresses, and the hidden set
              changes across the 06-12..06-23 gap with no raw pull, so each of those 59
              rows was dated from the store's visible events. Verify against the 10-22
              pull 0/0/0, content_hash equal; a re-run rewrites 0.
              Backup: C:\Users\kk\ontario-db-backup-2026-10-24-sdg-synth\

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
    return normalize.derive_canonical(ds, rec)


def old_dataset(slug, rev):
    """The dataset as datasets/<slug>.toml read at git revision `rev`."""
    import subprocess
    import tempfile
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    text = subprocess.run(["git", "show", f"{rev}:datasets/{slug}.toml"], cwd=root,
                          capture_output=True, check=True).stdout
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, f"{slug}.toml")
        with open(path, "wb") as f:
            f.write(text)
        return registry._parse(path)


def plan(ds, conn, old_ds=None):
    """Return (updates, stats) or exit with the reason the city is refused.
    `old_ds` is the config the store was built under (default: ds); only its
    identity settings are used, to recompute the stored keys."""
    old_ds = old_ds or ds
    keep = {k.lower() for k in ds.keep_fields}
    rows = conn.execute(
        "SELECT identity_key, min_snapshot_id, max_snapshot_id, number, street, unit, "
        "full, longitude, latitude, props, payload_hash FROM addresses").fetchall()

    unfaithful = []
    unfaithful_untouched = 0
    new_keys_of = defaultdict(set)   # old key -> new keys of its versions
    spans_of = defaultdict(list)     # new key -> (min, max, old key) of its rows
    updates = []
    for r in rows:
        props = json.loads(r["props"] or "{}")
        lon, lat = r["longitude"], r["latitude"]
        old = {c: r[c] for c in _CANONICAL}
        rec = derive(ds, r)
        if (ds.key_field and ds.key_field == old_ds.key_field
                and not r["identity_key"].startswith("syn:")):
            # a source-id key (leamington GlobalID): taken from a raw prop, never from
            # the canonical columns, so no derivation can move it - and is_volatile
            # may have stripped that prop from the stored blob, so it cannot be
            # recomputed to prove it either
            key = r["identity_key"]
        elif normalize._identity(old_ds, old, props, lon, lat) != r["identity_key"]:
            if any(rec[c] != old[c] for c in _CANONICAL):
                unfaithful.append(r["identity_key"])
                continue
            unfaithful_untouched += 1
            key = r["identity_key"]
        else:
            key = normalize._identity(ds, rec, props, lon, lat)
        new_keys_of[r["identity_key"]].add(key)
        spans_of[key].append((r["min_snapshot_id"], r["max_snapshot_id"], r["identity_key"]))
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

    owners = defaultdict(set)
    for old, news in new_keys_of.items():
        for new in news:
            owners[new].add(old)
    collisions, joined = {}, 0
    for new, olds in owners.items():
        if len(olds) < 2:
            continue
        ss = sorted(spans_of[new])
        if any(b[0] <= a[1] for a, b in zip(ss, ss[1:])):
            collisions[new] = olds
        else:
            joined += 1
    if collisions:
        sample = list(collisions.items())[:3]
        sys.exit(f"{ds.slug}: {len(collisions):,} new keys would merge distinct chains "
                 f"(e.g. {sample}) - refusing")


    rekeyed = sum(1 for old, news in new_keys_of.items() if news != {old})
    split = sorted(old for old, news in new_keys_of.items() if len(news) > 1)
    return updates, {"rows": len(rows), "chains_rekeyed": rekeyed, "split": split,
                     "joined": joined,
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
    if added and not removed and not modified:
        print("  only additions: rows the old rule keyed onto another row's key, which the "
              "importer's dedupe dropped - they were never stored, so no rewrite can add "
              "them; replay the pulls with tools/rebuild_from_pulls.py (hastings 2026-10-20)")
    return not (added or removed or modified) and pulled_ch == ch


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--city", required=True, help="dataset slug")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("--verify", action="store_true",
                    help="after (or instead of, with --dry-run) the rewrite, compare "
                         "the store with the vault's latest pull")
    ap.add_argument("--old-rev", help="git revision whose datasets/<slug>.toml the store "
                         "was built under, when the change edits [identity] (e.g. HEAD)")
    ap.add_argument("--backup-dir", help="directory for the pre-migration copy")
    ap.add_argument("--no-backup", action="store_true")
    args = ap.parse_args()

    ds = registry.load(args.city)
    if not os.path.exists(ds.db_path):
        sys.exit(f"no store at {ds.db_path}")

    conn = sqlite3.connect(ds.db_path)
    conn.row_factory = sqlite3.Row
    old_ds = old_dataset(ds.slug, args.old_rev) if args.old_rev else None
    updates, stats = plan(ds, conn, old_ds)
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
          + (f", {len(stats['split']):,} of them split" if stats["split"] else "")
          + (f", {stats['joined']:,} keys joining time-disjoint chains"
             if stats["joined"] else "")
          + (f"; {stats['unfaithful_untouched']:,} unchanged rows whose key does not "
             "recompute, left alone" if stats["unfaithful_untouched"] else ""))
    if args.verify and not verify(ds):
        sys.exit(1)


if __name__ == "__main__":
    main()
