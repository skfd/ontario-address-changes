r"""Migration: rebuild a city's store by replaying its own snapshot history through the
importer under today's rules.

For a rule change that reveals rows the old rule never stored, which no rewrite of
stored rows can recover. The case that made it (hastings, 2026-10-20): the old synth
key took House_No, which drops the suffix, so "295A MILL ST" and "295B MILL ST" at one
point shared a key and the importer's dedupe kept whichever came first in the file.
417 addresses (444 at the June baseline) were never stored, and on days the export
put the other sibling first, the stored chain switched to it. number_from_full tells
them apart; only the raw pulls hold the dropped ones.

The replay follows the old store's snapshots table exactly: same filenames, same
order, so ids line up and decisions already taken (repair_bad_snapshots drops, which
never reach the table) are kept. Each pull comes from data/<slug>/<filename> when a
local copy exists, else the vault (thawed if cold); a skipped day replays the file it
resolves to and is recorded as a skip by the importer itself.

A non-skipped day with no raw pull anywhere (hastings 06-15 to 06-23: the vault
starts later) is rebuilt from the old store: its active rows turned back into
features (stored props + point; ignored and volatile props are absent, which is what
they would have been), plus the rows the old rule hid on both bracketing raw days,
taken from the earlier one. That is only sound when the hidden set does not change
across the gap - checked here, refused otherwise.

The new store is built beside the old one (data/_rebuild_<slug>/) and swapped in only
with --swap, after a backup into --backup-dir. downloaded / remote_* timestamps are
carried over from the old snapshots table. Checks, all printed:
  - the snapshot list (ids, filenames, skipped flags) matches the old one;
  - at every non-skipped snapshot, every (key, hash) the old store had active is
    active in the new one (the replay only adds), and what it adds is listed by count;
  - recanonicalize.py --verify against the latest pull after the swap.

Run so far:
  2026-10-20  hastings (number_from_full): 82 snapshots, 7 bracketed from 06-11/06-24
              (444 hidden on both, identical). 31,716 -> 32,165 rows, 450 keys added,
              every one a suffix sibling at a shared point; every old active row kept;
              verify against the 10-20 pull 0/0/0. Backup:
              C:\Users\kk\ontario-db-backup-2026-10-20-suffixes\hastings.pre-rebuild.db

Not part of the daily run.
"""

import argparse
import dataclasses
import json
import os
import re
import shutil
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize, registry
from src.fetch import load_features

_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def raw_path(ds, filename):
    local = os.path.join(ds.data_dir, filename)
    if os.path.exists(local):
        return local
    from addressvault import Archived, Vault
    v = Vault(link_wait=False)
    date = _DATE.search(filename).group()
    try:
        return v.path(ds.slug, date)
    except Archived:
        v.thaw(ds.slug, date, wait=True)
        return v.path(ds.slug, date)
    except LookupError:
        return None


def _hidden(ds, old_ds, features):
    """Features whose new-rule key is distinct but whose old-rule key collided with
    an earlier row's: the rows the old rule dropped. {new key: feature}."""
    seen_old, seen_new, out = set(), set(), {}
    for f in features:
        rn = normalize.canonical(ds, f)
        if rn is None or rn["identity_key"] in seen_new:
            continue
        seen_new.add(rn["identity_key"])
        ko = normalize.canonical(old_ds, f)["identity_key"]
        if ko in seen_old:
            out[rn["identity_key"]] = f
        else:
            seen_old.add(ko)
    return out


def _stored_features(conn, sid):
    rows = conn.execute(
        "SELECT props, longitude, latitude FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchall()
    return [{"type": "Feature", "properties": json.loads(p or "{}"),
             "geometry": {"type": "Point", "coordinates": [lon, lat]}}
            for p, lon, lat in rows]


def _active(conn, sid):
    return set(conn.execute(
        "SELECT identity_key, payload_hash FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchall())


def rebuild(ds, old_ds):
    tmp = dataclasses.replace(ds, slug=f"_rebuild_{ds.slug}")
    shutil.rmtree(tmp.data_dir, ignore_errors=True)
    old = sqlite3.connect(f"file:{ds.db_path}?mode=ro", uri=True)
    snaps = old.execute("SELECT id, filename, skipped FROM snapshots ORDER BY id").fetchall()

    paths = {fn: raw_path(ds, fn) for _, fn, _ in snaps}
    gaps = [(sid, fn) for sid, fn, sk in snaps if not sk and paths[fn] is None]
    bracket = {}
    for sid, fn in gaps:
        before = [f for s, f, sk in snaps if s < sid and paths[f]]
        after = [f for s, f, sk in snaps if s > sid and paths[f]]
        if not before or not after:
            sys.exit(f"{fn}: no raw pull on one side of the gap - cannot bracket it")
        bracket[sid] = (before[-1], after[0])
    hidden_at = {}
    for fn in {f for pair in bracket.values() for f in pair}:
        hidden_at[fn] = _hidden(ds, old_ds, load_features(paths[fn]))
    for sid, (b, a) in bracket.items():
        if set(hidden_at[b]) != set(hidden_at[a]):
            sys.exit(f"snapshot {sid}: the hidden set changes across the gap "
                     f"({b} -> {a}) - refusing to infer it")

    last_features = None
    for sid, fn, sk in snaps:
        if paths[fn]:
            features = load_features(paths[fn])
            source = "raw"
        elif sk:
            features = last_features             # an unchanged day: same content
            source = "previous"
        else:
            b, _ = bracket[sid]
            features = _stored_features(old, sid) + list(hidden_at[b].values())
            source = f"stored + {len(hidden_at[b])} hidden from {b}"
        print(f"  {sid:>3} {fn}  ({source})")
        db.import_snapshot(tmp, fn, features)
        last_features = features

    new = sqlite3.connect(tmp.db_path)
    new_snaps = new.execute("SELECT id, filename, skipped FROM snapshots ORDER BY id").fetchall()
    if new_snaps != snaps:
        diff = [(a, b) for a, b in zip(snaps, new_snaps) if a != b][:5]
        sys.exit(f"snapshot list differs from the old store: {diff} - not swapping")
    for sid, dl, lm, cl in old.execute("SELECT id, downloaded, remote_last_modified, "
                                       "remote_content_length FROM snapshots"):
        new.execute("UPDATE snapshots SET downloaded = ?, remote_last_modified = ?, "
                    "remote_content_length = ? WHERE id = ?", (dl, lm, cl, sid))
    new.commit()

    added_total = 0
    for sid, fn, sk in snaps:
        if sk:
            continue
        o, n = _active(old, sid), _active(new, sid)
        if not o <= n:
            sys.exit(f"snapshot {sid}: {len(o - n):,} stored (key, hash) pairs missing "
                     f"from the rebuild (e.g. {sorted(o - n)[:2]}) - not swapping")
        added_total = max(added_total, len(n - o))
    new.close()
    old.close()
    print(f"every old active row kept at every snapshot; the rebuild adds up to "
          f"{added_total:,} rows per snapshot")
    return tmp


def swap(ds, tmp, backup_dir):
    os.makedirs(backup_dir, exist_ok=True)
    dest = os.path.join(backup_dir, f"{ds.slug}.pre-rebuild.db")
    if os.path.exists(dest):
        sys.exit(f"backup already exists: {dest}")
    src = sqlite3.connect(ds.db_path)
    dst = sqlite3.connect(dest)
    src.backup(dst)
    dst.close()
    src.close()
    src = sqlite3.connect(tmp.db_path)
    dst = sqlite3.connect(ds.db_path)
    src.backup(dst)                                  # overwrite in place, WAL-safe
    dst.close()
    src.close()
    shutil.rmtree(tmp.data_dir, ignore_errors=True)
    print(f"swapped in; old store backed up to {dest}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--city", required=True)
    ap.add_argument("--old-rev", required=True,
                    help="git revision of datasets/<slug>.toml before the rule change, "
                         "to tell which rows the old rule dropped")
    ap.add_argument("--swap", action="store_true", help="swap the rebuilt store in")
    ap.add_argument("--backup-dir")
    args = ap.parse_args()
    ds = registry.load(args.city)
    from tools.recanonicalize import old_dataset
    tmp = rebuild(ds, old_dataset(ds.slug, args.old_rev))
    if args.swap:
        if not args.backup_dir:
            sys.exit("--swap needs --backup-dir")
        swap(ds, tmp, args.backup_dir)


if __name__ == "__main__":
    main()
