# Research notes — Toronto, 2026-10

Raw findings behind `articles/researched/toronto-2026-10.md`. Notes, not prose.
Window researched: snapshots 2026-09-30 → 2026-10-30 (16 snapshots in the month; there is
no snapshot between 2 and 8 October). Research done 2026-11-10: store-side checks and the
City's open data by hand, plus three parallel web passes (Sugar Maple Way; Allanhurst,
Bathurst/Adelaide and Golden Ave; place names and downtown numbers), merged here.

Conventions as in earlier months: **FACT** = the linked page or record says it.
**INFERENCE** = a reading, not the source's. **SNIPPET** = seen only in a search-engine
summary — check by hand before printing. Every claim carries a URL. Empty searches are
recorded as results.

CKAN URL form (Toronto open data, `datastore_search`):
`https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=<RID>&filters=%7B%22STREET_NAME%22%3A%22<NAME>%22%2C%22STREET_NUM%22%3A%22<NUM>%22%7D`
Resource ids — DA development applications `8907d8ed-c515-4ce9-b674-9f8c6eefcf0d`;
BPa building permits active `6d0229af-bc54-46de-9c2b-26759b01dd05`; BPc cleared
`a96c0ba4-3026-402b-b09d-5b1268b8f810`; CoA-A Committee of Adjustment active
`51fd09cd-99d6-430a-9d42-c24a937b0cb0`; CoA-C closed `9c97254e-5460-4799-896f-c7823413c81c`.
Written below as e.g. BPc(ALLANHURST,100). All CKAN records read 2026-11-10.

---

## 0. Store-side findings (this repo, not the web)

- **Flags:** `python run.py flags` (2026-11-10) lists 23 open flags, none for toronto; the
  brief's `held_events` is empty.
- **Brief (2026-11-10):** net added 49, removed 32, status 48 (RESERVED→REGULAR), location 6,
  renumbered 3, significant 8, split events 3; rows 525,364 → 525,381 (+17). Gross: status 49,
  significant 7, the rest equal to net. Observed 30 pull days, 0 failed.
- **Derived from the net diff (snapshot ids 136 → 165), recomputed in code:**
  - 49 added = **37 addresses new to the file + 12 second points** for an address already on
    file (12 Benton Rd, 1117 Dundas St W, 62 Elmcrest Rd, 1197 Glencairn Ave, 3465 Keele St,
    186 and 188 Millwood Rd, 350 Passmore Ave, 1 The Bridle Path, 20 Verwood Ave,
    302 Wolverleigh Blvd, 39 Yorkleigh Ave). 33 of the 49 are RESERVED, 16 REGULAR.
  - 32 removed = **19 whose address stays on file under another point + 13 that left**:
    100 Allanhurst Dr, 103 Bathurst St, 37 Blue Springs Rd, 1125 Dundas St W, 69A Eighth St,
    2165 Gerrard St E, 107 Holborne Ave, 211 Mavety St, 15 Medford Ave, 670 Old Weston Rd,
    116 Pape Ave, 540 Pharmacy Ave, 38 Rockcliffe Blvd. All 32 had been on file since the
    first snapshot (2025-04-01).
  - RESERVED→REGULAR: 48 status-only + 4 that also moved (543 and 551 Adelaide St W,
    115 Bathurst St, 57 Balliol St) = **52 put in service**. All 52 on file since 2025-04-01.
  - The 8 "significant": those 4; two place-name-plus-move (38 Burton Rd, 1050 Military Trl);
    417V → 417 1/2 Westmount Ave with a small move; 110 Turnberry Ave → 125 Benny Stark St.
- **Daily timeline (snapshot pairs):**
  - 09-30 → 10-01: 18 removed, 32 status-only, 3 status+move. Removed and paired the same
    snapshot: 100 Allanhurst Dr (10 and 20 Mulham Pl go regular); 103 Bathurst St (111, 115
    Bathurst, 543, 551 Adelaide W go regular); 2165 Gerrard St E (2165A–D); 107 Holborne Ave
    (107A/B); 15 Medford Ave (15A/B); 116 Pape Ave (116A/B); 38 Rockcliffe Blvd (38A/B, 40A).
  - 10-01 → 10-02: + 4015 Eglinton Ave W (Land Entrance, regular); swaps at 45, 57 Balliol St
    and 124, 126 Milner Ave.
  - 10-08 → 10-09: 23 added, among them Sugar Maple Way ×6, 1380 Sheppard Ave W, 3465 Keele St
    (second point), 1195/1195R/1197/1197R Glencairn Ave, 239C/239R Aldercrest Rd, 1117/1119
    Dundas St W, 69R Eighth St, 62 Elmcrest Rd + 4 Laver Rd, 555 Glebeholme Blvd +
    302 Wolverleigh Blvd, 37/39 Yorkleigh Ave. Removed 1125 Dundas St W, 69A Eighth St.
    38 Burton Rd labelled; 130V → 130 1/2 Courcelette Rd; 417V → 417 1/2 Westmount Ave;
    71 → 69 Park Lane Crcl.
  - 10-09 → 10-12: + 85 Roselawn Ave, 127A/127B Watson Ave, 19 Yonge St, 22A Yonge St.
  - 10-14 → 10-15: + 73 Balliol St. 10-15 → 10-16: + 22 Penwood Cres (Winfields Park),
    16R Vanevery St; five Cornwall St points move 51–98 m.
  - 10-16 → 10-19: − 211 Mavety St. 10-19 → 10-20: 1050 Military Trl labelled.
  - 10-21 → 10-22: 110 Turnberry Ave (reserved second point) → 125 Benny Stark St.
  - 10-22 → 10-26: + 90R Douglas Ave, 343R Greenwood Ave, 350/350R Passmore Ave, 18/20 Verwood Ave.
  - 10-26 → 10-28: + 1B–1E Golden Ave, 2429 Bayview Ave, 1 The Bridle Path (second point).
  - 10-28 → 10-29: 227/229/231 Falstaff Ave, 27 Indian Road Cres, 1985 Kipling Ave go regular;
    swaps at 25 Indian Road Cres, 1983 Kipling Ave.
  - 10-29 → 10-30: + 12 Benton Rd, 8 Jodphur Ave, 354 King St W, 186/188 Millwood Rd;
    − 37 Blue Springs Rd, 670 Old Weston Rd, 540 Pharmacy Ave (540A/B go regular), swaps at
    190 Dixon Rd, 789 Euclid Ave; 118 → 120 Anndale Dr; 16 Benton Rd moves 77 m.
  - Note 37 Blue Springs Rd left on 10-30, a day after 227–231 Falstaff went regular (10-29).
- **Sugar Maple Way:** 100, 105, 110, 145, 195, 205, all Land, RESERVED, York Centre, ids
  60089947–60089953 (no 60089949); 1380 Sheppard Ave W is 60089955 and the second 3465 Keele St
  point 60089956 — one id run, one snapshot. `--near 145 Sugar Maple Way`: 1380 Sheppard Ave W
  126 m, 10 Carl Hall Rd 183 m, 3465 Keele St 213 m, 75 Canuck Ave 267 m. No near-match
  street name in the store (it is a debut, not a respelling).
- **125 Benny Stark St is not a rename.** Point 60036302, a RESERVED Land second point at
  110 Turnberry Ave since 2025-09-09, was relabelled 125 Benny Stark St and moved ~70 m on the
  10-22 snapshot. A REGULAR 125 Benny Stark St (10636255) and a REGULAR 110 Turnberry Ave
  (14038818) were on file before and after. Benny Stark St itself has been in the file since
  the first snapshot. So: 125 Benny Stark St now has two points, 110 Turnberry Ave one.
- **1 Golden Ave:** the base point (10758922, Structure, REGULAR) stays and moved a few metres
  on 10-28; 1B, 1C, 1D, 1E are new REGULAR Structure points in a line running north-east from
  it; no 1A on file. `--near`: 2112 Dundas St W 15 m, 25 Silver Ave 52 m, 2 Howard Park Ave 67 m.
- **239 Aldercrest Rd:** 239A and 239B have been RESERVED Land points since 2025-09-09; October
  adds 239C and 239R as RESERVED Structures. The brief's "239 → 239C, 239R" is the second half
  of a set, not a two-way split.
- **127 Watson Ave:** 127A/127B new RESERVED Land, 127 remains.
- **1195/1197 Glencairn Ave:** 1195, 1195R, 1197R new and a second 1197 point, all RESERVED.
- **Balliol St:** 73 Balliol St new on 10-15; the same snapshot reclasses 61–89 Balliol from
  Structure Entrance to Structure and nudges them. Store-only; not researched.
- **Cornwall St (10-16):** 50, 82, 84, 118 and 120 Cornwall St moved 51–98 m; 120 carries
  *Oak Street Housing Co-Op*. 118 and 120 moved west, 50/82/84 east — they look like points
  swapping ends of one block. No address changed.
- **Renumbers:** 118 Anndale Dr → 120 (10-30; no other 120 or 118 on file); 71 Park Lane Crcl
  → 69 (10-09; no other 69 or 71); 130V Courcelette Rd → 130 1/2 and 417V Westmount Ave →
  417 1/2 (both 10-09) — a `V` suffix restated as a half number.

---

## 1. The City's open data, per address (CKAN, read 2026-11-10)

**100 Allanhurst Dr → 10 / 20 Mulham Pl (file: 1 Oct)**
- FACT — BPc(ALLANHURST,100): `24 112413 DEM`, Elementary School, "Proposed demolition of
  existing 1 storey brick school with parking area."; applied 2024-02-06, issued 2024-10-30,
  **completed 2026-09-30**, Closed.
- FACT — BPa(ALLANHURST,100): `24 112377 BLD`, Elementary School, New Building: "Proposed
  demolition of existing 1 storey brick school with parking area and construction of new 2
  storey replacement elementary school and child care centre, complete with associated parking
  (48 spaces), site servicing, play areas and landscaping."; applied 2024-02-06, issued
  2025-04-24, status Inspection (still open).
- FACT — DA(ALLANHURST,100): `22 240161 WET 02 SA`, site plan, submitted 2022-12-16, Closed:
  "Proposed 2 storey, elementary school, child care centre, and associated parking, play fields
  and child care play yard."
- EMPTY — nothing in any of the five resources under MULHAM 10 or MULHAM 20.
- Lag: demolition permit closed 30 Sep 2026 → 100 Allanhurst gone from the 1 Oct snapshot
  (last seen 30 Sep). Next-day.

**103 Bathurst St → 111, 115 Bathurst St, 543, 551 Adelaide St W (file: 1 Oct)**
- FACT — DA(BATHURST,103) and (BATHURST,111): `11 289519 STE 20 OZ` and `11 289522 STE 20 SA`,
  submitted 2011-10-07: "a new 17 storey mixed use building complete with 2 stories of
  commmercial floor area (2375m2) and 255 resdiential units above"; `16 115615 STE 20 CD`,
  submitted 2016-02-11, draft plan of condominium, "17 storey mixed use building, comprised of
  256 units … Rezoning: 11-289519 STE 20 OZ, By-law 494-2014 (OMB)". All Closed.
- FACT — CoA-C(BATHURST,103): consent filed 2016-05-27, "To obtain consent to sever the
  property into four lots, create various easements/rights-of-way…", approved 2016-09-07,
  final 2017-02-14. CoA-C(ADELAIDE,543): 2018 consent refining the easements "created by
  Consent Decision B0028/16TEY", final 2018-07-20.
- FACT — BPc(BATHURST,103): `13 206962 BLD`, Mixed Use/Res w Non Res, New Building, "Proposal
  for a new 17 storey mixed use building, comprised of 225 residential units, 1,398 metre
  square of office uses and 945 metre square of retail space…", applied 2013-07-19, issued
  2015-01-07, **completed 2017-01-19**. (Unit count differs from the planning files' 255/256.)
- FACT — BPa(BATHURST,103) and (BATHURST,115): permits from 2016–17 for a ground-floor
  restaurant "with micro-brewery and retail" and office alterations. DA(ADELAIDE,543),
  (ADELAIDE,551), (BATHURST,115): the same 2011 rezoning file lists all of these numbers.
- INFERENCE (medium): the four reserved numbers are the four lots of the 2016 severance of
  a building whose permit closed in January 2017 — nothing ties a number to a lot, and the
  article does not say so; the file retired the single old number and put
  the four in service on 1 Oct 2026. Nothing in the open data says why now.

**Severances whose old number left as the lettered ones went regular (all 1 Oct unless noted)**
- **2165 Gerrard St E → 2165A–D.** FACT — BPc(GERRARD,2165): `22 149110 BLD` and
  `22 149146 BLD`, each "new 3 storey semi-detached fourplex", 4 units each; `22 149130 BLD`
  and `22 149158 BLD`, each "new 2 storey laneway suite at rear of 2165 Gerrard St." (Part A,
  Part B); all applied 2022-05-19, issued July 2023, **completed 2025-04-29**. `22 149167 DEM`
  (the detached house) completed 2024-10-08. CoA-C: a 2020 three-lot severance withdrawn; a
  2020 two-lot consent **Refused** 2020-12-02, record final 2023-04-06 (an appeal outcome is
  not in the open data). Lag: buildings complete → file, 17 months. Ten homes on the lot per
  the permits (4+4+1+1); the file has four numbers (A, C Land; B, D Structure).
- **107 Holborne Ave → 107A/B.** FACT — CoA-C(HOLBORNE,107): consent "to sever an existing
  residential lot into two undersized residential lots", approved 2022-09-14, final 2023-06-06.
  BPc: `23 181576 BLD` / `23 181578 BLD` (West House, East House), **completed 2024-10-18**;
  `23 181577 DEM` completed 2023-10-16. Lag ≈ 23½ months from completion.
- **15 Medford Ave → 15A/B.** FACT — CoA-C(MEDFORD,15): consent "to sever one lot into two
  residential lots", approved 2022-03-10, final 2022-09-20. BPc `22 217816 BLD` (15B) completed
  2025-01-09; BPa `22 217761 BLD` (15A) still at Inspection. Permit text itself says "15A
  Medford" / "15B Medford Ave." Demolition `22 217811 DEM` completed 2025-01-09.
- **116 Pape Ave → 116A/B.** FACT — CoA-C(PAPE,116): consent approved 2021-10-27, final
  2022-12-01. BPa `23 177518 BLD` and `23 177539 BLD`, two three-storey detached houses, both
  still at Inspection; `23 177551 DEM` completed 2025-08-24.
- **540 Pharmacy Ave → 540A/B (30 Oct).** FACT — CoA-C(PHARMACY,540): consent "to sever the
  property into two residential lots (Part 1 and Part 2), and convey a land widening to the
  City (Part 3)", approved 2022-04-05, final 2023-04-03. BPa `23 179527 BLD` / `23 179557 BLD`
  at Inspection; `23 179544 DEM` **completed 2025-10-17**. Lag from demolition closed: 12 months.
- **38 Rockcliffe Blvd → 38A/B (and 40A's swap).** FACT — CoA-A/C(ROCKCLIFFE,38): a 2020
  two-lot consent (approved 2020-11-05, still "Conditional Consent"); 2021 consents making
  "a total of three residential lots", approved 2022-04-05, final 2023-01-03; 2022 permits for
  two semis **Cancelled** 2022-12-09; a five-unit multiplex variance **Refused** 2026-02-26;
  BPa `26 257201 BLD` and `26 257255 BLD`, applied **2026-10-20**, each "a new semi-detached
  houseplex (4 units)", status Not Started. So the file put 38A/38B in service three weeks
  *before* the current permits were even applied for, with the old house's demolition not yet
  permitted. The file ran ahead here.
- **37 Blue Springs Rd → 227, 229, 231 Falstaff Ave (29/30 Oct).** FACT — BPa/BPc(BLUE
  SPRINGS,37): "demolish the existing 2 storey SFD-detached dwelling and sever the lot into 3
  parcels. A new 2 storey SFD-detached dwelling to be constructed on each new lot created" —
  Lot 1 West `22 111602`, Lot 2 Centre `22 111799` (both Inspection), Lot 3 East `22 113001`
  completed 2025-05-07; demolition `22 111642` completed 2022-10-05. CoA-C: the 2017 three-lot
  consent was **Refused** 2019-06-06, record final 2021-07-06 (appeal outcome not in open
  data; permits issued May 2022 imply it was allowed). EMPTY under FALSTAFF 229. `--near` not
  run; INFERENCE medium-high that the three Falstaff numbers are the three lots (corner lot
  re-fronted onto Falstaff): same two snapshots, coordinates within ~30 m of 37 Blue Springs.

**New reserved numbers (9 Oct unless noted)**
- **1195/1195R/1197/1197R Glencairn Ave.** FACT — CoA-A(GLENCAIRN,1197): consent filed
  2026-04-14 "to sever the property into two residential lots. File Nos. B0008/26NY,
  A0133/26NY and A0134/26NY will be jointly considered", heard and **approved 2026-07-23**,
  Conditional Consent (conditions to 30 Jul 2027). BPa: `26 233464 BLD` applied 2026-09-08,
  "new three-storey triplex with a detached garden suite in the rear yard"; `26 236856 BLD`
  applied 2026-09-14, "new 3 storey dwelling (fourplex) application pertains to the proposed
  severd lot municipally known as 1195 Glencairn Ave"; `26 236865 BLD` garden suite (Refusal
  Notice); `26 233495 DEM`. Lag: approval → file 78 days; the permit application used the
  number "1195" 25 days before the file had it. R = the two garden suites (INFERENCE high —
  two R points classed Structure behind two Land points; Hamilton-style R rule noted in June).
- **127 Watson Ave → 127A/B (12 Oct).** FACT — CoA-C(WATSON,127): consent filed 2025-09-18
  "to sever the property into two undersized residential lots", approved 2026-01-21, record
  final **2026-11-02**. File 21 days ahead of finality.
- **62 Elmcrest Rd (second point) + 4 Laver Rd.** FACT — CoA-A(ELMCREST,62): consent filed
  2023-06-22 "to sever the property into a total of two residential lots", approved
  2026-02-26, Conditional Consent. INFERENCE medium: corner lot, new lot fronts Laver.
- **37/39 Yorkleigh Ave.** FACT — CoA-A(YORKLEIGH,39): consent filed 2023-11-29 "to sever the
  property into two undersized residential lots", **Refused** 2025-05-01, yet status reads
  "Conditional Consent" — contradictory in the record itself; appeal outcome not in open data.
  Not printed.
- **239C/239R Aldercrest Rd.** FACT — CoA-A(ALDERCREST,239): two-lot consent filed 2024-01-12,
  **Refused** 2024-06-06, status "TLAB Appeal". BPa `25 208101 BLD`, "Proposed 2-storey semi
  detached dwelling with basement apartment. (Lot 1)", issued 2025-11-24, Inspection. Outcome
  of the appeal not in open data. Not printed beyond the store facts.
- **1117 (second point) / 1119 Dundas St W; 1125 retired.** FACT — DA(DUNDAS,1117):
  `23 237080 STE 10 OZ`, submitted 2023-12-19, "A City-initiated combined Official Plan &
  Zoning By-law Amendment application for a 10-storey, mass timber, mixed-use building
  containing 94 dwelling units (with a portion of them being affordable units)…", Closed;
  `26 137976 STE 10 SA`, submitted **2026-04-01**, Under Review, "Site Plan Approval for a 10
  storey residential building with 74 dwelling units, 23 of which will be affordable housing
  and a one-storey ancillary building at the rear of the site." 1125 Dundas St W (a Structure
  Entrance) left the same snapshot; EMPTY under DUNDAS 1125. INFERENCE medium-high: 1119 (a
  Structure point) is the ancillary building or the new building; unsourced.
- **90R Douglas Ave (26 Oct, regular).** FACT — BPc(DOUGLAS,90): `24 249497 BLD`, Laneway /
  Rear Yard Suite, "demolish existing sigle garage and build a two storey lane way house suite
  in backyard", issued 2025-11-21, **completed 2026-10-05**. Lag 21 days.
- **343R Greenwood Ave (26 Oct, regular).** FACT — CoA-A(GREENWOOD,343): variance filed
  2026-10-01 "to permit and maintain the existing building height, and rear (east) covered
  ground floor deck … of the existing rear two-storey ancillary building (laneway suite) which
  was constructed beyond the limits of the approved building permit", hearing 2026-11-25.
- **16R Vanevery St (16 Oct, regular).** FACT — BPa(VANEVERY,16): `25 165719 BLD` new 3 storey
  fourplex, issued 2025-08-26, Inspection; `25 230728 BLD`, Laneway / Rear Yard Suite,
  "Proposal to construct a new 2 storey garden suite.", issued 2026-01-09, Inspection.
  CoA-C: "To construct a new fourplex and a garden suite in the rear yard.", approved
  2025-07-24. INFERENCE high: 16R is the garden suite. Not printed (length).
- **18/20 Verwood Ave (26 Oct).** BPc(VERWOOD,20): replacement house completed 2025-07-17. No
  severance found. Silent on why a reserved 18 and second 20 appeared.
- **69A → 69R Eighth St (9 Oct).** FACT — BPa(EIGHTH,69): `25 134412 BLD` "interior
  alterations from 1 dwelling unit to 4 dwelling units", issued 2025-05-27; `26 106900 BLD`,
  Laneway / Rear Yard Suite, "Proposed garden suite", issued 2026-02-18, Inspection.
  INFERENCE medium-high: 69R is the garden suite; 69A (a Structure point) left the same
  snapshot. Not printed (length).
- **354 King St W (30 Oct).** FACT — BPc(KING,354): `18 270422 BLD`, Restaurant 30 Seats or
  Less, "Proposed interior alterations to existing restaurant on basement and ground level.",
  issued 2019-01-07, completed 2020-03-16. The number was in use in 2018; not silent.
- **186/188 Millwood Rd (second points, 30 Oct).** FACT — BPa(MILLWOOD,186) `24 232761 BLD`
  interior alterations to a semi; BPc(MILLWOOD,188) `24 238948 BLD` "convert existing three
  dwelling units to single dwelling unit", completed 2025-10-08. Nothing explains a reserved
  second point at each. Not printed.
- EMPTY (all five resources; second pass run per address with no row cap — the first pass
  capped rows across addresses and hid records, so only this list is to be trusted):
  1380 Sheppard Ave W; 2429 Bayview Ave; 1 The Bridle Path (tried STREET_NAME `THE BRIDLE`,
  `BRIDLE`, `THE BRIDLE PATH`, `BRIDLE PATH`); 19 Yonge St; 22A Yonge St; 73 Balliol St;
  85 Roselawn Ave; 8 Jodphur Ave; 350 Passmore Ave; 1 Golden Ave; 10 and 20 Mulham Pl;
  1125 Dundas St W; 302 Wolverleigh Blvd; 555 Glebeholme Blvd; 4 Laver Rd; 38 Burton Rd.
  First pass only (rows may have been hidden, not printed in the article): 4015 Eglinton
  Ave W; 211 Mavety St; 670 Old Weston Rd; 130 Courcelette Rd; 110 Turnberry Ave;
  118 Anndale Dr.

**William Baker (3465 Keele St)**
- FACT — DA(KEELE,3465): `21 119571 NNY 06 OZ`, submitted 2021-02-24, Closed: "Zoning By Law
  Amendment and concurrent Draft Plan of Subdvision applications to create 13 blocks within the
  William Baker Neighbourhood. Planned as new inclusive, compact and complete community that is
  walkable and well served by transit and active transportation…"; `21 119572 NNY 06 SB`,
  same date, Closed: "Draft plan of Subdivision and concurrent Rezoning applications (Phase 1)
  to create 3 development blocks, 2 public park blocks, a privately owned publicly accessible
  space block, 3 natural heritage woodlot blocks, a new public right-of-way, and road widening
  along Sheppard Avenue West."

**Others**
- **125 Benny Stark St.** FACT — DA(BENNY STARK,125): `21 228594 STE 09 OZ`, submitted
  2021-10-21, "Appeal Received": "redevelopment of the site for a mixed-use development
  comprised of 7 buildings throughout the site, anchored by a public park of approximately
  4,733 square metres"; `21 228596 STE 09 SB`, draft plan of subdivision "for 6 development
  blocks", Under Review. So the reserved point moved from 110 Turnberry onto a redevelopment
  site's number.
- **71 → 69 Park Lane Crcl.** FACT — BPa(PARK LANE,71): `25 226413 BLD`, new two-storey
  detached house, issued 2025-12-24; `25 229205 DEM` issued **2026-11-06**. Nothing says why
  the number changed. EMPTY under 69.
- **1050 Military Trl.** FACT — DA(MILITARY,1050): `20 145765 ESC 25 OZ`, submitted 2020-05-15,
  "Application to lift the Holding Symbol "H" for a proposed 5-storey institutional building,
  known as the Instructional Centre Phase 2 at the University of Toronto Scarborough campus.
  The proposed building will be located on the north corner of Military Trail and Pan Am
  Drive…". 1050 Military Trl is used for many UTSC records (a 2017 residence rezoning, a 2026
  sign permit for another building), so the number is the campus's, not one building's.

---

## 2. 100 Allanhurst Dr — the former Buttonwood school (web)

**Searched:** "100 Allanhurst Drive" Toronto; "Leonardo Da Vinci Academy" Allanhurst; "20 Mulham
Place"; "10 Mulham Place" Etobicoke; "Mulham Place" Toronto TCDSB/Catholic/school/Buttonwood;
"Buttonwood" Catholic school "Mulham".

- FACT (PDF read page by page) — Deputy Mayor Stephen Holyday, letter to Etobicoke York
  Community Council, 13 Sep 2019: "In 2018 the TCDSB purchased the former Buttonwood School
  property at 100 Allanhurst Dr., Ward 2, with the intention to develop an urgently needed new
  elementary school." Also: "The Buttonwood school site is adjacent and contiguous to
  Buttonwood Park, which spans northward to Eglinton Avenue."
  <https://www.toronto.ca/legdocs/mmis/2019/ey/bgrd/backgroundfile-137620.pdf>
- FACT (PDF read) — TCDSB, "Capital Project Status Update — New Catholic School at Buttonwood
  Hill", April 2025: "New Elementary School for 600 students with 5-room childcare"; "it was
  awarded to Pre-Eng Contracting Ltd Jan 2025"; "The existing school demolition is in progress
  and site excavation is at 50% progress."; "Anticipated Opening Date: September 1, 2027
  (construction completion- Spring 2027)"; SPA NOAC "Dec 16, 2024".
  <https://files-backend.assets.thrillshare.com/documents/asset/uploaded_file/2947/Corporateservices/2e407d18-b5fc-409f-bce2-1b223ad06cfe/capital-project-status-update-new-school-at-bu(1)(1).pdf?disposition=inline>
- FACT — Link2Build, 27 Aug 2020: "The school will be located on the former Toronto District
  School Board site at 100 Allanhurst Drive, in Etobicoke."; "The building will also provide 88
  new licensed child-care spaces." <https://www.link2build.ca/news/posts/province-commits-16m-to-etobicoke-school/>
- FACT — TCDSB letter, 11 Jun 2026: "the new Catholic elementary school being built on the
  former Buttonwood Public School site"; "The new boundary configuration will take effect
  beginning with the 2027–2028 school year." No school name given.
  <https://files-backend.assets.thrillshare.com/documents/asset/uploaded_file/2947/Corporateservices/82545c82-54a9-4002-aa8b-00bacddbfc85/New-Buttonwood-Elementary-School---Buttonwood-Boundary-Review-Update---June-11,-2026.pdf?disposition=inline>
- FACT — "TCDSB Projects in SPA", 26 Feb 2025, gives NOAC "Oct 25, 2024" for New Buttonwood
  Elementary (the TCDSB's own update says Dec 16, 2024; not reconciled, not printed).
  <https://www.toronto.ca/legdocs/mmis/2025/ex/bgrd/backgroundfile-253730.pdf>
- SNIPPET (not printed as fact) — Leonardo Da Vinci Academy, a private school, was at the
  Allanhurst campus (ourkids.net review, 403); a June 2019 Villa Charities release says it
  would move to the Columbus Centre, 901 Lawrence Ave W, for September 2020 (globenewswire,
  403). Holy Angels Catholic School was relocated to the Buttonwood site from September 2021
  during its own rebuild (tcdsb.org page would not load).
- EMPTY — "Mulham Place" in any source; nothing in CKAN under MULHAM 10 or 20.
- Store: 10 Mulham Pl is 76 m and 20 Mulham Pl 116 m from the 100 Allanhurst point.
- INFERENCE (medium) — 10 and 20 Mulham Pl are the numbers for the new school and child care.
  No source says so; the article says "nothing names them".
- Lag: demolition permit `24 112413 DEM` completed 2026-09-30 → address off the file at the
  next snapshot (1 Oct). The label "Leonardo Da Vinci Academy" was on the point to the end.

**Confidence:** high on the site's history, the replacement school and the permit date; the
Mulham numbers are an inference; the private school's dates are snippets.

---

## 3. 103 Bathurst St — oneeleven (web)

**Searched:** "543 Adelaide Street West" OR "551 Adelaide Street West" Toronto; "103 Bathurst"
Toronto Adelaide development; "111 Bathurst Street" Toronto development Adelaide urbantoronto.

- FACT — By-law 494-2014(OMB): "with respect to the lands municipally known as 103-111 Bathurst
  Street"; "the total number of dwelling units on the lot does not exceed 255".
  <https://www.toronto.ca/legdocs/bylaws/2014/law0494.pdf>
- FACT — UrbanToronto, 19 Mar 2012: "oneeleven is the name for Harhay Developments and Carttera
  Private Equities 17-storey loft-style condominum building by at 111 Bathurst Street where it
  meets Adelaide West." <https://urbantoronto.ca/news/2012/03/harhay-and-carttera-unveil-oneeleven-condominiums-bathurst>
- FACT — UrbanToronto, 28 May 2012: "Oneeleven will reach 17 storeys, with a total of 255
  units." <https://urbantoronto.ca/news/2012/05/database-project-day-oneeleven-condominiums>
- SNIPPET — completed/registered 2016 (strata.ca; 429 on open). The City's own permits show a
  ground-floor restaurant fit-out in 2016–17 (§1), which is the citable occupancy evidence.
- EMPTY — "543 Adelaide Street West", "551 Adelaide Street West", "115 Bathurst"; any 2026 event.
- INFERENCE (medium) — a decade-old building's four severed lots being put in service; why
  October 2026 is unexplained.

---

## 4. Sugar Maple Way, 1380 Sheppard Ave W, 3465 Keele St (web)

**Searched:** `"Sugar Maple Way" Toronto street naming North York Community Council`; `"Sugar
Maple Way" William Baker Downsview Canada Lands`; `"Sugar Maple Way" "1350 Sheppard" OR "Arbo"
naming public street staff report`; `"Sugar Maple Way" Toronto by-law OR "public highway" OR
"street naming"`; `toronto.ca public notice naming "Sugar Maple Way"`; `"Naming of" "1350
Sheppard Avenue West"`; `"Sugar Maple" by-law "to name"` (last two on toronto.ca).

- EMPTY — no community council naming item, staff report, public notice or by-law for "Sugar
  Maple Way". `secure.toronto.ca` (agenda item 2025.NY24.2, notice 6419) returned 403, so the
  council system itself was not searched. Hand-check before ever saying no by-law exists; the
  article says none was found.
- FACT (re-fetched) — Arbo project site, post dated **17 Aug 2026**: "Phase 1 of Arbo is now a
  Registered Subdivision"; public works created "such as the new Sugar Maple Way street and two
  new local parks"; blocks "will be home to up to 1,700 units" (20% affordable); "preserving 22
  acres of natural environment for public use". No registration date or plan number.
  <https://arbodownsview.ca/latest-updates/subdvision-registration-for-phase-1-arbo-downsview/>
- FACT (re-fetched) — City parks page, modified 11 Jun 2026, map caption: "…the locations of
  Woodland Park and New Park at 1550 Sheppard Ave W, connected by the planned road, Sugar Maple
  Way." Body gives the new park as "1350 Sheppard Ave. W." (the page disagrees with itself);
  "These names are placeholders and are not the official park names."
  <https://www.toronto.ca/city-government/planning-development/construction-new-facilities/park-facility-projects/downsview-parks-rec-facility-projects/new-parks-in-william-baker-district/>
- FACT — Ontario Construction News, 16 Oct 2025, earliest dated use of the name found:
  "Construction of Sugar Maple Way, a new east-west street south of the protected woodlot".
  <https://ontarioconstructionnews.com/canada-lands-to-host-open-house-on-site-preparation-for-arbo-neighbourhood>
- FACT — City staff report, 20 May 2025 (25 124861 NNY 06 OZ): "Zoning By-law 1082-2022 that
  was enacted by Council on July 22, 2022 for the William Baker/Arbo District Phase 1."; "an
  increase of the maximum unit count from 1,400 units to 1,700 units"; "Draft plan approval of
  the plan of subdivision was issued on December 11, 2024."
  <https://www.toronto.ca/legdocs/mmis/2025/ny/bgrd/backgroundfile-255599.pdf>
- FACT — Arbo site, 30 Apr 2026: "The construction of underground infrastructure at Arbo
  started on April 23." <https://arbodownsview.ca/latest-updates/sugar-maple-way-construction-update/>
  27 Jul 2026: "Construction of the new road called Sugar Maple Way is progressing"; "is
  expected to reach the base asphalt stage by late 2026."
  <https://arbodownsview.ca/latest-updates/arbo-phase-1-construction-updates-july-2026/>
- FACT — UrbanToronto, 30 Oct 2026: Phase 1 "approved for eight buildings up to 20 storeys."
  <https://urbantoronto.ca/news/2026/10/canada-lands-advances-second-phase-arbo-downsview.62075>
- FACT — RENX, 12 Dec 2024: "A 9.3-acre ecological park surrounding the woodlot", "A 1.2-acre
  active park", "An 11.9-acre natural heritage woodlot will be transferred to the city".
  <https://renx.ca/canada-lands-arbo-development-takes-its-next-step>
- SNIPPET (not printed as fact) — Canada Lands' Oct 2025 open-house panels: the name "honours
  the 300+ mature Sugar Maples that are being protected on site" (PDF too large to open).
  <https://www.clc-sic.ca/sites/default/files/documents/Panels%20-%20ARBO%20-%20Oct%2023%20Open%20House%20-%20English.pdf>
  City reports of 2022/2024 call the road "Street A".
- EMPTY — no source mentions 1380 Sheppard Ave W, the second 3465 Keele St point, or any Sugar
  Maple Way number; no builder named.
- Lag: registration announced 17 Aug 2026 → numbers reserved by the 9 Oct snapshot, 53 days.
  INFERENCE (medium): the reservations follow the registration; no source links them.

**Confidence:** high on what the street is and the registration post; naming record silent;
what each number is for, silent.

---

## 5. Labels (web)

**Gates to Benvenuto House — 38 Burton Rd (label added 9 Oct)**
- FACT (shapefile attribute table `HRAPQ32026_OpenData.dbf` downloaded and read 2026-11-10) —
  City Heritage Register open data, record `38 BURTON RD`: status "Listed", listed
  1975-12-10, type "Miscellaneous", construction "1891", architect "Brown, A. Page";
  description "Originally gates to Benvenuto House; 1891, installed by A. Page Brown -adopted
  by City Council on Dec. 10, 1975; house is not listed". No designation by-law.
  <https://open.toronto.ca/dataset/heritage-register/>
- FACT — ACO Toronto, "Burton Road Gates", alternate name "Gates to Benvenuto House", 38 Burton
  Road, 1891: "These gates were moved from their original site, and installed on Burton Road by
  A. Page Brown." <https://www.acotoronto.ca/building.php?ID=5774>
- FACT — Jamie Bradburn, 22 Jan 2020 (first in The Grid, 28 May 2013): "While the mansion was
  knocked down in 1932, several elements survived."; the "ornate gates Mackenzie shipped in from
  Italy" were "moved west to their current location at 38-44 Burton Road."
  <https://jamiebradburnwriting.wordpress.com/2020/01/22/1-benvenuto-place/>
- Conflicts, not resolved and not printed: demolition 1931 (TPL snippet) / 1932 (Bradburn) /
  1924 (lostrivers.ca); "38" vs "38-44"; 1891 installation by A. Page Brown (City) vs gates
  shipped by Mackenzie, who bought the house in 1897 (Bradburn). The article gives the City's
  wording and says the label is 51 years younger than the listing.
- EMPTY — no 2026 heritage or council item for 38 Burton Rd. SNIPPET: listed properties are to
  be prioritised for designation "before they are removed from the register on January 1,
  2027" (toronto.ca heritage register page) — not printed, no source ties it to the label.

**Sam Ibrahim Building — 1050 Military Trl (label added 20 Oct)**
- FACT (re-fetched) — U of T News, 14 Apr 2025: "The University of Toronto Scarborough has
  officially opened the Sam Ibrahim Building, a state-of-the art, five-storey space designed to
  support student learning…" <https://www.utoronto.ca/news/u-t-scarborough-celebrates-opening-sam-ibrahim-building>
- FACT — UTSC: "(formerly known as Instructional Centre 2)"; "A $25-million investment from
  Scarborough-based entrepreneur Sam Ibrahim". <https://www.utsc.utoronto.ca/home/sam-ibrahim-building>
  Address: "1050 Military Trail (The corner of Military Trail and Pan Am Drive)".
  <https://www.utsc.utoronto.ca/bosa/node/139>
- FACT — U of T Entrepreneurship, 16 May 2023: "He is the president and general manager of the
  Arrow Group of Companies". <https://entrepreneurs.utoronto.ca/?p=34063>
- Store: the labelled point is still RESERVED. Lag: official opening (14 Apr 2025 article) →
  label, 18 months.

**"Winfields Park" — 22 Penwood Cres (new, 16 Oct)**
- EMPTY — no source uses the spelling "Winfields Park".
- FACT — City staff report, 2 Oct 2025: "Further north is Windfields Park, a 31-hectare park
  that runs up to York Mills and south along the Wilket Creek Trail."
  <https://www.toronto.ca/legdocs/mmis/2025/ny/bgrd/backgroundfile-258988.pdf>
- SNIPPET — listings for 6 and 10 Penwood Cres describe backing onto "Windfields Park".
- Store: no other point carries either spelling as PLACE_NAME (`--place "Winfields Park"`
  returns only this row). INFERENCE (high): the file's label is Windfields Park misspelt. The
  article reports the spelling and the City's, and does not call it an error outright.
- EMPTY — City parks page for the park (JS-only), any 2026 entrance or works item.

---

## 6. Other numbers (web)

- **2429 Bayview Ave + second 1 The Bridle Path point (28 Oct; 47 m apart).** FACT — the same
  2 Oct 2025 staff report, "2425-2427 Bayview Avenue and 1 The Bridle Path – Official Plan
  Amendment & Zoning By-law Amendment Application – Approval" (24 245561 NNY 15 OZ): "to permit
  a 6-storey (22.5 metre plus 4.5 metres to mechanical penthouse) residential apartment
  building at 2425 - 2427 Bayview Avenue and 1 The Bridle Path."; "56 residential dwelling
  units and 122 vehicular parking spaces. The proposal also includes a 661.79 square metre
  on-site public park."; "The site consists of three lots."
  <https://www.toronto.ca/legdocs/mmis/2025/ny/bgrd/backgroundfile-258988.pdf>
  SNIPPET: By-law 486-2026 passed 21 May 2026 (notice 403). EMPTY: "2429 Bayview" anywhere.
  INFERENCE (low): the reserved numbers relate to the building or the park.
- **1B–1E Golden Ave (28 Oct).** FACT — Councillor Gord Perks, "2106-2112 Dundas St W & 1
  Golden Ave" (undated): a "10 storey mixed-use building" with "three at-grade commercial
  units, and 52 residential rental units in Sept. 2024"; "It remains under review."
  <https://www.gordperks.ca/2106_2112_dundas_st_w_1_golden_ave> FACT — UrbanToronto, 15 Aug
  2024: "Currently occupied by 3-storey mixed-use buildings"; "the property holds commercial
  units at ground level with four residential units above".
  <https://urbantoronto.ca/news/2024/08/mid-rise-rental-building-proposed-dundas-west-roncesvalles.56695>
  FACT — UrbanToronto database: "Construction Status Cancelled" (conflicts with Perks).
  <https://urbantoronto.ca/database/projects/2112-dundas-street-west.56612> Forum post, 6 Nov
  2025: "It's been downsized to just reno the fronts and add a rear addition." (a forum post;
  not printed). EMPTY — "1B/1C/1D/1E Golden Ave" anywhere; nothing in CKAN under GOLDEN 1.
  "Four residential units above" matching four new letters is a coincidence nobody confirms.
- **19 Yonge St, 22A Yonge St (12 Oct).** EMPTY — queries `"19 Yonge Street" OR "22A Yonge
  Street" Toronto`; with M5E / Union Station / Backstage / Dominion Public Building / kiosk.
  Store: 42 m apart; 22A is 20 m from 20 Yonge St.
- **354 King St W (30 Oct).** EMPTY for Toronto (hits are Hamilton's 354 King St W and a King
  St East condo). Store: 20 m from 350 King St W.

---

## Lag table (for the article)

| What | Record date | File | Lag |
|---|---|---|---|
| 100 Allanhurst demolition permit closed | 2026-09-30 | gone 2026-10-01 | next snapshot |
| 90 Douglas Ave laneway suite permit completed | 2026-10-05 | 90R, 2026-10-26 | 21 days |
| 127 Watson Ave severance final | 2026-11-02 | 127A/B, 2026-10-12 | file 21 days early |
| 38 Rockcliffe houseplex permits applied for | 2026-10-20 | 38A/B regular, 2026-10-01 | file 19 days early |
| Arbo Phase 1 registration announced | 2026-08-17 | Sugar Maple Way, 2026-10-09 | 53 days |
| 1197 Glencairn severance approved | 2026-07-23 | 1195/1197(R), 2026-10-09 | 78 days |
| 540 Pharmacy demolition permit closed | 2025-10-17 | 540A/B regular, 2026-10-30 | 12 months |
| 2165 Gerrard E fourplexes completed | 2025-04-29 | 2165A–D regular, 2026-10-01 | 17 months |
| Sam Ibrahim Building officially opened (article) | 2025-04-14 | label, 2026-10-20 | 18 months |
| 107 Holborne semis completed | 2024-10-18 | 107A/B regular, 2026-10-01 | 23½ months |
| oneeleven new-building permit closed | 2017-01-19 | 111/115 Bathurst, 543/551 Adelaide regular, 2026-10-01 | 9 years 8 months |
| Benvenuto gates listed | 1975-12-10 | label, 2026-10-09 | 50 years 10 months |

