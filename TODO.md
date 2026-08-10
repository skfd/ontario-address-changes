# Operator TODO — ontario-address-changes

Last updated: 2026-08-10. Tasks for the human operator. Field-coverage numbers come
from an audit of all 42 tracked cities (latest snapshot in each city DB).

## 1. Complete field selection for tracked cities

These cities are imported and tracking, but their field maps need a human decision:

- [ ] **waterloo** — no street-number field exists in the source (only the full
  `CIVIC_ADDR` string). Decide: have the number parsed out of `CIVIC_ADDR`, or
  accept full-address-only display.
- [ ] **lennox-addington** — no parsed street field in the source. Look at what
  `ADD_LABEL` contains (open a few rows in the report or the source layer); if it's
  a usable street label, select it; otherwise decide whether parsing from `ADDRESS`
  is worth it.
- [ ] **frontenac** — the source's `UnitNumber` column is 100% blank (22k rows, zero
  real values). Decide: unselect it, or keep it in case the county starts filling it.
- [ ] **hastings** — `number` maps to `House_No`, which drops the house suffix that
  `full` (`Full_Add`) keeps: "152 JAMIESON LN" as the number vs "152B JAMIESON LN" as
  the full address, on the 2,721 rows with a `House_Suf`. The source's `ADDRESS_NU`
  carries the combined form. Decide whether to remap `number` to `ADDRESS_NU` — but
  note the cost: hastings synthesizes identity from `["number", "street", "unit"]`, so
  remapping re-keys all 31k addresses and cannot be applied retroactively (one report
  showing the whole city retired and re-added). Found 2026-08-08 while ignoring
  `ADDRESS_NU` as a duplicate; it is a duplicate *of the wrong column*.
- [ ] No full-address field selected — reports fall back to "number street" (works,
  but omits units). Check each source layer for a full-address column; select it if
  one exists, otherwise note "source has none" in the TOML comment:
  - [ ] durham
  - [ ] hamilton
  - [ ] niagara-falls
  - [ ] peel-region
  - [ ] wellington
- [ ] No unit field selected — most were recorded as "source publishes no unit field"
  during onboarding; do one verification pass over each source schema:
  - [ ] toronto (especially — the old importer never looked)
  - [ ] brantford
  - [ ] chatham-kent
  - [ ] dufferin
  - [ ] lambton
  - [ ] peterborough-county
  - [ ] sarnia
  - [ ] thunder-bay
- [ ] Spot-check low coverage — open a handful of the blank rows and judge: wrong
  column selected, or genuinely unaddressed points (towers, outbuildings)? Note the
  verdict in each TOML:
  - [ ] dufferin — number 88% (~3.2k blank)
  - [ ] elgin — street 94% (~1.3k blank)
  - [ ] brant — number/street/full ~95%
  - [ ] windsor — street 99%

## 1b. Fields the sources have added since we last looked

Found 2026-08-08 by `data-integrity`'s `health.py --drift`, which compares each live
ArcGIS layer against what the store actually holds. Nothing was *dropped* anywhere,
which is the case that would have been urgent (a vanishing field fakes a whole-city mass
event). These are all additions.

- [x] **kitchener** (`LATITUDE`, `LONGITUDE`) and **windsor** (`X`, `Y`, `JOIN_FID`,
  `Join_Count`, `TARGET_FID`) — done 2026-08-08, `ignore_fields` on both. Worth knowing
  *why*, because the first reading was wrong: these are not columns about to start
  churning, they are **empty schema slots** — 0 of 132,060 rows and 0 of 133,331
  respectively, checked with `returnCountOnly` against the live layers, and kitchener's
  are typed as strings rather than numbers. An all-null prop never reaches `props`, so
  ignoring them suppressed nothing: regenerating both cities left every count and the
  whole `compared_fields` list byte-identical. It is pre-emptive, and the thing being
  pre-empted is narrower than report noise: on the day a publisher backfills one of
  these, every row's `payload_hash` changes and the city opens a fresh SCD-2 range for
  itself. Report-time noise could be fixed afterwards by regenerating; that store churn
  could not.
- [ ] **oakville** — a `SUITE` column alongside the `UNIT` it already maps. Decide which
  is the real unit field, or whether `SUITE` is an echo to ignore. Check whether it is
  populated first — the two above were not.
- [ ] Single new props, each worth one look for whether it is a class candidate, an echo,
  or nothing: burlington `PROPERTYDESCASSESS`, greater-sudbury `STREETPREFIX`, hamilton
  `SETTLEMENT` (hamilton has no full-address field selected — see §1), niagara-falls
  `StreetNoUpper`, sdg `LabelFullMod`, kawartha-lakes `StreetDirectionPrefix`,
  `StreetNameAlt2`, `StreetParity`.
- [ ] **renfrew** — 71 fields live against far fewer stored, but renfrew is frozen at
  06-29, so most of that is drift accumulated while we were not looking rather than a
  real roster change. Re-run `--drift` once it unfreezes before acting on it.

Static sources (toronto, waterloo) cannot be probed this way — no layer metadata to ask.

## 2. Find data sources for uncovered cities

Cities/counties with no working source (full reasons in `skipped.toml`, shown on the
landing page). ArcGIS Online search is exhausted for all of these — next steps are
human ones: browse each municipality's own open-data/GIS page, check provincial
portals (geohub.lio.gov.on.ca), or email the GIS department.

- [ ] Dead endpoints — worth asking the municipality where the data moved:
  - [ ] Belleville
  - [ ] Simcoe County
  - [ ] Oxford County
  - [ ] Northumberland County
  - [ ] Haldimand County (was a maintenance page — just retry first)
  - [ ] Middlesex County (one server takes six member municipalities with it:
        Lucan Biddulph, Newbury, North Middlesex, Southwest Middlesex,
        Strathroy-Caradoc, Thames Centre)
  - [ ] Cobourg
  - [ ] West Parry Sound
- [ ] No public address layer found at all — check muni portals / email GIS dept:
  - [ ] Perth County
  - [ ] Lanark County
  - [ ] Haliburton County
  - [ ] Essex County
  - [ ] Grey County
  - [ ] Prince Edward County
  - [ ] Halton Hills
  - [ ] North Bay
  - [ ] Timmins
  - [ ] Collingwood
  - [ ] Owen Sound
  - [ ] Innisfil
  - [ ] Kenora
  - [ ] Stratford
- [ ] Special cases — need a decision, not a search:
  - [ ] **Norfolk County** — layer exists but is token-secured; ask the county for
        access or an open mirror.
  - [ ] **Sault Ste. Marie** — only date-versioned URLs
        (`Collection_Addresses_<month>_<year>`). Decide: accept with a manual URL
        refresh every republish, or keep skipping.
  - [ ] **City of Peterborough** — data exists but licence is "Proprietary - All
        rights reserved". Ask the city about tracking/republication, or leave it to
        the County layer.
  - [ ] **Amherstburg** — only parcel/assessment data published; ask if civic
        address points exist.

## 3. Licence review

- [ ] Licence "Not identified" — find each one's actual licence on the publisher's
  portal and update the TOML. Tracking is fine meanwhile; republication/OSM use is
  not cleared:
  - [ ] brant
  - [ ] chatham-kent
  - [ ] elgin
  - [ ] frontenac
  - [ ] kawartha-lakes
  - [ ] leeds-grenville
  - [ ] lennox-addington
  - [ ] milton
  - [ ] muskoka
  - [ ] peel-region
  - [ ] peterborough-county
  - [ ] renfrew
  - [ ] sarnia
  - [ ] sdg
  - [ ] wellington
- [ ] Custom Terms of Use (OSM red) — read the terms; confirm change-tracking +
  publishing diff reports is permitted:
  - [ ] burlington
  - [ ] london
  - [ ] windsor

## 4. Periodic / ops chores

- [ ] **Re-probe `skipped.toml` quarterly** — endpoints come back or migrate
  (5 of 5 originally-dead cities were eventually recovered via ArcGIS Online).
- [ ] **Delete the 2026-08-09 store backups** — 2.9 GB outside the repo, kept while the
  prop-hashing migration settles (§5). Both passes verified idempotent and every
  affected city's latest diff verified byte-identical the same day, so these are
  belt-and-braces rather than a pending rollback:
  - `C:\Users\kk\ontario-db-backup-2026-08-09\` — all 42, 2.7 GB, pre-migration
  - `C:\Users\kk\ontario-db-backup-2026-08-09-preignore\` — the five `--reapply-ignore`
    cities, 190 MB, post-global pass. The narrower rollback point, and the only one
    that can undo `--reapply-ignore` alone.

  Reasonable to drop once a daily run has imported cleanly on top of the migration
  (i.e. after 2026-08-10 noon). Restoring either is a plain file copy over
  `data/<slug>/<slug>.db` with the scheduled task idle.
- [ ] **Watch the daily scheduled task** — check `logs/` and that the site commit/push
  ran. `addressvault report` is the first command (per-city-per-day: checked, unchanged,
  failed, or no attempt); `health.py --blocks --runs` is the project-side second.
  Currently outstanding: 2026-07-31 exited 1 after three attempts, and kingston has been
  failing since 2026-08-08 (below).
- [ ] **kingston: source down since 2026-08-08** — seven pull attempts across 08-08 and
  08-09, every one `arcgis error 500: Error invoking service`. The layer answered
  normally when probed late on 08-09 (count 77,294, first page fine), so it is
  intermittent on their side, not URL rot. Nothing to fix here and no config to change:
  `utility.arcgis.com/usrsvcs/servers/<guid>/` is AGOL proxying to Kingston's on-prem
  server, and there is no hosted alternative — the AGOL search returns only this one
  Civic Address Points service. Watch it; if the 500s persist past a week, ask the city.
- [ ] ~~Eight cities frozen since 2026-06-27/28~~ — **wrong, retracted 2026-08-10.**
  waterloo, dufferin, elgin, lambton, peel-region, sarnia, windsor and renfrew were
  never frozen: the vault has pulled and verified all eight every day throughout, e.g.
  waterloo `2026-08-09 … unchanged_since='2026-06-27'`. Their sources genuinely have not
  changed since June. What was frozen was the *measurement* — this repo's store records
  only changes, so a verified-but-unmoved city writes no row and reads as months stale.
  The `health.py --stale` section built to catch it inherited the same blind spot and
  reported 21 of 42 STALE against a true count of 1; it has been deleted rather than
  fixed. Use `addressvault report`. (The one real finding underneath, kingston, is the
  item above — it went unnoticed for two days inside that false list.)
- [ ] **Observe the failure-reporting split — review 2026-08-17** (one week after the
  2026-08-10 change). Failures moved out of the public reports and into the vault report;
  `health.py --stale` was deleted. Check, in order:
  1. `addressvault report` — is the city×day matrix actually the thing you reach for?
     Does every red cell carry a cause you can act on, or do some say only "failed"?
  2. Did kingston recover on its own, and did you notice *from the report* rather than
     from a nonzero exit code?
  3. `logs/runs.csv` — still under-recording? It had no row for 2026-08-06 or 08-08
     despite the vault logging checks for every city on both days. If it is still
     dropping runs, that ledger is next.
  4. Did anything reach for a staleness number and not find one? If the vault report
     answered it instead, the deletion was right; if not, note what was missing rather
     than rebuilding `--stale`.
  5. Public site — confirm a failing city just shows its last good data, with nothing
     about the failure anywhere in `docs/`.

  Open question deliberately left undecided: whether a city failing for N days should
  escalate beyond the vault report (a nonzero exit, a notification). Nothing escalates
  today — kingston's two-day outage produced only a red run. Decide it with a week of
  evidence, not now.
- [ ] **Per-city tuning pass** — reviewing each city's "modified" noise to pick
  `ignore_fields` (Toronto needed this — 387→3 modified), and checking whether the
  `[classes]` assignments (2026-06-12, sampled from one snapshot each) hold up against
  real transitions. This is the `city-tune` sweep tracked in `TODO-skills.md` §1, six
  cities done; it still needs a human eye per city. Don't run it as a separate pass.

## 5. Hand to coding agent when convenient

Code fixes found during the audits. Every one of them changes payload hashes → a
one-time "modified" spike, so batch them:

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

## Appendix: field coverage (latest snapshot, % non-null)

| slug | rows | number | street | unit | full |
|---|---:|---:|---:|---:|---:|
| barrie | 63,313 | 100 | 100 | 14 | 100 |
| brampton | 248,316 | 94 | 100 | 28 | 100 |
| brant | 19,322 | 94 | 95 | 7 | 95 |
| brantford | 38,673 | 100 | 100 | — | 100 |
| bruce | 51,666 | 100 | 100 | 7 | 100 |
| burlington | 60,325 | 100 | 100 | 17 | 100 |
| cambridge | 53,998 | 100 | 100 | 22 | 100 |
| chatham-kent | 59,210 | 100 | 100 | — | 100 |
| cornwall | 20,582 | 100 | 100 | 15 | 100 |
| dufferin | 27,075 | 88 | 100 | — | 100 |
| durham | 253,555 | 100 | 100 | 8 | — |
| elgin | 21,785 | 100 | 94 | 0 | 100 |
| frontenac | 22,347 | 100 | 100 | 0* | 100 |
| greater-sudbury | 70,003 | 99 | 100 | 14 | 100 |
| guelph | 53,889 | 100 | 100 | 25 | 100 |
| hamilton | 273,084 | 100 | 100 | 37 | — |
| hastings | 30,815 | 100 | 100 | 5 | 100 |
| huron | 38,190 | 100 | 100 | 11 | 100 |
| kawartha-lakes | 44,174 | 100 | 100 | 9 | 100 |
| kingston | 77,134 | 100 | 100 | 40 | 100 |
| kitchener | 131,898 | 98 | 100 | 45 | 100 |
| lambton | 56,897 | 100 | 100 | — | 100 |
| leeds-grenville | 54,008 | 100 | 100 | 2 | 100 |
| lennox-addington | 26,093 | 98 | — | — | 100 |
| london | 142,890 | 100 | 100 | 18 | 100 |
| milton | 46,321 | 100 | 100 | 8 | 100 |
| muskoka | 66,180 | 100 | 100 | 27 | 100 |
| niagara-falls | 207,845 | 100 | 100 | 12 | — |
| oakville | 71,051 | 100 | 100 | 8 | 100 |
| ottawa | 402,805 | 100 | 100 | 10 | 100 |
| peel-region | 503,923 | 100 | 100 | 33 | — |
| peterborough-county | 40,522 | 100 | 100 | — | 100 |
| quinte-west | 20,270 | 98 | 100 | 5 | 100 |
| renfrew | 33,130 | 100 | 100 | 1 | 100 |
| sarnia | 26,896 | 100 | 100 | — | 100 |
| sdg | 31,845 | 100 | 100 | 3 | 100 |
| thunder-bay | 45,049 | 100 | 100 | — | 100 |
| toronto | 525,438 | 100 | 100 | — | 100 |
| waterloo | 55,541 | — | 100 | — | 100 |
| wellington | 42,892 | 100 | 98 | 1 | — |
| windsor | 118,841 | 100 | 99 | 29 | 100 |
| york | 431,535 | 100 | 100 | 15 | 100 |

`—` = field not selected in the TOML. `0*` = selected but all source values blank.
