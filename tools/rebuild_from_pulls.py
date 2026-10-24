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
never reach the table) are kept, holes included (muskoka has no id 18). Each pull
comes from data/<slug>/<filename> when a local copy exists, else the vault: a cold day
is thawed, or with --dump-dir streamed out of the archive into that directory and
deleted once read (no vault write, and no 24 h of thawed copies - brampton's history is
~29 GB of them). A skipped day replays the file it resolves to and is recorded as a
skip by the importer itself.

A non-skipped day with no raw pull anywhere (hastings 06-15 to 06-23: the vault
starts later), or named with --stored-day because its vault copy is not the pull the
store imported (frontenac 07-16: imported 18:02 UTC, the vault kept a re-fetch from
18:56 that had already dropped four rows), is rebuilt from the old store: its active
rows turned back into features (stored props + point; ignored and volatile props are
absent, which is what they would have been - except a mapped column or the key_field,
put back from the stored canonical column and key: renfrew ignores Full_Address, the
source of `full`), plus the rows the old rule hid on both bracketing raw days,
taken from the earlier one. That is only sound when the hidden set does not change
across the gap - same keys, same payloads - and the row the old rule kept on each
colliding key is the one the old store has on that key all through the gap; checked
here, refused otherwise. A hidden key that is also a stored key that day is refused
too (the importer's dedupe would silently drop one of them).

--gap-dates FILE is the one way past a hidden set that does change (sdg 2026-10-24:
53 hidden addresses appear and 6 go across 06-12..06-23). A TOML file dating every
difference row explicitly, keyed by its new-rule identity key:

    [added]                         # hidden after the gap, absent before it
    "syn:3fcb..." = "2026-06-15"    # 65 Timberline Dr - first snapshot that has it
    [gone]                          # hidden before the gap, absent after it
    "syn:d0da..." = "2026-06-18"    # 199 Patterson St - first snapshot without it

A date must be a non-skipped snapshot inside the gap or the first raw snapshot after
it. An added row dated to that raw snapshot is injected on no gap day (it enters from
the pull); a gone row dated there is injected on every gap day (the pull drops it). If
that snapshot was a skip in the old store it now records those changes, so its skipped
flag may flip 1 -> 0 - only there, only when the file dates a row to it, and printed.
The file must cover the difference exactly: an undated difference row, a listed key
that is not one, a wrong side, or a date out of range is refused. Take the dates from
evidence in the old store's own visible events (the day neighbouring id-less rows
appeared, the day a parent retired); with none, the first raw pull that shows the
change. Without the flag nothing changes.

--tiebreak is for a change to WHICH row of a duplicate identity_key is stored
(db.tiebreak_rank, 2026-10-24: the file-order dedupe became a fixed order). There the
replay legitimately swaps stored rows, so the "only adds" check below is narrowed, not
dropped: an old (key, hash) may be missing only when that snapshot's replayed features
carried the key on two or more rows with different hashes, the old hash among them,
and the rebuild holds the key - the row lost the tie, nothing else. On a gap day the
stored row of a contested key is joined by every row of that key present (same hash)
on BOTH bracketing pulls, and the importer's tie-break picks among them: a row on both
sides is assumed present in between, as the hidden-set check assumes of hidden rows,
and a row on one side only is not. Skip flags may change either way (a day whose only
"change" was the export reordering a duplicate pair becomes a skip - greater-sudbury
72 such days); ids and filenames may not. All of it is printed.

The new store is built beside the old one (data/_rebuild_<slug>/) and swapped in only
with --swap, after a backup into --backup-dir. downloaded / remote_* timestamps are
carried over from the old snapshots table. Checks, all printed:
  - the snapshot list (ids, filenames, skipped flags) matches the old one, except that
    a skip may turn into a change (never the reverse) on a raw day - the same pull, so
    only a row the old rule hid can have changed (sdg 2026-10-24: 17 such days) - or
    on the day after a gap that --gap-dates dates rows to;
  - at every snapshot, every (key, hash) the old store had active is active in the new
    one (the replay only adds), and what it adds is listed by count;
  - recanonicalize.py --verify against the latest pull after the swap.

Run so far:
  2026-10-20  hastings (number_from_full): 82 snapshots, 7 bracketed from 06-11/06-24
              (444 hidden on both, identical). 31,716 -> 32,165 rows, 450 keys added,
              every one a suffix sibling at a shared point; every old active row kept;
              verify against the 10-20 pull 0/0/0. Backup:
              C:\Users\kk\ontario-db-backup-2026-10-20-suffixes\hastings.pre-rebuild.db
  2026-10-23  prince-edward-county (NGUID key, after recanonicalize re-keyed the store
              so old and new keys compare): 23 snapshots, all raw. 27,436 -> 27,618
              rows, up to 182 added per snapshot (94B/94C Wilolea shape); every old
              active row kept; verify against the 10-20 pull 0/0/0. Backup:
              C:\Users\kk\ontario-db-backup-2026-10-23-pec-nguid\prince-edward-county.pre-rebuild.db
  2026-10-23  ajax (FACILITYID -> synth number/street/unit) and west-parry-sound (synth ->
              globalid): key-basis changes, so the (key, hash) subset check cannot pass by
              construction. Built with --old-rev HEAD, no --swap; checked instead that every
              old payload_hash (as a multiset) stays active at every non-skipped snapshot,
              then swap(). ajax 38,400 -> 38,432 rows (32 hidden addresses back); wps 21,737
              rows on 21,735 keys (two renumbers now modifications). Verify 0/0/0 each.
              Backups: C:\Users\kk\ontario-db-backup-2026-10-23-rekey\<slug>\
  2026-10-24  sdg (Unique_ID -> synth number/street/unit + point, after recanonicalize
              re-keyed the store): 69 snapshots, 6 rebuilt from the store across the
              06-12..06-23 gap with --gap-dates (file kept beside the backup, 53 added /
              6 gone): Timberline Dr x36 added 06-15, Patterson St 199/201 gone 06-18
              (Armstrong Rd NS_3731/3732 on their points), Labrosse St 20A-22B gone and
              24A-26B added 06-22, Airport Rd 19686-1..9 added 06-23, 4 with no evidence
              added 06-24. 32,072 -> 34,130 rows; 1,863 (06-11) to 2,020 (10-23) hidden
              addresses back. 18 skips became changes: 06-24 (the 4 dated there) and 17
              raw days where only a hidden row changed. Every old active payload kept at
              every snapshot; a second build was row-for-row identical; verify against
              the 10-22 pull 0/0/0. Backups:
              C:\Users\kk\ontario-db-backup-2026-10-24-sdg-synth\

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
import tomllib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db, normalize, registry
from src.fetch import load_features

_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


class Cold(str):
    """A cold vault day left in the archive (--dump-dir): the canonical date, read by
    features() with a restic dump each time."""


def raw_path(ds, filename, dump_dir=None):
    local = os.path.join(ds.data_dir, filename)
    if os.path.exists(local):
        return local
    from addressvault import Archived, Vault
    v = Vault(link_wait=False)
    date = _DATE.search(filename).group()
    try:
        return v.path(ds.slug, date)
    except Archived:
        if dump_dir:
            snap = v.snapshot(ds.slug, date)
            return Cold(snap.unchanged_since or snap.date)
        v.thaw(ds.slug, date, wait=True)
        return v.path(ds.slug, date)
    except LookupError:
        return None


def features(ds, path, dump_dir=None):
    """A pull's features as a list (the replay reads one more than once). A Cold day is
    dumped into dump_dir, read, and deleted."""
    if not isinstance(path, Cold):
        return list(load_features(path))
    from addressvault import Vault, archive
    os.makedirs(dump_dir, exist_ok=True)
    target = os.path.join(dump_dir, f"{ds.slug}-{path}.geojson")
    if not archive.dump(Vault(link_wait=False).root, ds.slug, str(path), target):
        sys.exit(f"{ds.slug} {path}: restic dump failed")
    try:
        return list(load_features(target))
    finally:
        os.remove(target)


def _collisions(ds, old_ds, features):
    """(hidden, kept). hidden = {new key: (feature, payload_hash)}: features whose
    new-rule key is distinct but whose old-rule key collided with an earlier row's - the
    rows the old rule dropped. kept = {old key: new key} of the row the old rule kept
    on each colliding key."""
    seen_old, seen_new, hidden, kept = {}, set(), {}, {}
    for f in features:
        rn = normalize.canonical(ds, f)
        if rn is None or rn["identity_key"] in seen_new:
            continue
        seen_new.add(rn["identity_key"])
        ko = normalize.canonical(old_ds, f)["identity_key"]
        if ko in seen_old:
            hidden[rn["identity_key"]] = (f, rn["payload_hash"])
            kept[ko] = seen_old[ko]
        else:
            seen_old[ko] = rn["identity_key"]
    return hidden, kept


def _hidden(ds, old_ds, features):
    """The rows the old rule dropped. {new key: feature}."""
    return {k: f for k, (f, _) in _collisions(ds, old_ds, features)[0].items()}


def load_gap_dates(path):
    """--gap-dates file -> {new key: ("added" | "gone", date)}."""
    with open(path, "rb") as f:
        doc = tomllib.load(f)
    if set(doc) - {"added", "gone"}:
        sys.exit(f"{path}: only [added] and [gone] tables are allowed, not "
                 f"{sorted(set(doc) - {'added', 'gone'})}")
    out = {}
    for kind in ("added", "gone"):
        for key, date in doc.get(kind, {}).items():
            if not isinstance(date, str) or not _DATE.fullmatch(date):
                sys.exit(f"{path}: {key} = {date!r} is not a YYYY-MM-DD date")
            if key in out:
                sys.exit(f"{path}: {key} is in both [added] and [gone]")
            out[key] = (kind, date)
    return out


def _plan_gaps(ds, old_ds, snaps, paths, bracket, gap_dates, dump_dir=None):
    """What each no-pull gap day gets beyond its stored rows. Returns
    ({gap sid: [hidden features]}, {gap sid: {old key: kept new key}}, {sids that may
    flip from a skip into a change}), or exits with the reason it cannot."""
    coll = {fn: _collisions(ds, old_ds, features(ds, paths[fn], dump_dir))
            for fn in {f for pair in bracket.values() for f in pair}}
    date_of = {sid: _DATE.search(fn).group() for sid, fn, _ in snaps}
    sid_of = {fn: sid for sid, fn, _ in snaps}
    skipped = {sid: sk for sid, _, sk in snaps}
    inject, kept, flips, used, undated = {}, {}, set(), set(), []
    for b, a in sorted(set(bracket.values())):
        (hb, kb), (ha, _) = coll[b], coll[a]
        gap = sorted(s for s, pair in bracket.items() if pair == (b, a))
        changed = sorted(k for k in hb.keys() & ha.keys() if hb[k][1] != ha[k][1])
        if changed:
            sys.exit(f"snapshots {gap}: {len(changed)} hidden rows change payload across "
                     f"the gap ({b} -> {a}, e.g. {changed[:2]}) - refusing to infer when")
        diff = hb.keys() ^ ha.keys()
        if diff and gap_dates is None:
            sys.exit(f"snapshots {gap}: the hidden set changes across the gap ({b} -> {a}: "
                     f"{len(ha.keys() - hb.keys())} added, {len(hb.keys() - ha.keys())} "
                     f"gone) - refusing to infer it; --gap-dates can date them")
        allowed = {date_of[s] for s in gap} | {date_of[sid_of[a]]}
        for s in gap:
            inject[s] = [f for k, (f, _) in hb.items() if k in ha]
            kept[s] = kb
        for k in sorted(diff):
            kind, side = ("gone", hb) if k in hb else ("added", ha)
            if k not in (gap_dates or {}):
                r = normalize.canonical(ds, side[k][0])
                undated.append(f"{k} ({kind}: {r['full'] or (r['number'], r['street'])})")
                continue
            listed, date = gap_dates[k]
            if listed != kind:
                sys.exit(f"--gap-dates: {k} is under [{listed}] but is {kind} across "
                         f"{b} -> {a}")
            if date not in allowed:
                sys.exit(f"--gap-dates: {k} = {date} is neither a non-skipped snapshot in "
                         f"the gap {b} -> {a} nor the raw snapshot after it")
            used.add(k)
            if date == date_of[sid_of[a]] and skipped[sid_of[a]]:
                flips.add(sid_of[a])
            for s in gap:
                if (date_of[s] < date) if kind == "gone" else (date_of[s] >= date):
                    inject[s].append(side[k][0])
    if undated:
        sys.exit(f"--gap-dates does not date {len(undated)} hidden-set difference rows: "
                 + "; ".join(undated[:10]))
    stale = set(gap_dates or {}) - used
    if stale:
        sys.exit(f"--gap-dates names {len(stale)} keys that are no hidden-set difference "
                 f"(e.g. {sorted(stale)[:3]})")
    return inject, kept, flips


def _stored_features(conn, sid, ds):
    """A day's active rows as features. Stored props lack what the importer strips -
    ignored columns, which can include a mapped one (renfrew ignores Full_Address,
    the source of `full`), and volatile ones, which can include the key_field
    (GlobalID) - so those come back from the stored canonical column and key.
    Ignored and volatile props stay out of the hash either way, and _clean is
    idempotent, so the importer re-derives the stored row exactly."""
    rows = conn.execute(
        "SELECT props, longitude, latitude, identity_key, number, street, unit, full "
        "FROM addresses WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?",
        (sid, sid)).fetchall()
    out = []
    for p, lon, lat, key, *canon in rows:
        props = json.loads(p or "{}")
        for name, value in zip(("number", "street", "unit", "full"), canon):
            src = ds.fields.get(name)
            if src and src not in props and value is not None:
                props[src] = value
        if ds.key_field and ds.key_field not in props and not key.startswith("syn:"):
            props[ds.key_field] = key
        out.append({"type": "Feature", "properties": props,
                    "geometry": {"type": "Point", "coordinates": [lon, lat]}})
    return out


def _contested(ds, feats):
    """Keys a day carries on rows with two or more different payload hashes - the
    groups whose stored row the tie-break decides. {key: {hash: feature}}."""
    return {k: g for k, g in _groups(ds, feats).items() if len(g) > 1}


def _groups(ds, feats, keys=None):
    """{key: {hash: feature}}, for the given keys only when given (singletons too)."""
    out = {}
    for f in feats:
        r = normalize.canonical(ds, f)
        if r is not None and (keys is None or r["identity_key"] in keys):
            out.setdefault(r["identity_key"], {}).setdefault(r["payload_hash"], f)
    return out


def _tie_candidates(old, sid, before, after):
    """Rows to put beside a gap day's stored rows for the tie-break: for each contested
    key the old store holds that day, the rows present (same payload hash) on BOTH
    bracketing pulls other than the stored one. Returns (features, keys whose
    candidates differ across the gap)."""
    stored = dict(_active(old, sid))
    out, changed = [], 0
    for k in set(before) | set(after):
        if k not in stored:
            continue
        b, a = before.get(k, {}), after.get(k, {})
        changed += set(b) != set(a)
        out.extend(f for h, f in b.items() if h in a and h != stored[k])
    return out, changed


def _next_snapshot_id(tmp, sid):
    """Make the rebuilt store's next snapshot id the old store's: a snapshot deleted
    from the old table (muskoka id 18, the 06-28 field-stripped pull) leaves a hole
    the AUTOINCREMENT replay would otherwise close, shifting every later id."""
    conn = db.init_db(tmp)
    conn.execute("DELETE FROM sqlite_sequence WHERE name = 'snapshots'")
    conn.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('snapshots', ?)", (sid - 1,))
    conn.commit()
    conn.close()


def _refuse(msg, *conns):
    for c in conns:                  # closed, so a retry in-process can clear the dir
        c.close()
    sys.exit(msg)


def _active(conn, sid):
    return set(conn.execute(
        "SELECT identity_key, payload_hash FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchall())


def rebuild(ds, old_ds, gap_dates=None, tiebreak=False, dump_dir=None, stored_days=()):
    tmp = dataclasses.replace(ds, slug=f"_rebuild_{ds.slug}")
    shutil.rmtree(tmp.data_dir, ignore_errors=True)
    if os.path.exists(tmp.db_path):
        sys.exit(f"cannot clear {tmp.data_dir} (open elsewhere?) - not rebuilding over it")
    old = sqlite3.connect(f"file:{ds.db_path}?mode=ro", uri=True)
    snaps = old.execute("SELECT id, filename, skipped FROM snapshots ORDER BY id").fetchall()

    unknown = set(stored_days) - {fn for _, fn, sk in snaps if not sk}
    if unknown:
        _refuse(f"--stored-day names no recorded snapshot: {sorted(unknown)}", old)
    locate = (lambda fn: raw_path(ds, fn, dump_dir)) if dump_dir else (lambda fn: raw_path(ds, fn))
    paths = {fn: None if fn in stored_days else locate(fn) for _, fn, _ in snaps}
    gaps = [(sid, fn) for sid, fn, sk in snaps if not sk and paths[fn] is None]
    bracket = {}
    for sid, fn in gaps:
        before = [f for s, f, sk in snaps if s < sid and paths[f]]
        after = [f for s, f, sk in snaps if s > sid and paths[f]]
        if not before or not after:
            sys.exit(f"{fn}: no raw pull on one side of the gap - cannot bracket it")
        bracket[sid] = (before[-1], after[0])
    inject, kept, flips = _plan_gaps(ds, old_ds, snaps, paths, bracket, gap_dates, dump_dir)
    groups_at = {}
    if tiebreak and bracket:            # two passes: contested anywhere, then those rows
        files = sorted({f for pair in bracket.values() for f in pair})
        keys = set()
        for fn in files:
            keys |= set(_contested(ds, features(ds, paths[fn], dump_dir)))
        for fn in files:
            groups_at[fn] = _groups(ds, features(ds, paths[fn], dump_dir), keys)

    contested = {}                       # sid -> {key: candidate hashes}, --tiebreak
    last_features = None
    for sid, fn, sk in snaps:
        if paths[fn]:
            # list, not the stream: an unchanged day after it re-imports these.
            feats = features(ds, paths[fn], dump_dir)
            source = "raw"
        elif sk:
            feats = last_features                # an unchanged day: same content
            source = "previous"
        else:
            stored = _stored_features(old, sid, ds)
            keys, on_kept = set(), {}
            for f in stored:
                kn = normalize.canonical(ds, f)["identity_key"]
                keys.add(kn)
                ko = normalize.canonical(old_ds, f)["identity_key"]
                if ko in kept[sid]:
                    on_kept.setdefault(ko, set()).add(kn)
            moved = sorted(ko for ko, kn in kept[sid].items() if on_kept.get(ko) != {kn})
            if moved:
                sys.exit(f"snapshot {sid}: the stored row on colliding keys {moved[:3]} is "
                         f"not the one the old rule kept before the gap - refusing")
            extra = inject[sid]
            dup = keys & {normalize.canonical(ds, f)["identity_key"] for f in extra}
            if dup:
                sys.exit(f"snapshot {sid}: {len(dup)} hidden keys are stored keys that day "
                         f"(e.g. {sorted(dup)[:2]}) - refusing")
            feats = stored + extra
            b, a = bracket[sid]
            source = f"stored + {len(extra)} hidden, {b} -> {a}"
            if tiebreak:
                ties, changed = _tie_candidates(old, sid, groups_at[b], groups_at[a])
                feats += ties
                source += (f"; + {len(ties)} tie candidates on both sides, "
                           f"{changed} keys' candidates differ across the gap")
        print(f"  {sid:>3} {fn}  ({source})")
        if tiebreak:
            contested[sid] = {k: set(g) for k, g in _contested(ds, feats).items()}
        _next_snapshot_id(tmp, sid)
        db.import_snapshot(tmp, fn, feats)
        last_features = feats

    new = sqlite3.connect(tmp.db_path)
    new_snaps = new.execute("SELECT id, filename, skipped FROM snapshots ORDER BY id").fetchall()
    # A raw day the old rule saw as a skip may record a change now: the same pull, so
    # the old rule's deduped content was unchanged and what changed is a row it hid
    # (sdg: a bare-prefix row added, retired or edited). Never the other way round.
    raw = {sid for sid, fn, _ in snaps if paths[fn]}
    got = dict((sid, sk) for sid, _, sk in new_snaps)
    # --tiebreak: either way, on any day - the kept row of a contested key is a
    # different row now, so a day can gain a change or lose one; printed below
    expect = [(sid, fn, got.get(sid, sk) if tiebreak else
               0 if sid in flips or (sid in raw and got.get(sid) == 0) else sk)
              for sid, fn, sk in snaps]
    if new_snaps != expect:
        diff = [(a, b) for a, b in zip(expect, new_snaps) if a != b][:5]
        _refuse(f"snapshot list differs from the old store: {diff} - not swapping", old, new)
    flipped = 0
    for sid, fn, sk in snaps:
        if sk == got[sid]:
            continue
        flipped += 1
        if sid in flips:
            print(f"snapshot {sid} ({fn}): skip -> change, as --gap-dates dates rows to it")
        elif sk:
            print(f"snapshot {sid} ({fn}): skip -> change, a hidden or tied row changed")
        else:
            print(f"snapshot {sid} ({fn}): change -> skip, only a tied row's pick moved")
    for sid, dl, lm, cl in old.execute("SELECT id, downloaded, remote_last_modified, "
                                       "remote_content_length FROM snapshots"):
        new.execute("UPDATE snapshots SET downloaded = ?, remote_last_modified = ?, "
                    "remote_content_length = ? WHERE id = ?", (dl, lm, cl, sid))
    new.commit()

    # a skip extends no span, so what is live at a snapshot is what was live at the
    # last non-skipped one up to it - in each store, as their skips now differ
    def live(snapshots):
        last, out = None, {}
        for sid, _, sk in snapshots:
            last = last if sk else sid
            out[sid] = last
        return out
    live_old, live_new = live(snaps), live(new_snaps)
    added_total, swapped = 0, set()
    for sid, fn, sk in snaps:
        o, n = _active(old, live_old[sid]), _active(new, live_new[sid])
        missing = o - n
        if tiebreak and missing:
            nkeys = {k for k, _ in n}
            cand = contested.get(sid, {})
            lost = {(k, h) for k, h in missing if k in nkeys and h in cand.get(k, ())}
            if lost:
                print(f"  {sid:>3} {fn}: {len(lost):,} stored rows lose the tie-break")
                swapped |= {k for k, _ in lost}
            missing -= lost
        if missing:
            _refuse(f"snapshot {sid}: {len(missing):,} stored (key, hash) pairs missing "
                    f"from the rebuild (e.g. {sorted(missing)[:2]}) - not swapping", old, new)
        okeys = {k for k, _ in o}
        added_total = max(added_total, sum(1 for k, _ in n - o if k not in okeys))
    rows_old = old.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]
    rows_new = new.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]
    new.close()
    old.close()
    if tiebreak:
        print(f"{len(swapped):,} keys store another of their rows at some snapshot "
              f"(e.g. {sorted(swapped)[:5]}); {flipped} skip flags changed")
    print(f"every other old active row kept at every snapshot; the rebuild adds up to "
          f"{added_total:,} keys per snapshot; {rows_old:,} -> {rows_new:,} rows")
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
    ap.add_argument("--gap-dates", metavar="FILE",
                    help="TOML dating each hidden-set difference row across a no-pull "
                         "gap: [added] / [gone] tables, new key -> snapshot date")
    ap.add_argument("--tiebreak", action="store_true",
                    help="the change moves which row of a duplicate key is stored: "
                         "excuse exactly those swaps (see above)")
    ap.add_argument("--stored-day", action="append", default=[], metavar="FILENAME",
                    help="rebuild this recorded day from the old store, as if it had no "
                         "raw pull: its vault copy is not the pull the store imported "
                         "(frontenac-2026-07-16.geojson, re-fetched after the import)")
    ap.add_argument("--dump-dir",
                    help="stream cold pulls out of the archive into this directory, "
                         "one at a time, instead of thawing them")
    ap.add_argument("--swap", action="store_true", help="swap the rebuilt store in")
    ap.add_argument("--backup-dir")
    args = ap.parse_args()
    ds = registry.load(args.city)
    from tools.recanonicalize import old_dataset
    gap_dates = load_gap_dates(args.gap_dates) if args.gap_dates else None
    tmp = rebuild(ds, old_dataset(ds.slug, args.old_rev), gap_dates, args.tiebreak,
                  args.dump_dir, args.stored_day)
    if args.swap:
        if not args.backup_dir:
            sys.exit("--swap needs --backup-dir")
        swap(ds, tmp, args.backup_dir)


if __name__ == "__main__":
    main()
