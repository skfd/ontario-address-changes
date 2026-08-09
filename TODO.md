# Operator TODO — ontario-address-changes

Last updated: 2026-08-08. Tasks for the human operator. Field-coverage numbers come
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
- [ ] **Watch the daily scheduled task** — check `logs/` and that the site
  commit/push ran; a silently failing source shows up as a stale "generated" date
  on its report.
- [ ] **Eight cities have been frozen since 2026-06-27/28** (found 2026-08-08 while
  working the coordinate sweep): waterloo, dufferin, elgin, lambton, peel-region,
  sarnia, windsor, and renfrew (06-29). The vault hands back the same dated file every
  day, so `run.py`'s filename check short-circuits before `db.already_imported` and no
  snapshot row is written at all — not even a skip. That is why the log reads
  `already imported: elgin-2026-06-27.geojson` six weeks on, and why elgin,
  peel-region and waterloo are still baseline-only and unauditable. Not one dead
  server: the eight sit on eight different hosts, and the refusal guards only landed
  2026-08-08, so this predates them. Next step is the vault side, not this repo.
  Because no row is written, this failure is invisible to `logs/runs.csv` (which has
  reported success every day) — worth a staleness check that reads max snapshot age
  per city rather than run exit codes.
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

Two more of the same shape are open, detailed in `TODO-skills.md` §1. Batch them
together and give them the same backfill treatment:

- [ ] Pattern-match the ESRI id spellings `_VOLATILE_KEYS` misses (`^objectid(_\d+)?$`,
  `^fid(_\d+)?$`) — hastings' `OBJECTID_12` is ignored per-city today.
- [ ] Strip whitespace *around* prop values, not just values that are entirely
  whitespace. Renfrew's `Full_Address` churned 1,060 rows on a trailing space the
  canonical `full` strips before comparing; it is ignored per-city today, which is a
  workaround for a gap every city shares.

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
