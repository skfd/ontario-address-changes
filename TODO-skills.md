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
  - [ ] elgin / peel-region / waterloo — baseline only, blocked on the frozen vault for
    anything needing a diff. But `audit.py --coords` (added 2026-08-08) needs none, and
    it has already read their coordinate duplicates off the single snapshot:
    - **elgin** `x`/`y` — stale *and* mixed-CRS: 18,716 rows in degrees and 2,720 in
      UTM 17N metres in the same column, 9,551 of 21,436 rows over 11 m from the
      geometry, p99 585 m. The worst duplicate found in any city so far. Phantom-only
      by the identity rule, so it can only manufacture updates — but a lot of them.
    - **peel-region** `LATITUDE`/`LONGITUDE` — stale, p99 16.0 m, 5,871 of 503,920 rows
      over 11 m. Worst combination available: a stale copy on a real-`key_field` city,
      so the re-sync will *mask* real moves rather than only invent them.
    - **waterloo** `LATITUDE`/`LONGITUDE` — faithful, max 0.69 m over 55,541 rows, the
      cleanest of the nine. Ignore it, but there is no hurry.

    Three for three on the identity rule's phantom/masking prediction is untested here —
    that needs a diff. The faithful/stale call does not.
  - [ ] the other 31 — no coordinate duplicate to find (see the sweep note below),
    but never given a full pass on identity, field map or classes.

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

  Written into the skill 2026-08-08 (`references/ignore-fields.md` "Which noise pattern
  to expect", cross-linked from `identity.md`), along with the correction it forces: the
  reference used to say a category stuck at 0 always means echoes, which is wrong for
  Location Adjustments on a synth + `use_geometry` city. `classes.md` picked up the
  full-only rule at the same time.

  The measurement behind faithful-vs-stale is now `audit.py --coords` (2026-08-08)
  instead of a one-off script per city. It reproduces all six recorded verdicts. Three
  things it got wrong before it did, all worth keeping in mind if it is ever retuned:

  - Judging on the **max** deviation called guelph (315 wild rows of 53,889) and
    hastings (13 of 30,815) stale when neither is. The p99 is what tracks a *bulk* of
    drifted rows, which is what makes a re-sync a mass event.
  - Measuring only the **latest snapshot** called renfrew faithful, because the county
    had re-synced it on 06-29. It samples five snapshots across history for that reason.
  - Matching prop names **exactly** missed two cities outright, and pairing the
    survivors **by position** then matched an easting against a latitude. Names are now
    tokenised (whole-name cover, so CITY and PARITY are not northings) and paired within
    a family — geographic with geographic, projected with projected.

  **The coordinate-duplicate sweep is now complete**, which the narrower regex screen it
  started as could not have told us: 11 of the 42 cities publish a duplicate pair at all,
  and every one has been measured. Stale: elgin, peel-region, quinte-west, renfrew.
  Faithful: burlington, dufferin, guelph, hastings, kawartha-lakes, kitchener, waterloo.
  The remaining 31 publish no coordinate column, so there is nothing there to find — the
  rest of their `city-tune` pass is still open, just not this part of it.

  Two cities came in on the fixed detector and had never been looked at:
  - **dufferin** — two faithful pairs, `LONGITUDEX`/`LATITUDEY` (deviation exactly 0.00 m:
    stored at the same 5 dp as the geometry) and `EASTINGX`/`NORTHINGY` (UTM 17N, max
    6.83 m, tightly clustered). Ignore both; no hurry. Config is still completely bare —
    no `ignore_fields`, no `classes` — and it is one of the eight frozen cities.
  - **kawartha-lakes** — `Xlong`/`Ylat`, faithful, max 1.32 m at p99 over 44,204 rows,
    with 9 individually broken rows out of range.

- [x] Global fix for the ESRI id spellings `_VOLATILE_KEYS` missed, and for padded prop
  values. Both coded 2026-08-09 as `normalize.is_volatile()` and a `.strip()` in
  `_clean_props`; migration not yet run. Measured blast radius, the per-city workarounds
  they replace, and a pending whole-store re-hash in five cities that the measurement
  turned up are all in `TODO.md` §5.
- [ ] `audit.py --identity` reports flap history-wide, so damage predating a config fix
  still shows (muskoka: 16.75%). Add a per-snapshot breakdown, or teach the reference to
  always cross-check the per-diff summary for when the spikes stopped.

## 2. data-integrity — ends in a trust decision about a snapshot or a run

Shipped 2026-08-08 (`.claude/skills/data-integrity/`). Triggered by "the daily run did
something weird", takes logs and HTTP rather than the field config, and never edits a
dataset. `health.py` has four sections — `stale`, `blocks`, `runs` (local, the default
set) and `--drift` (the one network pass) — with a reference per decision.

First run found two things nobody was looking for:

- **The frozen list is bigger than eight.** Ranking every city against its own gap
  history (p90, 3-day floor) flags 18 of 42, and the eight in `TODO.md` §4 are only the
  worst. Behind them: niagara-falls 36d, durham 25d, thunder-bay / london / chatham-kent
  15d, bruce / cornwall 10d. Two distinct shapes — a clean cliff (niagara-falls: daily,
  then nothing, after a max gap of 5) and a *degrading cadence* (cornwall 1→6→7→8,
  london 1→11→15). The degrading kind raises its own p90 as it decays, so it ranks lower
  than a cliff of the same age; rank is not severity.
- **kingston's layer is erroring.** `--drift` gets "Error invoking service" from the
  layer json, and `update.log` carries three `ERROR (kingston)` lines from the same run.
  Neither on its own would have been convincing.

`--drift` also turned up city-tune work, all of it new fields the sources added: a fresh
coordinate duplicate in **kitchener** (`LATITUDE, LONGITUDE`, on top of the `X_COORD,
Y_COORD` already ignored) and in **windsor** (`X, Y`), a `SUITE` column in **oakville**
sitting alongside the `UNIT` it already maps (so: a second unit column, echo or
otherwise), and single new props in burlington, greater-sudbury, hamilton,
niagara-falls, sdg and kawartha-lakes. Nothing was DROPPED anywhere, which is the one
that would have been urgent.

- [x] **Corrupt-pull triage.** Decide whether a mass event is a real upstream change or
  a degraded pull. Signatures already seen: a row count that is an exact multiple of 2000
  (address-vault's ArcGIS paging loop ending on a transient blank page — kitchener
  102,000 of 131,912, huron 20,000 of 38,300), an attribute-stripped pull where every
  field but the identity key is null (muskoka 2026-06-28), and plain row-count cliffs.
  Narrower than it was since 2026-08-08: all three signatures are now refused at
  fetch/import time (TODO.md §5), so the skill's job is the leftovers — a degraded
  pull small enough to pass the thresholds, and deciding whether a city failing on
  the guard every day is damage or a real source change that needs a config edit.
- [x] **Repair.** `tools/repair_bad_snapshots.py` is now `--city <slug> --drop <filename>
  [--rekey] [--dry-run]` instead of a hardcoded three-city dict; the SCD-2 rebuild and
  content-hash recompute are untouched. The 2026-08-08 one-shot it started as is kept in
  the docstring, since it is the only worked example of `--rekey`.
- [x] **Run-log triage.** `health.py --runs`, with `references/runs.md` carrying which
  outcomes are deliberate (`offline`, `metered`, retries, laptop-off days, ottawa's F5)
  and which are real.
- [x] **Source drift.** `health.py --drift`. Subtracts volatile ids, edit-metadata and
  `ignore_fields` so what it lists is genuinely unstored.

Open on it:

- [ ] `--drift` cannot probe `access = "static"` cities (toronto, waterloo) — no layer
  metadata to ask. Their drift needs a file in `data/<slug>/` inspected instead.
- [ ] The `stale` flag is deliberately sensitive and has no way to tell "we stopped
  recording" from "the source stopped publishing". Confirming that is vault-side.
