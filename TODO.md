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
- [ ] **waterloo — the key_field only covers 29% of the city.** Found 2026-08-10 while
  ignoring its coordinate duplicate. `ADDRESS_ID` is populated on 15,861 of 55,541 rows;
  the other 39,680 fall through to `synth_fields = ["full"]`, so the city runs on two
  identity regimes at once (`95099.0` vs `syn:d19669…`). Nothing is wrong today — 55,541
  distinct keys, zero collisions — but the day the city backfills `ADDRESS_ID` on the
  rest, all 39,680 switch key form and report as retired + re-added on one day. Two
  choices, both re-keying and neither retroactive: leave it and accept the risk, or set
  `key_field = ""` so the whole city synthesizes (uniform and immune, but it re-keys the
  15,861 today and gives up a stable id where the source does provide one). Note also the
  ids are stored float-formatted (`95099.0`, out of the shapefile), so a source switch to
  integer formatting re-keys those 15,861 by itself.
- [ ] **dufferin — `FULLADDY` disagrees with its own components on 857 rows (3.2%).**
  Found 2026-08-10. It is the mapped `full`, so it is what the reports display, and it is
  hand-maintained rather than derived: 359 rows carry a *different house number* than
  `STREETNUM` (many in runs where `FULLADDY` holds the neighbour's number — 713051 shown
  as 713053, 713053 as 713055, 713055 as 713057, the signature of a spreadsheet fill off
  by one row), 466 disagree on the street text (mostly styling — "30 SIDEROAD" vs "30TH
  SIDE ROAD" — but some name a different road outright: "10 SIDEROAD" vs "10TH LINE"),
  and 4 lost the separating space ("58744810 SIDEROAD"). The remaining 26,214 match.
  Decide whether to keep publishing the county's string as-is, or unmap `full` and let
  reports compose "number street" from the cleaner components. Not urgent and not an
  identity risk (`key_field = "ID"`, and `full` is not in `synth_fields`), but it means
  ~1.3% of displayed dufferin addresses show a number that belongs to a neighbour.
- [ ] **elgin — `StrNum2` is the hastings trap in miniature.** Found 2026-08-10. It
  duplicates the mapped `StrNUM` on 21,771 of 21,785 rows, and on the 14 where they
  differ it is sometimes the *better* value — it keeps the house suffix that `StrNUM`
  drops and that `full` shows ("1" vs "1B CHATHAM ST", "47" vs "47B MILTON STREET") — but
  not reliably: on others `StrNUM` is right and `StrNum2` is the broken one (`33220
  TALBOT LINE` vs `0`, `33711 FIRST LINE` vs `33609`). So it is not simply the column we
  should have mapped, and remapping would re-key the city anyway (synth from
  number/street/unit). The open call is narrower: leave it compared, or add it to
  `ignore_fields` + `keep_fields` so its echo cannot manufacture updates while the values
  stay in `props`. Left alone for now — it is 14 rows, and unlike hastings' 2,721 there
  is no volume argument either way.
- [x] **No full-address field selected — all five checked 2026-08-10, all five confirmed
  "source has none."** Every layer's live field list was read in full and every candidate
  column's fill rate measured; each TOML now says so in a comment rather than leaving the
  silence ambiguous. Reports keep falling back to "number street", which is correct here.
  - [x] durham (21 fields), hamilton (13), niagara-falls (15), peel-region, wellington (13)

  One consequence found on the way, in durham only: `CIVIC_SFX`, the house-number suffix,
  is a separate column populated on 1,173 of 253,570 rows (0.5%), and with no `full` to
  fall back on those addresses display without it. Not fixable in config — the field map
  is 1:1, not a concatenation — and not an identity risk, since `MXADDRESSCODE` is a real
  `key_field`. The value is stored and compared in `props` either way. Noted, not open.
- [x] **No unit field selected — all eight checked 2026-08-10.** Seven confirm "source
  publishes no unit column"; one does not, and is the new item below. Each source's field
  list was read live (toronto from its geojson, having no layer metadata to query), and
  because a missing *column* does not mean missing *data*, every city's number/full column
  was also scanned for units embedded as `<unit>-<number>`. Ranges were separated from
  units by a test a range cannot pass: many distinct left parts sharing one right part.
  - [x] toronto — 37 properties, nothing unit-like, `unit` null on all 525,473 rows. Its
    1,635 hyphenated numbers are all LO_NUM-HI_NUM ranges, which is what the `keep_fields`
    range gate already assumes. The "old importer never looked" worry is now closed.
  - [x] **brantford — the exception: units exist, and we are not tracking them.** See below.
  - [x] chatham-kent (10 fields, 2 hyphens, one a range), dufferin (9 fields — verified
    2026-08-10; the bare config is a bare source, not an oversight), lambton (11 fields,
    7 embedded `<number>-<unit>`), peterborough-county (9 fields, ~31 embedded),
    sarnia (15 fields; its 11 hyphens are all ranges), thunder-bay (17 fields, 14 embedded)
  - Of the embedded stragglers, none exceeds 0.1% of its city, so all are noted in the
    TOMLs rather than parsed. Two thunder-bay fields that look like unit candidates are
    not: `ADDRESS_QUALIFIER` is a house-number suffix (A, B, 1/2) and `SPLITLOC` is which
    side of a split street the point is on (part of the street name, "FREDERICA ST E").
- [ ] **brantford — units are published, embedded in the number, and unmapped.** Found
  2026-08-10 by the pass above. 2,213 of 38,981 rows (5.7%) carry `STREETNUM` /
  `FULLADDRESS` in `<unit>-<number>` form, and they are unambiguously units rather than
  ranges: 177 distinct left parts share the right part "77", 138 share "21", 116 share
  "20" — no house-number range can repeat its high end across 177 low ends. (The other
  436 hyphenated rows read left>=right and are ranges proper.) So this is waterloo's
  decision, not dufferin's: have the unit parsed out of `STREETNUM`, or accept that 5.7%
  of brantford displays as "12-73 MORTON AVE W" with no unit field. Note the cost either
  way — identity synthesizes from `["number", "street"]`, so adding `unit` re-keys all
  38,981 rows and cannot be applied retroactively.
- [ ] **thunder-bay — `number` drops the house suffix on 347 rows.** Found 2026-08-10, the
  hastings trap in a third city. `number` maps to `ADDRESS_NUMBER`, an Integer, so it holds
  "688" where the String `ADDRESS` column holds "688B" and `full` (`COMPLETE`) shows "688B
  CITY RD"; the two disagree on 347 of 45,098 rows. `ADDRESS` is the column that should
  have been mapped. Weaker than hastings on both sides of the trade: only 347 rows rather
  than 2,721, but also cheaper to live with, because `full` already displays the suffix and
  `ADDRESS` is stored and compared in `props` regardless. Remapping re-keys all 45,098
  (synth from `["number", "street"]`) and is not retroactive. Leave it unless the display
  gap starts mattering.
- [ ] Spot-check low coverage — open a handful of the blank rows and judge: wrong
  column selected, or genuinely unaddressed points (towers, outbuildings)? Note the
  verdict in each TOML:
  - [x] dufferin — number 88% (~3.2k blank). Checked 2026-08-10: **genuinely
    unaddressed, same shape as elgin.** On all 3,270 blank-number rows `FULLADDY` equals
    `STREETNAME` exactly ("20 SIDEROAD" as the whole address), so no number exists
    anywhere on the row to have been missed. The layer is `Dufferin_County_Entrances` —
    driveway/field entrances, many of which have no civic number to carry.
  - [x] elgin — street 94% (~1.3k blank). Checked 2026-08-10: **genuinely unaddressed
    points, not a wrong column.** All 1,253 blank-street rows carry `Condition` values
    like "No Sign" and either `StrNUM = '0'` (275 rows, so `full` reads "0" too) or a
    real number with no street at all (1,040, mostly Southwold). These are located
    parcels awaiting a civic address, which is what the column should say about them.
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
- [x] **oakville** — a `SUITE` column alongside the `UNIT` it already maps. Done
  2026-08-10, and the answer was "check whether it is populated first": **0 of 71,049
  rows**, same empty-schema-slot shape as kitchener and windsor above. Never reached the
  store in any of the 7 snapshots either. So it is not a second unit column at all, and
  the re-key trap the item was written around does not apply. Documented in the TOML,
  deliberately *not* ignored — an ignore is right for an empty coordinate slot and wrong
  here, because a backfill of a unit column is content we want. Seven more columns in
  that layer are empty the same way (TOP_ALIAS, ADDR_ALIAS, POSTAL, CITY, PROV,
  STREET_TYPE_PREFIX, STREET_DIR_PREFIX).
- [x] **Single new props — all eight looked at 2026-08-10, and the answer is the same for
  every one: an empty schema slot.** burlington `PROPERTYDESCASSESS` (0 of 60,326),
  greater-sudbury `STREETPREFIX` (0 of 70,100), hamilton `SETTLEMENT` (0 of 273,459),
  niagara-falls `StreetNoUpper` (0 of 207,958), sdg `LabelFullMod` (0 of 33,630),
  kawartha-lakes `StreetDirectionPrefix` / `StreetNameAlt2` / `StreetParity` (0 of 44,213
  each). Live counts by `returnCountOnly`, cross-checked against every store: not one has
  ever reached `props`, over 191 snapshots between them. So none is an echo, none is a
  class candidate *yet*, and none can fake anything today.

  **None was ignored**, which is the point worth keeping. The pre-emptive `ignore_fields`
  that kitchener's and windsor's empty slots got is right for a coordinate duplicate and
  wrong for all eight of these, by the rule oakville's `SUITE` established: it depends on
  what the column would carry if filled, and every one of these would carry address
  content (street prefixes, a full-address variant, a range's upper bound) or a real
  boundary. Suppressing that backfill is exactly what we would not want.

  One config edit came out of it: hamilton's `SETTLEMENT` joined `[classes] boundary`,
  ahead of any data, on the same reasoning as burlington's `NAME` — `[classes]` is
  report-time and retroactive, so carrying it costs nothing and it keeps a settlement
  backfill out of the generic Updated table. Grouped as boundary on the sdg precedent.
  Verified: regenerating all 21 hamilton reports changed nothing but the timestamp line.

  Nearly-empty siblings noticed alongside, all subsumed by mapped fields and left alone:
  greater-sudbury `STREETSUFFIX` (12 rows), `ADDRESSNUMBERPREFIX` (17),
  `ADDRESSNUMBERSUFFIX` (372).
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
  - `C:\Users\kk\ontario-db-backup-2026-08-20-preignore\` — the 17 cities whose
    ignore_fields changed in the 2026-08-20 flag-review + tuning pass, 1.2 GB, taken
    before that day's `--reapply-ignore` run. Same drop rule: safe once a daily run
    has imported cleanly on top (after 2026-08-21).

  Reasonable to drop once a daily run has imported cleanly on top of the migration
  (i.e. after 2026-08-10 noon). Restoring either is a plain file copy over
  `data/<slug>/<slug>.db` with the scheduled task idle.

  **That gate is met** (2026-08-10): `logs/runs.csv` records 12:00:02 → 12:33:26, one
  attempt, exit 0 — the first full daily run against the migrated stores. Both
  directories were confirmed intact and matching what this note claims (126 files /
  2.69 GB, 5 files / 0.19 GB). Deletion itself is the operator's to run; tick this off
  once it has.
- [ ] **Watch the daily scheduled task** — check `logs/` and that the site commit/push
  ran. `addressvault report` is the first command (per-city-per-day: checked, unchanged,
  failed, or no attempt); `health.py --blocks --runs` is the project-side second.
  Currently outstanding: 2026-07-31 exited 1 after three attempts.
  (Kingston, below, cleared itself on 2026-08-10.)
- [x] ~~**kingston: source down since 2026-08-08**~~ — **recovered on its own 2026-08-10.**
  Seven pull attempts across 08-08 and 08-09, every one `arcgis error 500: Error invoking
  service`; today's noon run pulled it normally (`expect=77,294`, no ERROR line, and
  `docs/kingston/report-2026-08-10.html` published). Intermittent on their side, as the
  08-09 probe suggested, not URL rot — nothing was changed here. Worth noting for the
  08-17 review: the recovery was spotted by reading `logs/update.log`, not from
  `addressvault report`, which is question 2 of that review answered the wrong way round.
  If the 500s return and persist past a week, ask the city; there is no hosted
  alternative (`utility.arcgis.com/usrsvcs/servers/<guid>/` is AGOL proxying to
  Kingston's on-prem server, and the AGOL search returns only this one service).
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
  3. `logs/runs.csv` — still under-recording? **Half of this premise was wrong; see the
     item below.** Of the two rowless days, 08-06 is a genuine ledger drop (machine awake
     across noon, 3 vault snapshots pulled, no row) and 08-08 is not (machine asleep
     through noon, so no run existed to record). Judge the ledger on 08-06's shape only.
  4. Did anything reach for a staleness number and not find one? If the vault report
     answered it instead, the deletion was right; if not, note what was missing rather
     than rebuilding `--stale`.
  5. Public site — confirm a failing city just shows its last good data, with nothing
     about the failure anywhere in `docs/`.

  Open question deliberately left undecided: whether a city failing for N days should
  escalate beyond the vault report (a nonzero exit, a notification). Nothing escalates
  today — kingston's two-day outage produced only a red run. Decide it with a week of
  evidence, not now.
- [ ] **A Windows Update restart skips the day silently — diagnosed 2026-08-12, left
  unfixed by choice.** Found while checking why 08-12 had no run at all: no `runs.csv`
  row, zero lines in `update.log`, no vault snapshots pulled, and the task itself
  reporting `LastRunTime = 08-11 12:00` with `NextRunTime = 08-13 12:00`.

  The trigger is a Windows Update restart, not ordinary sleep — the first reading here
  was "the laptop was asleep", and that was the symptom. The System log shows two
  `system initiated reboot from Modern Standby` events at 05:29–05:33 with
  `LastBootUpTime = 05:33:09`, after which the machine went straight back into Modern
  Standby and stayed there past noon. The same shape explains 08-08 (asleep 02:11–13:16).
  It does *not* explain 08-06, which was awake across noon — that one is a real
  `runs.csv` drop, and is now the only evidence for the ledger question in the item above.

  **The mechanism that actually matters is `LogonType: Interactive`** on
  `kk-ontario-update`. An Interactive task can only run while `kk` is logged on, so after
  an unattended reboot there is no session for it to run in and the trigger cannot fire at
  all — no power setting changes that. `StartWhenAvailable = True` does not rescue it
  either: the machine woke at 21:51 and 12 minutes later no catch-up had fired and
  `NextRunTime` still read 08-13. That setting reads like it covers exactly this case and
  does not.

  `WakeToRun = True` was tried on 08-12 and **reverted the same evening** — decided
  against having code wake the machine. So the task is back at its original settings
  (`WakeToRun` and `DisallowStartIfOnBatteries` both as they were) and this failure mode
  is open by choice, not oversight. The options that do not involve waking anything, if it
  ever becomes worth fixing: a today-guard in `daily-update.ps1` keyed on `runs.csv` (it
  already writes one row per run, so "did today succeed?" is a two-line check) which would
  make the trigger safe to repeat through the afternoon or fire on logon; or switching
  `LogonType` to `Password`, the only variant that both survives an unattended reboot and
  keeps `git push` working, since a real logon unlocks the DPAPI key behind Credential
  Manager and S4U does not.

  The broader point for the 08-17 review: this failure mode is invisible to every surface
  we have. `addressvault report` shows "no attempt", which is also what a metered skip
  shows; `runs.csv` shows nothing at all; the site just goes stale. It is the same blind
  spot the deleted `health.py --stale` had, arriving from the opposite direction — that
  one measured the store and missed unchanged cities, this one misses days the pipeline
  never ran. Question 4 of the review ("did anything reach for a staleness number") should
  be read with this in mind.
- [ ] **Watch for more `index.lock` publish failures — observing, deliberately not fixed.**
  The manually-triggered 08-12 run updated all 42 cities cleanly and then lost the publish
  to a 0-byte `.git/index.lock`: `git add docs` failed, so nothing was staged, committed or
  pushed, and the run ended `publish-failed` with the site a day stale. Recovered by hand
  the same evening (`e22515ad`) — the lock was removed and the run's own `docs/` output
  committed unmodified.

  The lock was orphaned at 22:12 and hit at 22:50, i.e. 38 minutes old with no git process
  holding it. `daily-update.ps1:132` only sweeps locks older than **60 minutes**, so it
  correctly left this one alone and had no retry behind it. A lower threshold, or one retry
  of the `add` after clearing a lock with no live process behind it, would have made it
  self-healing.

  **Deliberately unchanged pending more cases.** The one observation is contaminated: a
  human/agent was running `git` in the repo during that run, which is not what happens at
  noon, so this may be self-inflicted rather than a real recurring fault. Collect further
  instances before touching the constant — if they only ever appear on manually-triggered
  runs with someone working in the repo, the sweep is fine as written.
- [x] **Per-city tuning pass** — DONE 2026-08-20 across all 42: 17 cities via the
  flag-review session (ignore_fields/classes debts + the new `location_min_move_m`
  floor), the other 25 via a full `audit.py` sweep the same day (commit `4f2e77b8`).
  Nine of the 25 took config (bruce ARN, cornwall LAST_EDIT, elgin Condition + MUNI
  class, greater-sudbury components + NAME place_name class, hamilton street
  components, kawartha-lakes Xlong/Ylat + composites, london composites, milton
  DISPLAY_NAME/LABEL_ANGLE/ASSIGNED_BY/PROP_RSN, lennox-addington ADD_LABEL +
  BELL_MUNIC class); the rest were clean, frozen at one snapshot, or already tuned.
  `--reapply-ignore` run same day for all 17 ignore-touched cities (the nine plus
  the eight from the flag review). The §1 field-map remaps stay open — this pass
  deliberately did not touch identity or field maps. Watch item from the sweep:
  chatham-kent shrank ~500 rows over July and has not republished since
  2026-07-24 — a data-integrity look, not a config one.

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
