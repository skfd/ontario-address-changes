# Repairing a store

For when a snapshot that is not an observation of the city got recorded anyway. Reports
are rebuilt from the store on every run, so the bad day keeps producing its fake event
until the store itself is fixed — deleting the HTML does nothing.

```
python tools/repair_bad_snapshots.py --city <slug> --drop <filename> [--rekey] [--dry-run]
python run.py report --city <slug>
```

**Always `--dry-run` first, and take a copy of `data/<slug>/<slug>.db` before the real
run.** Nothing here can be undone.

## Decide before you reach for it

The guards refuse suspect pulls before writing (`corrupt-pulls.md`), so a snapshot that
needs removing has already passed them. That makes it the rarer case, and the bar is
correspondingly high: this rewrites recorded history.

- **Is the snapshot wrong, or just surprising?** A source can legitimately do something
  drastic. Wrong means "not an observation of this city" — a truncation, a stripped
  field roster, a mirrored copy served by mistake.
- **Is the day recoverable instead?** Almost never: the services serve current data only.
  Do not re-fetch and re-import under the old date hoping to get the real state.
- **Was the report published?** It cannot be un-published. Repairing still fixes the
  archive going forward, which is the point, but say so plainly rather than implying the
  event never happened.

## What it does

Deletes the named snapshot rows, then rebuilds `addresses` from the active set of each
*surviving non-skipped* snapshot, so every SCD-2 range boundary lands where a clean
import would have put it. It also recomputes each surviving snapshot's `content_hash`,
which gates the "no changes → record a skip" fast path — leaving those stale makes the
next run take the wrong branch. A skipped snapshot's hash is by definition the preceding
one's.

Dropping a day is not a loss of information. SCD-2 already means "the last observation
holds until the next one", which is exactly the right reading of a day we failed to
observe.

## --rekey

Recomputes every `identity_key` from the city's *current* config. This is the one
operation here that rewrites history rather than removing from it, and it only makes
sense together with the `[identity]` change it implements — `city-tune`'s `identity.md`
is where that decision belongs.

Used once, for muskoka: its coordinates jitter up to 1.36 m between republishes, which
crosses the 5 dp (~1.1 m) rounding in `normalize._identity` and minted a new key for ~43%
of the city on any republish, leaving 157,666 keys in a 66k-row city.

Watch the `collisions` count it reports. Two source rows collapsing onto one key means
the new basis is coarser than the old one; import keeps whichever it saw first, and since
row order is not preserved in a rebuild, the tool picks deterministically instead. A
handful is tolerable (muskoka accepted 279); a large number means the basis is wrong.

## Ops lesson, learned the hard way

**Disable the `kk-ontario-update` scheduled task before migrating or repairing stores.**
The noon run fired mid-migration on 2026-08-08, imported against un-migrated stores under
the new hashing rules, and had to be killed and rolled back from a DB backup before it
committed.
