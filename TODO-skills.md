# Skill backlog — ontario-address-changes

Last updated: 2026-08-08. Claude Code skills for `.claude/skills/`, drawn from work that
has already recurred across the 42 tracked cities. Unlike `TODO.md` (per-city decisions
for the human operator), these are tooling tasks: each turns a procedure we have run by
hand into something repeatable.

Two tracks, split by what the work *ends in* — a config edit, or a trust decision about
an observation. An earlier draft of this file split the same work eight ways; that was
wrong, because four of those skills would have loaded the same city DB, walked the same
history, and ended in the same file. Keep the tracks broad and use `references/` for the
per-decision detail, so only what is needed gets read.

## 1. city-tune — ends in a `datasets/<slug>.toml` edit

Shipped 2026-08-08 (`.claude/skills/city-tune/`). Covers identity key, field map,
change classes, ignore/keep fields, and onboarding, over one `audit.py` pass.

- [x] `ignore_fields` / `keep_fields` — built out of the Guelph review.
- [x] identity health — collisions, flap rate, keys-vs-rows.
- [x] field map — coverage of mapped slots, candidates for unmapped ones.
- [x] class candidates — low-cardinality props cross-referenced with solo churn.
- [x] onboarding path — source resolution, licence/OSM compat, `skipped.toml`.

Remaining work on it:

- [ ] Work `TODO.md` §1 with it: waterloo's unparsed `CIVIC_ADDR`, lennox-addington's
  `ADD_LABEL`, the five cities with no full-address field, the unit-field verification
  pass starting with toronto. The skill exists; the decisions are still open.
- [ ] Give every city one `city-tune` pass. This started narrower — a screen over all 42
  (regex on prop names in the latest snapshot vs `ignore_fields`) found 8 carrying
  unignored coordinate duplicates, none of which had ever recorded a Location Adjustment.
  Six audits in, the duplicate has never been the city's largest noise source; it was a
  tripwire that got the city looked at, and the real find was elsewhere every time
  (hastings' `RnoTXT2`, kitchener's `ROLL_REFERENCE`, renfrew's `report._category` bug,
  which was mislabelling four *other* cities). So the remaining 34 are worth a pass too,
  not only the ones the regex flagged. A city with just a baseline report cannot be
  swept — there is no diff to tally — which is what currently blocks elgin, peel-region
  and waterloo, behind the frozen-vault bug in `TODO.md` §4 rather than behind anyone's
  attention: flag the config, don't claim a bug.

  - [x] **guelph** (2026-08-08) — masking pattern: real coordinate moves demoted to
    generic updates because `LAT/LONG/UTM_X/UTM_Y` rode along. 520 moves on one day
    alone. Location Adjustments fires on 7 of 24 reports now.
  - [x] **hastings** (2026-08-08) — phantom pattern: the duplicates moved on 4 rows
    whose *rounded* coordinates never changed (source jitter below 5 dp), so they
    manufactured updates rather than demoting real ones. Location Adjustments stays 0
    and that is correct. The real find there was `RnoTXT2` (alias "ARN", the assessment
    roll number) backfilled from UNK: 158 of 159 solo changes.
  - [x] **quinte-west** (2026-08-08) — phantom pattern, and *only* ever phantom: see the
    identity rule below. Ignored `lat, long` (a stale full-precision copy — 1,720 of
    20,290 rows already differ from the geometry by >10 m, one carries a projected
    northing instead of a latitude) and `label` (number + unit suffix). Both pre-emptive:
    the city's whole history holds exactly one modification, a `label` correction of
    "13" to "3" on a row already numbered 3, which the change retroactively removed.
  - [x] **burlington** (2026-08-08) — phantom pattern, and only ever phantom (same
    identity rule). Unlike quinte-west the duplicates are *faithful*: worst deviation
    from the geometry is 1.35e-5 over 60,326 rows, so they are the hastings shape
    exactly — an 8 dp echo of a geometry compared at 5 dp, movable only by jitter below
    the resolution. Ignored `LATITUDE, LONGITUDE` plus `PROPERTYRSN` (property-system
    surrogate, near-monotonic with OBJECTID, `keep_fields` so consumers keep the link).
    The audit's larger find was again elsewhere: both of the city's two real
    modifications are classifiable, so `PROPCODE`/`PROPDESC` joined `status` (Tenant →
    Secondary Building now groups as a Status Change instead of a generic update) and
    `NAME` became `place_name` ahead of a rename.
  - [x] **kitchener** (2026-08-08) — masking pattern, as the identity rule predicts for a
    real `key_field`. `X_COORD, Y_COORD` are the geometry reprojected into the layer's own
    UTM 17N and stored as full-precision metres — faithful (worst deviation 1.35e-5 deg
    over 132,060 rows, the burlington shape) but finer than the 5 dp everything else is
    compared at, so they rode along with 179 real moves and invented 5. Location
    Adjustments went 0 → 192. The larger find was again elsewhere: `ROLL_REFERENCE` (MPAC
    roll, 610 null→roll backfills + 188 re-rolls) and the `ROADSEGMENTID`/`PARCELID` join
    keys, all three `keep_fields`. 2026-08-03 generic Updated 1410 → 56, Status 9 → 103.
  - [x] **renfrew** (2026-08-08) — phantom pattern, and the *stale* variety, caught
    mid-repair: on 2026-06-15 the county's `Latitude, Longitude` sat more than 1e-4 deg
    from the geometry on 720 rows (worst 6.7e-3, ~530 m), and on 2026-06-29 the county
    recomputed them — 1,484 of the 1,498 edited rows moved closer to the geometry, none
    further, leaving the layer within 2e-5. The geometry never moved, so all 1,547
    updates that day were the copy catching up. Also ignored `Full_Address` (the mapped
    column behind `full`, churning on trailing spaces the canonical strips, 1,060 rows),
    `RollNumber`/`NGUID`/`Comment` (`keep_fields`; between them they demoted 47 status
    flips). 06-29 generic Updated 1573 → 4, 06-13 3062 → 1974 — what is left there is the
    real `UnitPreTyp` vocabulary sweep, which already collapses to one bulk line.
    Renfrew also turned up a `report._category` bug: a change to `full` *alone* counted as
    Renumbered, which mislabelled the county's 1,104-row highway restyling ("17883 Highway
    60" → "17883 60 Highway", `Add_Number` untouched). Now read against the field map —
    full-only is a renumber only where no `number` is mapped (waterloo), a rename where no
    `street` is (lennox-addington), and otherwise a generic update. Four other cities were
    carrying the same mislabel: brantford (12 reports), frontenac (6), barrie (5),
    thunder-bay (1), every one of them a restyle, a backfill or a spelling fix.
  - [ ] elgin / peel-region / waterloo — baseline only, blocked on the frozen vault;
    revisit once each has a diff.
  - [ ] the other 34 — no coordinate duplicate flagged, never given a full pass.

  **Which pattern to expect is predictable from `[identity]`** (found 2026-08-08, and it
  retro-explains guelph and hastings). Synthesized identity includes the 5 dp geometry
  when `use_geometry` (`normalize.py:161`), so a real move past ~1.1 m mints a new key
  and reports as retired + added — never a modification. `location` is only ever assigned
  to a *modified* row (`report._category`), so for those cities Location Adjustments is
  structurally unreachable and its 0 is correct, not a config bug. Coordinate duplicates
  there can only manufacture updates.
  - synth + geometry, phantom-only: **elgin** (+ hastings, quinte-west, burlington,
    renfrew, all confirmed)
  - real `key_field`, masking possible: **peel-region** (`ROPADRID`), **waterloo**
    (`ADDRESS_ID`) (+ guelph, kitchener, both confirmed)

  Six for six so far. Within the phantom half there are two mechanisms, and only the
  churn tally separates them: a *faithful* echo at finer precision than the 5 dp compare
  (hastings, burlington, kitchener's projected pair) moves only on jitter, while a
  *stale* copy (quinte-west, renfrew) drifts freely and fires whenever the publisher
  recomputes it. The stale kind is the one worth ignoring pre-emptively — renfrew's had
  wandered 530 m before the county re-synced it.

  This narrows what to look for but does not replace the churn tally (`audit.py --tags`),
  which is still what shows whether the duplicate has actually moved.

- [ ] Consider a global fix for ESRI id spellings `_VOLATILE_KEYS` misses. Hastings
  publishes `OBJECTID_12` (its alias is literally "OBJECTID_1"), which was being
  compared until 2026-08-08 and is now ignored per-city. A pattern match
  (`^objectid(_\d+)?$`, `^fid(_\d+)?$`) in `normalize.py` would cover every city at
  once — but it changes hashing for all 42 stores, so it needs the
  `tools/backfill_props_hash.py` treatment, not a casual edit.
- [ ] Consider a global fix for padded prop values. `_clean` strips the canonical fields
  but `_clean_props` only drops values that are *entirely* whitespace, so a source that
  re-pads a real value churns the prop while the canonical sits still — renfrew's
  `Full_Address` did it on 1,060 rows ("2502 Calabogie Road " → "2502 Calabogie Road").
  Same family as the whitespace-only fix in `TODO.md` §5 and the same cost: stripping
  prop strings re-hashes all 42 stores, so it needs `tools/backfill_props_hash.py`.
- [ ] `audit.py --identity` reports flap history-wide, so damage predating a config fix
  still shows (muskoka: 16.75%). Add a per-snapshot breakdown, or teach the reference to
  always cross-check the per-diff summary for when the spikes stopped.

## 2. data-integrity — ends in a trust decision about a snapshot or a run

Not built yet. Triggered by "the daily run did something weird", takes logs and HTTP
rather than the field config, and never edits a dataset.

- [ ] **Corrupt-pull triage.** Decide whether a mass event is a real upstream change or
  a degraded pull. Signatures already seen: a row count that is an exact multiple of 2000
  (address-vault's ArcGIS paging loop ending on a transient blank page — kitchener
  102,000 of 131,912, huron 20,000 of 38,300), an attribute-stripped pull where every
  field but the identity key is null (muskoka 2026-06-28), and plain row-count cliffs.
  Narrower than it was since 2026-08-08: all three signatures are now refused at
  fetch/import time (TODO.md §5), so the skill's job is the leftovers — a degraded
  pull small enough to pass the thresholds, and deciding whether a city failing on
  the guard every day is damage or a real source change that needs a config edit.
- [ ] **Repair.** Generalize `tools/repair_bad_snapshots.py` from a one-shot script into
  an on-demand tool: drop the bad snapshot, rebuild the store's SCD-2 history, regenerate.
- [ ] **Run-log triage.** Read `logs/runs.csv` and the daily log; separate genuine
  failures from expected skips (`offline`, `metered`, F5 connection rate-limits on
  ottawa) and report only what needs a human.
- [ ] **Source drift.** Periodic health check across all 42 `data_url`s: URL rot, schema
  drift (fields added or dropped since the last audit), licence text changes. Feeds
  city-tune rather than duplicating it.
