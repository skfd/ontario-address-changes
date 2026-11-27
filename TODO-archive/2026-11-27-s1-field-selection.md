# TODO.md §1 and §1b: closed items

Moved verbatim out of [TODO.md](../TODO.md) on 2026-11-27; the text is as it stood at
TODO.md's last update, 2026-10-31. History and finished work, not required reading.
Open items stay in TODO.md; where one was shortened there, its full text is here.

## 1. Complete field selection for tracked cities

- [x] **waterloo** — no street-number field exists in the source (only the full
  `CIVIC_ADDR` string). Decide: have the number parsed out of `CIVIC_ADDR`, or
  accept full-address-only display. Measured 2026-08-20: **all 55,541 active full
  values parse cleanly** as `<number>[suffix] <street>` (zero exceptions), so a
  parse is mechanically safe. Identity synthesizes from `full` for the 71% without
  `ADDRESS_ID`, so populating `number` does not re-key; it would need the
  remap-style full-history rewrite (lennox ADD_LABEL precedent) to land event-free,
  via a parse variant of `tools/remap_canonical_from_prop.py`.
  **Done 2026-10-20, number and unit both.** The live layer behind the 10-16 re-point
  publishes units at the end of `CIVIC_ADDR` ("29 BARREL YARDS BLVD 1205", "300 REGINA
  ST N 2 204", "25 WESTMOUNT RD N PH B"), and the address is `<number> <STREET_NM>[
  <unit>]` on 55,844 of 55,845 rows, so the split anchors on the mapped street:
  `number_unit_from_full = true` (`normalize.number_unit_from_full`). The one exception
  is the publisher's ("526B BROOKMILL CRES" filed under BEAVER CREEK RD): number 526B,
  no unit. Neither column is in the identity basis; the whole store was rewritten
  first with `tools/recanonicalize.py` (55,845 rows, no re-key) and verified against
  the 10-16 pull: 0 added/removed/modified, content_hash equal. Unit coverage 0 -> 42%.
- [x] **lennox-addington** — no parsed street field in the source. `ADD_LABEL`
  answered half of this on 2026-08-20: it is the house number WITH its suffix
  ('137A'), not a street label — measured, then made the `number` source via a
  full-history migration (`tools/remap_canonical_from_prop.py`, 3,741 rows, no
  event; identity keys on `full`, so nothing re-keyed). What remains open is the
  street half: decide whether parsing street out of `ADDRESS` is worth it, or
  accept full-address-only street display. Measured 2026-08-20: **97.0% of the
  26,155 full values parse** as `<number>[suffix] <street>`. The 778 that don't
  split two ways: **138 are embedded units in `<unit>-<number> <street>` form**
  (`A1-291 Newburgh Road`; confirmed units by the shared-right-part test — 16
  distinct units at 391 Dundas St W, 14 at 236 Newburgh Rd), the brantford
  pattern in a second city at 0.5% of rows; the other 640 are campground sites
  ("Site 14 Pickerel Park Rv Resort", "Site N/A …"), bare numbers ("70"), and
  bare street names — genuinely non-standard rural addressing, not a parse gap.
  **Done 2026-10-03** (ticked 2026-10-20): `street_from_full = true`, history rewritten
  by `tools/derive_street_from_full.py`, 26,168 of 26,182 rows got a street.
- [x] **frontenac** — the source's `UnitNumber` column is 100% blank (22k rows, zero
  real values). Decide: unselect it, or keep it in case the county starts filling it.
  **Kept, closed 2026-08-20.** Re-measured: still 0 of 22,381 active rows. The
  oakville `SUITE` rule decides it — a unit backfill is address content we want,
  and keeping the selection costs nothing (a blank canonical field displays
  nothing). Verdict noted in the TOML.
- [x] **hastings** — `number` maps to `House_No`, which drops the house suffix that
  `full` (`Full_Add`) keeps: "152 JAMIESON LN" as the number vs "152B JAMIESON LN" as
  the full address, on the 2,721 rows with a `House_Suf`. The source's `ADDRESS_NU`
  carries the combined form. Decide whether to remap `number` to `ADDRESS_NU` — but
  note the cost: hastings synthesizes identity from `["number", "street", "unit"]`, so
  remapping re-keys all 31k addresses and cannot be applied retroactively (one report
  showing the whole city retired and re-added). Found 2026-08-08 while ignoring
  `ADDRESS_NU` as a duplicate; it is a duplicate *of the wrong column*.
  2026-08-20 update: lennox-addington's twin of this was fixed event-free with
  `tools/remap_canonical_from_prop.py` (rewrite history to the new mapping before
  the next import — the house rule is to prefer that over letting the phantom event
  land). That tool refuses hastings because `number` is in the identity basis; an
  event-free fix here would need a dedicated identity migration on top — rewrite
  every historical row's synthesized key under the new number, verify zero key
  collisions, keep each row's version chain paired. Derivable in principle (keys are
  computed from stored fields), but it is surgery on the one non-retroactive layer;
  spec it as its own tool with a collision dry-run if the display gap ever justifies it.
  2026-10-20: `tools/recanonicalize.py` now does the re-key half (faithfulness, collision
  and touching-span checks, verify against the vault pull), but it derives from the stored
  canonical columns only. Hastings needs `number` read from the `ADDRESS_NU` prop, so it
  would need a prop-sourced derive step added to that tool first.
  **Done 2026-10-20, and it was worse than a display gap.** `number_from_full = true`: the
  head of `Full_Add` equals `ADDRESS_NU` on all 31,361 rows, and is derivable for history.
  The verify then showed the real cost of the old key: suffix siblings at one point
  ("295A"/"295B MILL ST") shared it, so the importer's dedupe dropped one of them - 444
  addresses at the 06-11 baseline (417 today) were never stored, and on 16 days the other
  sibling won and the chain switched to it. Rebuilt by replaying all 82 snapshots with
  the new `tools/rebuild_from_pulls.py` (7 early days with no raw pull anywhere bracketed
  from 06-11/06-24, whose hidden sets are identical): 450 keys added, all same-point
  suffix siblings, every old active row kept at every snapshot, verify 0/0/0. Pages: the
  baseline gains 444; a handful of past suffix-only "modified" rows now read as retired +
  added, as any hastings renumber does (number is in the synth basis).
  Expected follow-on: `number` left `[fields]`, so address-vault's sketch basis changed -
  a vault-only churn flag on the next distinct pull is the known artifact
  (vault-churn-after-field-remap). Same for thunder-bay.
- [x] **elgin — `StrNum2` is the hastings trap in miniature.** Moot 2026-10-16: elgin was
  re-pointed to a layer with no StrNum2, whose Civic keeps the suffix. Found 2026-08-10. It
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
- [x] **brantford — units are published, embedded in the number, and unmapped.** Found
  2026-08-10 by the pass above. 2,213 of 38,981 rows (5.7%) carry `STREETNUM` /
  `FULLADDRESS` in `<unit>-<number>` form, and they are unambiguously units rather than
  ranges: 177 distinct left parts share the right part "77", 138 share "21", 116 share
  "20" — no house-number range can repeat its high end across 177 low ends. (The other
  436 hyphenated rows read left>=right and are ranges proper.) So this is waterloo's
  decision, not dufferin's: have the unit parsed out of `STREETNUM`, or accept that 5.7%
  of brantford displays as "12-73 MORTON AVE W" with no unit field. Note the cost either
  way — identity synthesizes from `["number", "street"]`, so adding `unit` re-keys all
  38,981 rows and cannot be applied retroactively.
  **Done 2026-10-20, retroactively.** Re-measured on the 09-18 pull: 2,226 hyphenated rows in
  106 groups sharing a civic number (90 with five or more units, one single), and
  `STREETNUMIN` holds the right part on every one - the publisher's own reading. The "436
  ranges" are gone from this layer. `unit_from_number = true` splits "<unit>-<number>",
  unit joined `synth_fields`, and `tools/recanonicalize.py --old-rev HEAD` re-keyed all
  39,510 rows of history (no collision); verify 0/0/0, no page count moved.
- [x] **leamington — units sit inside `Addressche` between number and street.** Found
  2026-10-23 at onboarding: 479 of 11,424 rows (4.2%) read "24 UNIT 300 SEACLIFF DRIVE EAST",
  "1217 FLR 01 MERSEA RD 2", "20 APT 3 FOUNDRY STREET"; 142 number+street groups (718 rows)
  share one civic address. Not `number_unit_from_full`'s shape (unit after the street), which
  would read the number as "24 UNIT 300". Identity is GlobalID, so a parse (a designator word
  plus one token between `AddressNum` and `StreetName`) changes display only, no re-key.
  Low stakes while the city is gated off the site.
  **Done 2026-10-23:** `unit_from_full = true` (`normalize.unit_from_full`), unit kept with
  its designator ("UNIT 300", "FLR 01"; UPPER/LOWER/REAR/FRONT alone), anchored on the mapped
  number and street columns. 488 of 488 rows of that shape parsed; history rewritten by
  `tools/recanonicalize.py` (488 rows, 0 re-keyed, verify 0/0/0), which now keeps a source-id
  key under an unchanged `key_field` without recomputing it. `[fields]` unchanged, so no
  vault churn. Left unparsed: 68 rows with the unit *after* the street (`7 CHERRY LANE UNIT
  1..49`, `109 ROBSON ROAD UNIT 101..904`) and 14 messy rows. Adding the trailing shape with
  the same anchoring would take same-address groups from 9 (96 rows) to about 2.
  **Trailing shape added 2026-10-24** (designator + one token after the street): 69 more rows.
- [x] **thunder-bay — `number` drops the house suffix on 347 rows.** Found 2026-08-10, the
  hastings trap in a third city. `number` maps to `ADDRESS_NUMBER`, an Integer, so it holds
  "688" where the String `ADDRESS` column holds "688B" and `full` (`COMPLETE`) shows "688B
  CITY RD"; the two disagree on 347 of 45,098 rows. `ADDRESS` is the column that should
  have been mapped. Weaker than hastings on both sides of the trade: only 347 rows rather
  than 2,721, but also cheaper to live with, because `full` already displays the suffix and
  `ADDRESS` is stored and compared in `props` regardless. Remapping re-keys all 45,098
  (synth from `["number", "street"]`) and is not retroactive. Leave it unless the display
  gap starts mattering. (2026-08-20: same verdict as hastings above — an event-free fix
  exists in principle via a history rewrite plus identity migration, see the hastings
  entry; at 347 rows it is even further from justifying that surgery.)
  **Done 2026-10-20.** `number_from_full = true` (head of `COMPLETE`, equal to `ADDRESS` on all
  but 2 of 45,102 rows: a bare "171", now kept, and one row with no ADDRESS). 359 rows
  rewritten, 356 chains re-keyed, 1 split, 1 join ("660 VICTORIA AVE E" lacked a number on
  06-11 and came back with one on 07-24 - now one address, shown as renumbered). Verify
  0/0/0. Backups for all three in `C:\Users\kk\ontario-db-backup-2026-10-20-suffixes\`.

From "Spot-check low coverage" (the parent item stays in TODO.md):

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
  - [x] brant — number/street/full ~95%. Checked 2026-08-20: **genuinely
    unaddressed, no wrong column.** 905 of 19,333 active rows are bare placeholder
    points whose props hold nothing but `CIVIC_ADDRESS_TYPE`/`PLACE_NAME`/
    `PROVINCE` — no address content anywhere on the row to have been missed — and
    ~330 more are street-only entrances (`full` = "PARKSIDE DRIVE", no number),
    the dufferin shape. Verdict in the TOML.
  - [x] windsor — street 99%. Checked 2026-08-20: **genuinely unaddressed
    parcels, no wrong column.** The 696 blank-street rows carry only a legal
    description (`Legal1` = "PLAN 1056 LOTS 314 TO 317 …") — parcels without a
    civic address. But the check surfaced something else: those rows' `number`
    and `full` are the literal string **"None"** — the source's ETL leaks
    Python's `str(None)` (verified in the raw geojson: `"Ward": "None"`), so the
    appendix's 100% number coverage is really 99.4%. The store-wide version of
    this finding is in §5.

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
- [x] **renfrew** — 71 fields live against far fewer stored, but renfrew is frozen at
  06-29, so most of that is drift accumulated while we were not looking rather than a
  real roster change. Re-run `--drift` once it unfreezes before acting on it.
  **Unfrozen** (noted 2026-10-16): the county layer moved 08-28 (+6,222, two member
  municipalities loaded), 09-10 (+1,588, Laurentian Hills) and last on 09-24, so the
  precondition is met; `.claude/skills/data-integrity/health.py --drift` is ready to run.
  **Run 2026-10-16: nothing to do.** All 33 "new" fields are empty NENA schema slots - 0 of
  46,965 rows filled each (A5, AddCode, AddNum_Pre, Post_Code, Post_Comm, LSt_*, St_PreMod,
  Floor, Room, Seat, ...). Every *filled* live field missing from props is already in
  `ignore_fields` or volatile ESRI/edit metadata. None ignored pre-emptively, by the rule
  above: Post_Code and the street parts would carry address content if filled.

Static sources (toronto, waterloo) cannot be probed this way — no layer metadata to ask.
