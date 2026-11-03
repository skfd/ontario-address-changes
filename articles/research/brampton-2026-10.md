# Research notes — Brampton, 2026-10

Raw findings behind `articles/researched/brampton-2026-10.md`. Notes, not prose.
Window researched: net 2026-09-30 → 2026-10-31 (26 snapshots inside the month; 30 pull
days, 0 failed). Research done 2026-11-03.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **SNIPPET** = seen only in a search-engine summary; the page itself could not
be read — do not print. **EMPTY** = searched, nothing found. Every claim carries a URL.

Source caveat (as in September): the City's monthly addressing lists live at URLs named
only by month and are overwritten each year. On 2026-11-03 `September.pdf` is the
September 2026 list (PDF created 2026-10-30, pages "Printed: October 14, 2026");
`October.pdf` still serves October 2025 (created 2025-11-28). The October 2026 list,
and with it the October two-unit register, is not published yet.

---

## 0. Store-side findings (this repo, not the web)

Net, 09-30 → 10-31: rows 249,740 → 250,071 (+331); added 348, removed 17, location 1
(floor 25 m), significant 36, 3 split events. Gross: added 348, removed 17, location 1,
significant 107. No HELD events; no open or reviewed flag for brampton in October.

**Quarter-million.** Row count by snapshot: 10-23 249,999; 10-24 250,006. The file
first holds more than 250,000 rows on the 24 October snapshot. (Rows, not distinct
addresses; the brief's "rows" line.)

**Added 348, by kind (`PROP_CODE_DESC` on the new row):** Single Family Detached 240,
Semi Detached 48, Commercial 23, Freehold Townhouse 20, Stacked Townhouse 8, Industrial
Condo 4, Industrial 2, Live/Work Commercial 1, Link Home 1, Day Care 1. By unit: 263
unit "2", 55 no unit, 30 other units.

Decomposition: 263 Unit 2s on existing houses (§3); 44 on Glowing Cres + Carl Finlay Dr
(§1); 16 units at 50 Sunny Meadow Blvd (§5); 8 Palleschi Dr (§6); 4 units at 2
Automatic Rd, 3 at Eamont St; 1-247 Main St N (§2); 612 Fogal Rd (§4); scattered
units: 1-9415 Clarkway Dr, 101-8 Sea Lion Rd, 103-6161 Mayfield Rd, 3-20 Whybank Dr,
402-60 Gillingham Dr, 7-10 Tasker Rd; 26 Cornwall Rd, 36 Ryegrass Cres.

**Unit 2s:** 263, on 230 distinct streets, every ward (6: 67, 10: 43, 4: 27, 5: 25, 9:
25, 8: 20, 2: 19, 7: 15, 1: 12, 3: 10). Property code: SFD 194, Semi 48, Freehold
Townhouse 20, Link Home 1. Added on 18 different snapshots, up to 27 a day (10-07).
Thornbird Cres's 15 and Brisdale Dr's 4 "gains" in the brief are all Unit 2s (Thornbird:
2-14 … 2-82, Freehold Townhouse, ward 6, eight different days). Earlier months (Sept
notes): Jul 265, Aug 243, Sep 246.

**Wards gaining:** 10 +89 = 32 Glowing + 12 Carl Finlay + 43 Unit 2s + 2 commercial
units. 6 +70, 9 +42.

**Removed 17:**
- 8 commercial units at the McVean Dr plaza, all on the 10-16 snapshot (last seen
  10-15): 41- and 42-11615, 33-11625, 56- and 61-11635, 24-11645, 67-11665, 72-11695
  McVean Dr. All Commercial, ward 10. 61-11635 had only been on file since 09-22. Bases
  and the other units remain (e.g. 11615: 201–211, 34–40 still present).
- 247 Main St N (Office, HERITAGE "DESIGNATED", id 1723918) → see §2.
- 10-23: 5759 Mayfield Rd (Farm, ward 10), 8331 Heritage Rd (Farm, ward 6), 146
  Salvation Rd (Commercial) and 150 Salvation Rd (Other), both ward 6, and one
  "UNASSIGNED" record coded Vacant Institutional (ward 6).
- 10-20: 622-25 Peel Centre Dr (Commercial unit, ward 7).
- 10-30: 122 Eldomar Ave and 2-122 Eldomar Ave (SFD + its Unit 2, ward 3), together.

**Modified (net 36):** PROP_CODE_DESC 18 (Corporation Dr units → Commercial, 4 Newkirk
Crt units Commercial → Industrial, 3 Hansen Rd N Unit 2s SFD → Semi, etc.);
SITE_PLAN_NUMBER 8 (21–27 Clarence St gain SPA-2020-0157; 30/32 McLaughlin Rd N flip
back from SPA-2020-0034 to -0035, the reverse of September's edit); 0 McVean Dr (§1);
50 Sunny Meadow Blvd base moved 64 m on 10-22; 18 Corporation Dr PRIMARY → FRONTDOOR;
the usual oscillating rows (0 Fairhill Ave ↔ 0 Salvation Rd, UNASSIGNED ↔ Queen St E,
unit-in-number toggles at 5-15 Ashby Field, 11-17 Ray Lawson, 5-65 Romilly, 2-63
Seachart, 14-16 Strathearn).

**Gross vs net, significant 107 vs 36:** 45 of the gross are one edit on 10-24 (the
assumption date on the Glowing/Carl Finlay rows, §1, which net does not see because
those rows did not exist at the opening snapshot); most of the rest are the
oscillating rows, on the Sunday snapshots 10-04 (9), 10-11 (12), 10-18 (6) and 10-26
(11, a Monday snapshot after a skipped Sunday).

---

## 1. Glowing Crescent and Carl Finlay Drive 51–73

Store: 10-15 snapshot, 32 addresses on GLOWING CRES (3 to 34, consecutive, every
number) and 12 on CARL FINLAY DR (51 to 73, odd). All Single Family Detached, ward 10,
LOT 16 CON. 9 N.D., `BLOCK_PLAN` 50-2, `SEC_PLAN_AREA` 50, no `REG_PLAN_NUMBER`.
Glowing postal L6W1M3 (sic — an L6W code, a downtown-Brampton prefix; not printed),
Carl Finlay L6P4E2. Carl Finlay 1–50 (and unit 2s) on file since the first snapshot
(06-10).

`--near 10 Glowing Cres`: 59 Carl Finlay Dr 26 m, 0 McVean Dr 57 m, 14 Avatar Cres 70 m,
43 Trail Rider Dr 104 m, 2-4 Buttonwood Rd 117 m. `--near 34 Glowing Cres`: 2-32
Possession Cres 23 m, 9 Platoon Cres 92 m, 11 Autumn Olive Way 107 m. So Glowing sits
inside an already-built street grid west of McVean Drive. 11615 McVean Dr (the plaza,
§7) is at 43.80916, −79.73603, about 600 m northwest.

0 McVean Dr (id 1735824), same lot 16 Con 9 N.D., block plan 50-2: coded **Farm**
06-10 .. 10-14; on the 10-15 snapshot (the same day as the 44) recoded **Single Family
Detached**, moved ~45 m, `GIS_ID` 151065 → 1706980. It carried
`REG_PLAN_ASSUMP_DATE` 1675814400000 (= 2023-02-08). The 44 new rows arrived with the
same value; on the 10-24 snapshot all 45 had it blanked.

- **EMPTY** — "Glowing Crescent" Brampton: no result; search returns other streets only.
- **EMPTY** — not on the City's September 2026 Municipal Addressing List (M2198 Ovenbird
  Cir / Mustafa Cres is that list's only registered plan; see §4).
  https://www.brampton.ca/EN/residents/Building-Permits/homeowners/Municipal%20Addressing%20List/September.pdf
- **SNIPPET, not used** — a City planning notice for a Weston Consulting application at
  11423 McVean (file 21T-17003B, about 2017) shows Carl Finlay Drive on its location
  map, "four residential blocks … 14 single-detached lots". Different lot count, no date,
  not shown to be this land. Not printed.
- **SNIPPET, not used** — listings place Carl Finlay Dr in "Toronto Gore Rural Estate",
  cross streets given as "MARTIN BYRES/ COUNTRYSIDE DR". Not printed.
- **INFERENCE, printed as such** — the farm-coded point on the same lot was recoded the
  same day; the file records the coincidence, not a severance or plan.

## 2. 247 Main Street North

Store: 247 MAIN ST N, id 1723918, Office, HERITAGE DESIGNATED, SITE_PLAN SP99-098,
ward 1; last on 10-06. On 10-07 a new record 1-247 MAIN ST N, id 333562369, unit 1,
**Day Care**, same heritage flag and site plan, 4 m from the old point. No plain 247
remains. Counted as 1 removed + 1 added.

- **FACT** — City of Brampton By-law 64-2009, designating 247 Main Street North under
  Part IV of the Ontario Heritage Act (PDF created 2009-08-06; passing date illegible in
  the scan). Schedule B: "a very good example of late 19th century masonry,
  multi-gabled residences"; "This vernacular Queen Anne style home"; "reflects the work
  of Jesse Perry, a well-known builder in Brampton"; associated with "Benjamin Justin. B.
  Justin practiced law in Brampton for many years and was later appointed Judge. He held
  this position until 1932. He also served as the town mayor for a three-year term from
  1903-1905"; "functions as a landmark on Main Street North"; "part of the Washington
  Block"; "in 1978 part of the property was granted to the City for the expansion of
  Highway 10 (Main Street)".
  https://www.brampton.ca/EN/City-Hall/Bylaws/Archive/064-2009.pdf
- **SNIPPET, not used** — the City's heritage plaque brochure reportedly calls it the
  Justin House; not read. Not printed.
- **SNIPPET, not used** — a commercial listing offered 247 with 249 Main St N together;
  undated. Not printed.
- **EMPTY** — no licence, operator, permit or notice naming a day care at 247 Main St N.
  Record silent on who, or whether one operates there yet.

## 3. The Unit 2s and the City's September two-unit register

- **FACT** — September 2026 Municipal Addressing List, "REGISTERED TWO UNITS
  DWELLINGS", "Registration Date: As of: September 01, 2026 - September 30, 2026",
  "Printed: October 14, 2026", 10 pages: 236 entries "<number> <street>, Unit #2".
  Front page also lists "Three Unit Dwelling" for 37 Rainforest Drive, Unit #3 and 30
  Stanley Carberry Drive, Unit #3.
  https://www.brampton.ca/EN/residents/Building-Permits/homeowners/Municipal%20Addressing%20List/September.pdf
- **Store cross-check** — of the 236, 231 matched a September Unit 2 automatically (by
  civic number + street); the other 5 checked by hand with lookup.py: 2-338 Hansen Rd N
  (09-17), 2-177 Rutherford Rd N (09-10), 2-66 Buckland Way (09-09), 2-114 Turquoise
  Cres (09-05) — all September Unit 2s, so 235 of 236. The last, "10 Pauline Cres Unit 4,
  Unit #2", lines up with 4A-10 Pauline Cres, added 09-30 (units 1–4 on file since June).
  Carl Finlay Dr: numbers 1–49 (with gaps) on file since 06-10. None matched an
  October addition. So September's register ↔ September's file, as August's did.
- **INFERENCE, printed as such** — October's 263 are the same kind of record; the
  City's October register is not published, so it cannot be matched yet.
- Background from September notes (still valid): ARU page and By-law 157-2022.
  https://www.brampton.ca/EN/residents/Building-Permits/second-dwelling

## 4. 612 Fogal Road

Store: 612 FOGAL RD, Live/Work Commercial, ward 8, added 10-07. 602 on file since 06-10,
608 since 06-26, 620/622 since 07-11, 610 since 09-25. 138 Falby Rd's row changed on
09-15 (September notes: Live/Work Residential → Live/Work Commercial).

- **FACT** — September 2026 list, "TOWNHOUSES LIVE WORK Commercial Portion only": "M2143
  BLK 13 … 612 Fogal Road — Commercial Portion of Live Work at 138 Falby Road" (also
  602/608/610 for 148/142/140 Falby, 620 for 138 and 622 for 128 Falby).
  Same URL as §3.
- **INFERENCE** — the list (printed 14 Oct) assigns 612 to the shopfront of the live/work
  townhouse at 138 Falby; the file had it on the 7th. Printed as such.

## 5. 50 Sunny Meadow Boulevard

Store: base 50 SUNNY MEADOW BLVD, FRONTDOOR, Commercial, SP06-077, ward 9; moved 64 m on
10-22. 16 new units (201–203, 213–216, 218, 223, 224, 305, 306, 308, 313, 315, 318) on
10-22 (3), 10-23 (12), 10-29 (1); 54 units on file at month end. Other unit points were
reissued/re-placed on 10-22 (many spans close 10-21 and reopen 10-22) — not counted as
added because ids carried; not unpicked further.

- **FACT (listing)** — LoopNet: "50 Sunny Meadow Blvd - Sunny Meadow Medical Center",
  condo units 747–1,448 SF (Jan 2024 listing).
  https://loopnet.ca/Listing/50-Sunny-Meadow-Blvd-Brampton-ON/31643326
- **EMPTY** — no City notice explaining new unit numbers in October. Record silent.

## 6. Palleschi Drive 100–170

Store: 100, 110, 120 … 170 PALLESCHI DR (step of 10), Stacked Townhouse, ward 8, all on
10-21, SEC_PLAN_AREA 41, LOT 5 CON. 9 N.D. `--near 100 Palleschi`: 4320 Queen St E 108 m,
55 Attmar Dr 144 m, 8710 The Gore Rd 164 m. Palleschi 2–14 etc. on file since 06-10.

- **EMPTY** — no development application, site plan or addressing-list entry for these
  numbers (not on the September list). Listings on the street are for existing freehold
  towns (67, 10 Palleschi). Record silent.

## 7. McVean Drive plaza units

- **SNIPPET/listing, not used for the retirement** — RE/MAX listings describe 11645
  McVean as "a brand new 100% commercial retail plaza located at Mayfield Rd & Mcvean
  Dr", and 11615 McVean as a plaza at the same corner.
  https://www.remax.ca/on/brampton-toronto-gore-rural-estate-real-estate/20-11645-mcvean-drive-wp_idm73000004-28800714-lst
- **EMPTY** — nothing on why eight unit numbers (one of them only a month old) left on
  one day. Record silent.

## 8. Other retirements

- **EMPTY** — 5759 Mayfield Rd (farm; 127 m from the centre of September's Plan M2197
  streets per September notes), 8331 Heritage Rd (farm), 146/150 Salvation Rd, 122
  Eldomar Ave, 622-25 Peel Centre Dr: not searched beyond a pass; nothing found. Record
  silent.

## Not researched

2 Automatic Rd units (Industrial Condo, SP03-059), 25/15 Eamont St units, the scattered
commercial units, the PROP_CODE_DESC recodes, the oscillating rows (source behaviour,
described from the store).
