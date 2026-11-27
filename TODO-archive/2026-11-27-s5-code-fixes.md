# TODO.md §5: closed code fixes, and detail behind open ones

Moved verbatim out of [TODO.md](../TODO.md) on 2026-11-27; the text is as it stood at
TODO.md's last update, 2026-10-31. History and finished work, not required reading.
Open items stay in TODO.md; where one was shortened there, its full text is here.

## 5. Hand to coding agent when convenient

- [x] **Cache the per-snapshot diffs (found 2026-10-16).** The daily render was ~33 min
  of CPU, almost none of it HTML: `_chronological_diffs` recomputed every consecutive
  `diff.compute_diff` pair for every city, every day, and each one loaded *both whole
  active sets* (~6 s a pair on toronto, 838 s for its 122 pairs). **Done 2026-10-19,
  without a cache.** A row active at both snapshots is one span and can never be in
  the diff, so `compute_diff` now reads only the spans that end or start between the
  two (`diff._boundary`): same answer, cost proportional to the change. Nothing is
  stored, so there is nothing to invalidate: config edits, backfills, remaps and
  re-baselines are seen on the next render as before. Verified against the old method
  on every pair in all 77 stores plus a first-to-last and a month-long span each (zero
  mismatches; diffing 2,836 s -> 31.5 s), and `tests/test_diff_boundary.py` keeps the
  old method as its oracle. Full `report --all`: **1 min 49 s**, pages byte-identical.
  One trap on the way, kept in the test: a plain index on `min_snapshot_id` won the
  query plan for every "active at S" query (`min <= S AND max >= S`), whose min side
  matches all of history, which stalled a profiled render for over an hour and
  re-sampled three hulls. The start index is on the expression `min_snapshot_id + 0`
  so only `_boundary` can use it. **Measured on the 10-20 noon run:** `RENDER` -> `END`
  12:13:42 -> 12:15:34, 1 min 52 s (10-18: 12:16 -> 12:49), and the whole run 15.5 min.
- [x] **Render cities in parallel (found 2026-10-16).** Dropped 2026-10-19: with the diff
  fix the whole render is under two minutes on one core, so a process pool and the
  two shared writers it would have to handle (`flags.record`, the ledger reload) buy
  nothing worth the risk. Revisit only if the render climbs back past ~10 min.
- [ ] **Audit what the importer's dedupe drops, per city (found 2026-10-20).** `db._records`
  keeps the first row per identity_key and drops the rest ("note: N duplicate identity_key
  rows dropped"). That is harmless only when the dropped rows are identical to the kept
  one: hastings' old key hid 444 distinct suffix siblings behind that line for four
  months (fixed by rebuild, see section 1). Measured on the latest pulls: hastings' 6
  remaining drops are byte-identical; **windsor drops 14,490 rows a day (12,127 keys) and
  none is identical** - the PropertyParcels layer carries several parcel records per
  address point, differing in `propertyrsn`, `Frontage`, `Depth`, `AmandaArea`, `Ward`.
  Which parcel's attributes are stored then depends on file order, so a reordered export
  reads as modifications that are not real. Decide per city: ignore the parcel attributes
  (they are not address data), or key on something that separates the records. Sweep the
  other 76 stores' drop counts first.
  **Swept 2026-10-23, all 78 latest vault pulls** (the log can't answer it: `_records` runs
  only on a fresh import, so 63 cities that recorded "no changes" printed no line). 42 cities
  drop nothing; most of the rest drop rows that differ only in ignored/volatile fields.
  Real problems, by stake (scripts + per-city JSON in `%TEMP%\dedupe-audit\`):
  - **sdg: 2,019 distinct addresses (~6%) never stored.** **Done 2026-10-24:** pure synth, history
    rebuilt (32,072 -> 34,130 rows; the June no-pull gap dated by evidence,
    `tools/gap-dates/sdg.toml`). Was: `Unique_ID` is a bare township
    prefix (`ND_`, `SS_`, ...) on the 2,012 rows with no SDGCivicID; 13 keys hold them all.
    The TOML's "populated on all but 1 row" is wrong. Fix: treat a prefix-only key as blank
    (falls back to synth, 14 real upstream dups left) or go pure synth (0 collisions); either
    way `rebuild_from_pulls.py` then `recanonicalize.py --verify` (hastings precedent).
  - **windsor: no address hidden, parcel attributes by file order.** 14,490 rows/12,127 keys
    differ only in `propertyrsn`/`Frontage`/`Depth`/`AmandaArea`, and on 4,704 also `Ward`.
    Ignoring all five (ward is vault-only by the overlay policy) leaves 0; the
    `[classes] boundary = ["Ward"]` line then goes dead and should go. Hashes only:
    `tools/backfill_props_hash.py --reapply-ignore --city windsor`. **Done 2026-10-23**, verify 0/0/0.
  - **brampton: 1,206 addresses stored at a SECONDARY/FRONTDOOR point.** `ADDRESS_ID` repeats
    across point types; no config fix (coords are hashed, no row filter). Stable so far.
  - **greater-sudbury: fake events now.** Key 105696 alternates between "1545 Redfern Street"
    and "119 Vaillancourt Crescent" across snapshots; duplicate ADDRESSIDs upstream.
  - **muskoka: 46 suffix siblings hidden** (`StreetQual` not in the key) and coordinates
    flipping on 114 of 199 keys. `synth_props = ["PropertyNum", "StreetQual"]` recovers 45;
    re-key, so rebuild + recanonicalize.
  - **ajax: 32 hidden** behind 24 FACILITYIDs; pure synth gives 0 collisions; baseline-only,
    so re-baseline. **Done 2026-10-23** by replaying its pulls: 38,400 -> 38,432.
  - **durham: 11 hidden** (MXADDRESSCODE shared by unit/suffix siblings; REGION_ID unique,
    stability unmeasured) - report upstream; a 253k re-key isn't worth 11 rows.
  - Small (frontenac 3, renfrew 1, lennox-addington 23, cornwall, caledon, grey, haliburton,
    hamilton, pickering, blue-mountains, waterloo-region, huron, haldimand): no change.
  - Cross-cutting: a **deterministic tie-break** in `db._records` (PRIMARY first, then lowest
    payload_hash) would stop the sudbury and muskoka flips and make brampton keep PRIMARY.
    No re-key; one round of modifications on affected keys unless backfilled.
  **Tie-break done 2026-10-24.** `db.tiebreak_rank`: an `[identity] prefer = {field, value}`
  row first (brampton ADDRESS_TYPE = PRIMARY), then content order (number, street, unit,
  full, lon, lat, props) - content rather than payload_hash because hash order still swapped
  muskoka's kept point 70 times over its pulls, content order 0. History rewritten with
  `rebuild_from_pulls.py --tiebreak` for the 14 cities where the kept row ever differed
  (brampton: 1,348 keys now keep their PRIMARY point);
  greater-sudbury's six flapping keys are now one version each (105696 was 45). muskoka got
  StreetQual in its key the same night (45 suffix siblings back). Each verified 0/0/0.
  Four cities need nothing new (hamilton, haliburton, huron, pickering: the rule picks the
  stored row everywhere). lambton has an older, separate problem: its store does not replay
  from its June pull at all (56,897 pairs differ at snapshot 1) - not looked into.
- [x] **lambton replay: cause found 2026-10-30, fix is a design call.** **Option 1 built 2026-10-31:**
  `rebuild_from_pulls.py --map-rev REV --map-until FILENAME` (repeatable, paired) replays snapshots
  up to that pull filename under the TOML at REV; verified on lambton (`--map-rev a3370d580
  --map-until lambton-2026-08-24.geojson --tiebreak`, 11 restic dumps, 9 min): 0/0/0 at all 51
  snapshots, 113,918 rows both sides; the one flip is snapshot 16 change -> skip (hash artifact).
  Inside an era the era TOML is also the old rule, so `--old-rev` reaches post-era snapshots only.
  Six tests in `tests/test_rebuild_eras.py`. Output store was at `data/_rebuild_lambton/`, removed. `rebuild_from_pulls.py`
  hands today's `datasets/lambton.toml` to `normalize.canonical` for every raw day, but the
  publisher renamed every column on 2026-09-15 (`STNUM/STNAME/ADDRESS` -> `Add_Number/St_Name/
  full_add`, commit e07858647). On the June pulls (`data/lambton/lambton-2026-06-10.geojson`,
  06-24 byte-identical) none of today's names exist, so number/street/full are null on all
  56,903 features and the synth key degrades to geometry only: 56,897 missing + 56,897 extra,
  zero keys in common. Replayed under the pre-switch map (`a3370d580`) the same pull gives
  0/0 against snapshot 1, and snapshot 16 (06-25, from the vault) also 0/0; snapshot 50
  replays 0/0 under today's map. So snapshots 1-20 fail, 21+ are fine. **The live store is
  right** (56,158 keys survive the switch, 739 gone, 824 new, as the TOML comment and the
  six 09-15 flags say); its 6 June duplicate keys are identical-hash pairs, so the 10-24
  tie-break picks the stored row and lambton needs no rebuild today. The item only blocks
  a future one - and the same shape is coming for wps (NENA re-point, kept history next
  time) and elgin 2027. Dead ends: `--stored-day` cannot bracket snapshot 1 (no raw pull
  before it) and would re-inject canonical columns under today's names; translating June
  pulls into the new schema cannot reproduce any June payload_hash (`full_add` embeds
  Inc_Muni, props roster differs) and would erase the filed 09-15 technical event.
  Options, pick one when a lambton rebuild is actually needed:
  1. **Era-aware replay in the tool** (recommended): `--map-rev REV --map-until FILENAME`
     (repeatable); for snapshots up to that filename build the dataset via
     `recanonicalize.old_dataset` (already imported there) and pass the swapped fields /
     synth / ignore / classes per snapshot. Key basis is the same in both eras, so no
     re-key, no history rewrite, ~30 lines. Needs cold vault pulls for 06-25 and every
     post-switch non-skipped day (`--dump-dir`), and `--tiebreak` (or a widened excuse)
     because snapshot 16 replays as a skip - its stored "change" was a hashing artifact.
  2. **Copy snapshots/addresses <= 20 verbatim, replay from 21.** Fewest pulls, no re-key;
     but a future rule that must reach June rows (number_from_full, a synth change) can't be
     replayed into copied rows - they'd need `recanonicalize.py` separately.
  3. **Era-aware TOML** (`[fields]` + `[fields.until."2026-09-14"]`, consumed by registry ->
     normalize with a date). Fixes replay, `recanonicalize --verify` and the wps/elgin cases
     in one place, but touches the daily importer and every tool across 77 datasets. Only
     if publisher renames become routine.
- [x] **Stream the GeoJSON import (found 2026-10-16).** `fetch.load_features` does one
  `json.load` of the whole file — up to ~590 MB for york/peel/toronto — and
  `db.import_snapshot` then iterates `features` once. Switch to `ijson.items(f,
  "features.item")` (the vault already depends on ijson) and pass the iterator through;
  `import_snapshot` only needs a count at the end, not `len(features)` up front. Halves
  peak memory per worker, so `--jobs` can go above 6 without the big three colliding,
  and removes the multi-second parse stall on changed days. No hash change.
  **Done 2026-10-23.** `load_features` is a generator over `ijson.items(..., use_float=True)`
  (falls back to `json.load` on what yajl refuses: NaN, >int64, 1e400). On the real 10-23
  pulls: toronto 2,128 -> 659 MB peak for a full import, york 1,599 -> 599 MB, contents and
  `_content_hash` identical; 1.5-3 s *slower* per city (ijson parses slower than json.load),
  so the stall moved into the import rather than vanishing.
- [x] **"None" / "<Null>" in the canonical fields (found 2026-10-16).** `_NULL_LITERALS`
  drops them from props only; `_clean` (the canonical number/street/unit/full) honours
  just "N/A". Stored canonical values today: windsor number + full "None" on 696 rows,
  norfolk unit "<Null>" 12, durham unit 5, leeds-grenville unit 2. Folding them into
  `_CANONICAL_NULL_LITERALS` re-keys those rows (unit/number are in the synth basis), so
  it is a full-history remap per store (`tools/remap_canonical_from_prop.py` shape), not
  a filter edit. Small, but each is a latent mass event the day the publisher fixes its
  export.
  **Done 2026-10-20.** `_CANONICAL_NULL_LITERALS` is now `_NULL_LITERALS`, and the four
  stores were rewritten first by the new `tools/recanonicalize.py`, which may re-key:
  it proves each moved row's stored key recomputes from the stored row, refuses a new
  key that would fold two chains together, and refuses touching same-hash spans it
  would create. windsor 696 rows re-keyed, norfolk 12 re-keyed, durham 5 and
  leeds-grenville 2 (key_field cities, unit + hash only). Each verified against its
  latest vault pull: 0 added/removed/modified, content_hash equal; re-run rewrites 0.
  Backups in `C:\Users\kk\ontario-db-backup-2026-10-20-recanonicalize\`. Re-render moved the two baseline pages only (windsor 06-11,
  waterloo 10-16); addressless rows now read "(no address)" instead of their `syn:`
  hash (12 more baseline pages, label only).
- [x] **Touching same-hash spans in 20 stores (found 2026-10-20).** A key holding two
  spans with no non-skipped snapshot between them and the same `payload_hash` is a span
  the importer would have extended. The `recanonicalize.py` dry run over all 77 stores
  found them in 20 (keys / pairs): guelph 53,849 / 270,430, chatham-kent 56,147,
  huron 17,344, renfrew 4,834 / 5,591, brampton 2,742 / 4,687, kingston 1,091 / 1,094,
  kitchener 1,067, durham 957, simcoe 402 / 781, york 261, toronto 191 / 346, hastings
  163, thunder-bay 129, barrie 7, cornwall 2, milton 2, and one each in bruce, hamilton,
  kawartha-lakes, quinte-west (one figure = one pair per key). Most likely left by the
  hash backfills and `--reapply-ignore` passes, which rewrote each version's hash in place
  but never merged versions that became equal. Harmless to the diff (equal hash = no
  modification), but each is an extra row and a false "version" in history. Fix: a
  merge pass (extend the first span's max, delete the second), dry-run and backup
  first, verify `report --all` pages unchanged. Confirm the backfill cause before
  fixing, in case an importer path still splits spans.
  **Done 2026-10-20.** Cause confirmed: the importer cannot leave such a pair (it extends
  on an equal hash and inserts only the keys it did not extend); every boundary sits on
  a past re-hash, e.g. guelph's five whole-city ones (07-24, 07-29, 08-04, 08-09, 08-30)
  and chatham-kent 09-30. New `db.merge_touching_spans`, run over the 20 stores by
  `tools/merge_touching_spans.py`: 359,012 rows folded, re-run 0. The active set at
  every live snapshot of all 20 stores fingerprinted identical before/after, and
  `report --all` left every report page byte-identical; only the landing-map hulls
  moved (even-stride sample over row order). Backups in
  `C:\Users\kk\ontario-db-backup-2026-10-20-mergespans\`. The four hash-rewriting
  tools (backfill_props_hash, remap_canonical_from_prop, derive_street_from_full,
  recanonicalize) now call the merge themselves, so no new pairs are left behind.

- [x] **Extend `EDIT_METADATA_FIELDS` with the `creationdate` / `modificationdate`
  spellings.** Found 2026-08-20 during the west-parry-sound onboarding: the source
  publishes esri editor-tracking as `CreationDate`/`ModificationDate`, which the
  global set misses (it has `created_date`/`last_edited_date` family only). WPS
  pre-ignored them per-city before its first import, so nothing is stored anywhere
  under those spellings today — meaning the global add is currently free (no
  backfill needed). **DONE 2026-08-21**, and it was still free: re-checked all 53
  stores immediately before the edit and no row anywhere carries a prop under those
  two spellings (nor `Creator`/`Editor`, esri's matching newer name columns — those
  are deliberately *not* added, since nothing publishes them and "Editor" is a
  plausible real column name elsewhere).
- [x] **Drop literal `"None"` string values in `_clean_props`, the way
  whitespace-only values are dropped.** Found 2026-08-20 during the windsor
  spot-check: sources whose ETL leaks Python's `str(None)` publish the text
  "None" where they mean null (verified against windsor's raw geojson —
  `"Ward": "None"` — so it is their export, not our importer). Measured across
  all 42 stores' active rows: **toronto 525,469 rows** (essentially the whole
  city: `ADDRESS_STATUS`, `HI_NUM_SUF`, `LO_NUM_SUF`, `PLACE_NAME`,
  `PLACE_NAME_ALL`, `LINEAR_NAME_DESC`), **windsor 5,572** (`Ward`, plus 696
  rows whose *canonical* `number`/`full` are "None" — those same 696 unaddressed
  parcels, so cleaning also fixes their display and corrects the appendix's
  windsor number coverage from 100% to 99.4%), **milton 1**. Stable today, so
  no churn — the exposure is the kitchener-empty-slot shape: the day a publisher
  fixes their export to emit real nulls, every affected row re-hashes at once
  (toronto = a 525k-row store event). Same treatment as the earlier normalize
  fixes: code change + `backfill_props_hash.py` in one batch, backup first,
  scheduled task idle. Decide the value set consciously ("None" exact-match
  only, or also "NULL"/"<Null>"/"N/A" — the latter were not measured).

  **DONE 2026-08-21.** The value set was measured first, across all 53 stores and
  all history rather than active rows only, and the answer narrowed the fix:
  `_NULL_LITERALS = {"None", "<Null>"}`, exact case, nothing else. Only those two
  are machine artefacts — Python's `str(None)` and ArcGIS's rendering of an empty
  cell written out as text. The near misses were all real values and are kept:
  **"Unknown"/"UNKNOWN" 541,943 occurrences** (toronto `GENERAL_USE` on every row,
  kitchener `UNIT_TYPE` 2,395, west-parry-sound `CODE` 1,111 — a coded domain, not
  a null), `na`/`NA` 70, `?` 17, `-` 1, `NONE` 1. "NULL" and "N/A" turned out not
  to occur at all, so the question they posed was moot.

  Migration ran the same evening (scheduled task idle, next run ~15 h out; all 53
  stores backed up to `C:\Users\kk\ontario-db-backup-2026-08-21-nullliterals`,
  2.9 GB): **544,003 rows rewritten** — toronto 538,407, windsor 5,572, norfolk 12,
  muskoka 6, durham 5, leeds-grenville 1 (the last four are the `<Null>` holders,
  all in unit columns). Re-run reports 0, row count unchanged at 5,377,178, zero
  literal-null values left in any store, 41 tests green. Note the row counts are
  *all history*, not the active-row figures the 2026-08-20 measurement quoted
  (toronto 538,407 vs 525,469 active); milton's 1 is not in the list because its
  value was `LOT = "NONE"`, uppercase, which is kept.

- [x] **Follow-up out of the above: windsor's 696 canonical `"None"` values are
  still there, and clearing them needs an identity migration.** The props fix
  cannot reach them: `normalize.canonical` derives `number`/`full` from the *raw*
  feature via `_clean`, not from the cleaned props blob, so those 696 unaddressed
  parcels still display number/full = "None" (`street_address`/`Address` are the
  mapped columns and both carry the literal). Stable, not churning — `_clean` will
  keep computing "None" on every import, so store and import agree and no event
  lands. Fixing it means teaching `_clean` the same `_NULL_LITERALS` rule, and
  that is the heavier surgery: windsor synthesizes identity from
  `number + street + unit` + geometry, so blanking `number` re-keys all 696 rows —
  `tools/remap_canonical_from_prop.py` explicitly refuses a canonical in the synth
  basis, and it would land as 696 retired + 696 added. Needs an identity-rewriting
  migration (rewrite `identity_key`, the canonical columns and `payload_hash`
  across all history in one pass, the way the lennox `ADD_LABEL` remap did for a
  non-identity column). Blast radius is windsor's 696 rows and nothing else: the
  only other canonical literals anywhere are `<Null>`/`?`/`Unknown`/`NA` in unit
  columns (muskoka 22, norfolk 12, durham 5, and one row each in amherstburg,
  kingston, leeds-grenville, lennox-addington) — 41 rows total, and all but the 18
  `<Null>` ones are values we deliberately keep. Worth doing when the appendix's
  windsor number coverage (100% -> 99.4%) is next being corrected, not before.
  Re-measured 2026-10-16, after the 10-12 re-point to the licensed `PropertyParcels`
  layer: still exactly 696 active rows with `number` = `full` = "None", so the new
  layer carries the same ETL leak and the item stands unchanged.

- [x] Add `objectid_1`/`globalid_1` variants to `_VOLATILE_KEYS` (normalize.py) —
  present in 7 cities' stored props; mass-modify risk if a provider reassigns them.
  Done 2026-08-08. `objectid_1` landed earlier in `363e435f`; `globalid_1` turned
  out to affect only lennox-addington, not 7 cities.
- [x] Make `_clean_props` drop whitespace-only values (frontenac stores 22k blank
  `" "` units). Done 2026-08-08. Real blast radius was 27 cities / 670,584 active
  rows, led by london 125k, windsor 117k, lambton 52k — frontenac was mid-pack.

Both were backfilled in place by `tools/backfill_props_hash.py` rather than
allowed to spike, so the reports lost the noise without gaining a phantom event
(guelph's latest went 25 modified → 1). The backfill rewrote 884,765 rows: it has
to cover closed historical spans too, not just the active ones, because every
report is rebuilt from the store on each run and a partial pass would invent a
change at the boundary. Only one already-published row was ever wrong (a hamilton
POSTAL_CODE `-> " "` on 2026-08-03); the bug was latent, not active, because a
source that pads a column pads it identically on every republish.

Two more of the same shape shipped 2026-08-09 (`normalize.py` + tests +
`backfill_props_hash.py`), and the migration **has been run**: 406,452 rows
rewritten, re-run reports 0 (idempotent), row count unchanged at 4,964,901, 28
tests green. Stores were backed up first to
`C:\Users\kk\ontario-db-backup-2026-08-09\` (42 files, 2.7 GB). The scheduled task
was not disabled this time and did not need to be — the migration ran at 13:45
against a run that had finished at 13:41, with the next one 22 hours out.

- [x] Pattern-match the ESRI id spellings `_VOLATILE_KEYS` misses (`^objectid(_\d+)?$`,
  `^fid(_\d+)?$`) — hastings' `OBJECTID_12` is ignored per-city today. Now
  `normalize.is_volatile()`, a predicate rather than a set, because `health.py --drift`
  filtered "new" fields by set membership and would otherwise have started reporting
  `OBJECTID_12` as a new field. Blast radius is hastings alone: 31,101 rows, the only
  numbered spelling stored anywhere in the 42 stores.
- [x] Strip whitespace *around* prop values, not just values that are entirely
  whitespace. Renfrew's `Full_Address` churned 1,060 rows on a trailing space the
  canonical `full` strips before comparing; it is ignored per-city today, which is a
  workaround for a gap every city shares. Blast radius is much wider than renfrew:
  199,944 rows over 36 cities, led by huron `StreetName` (93,995 — every row in the
  city), burlington `ADDRESS` (50,149), thunder-bay `ROOT` (34,590) and renfrew
  `ADDRRANGE` (11,908). Renfrew's 1,060 was the smallest instance of the pattern, not
  a typical one.

Together the two fixes rewrite **230,302 rows**. Two checks worth keeping: no
already-listed volatile key is still stored in any store (so generalizing the
backfill's `_reclean` from a hardcoded delta to `normalize._clean_props` costs
nothing retroactively), and zero whitespace-only values remain anywhere, which
confirms the 2026-08-08 backfill held completely.

### Found 2026-08-09 while measuring: five cities carry a pending whole-store re-hash

Not caused by the two fixes, and the reason the dry run reports 406,452 rows rather
than 230,302. Every per-city `ignore_fields`/`keep_fields` edit from the 2026-08-08
city-tune passes landed *after* `backfill_props_hash.py` ran that day, so those
cities' stored rows are still hashed on the pre-edit basis. On their next import
every active row re-hashes at once:

| city | active rows | reading as modified | cause |
|---|---:|---:|---|
| kitchener | 132,060 | 100% | `keep_fields`, plus stored `X_COORD`/`Y_COORD` |
| renfrew | 39,050 | 100% | `keep_fields`, plus `Full_Address`/`Latitude`/`Longitude` |
| burlington | 60,326 | 100% | `keep_fields`, plus `LATITUDE`/`LONGITUDE` |
| hastings | 30,857 | 100% | stored `OBJECTID_12`, `ADDRESS_NU`, `X`, `LAT`, ... |
| quinte-west | 20,290 | 100% | stored `long`/`lat`/`label` |

Toronto is the control: it has five `keep_fields` and sits at 0%, because those
predate the 08-08 migration and were absorbed by it.

Severity is store-level only. `diff.field_changes` applies `ignore_fields` at report
time too (`src/diff.py:83`), so a modification whose only changed props are ignored
is discarded and **nothing phantom reaches the site**. What does happen is the thing
the kitchener note in §1b calls not retroactively fixable: the whole city closes its
SCD-2 spans and opens fresh ones on one day for no reason.

The `keep_fields` half is **fixed** by the 2026-08-09 migration (the backfill
re-applies today's `keep_fields` to the hash basis — see its docstring). Measured
after it ran, the 37 other cities are at zero and these five are unchanged at 100%:

| city | active rows | will churn on next import |
|---|---:|---:|
| kitchener | 132,060 | 132,060 (`X_COORD`, `Y_COORD`) |
| burlington | 60,326 | 60,326 (`LATITUDE`, `LONGITUDE`) |
| renfrew | 39,050 | 39,050 (`Full_Address`, `Latitude`, `Longitude`) |
| hastings | 30,857 | 30,857 (`ADDRESS_NU`, `STREET_NAM`, `UNIQUE_ID`, `X`, `LAT`, `LONG`) |
| quinte-west | 20,290 | 20,290 (`long`, `lat`, `label`) |
| | | **282,583** |

Hastings' `OBJECTID_12` dropped off that list — the new global pattern covers it —
but its other five per-city ignores remained.

- [x] Taught `backfill_props_hash.py` an opt-in `--reapply-ignore` and ran it on the
  five, 2026-08-09: kitchener 133,514 rows, burlington 60,340, renfrew 45,700,
  hastings 31,101, quinte-west 20,299 (290,954 total, whole stores — every row
  carried the ignored props). Next-import churn across all 42 cities is now **0**,
  down from 282,583. The flag rewrites history and the values leave the store,
  recoverable only by re-importing the vault's snapshots, so it is opt-in and
  per-city rather than a default. Backup taken first at
  `C:\Users\kk\ontario-db-backup-2026-08-09-preignore\` (the five, post-global-
  migration, 190 MB), which is the targeted rollback point — the full 2.7 GB backup
  from the same day predates the global pass.
- [x] Made it not recur: `city-tune`'s SKILL.md now ends its edit checklist with the
  backfill step, because an `ignore_fields`/`keep_fields` edit is only half-applied
  until it runs.

**Verification that mattered most:** across 697,406 rewritten rows the latest diff of
every affected city is byte-identical to what today's run logged before the
migration — huron 43/32/0, thunder-bay 58/9/181, kitchener 156/8/354, renfrew
65/38/46, burlington 0/0/1, hastings 1/0/0, quinte-west 1/0/0, guelph 0/0/0. That is
the expected result rather than a lucky one: `diff.field_changes` was already
filtering these props at report time, so the reports never saw them. The store is now
consistent with what the reports have been showing all along. No regeneration or
republish was needed; tomorrow's run publishes normally.

**Ops lesson:** disable `kk-ontario-update` before migrating the stores. The noon
run fired mid-migration on 2026-08-08, imported against un-migrated stores with the
new hashing rules, and had to be killed and rolled back from a DB backup before it
committed.

### Done 2026-08-08: stop recording corrupt pulls

`tools/repair_bad_snapshots.py` deleted three snapshots taken from degraded
upstream responses (kitchener + huron 2026-07-28, muskoka 2026-06-28). All three
guards against a repeat are now in:

- [x] address-vault `fetch/arcgis.py`: a mid-stream empty page ended the paging
  loop, so a transient blank page was written as a complete layer. Now probes
  `returnCountOnly=true` alongside the layer metadata (same retry budget) and
  raises if the pull lands more than 1% below that count. Only the short side is
  checked — rows added while we page are normal. A layer that refuses the count
  query is pulled unchecked rather than failed.
- [x] Reject a pull where a mapped field that was ~100% populated returns ~0%
  populated (muskoka 2026-06-28, york 2026-07-31). In `db.import_snapshot`, ahead
  of any write, alongside a row-count floor.
- [x] `EDIT_METADATA_FIELDS` has `last_edited_user`/`created_user` but not
  `lasteditor` — renfrew's 846-row editor wipe counted as a modification. Added;
  no `backfill_props_hash.py` run was needed, because the source had already
  wiped the values, so no current row hashes it. Regenerating renfrew's reports
  dropped the phantom event (`compute_diff` discards a modification whose only
  changed field is filtered).

Thresholds were measured, not guessed, over the whole history: across 620
consecutive snapshot pairs the largest genuine row-count drop is 0.63% (sdg
2026-08-01), and across 2,288 field-pairs the largest genuine coverage loss is a
relative 1.5% (milton unit 2026-06-18). The degraded pulls lost 23–48% of their
rows or all of a field at once, so the guards sit an order of magnitude clear of
real movement. Rerun that measurement before loosening either constant.

A refusal is visible on the site, not just in the logs. `db.import_snapshot`
records it in the city's new `blocks` table and `run.py` renders a refused city
even though it failed, so the landing row gets a red "needs a look" badge with
the reason and the city page gets a banner. A pull that passes clears it by
itself, including an unchanged republish that takes the content-hash skip path.
This is the one state deliberately styled apart from an ordinary failure: a
fetch error fixes itself tomorrow, a refusal is waiting on you.

Deliberate asymmetry, decided 2026-08-08: only the *tracker's* guard produces
that banner. A pull refused by the vault (a truncation) fails before the tracker
imports anything, so the public site just goes stale with no explanation — and
that is fine. The vault's own `report.html` shows those under "Refused — needs a
look", which is the operator surface for them. Don't plumb vault refusals
through to the public site without a reason to revisit it.

Known gap, accepted: the tracker's 5% row floor cannot see a small truncation
(replayed against real renfrew data, a 2.6% short pull imports cleanly). The
vault's count probe is what catches those, so the gap is real only for static
sources, which report no count. There is deliberately no per-run override — a
source that genuinely shrinks past a threshold should stop the city and get a
human's attention, not a flag.
