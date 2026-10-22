# Research notes — Brampton, 2026-09

Raw findings behind `articles/researched/brampton-2026-09.md`. Notes, not prose.
Window researched: net 2026-08-31 → 2026-09-30 (27 snapshots inside the month; 30 pull
days, 0 failed; three days read back unchanged). Research done 2026-10-22.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **SNIPPET** = seen only in a search-engine summary; the page itself could not
be read — do not print. **EMPTY** = searched, nothing found. Every claim carries a URL.

Source caveat: the City's monthly addressing lists live at URLs named only by month
(`.../Municipal Addressing List/August.pdf`) and are overwritten each year — on
2026-10-22 `August.pdf` is the August 2026 list (PDF created 2026-09-15, title "1. New
and Changed Addressing August 2026.xlsx") but `September.pdf` still serves September
2025 (created 2025-10-21). Links to these lists will point at a different year's list
after the next overwrite; the facts quoted here are from the versions read on
2026-10-22.

---

## 0. Store-side findings (this repo, not the web)

Net, 08-31 → 09-30: rows 249,311 → 249,740 (+429); added 479, removed 50, location 16
(floor 25 m, `location_min_move_m` in datasets/brampton.toml), significant 29, 7 split
events. Gross: added 479, removed 50, location 16, significant 59. The gross-vs-net gap
in "significant" (59 vs 29) is a handful of rows flipping back and forth on successive
Sunday snapshots (see §9). HELD and excluded from every number: 2026-09-27, 64 rows
changed only `HERITAGE` (LISTED → None), technical mass-modified flag.

**Added 479, by kind (store, `PROP_CODE_DESC` on the new row):** Single Family Detached
278, Freehold Townhouse 99, Semi Detached 53, Commercial 13, Road Widening 10, Low Rise
MultiResidential Apt 10, Commercial Condo 6, Link Home 4, Industrial 3, other 3.
By unit: 201 with no unit, 247 with unit "2", 31 other units.

The 479 decompose as: 162 on the five new streets of Plan M2197 (§1); 25 Temple Manor
Road reissues (§3); 246 "Unit 2" on existing houses outside those streets (§4); 10
units at 7 English St (§2); the rest scattered (§5–8).

**Removed 50:** 25 Temple Manor (reissued the same day as Temple Manor Road, §3); 10
units at 370 Main St N (§6); 3 park records on one lot (§7); 1A-245 and 245A Queen St E
(§8); 58-8887 The Gore Rd (commercial condo unit); 21-811 Bovaird Dr W, 61-11615 McVean
Dr, 8069 Mississauga Rd, 37-2730 North Park Dr (commercial units); 10 Kennedy Rd N
(commercial, SECONDARY); 5-15A Fisherman Dr (Place Of Worship); 2-106 Church St (a unit
2); 9416 Highway 50 and 7715 Kennedy Rd ("Residential - Other").

**Busiest days (brief):** 09-01 +130 (120 of them Plan M2197), 09-02 +49 (42 M2197),
09-13 25 added / 25 removed (Temple Manor) + 9 moves + 13 significant (370 Main St N),
09-22 +20 (2 Dewside Dr units, 8887 The Gore units, 37 Rainforest units, and the three
park records out), 09-04 +26 (unit 2s).

**Wards gaining (brief):** 10 +217 (162 M2197 + 42 unit 2s + others), 6 +75, 9 +34.
Ward 6 "losing 25" is the Temple Manor reissue, not a loss — not printed.

### Plan M2197 (Maha Cres, Maxmara St, Acres Crt, Sindh Dr, Orangevalley St)

Store: 162 addresses, all ward 10, `SEC_PLAN_AREA` "48 (b)", all PRIMARY. First on
file 09-01 (Maha 43, Maxmara 27, Orangevalley 22, Sindh 20, Acres 8 = 120) and 09-02
(Maha 16, Maxmara 26 = 42). Property codes: Single Family Detached 100 (Maha 43,
Maxmara 23, Orangevalley 14, Sindh 12, Acres 8), Freehold Townhouse 62 (Maha 16,
Maxmara 30, Orangevalley 8, Sindh 8). Postal codes mostly empty (Maxmara carries
L6S3E/L6S3E9). Centroid 43.7866, −79.7630. `--near 5847 Mayfield Rd`: 1 Maxmara St
58 m, 6 Acres Crt 84 m, 26 Maha Cres 135 m, 1 Sindh Dr 233 m, 1 Orangevalley St 287 m,
11800 Airport Rd 333 m. Nearest other streets to the centroid: 5759 Mayfield Rd 127 m,
11796 Airport Rd 438 m (east, −79.7586), 11825 Torbram Rd 570 m (west, −79.7675),
101-60 Lacoste Blvd 725 m. So: south side of Mayfield Road, between Torbram Road and
Airport Road. No `PLACE_NAME` field in this layer. The 100 detached addresses in the
file are exactly the 100 numbered lots on the City's list (§1); the 62 townhouse
addresses are not on the list (its header: "all corner lots and blocks addressed at
time of permit application").

### 7 English St

Base row 1804325 on file since 2026-06-10, "Low Rise MultiResidential Apt", ward 1,
43.69381, −79.77197. On the 09-16 snapshot ten new rows, units 1–10, ADDRESS_IDs
326276124–326276133 (consecutive), same property code, placed within ~10 m of the
base. Parent remains. `--near`: 66 Isabella St 26 m, 2-367 Main St N 52 m, C-2 Murray
St 105 m. 7 English St to 370 Main St N: 155 m (store coordinates).

### Temple Manor

Old rows: 25 records, street "TEMPLE", `STREET_TYPE` "MANOR", full "2 TEMPLE MANOR" …
"27 TEMPLE MANOR" plus "2-22 TEMPLE MANOR"; all Freehold Townhouse, ward 6, postal
L6Y 6C4/6C5; on file 06-10 .. 09-12. New rows on 09-13: 25 records, street "TEMPLE
MANOR", type "RD", full "2 TEMPLE MANOR RD" …, identical coordinates and postal codes,
new ADDRESS_IDs (hence retire + add in the tracker, not a rename). `--near 2 Temple
Manor Rd`: 2-439 Rivermont Rd 32 m, 2-3 Mussle White Rd 39 m, 8599 Financial Dr 89 m.
The brief lists TEMPLE MANOR as a street "appearing for the first time" — it is not;
not printed as a new street.

### 370 Main St N

Base 370 MAIN ST N (SECONDARY, Commercial) unchanged. Units re-placed 09-11 .. 09-14:
- gone on 09-11: 122C, 123, 125, 21, 22, 24;  gone on 09-12: 105, 108, 23, 25B.
- 09-12: 25A became 29 (same id, moved 45 m); 28 moved 69 m.
- 09-13: units 2–19 and 25–27 moved (2: 166 m, 3: 151 m, 4: 137 m, 19: 137 m, 5: 124 m,
  18: 121 m, 7: 89 m, 8 and 16: 73 m, 15: 49 m, 9: 45 m, 25: 43 m, 14: 25 m; the rest
  under the 25 m floor); unit 1 (id 1784936) became unit 20.
- 09-14: ids for 6 and 17 swapped labels; a new row (id 323414784) became unit 1.
Net: 10 unit records retired, 0 added, 12 moves ≥ 25 m, 4 unit relabels. Units now on
file: 1–20, 25–29. Previously 1–28 with 25A, 25B, 105, 108, 122C, 123, 125.

### Unit 2 additions

Net unit-2 additions on existing streets: 246 (247 incl. 2-22 Temple Manor Rd), on 227
distinct streets, every ward (6: 45, 10: 42, 9: 29, 5: 26, 4: 22, 1: 21, 8: 20, 7: 18,
2: 17, 3: 6). Property code of the new row: Single Family Detached 176, Semi Detached
53, Freehold Townhouse 11, Link Home 4, other 2. All 246 have their base address on
file. Added on 20 different snapshots, 11–24 a day. Same measure for earlier months:
July 265 (of 476 added), August 243 (of 364). The live feed's rows for a unit 2 and its
base (2-13 Agar Lane / 13 Agar Lane, 2-37 and 3-37 Rainforest Dr) carry no permit
fields (PERMIT_NO, PERMIT_TYPE, WORK_TYPE all null) — the file does not say what a
unit 2 is.

### Splits (brief, verified)

- 7 English St → units 1–10, parent remains (above).
- 2 Dewside Dr → 104, 202, 204, 207 on 09-22; Commercial Condo, site plan SP14-031;
  base is FRONTDOOR; units 101, 106–108, 110–113, 201, 201B, 203, 205, 206, 208 were
  already on file. `--near`: 2 Dewridge Crt 59 m, 10665 Bramalea Rd 121 m.
- 15 Eamont St → 13 (09-15), 15 (09-30), 16 (09-19); Commercial, ward 6; 12 and 18
  already there; 14 arrived 10-17. `--near`: 145 Lagerfeld Dr 91 m, 25 All Nations Dr
  112 m.
- 245 Queen St E → 4 and 5 (09-17); same day 1B became 3 (same id) and 1A and 245A
  were retired. Units now 1, 2, 3, 4, 5; before: 1, 1A, 1B, 2 and 245A. Commercial.
- 25 Newkirk Crt → 11 and 14 (09-04), Industrial.
- 37 Rainforest Dr → units 2 and 3 on 09-22, Single Family Detached, parent remains.
- 8887 The Gore Rd → 48 and 50 (09-22); 58 retired 09-07; Commercial Condo.

### Park records

0 Blue Jay Ave (id 1896225, PRIMARY), 0 Countryside Dr (id 1842242, PRIMARY) and 10800
McVean Dr (id 1910981, SECONDARY): all "Municipal Park", all LOT 15 CON. 8 N.D., ward
10, all last on the 09-21 snapshot, gone 09-22. 10800 McVean Dr sat at 43.79645,
−79.72957. 1 and 3 Blue Jay Ave remain. Two other "0 Countryside Dr" Municipal Park
rows (same lot) and one on Lot 16 Con 5 are still on file.

### Other moves and edits

- 5405 Countryside Dr (Industrial, ward 10) moved 123 m on 09-23; 1-5405 stayed put.
- 314-50 Sunny Meadow Blvd moved 45 m on 09-02 (and again 10-22).
- 181 Rutherford Rd S moved 25 m (at the floor; the brief counts 16 moves, my recount
  17 — use the brief).
- PROP_CODE_DESC 10: 65-90 Maritime Ontario Blvd Commercial → Commercial Condo; 138
  Falby Rd Live/Work Residential → Live/Work Commercial; 116 Remembrance Rd Residential
  - Other → Single Family Detached; seven unit-2 rows recoded between Single Family
  Detached / Semi Detached / Link Home / Residential - Other.
- SITE_PLAN_NUMBER 4: 30, 32, 2-30, 2-32 McLaughlin Rd N SPA-2020-0035 → -0034.
- 6-255B Rutherford Rd S Industrial → Commercial and FRONTDOOR → PRIMARY.

### Oscillating rows (the gross/net gap)

On Sunday snapshots (09-06, 09-13, 09-20, 09-27) a fixed set of rows flips and flips
back: 0 Salvation Rd ↔ 0 Fairhill Ave (one id), 0 Daviselm Dr ↔ 0 Bramalea Rd, 0 Dixie
Rd ↔ UNASSIGNED, UNASSIGNED ↔ Queen St E, UNASSIGNED ↔ 0 Selby Rd; and 2-12 Newhaven
Manor, 51-67 Ardglen Dr, 5-15 Ashby Field Rd, 14-16 Strathearn Ave, 11-17 Ray Lawson
Blvd, 2-63 Seachart Pl, 5-85 Resolution Dr, 5-65 Romilly Ave, 5-25 Cherrycrest Dr
toggling the unit between `UNIT_NO` and the front of `CIVIC_NUMBER`. Full address
unchanged for the unit rows. Net effect at month end: 0 Salvation Rd reads 0 Fairhill
Ave; UNASSIGNED reads Queen St E; three unit rows ended on the other side.

**Flags.** No open flag for brampton. Reviewed inside September: 09-02 and 09-09
REG_PLAN_NUMBER on 61 Boundary Creek Path / Brasstown Valley Trail rows (technical,
field now ignored); 09-27 HERITAGE 64 rows (technical, held). Nothing held touches the
stories above.

---

## 1. Plan M2197 — Maha Crescent, Maxmara Street, Acres Court, Sindh Drive, Orangevalley Street

- **FACT** — City of Brampton, Planning, Building and Growth Management, Building
  Division, "Municipal Addressing List", August 2026, dated September 14, 2026 (PDF
  created 2026-09-15). Front page: "REGISTERED PLANS: M2196 See Attached Report - Mylar
  to follow / M2197 See Attached Report - Mylar to follow"; "ALL CORNER LOTS AND BLOCKS
  ADDRESSED AT TIME OF PERMIT APPLICATION". Attached report "REGISTERED PLAN: M2197
  STATUS: Active", lots 1–101, type SFD: lots 1–43 = 66 down to 10 (even) and 9 to 39
  (odd) Maha Cres; 44–51 = 1–15 (odd) Maxmara St; 52–59 = 2–16 (even) Acres Crt; 60 =
  Unassigned; 61–74 = 21–37 (odd) and 70–62 (even) Maxmara St; 75–86 = 9–19 (odd) and
  20–10 (even) Sindh Dr; 87–100 = 9–21 (odd) and 22–10 (even) Orangevalley St; 101 = 72
  Maxmara St. 100 numbered lots; all 100 are in the file as Single Family Detached and
  nothing else in the file's SFD set is off the list (checked 2026-10-22).
  https://www.brampton.ca/EN/residents/Building-Permits/homeowners/Municipal%20Addressing%20List/August.pdf
- **FACT** — same document, front page: "ADDITIONAL REGISTERED UNITS ADDRESSING:
  Registered Two-Unit Dwelling Report - August 1 - August 31, 2026 See attached
  report" (used in §4).
- **INFERENCE** — the file carried the 100 lot addresses on 1–2 September; the City's
  PDF listing them is dated 14 September. The open-data layer ran ahead of the
  published list by about two weeks. The 62 townhouse addresses on the same streets
  are not on the list; the header says blocks are addressed at permit time.
- **FACT** — City of Brampton "Street Naming Policy", effective June 13, 2005, approved
  by City Council: Development Services Division "maintains, compiles and updates a
  'Master List of Approved Street Names for the City of Brampton'" and assigns
  "pre-approved street names drawn from the Master List to new proposed plans of
  subdivisions"; names go to the "Region of Peel Street Names Committee"; "Street
  names not to be provided by the applicant, but instead, from the 'Master List'".
  https://www.brampton.ca/EN/City-Hall/policies-directives/Documents/Street%20Naming%20Policy.pdf
- **EMPTY** — "Maha Crescent", "Maxmara Street", "Sindh Drive", "Orangevalley Street",
  "Acres Court" Brampton: no council item, by-law, developer page or news story names
  the subdivision, its builder or the origin of the names. The master list itself is
  not online. Record silent on the names.
- **FACT, context only, not used** — Secondary Plan Area 48(b) "Countryside Villages"
  is bounded by Mayfield Road (north), Countryside Drive (south), Dixie Road (west) and
  the West Humber tributary (east); the file tags these rows "48 (b)".
  https://www.brampton.ca/EN/Business/planning-development/Plans-and-Policies/secondary%20plans/SPA48b%20Countryside%20Villages.pdf
- **SNIPPET, not used** — an OZS-2025-0029 planning item for "Georgian Mayfield Inc."
  on Mayfield Road; no evidence it is this plan.

## 2. 7 English Street

- **FACT** — City of Brampton By-law 197-2016, "To designate the property at 7 English
  Street, Brampton as being of cultural heritage value or interest pursuant to the
  Ontario Heritage Act", passed 14 September 2016. Schedule B: "located on the south
  side of English Street, west of Main Street North, and contains a two-and-a-half
  storey dwelling, driveway and parking lot"; "Second Empire style mansion"; "Built in
  the early 1870s, the two-and-a-half storey, 14-room brick home at 7 English Street
  features a mansard roof with multiple arched dormer windows"; "C. J. Wheelock
  surveyed Plan BR-25 in 1873. Later that year, John Wesley Beynon and his wife bought
  all of Lot 1 for $307"; Beynon "was a barrister, honoured with the status of King's
  Counsel"; sold 1885 to William Wilson, 1901 to Sarah Jane Magill — "The Magill family
  named the home 'Gillcrest'"; 1919 to Bertha Algie "for $1.00", granddaughter of
  Edward Dale of the Dale Estate nurseries ("The Flower Town of Canada"); "In 1945,
  Edgar Alan Algie bought the property and turned the house into apartments. The Algie
  family sold the home in 1955." Heritage attributes include "Three-storey, central
  tower with brackets", "Mansard roof", "Prominent structure along English Street and
  visible from Main Street". The by-law does not say how many apartments.
  https://www.brampton.ca/EN/City-Hall/Bylaws/2016/197-2016.pdf
- **EMPTY** — no permit, listing or news item for 7 English Street in 2025–2026. Nothing
  says why ten unit numbers were assigned now, or whether the count of apartments
  changed. Listings exist for 6 English St (multi-unit house) and 71 English St — other
  buildings, not used.

## 3. Temple Manor → Temple Manor Road

- **FACT** — OpenStreetMap (Nominatim) returns "Temple Manor Road, Brampton, Peel
  Region, Ontario, L6Y 6C2" at 43.63232, −79.79679, type residential — the same spot
  as the file's rows.
  https://nominatim.openstreetmap.org/search?q=Temple%20Manor%20Road%2C%20Brampton&format=json
- **SNIPPET, do not print** — a rental listing for "23 Temple Manor Road" describes an
  "executive freehold townhouse built by Great Gulf"; the only URL is a 5,000-page
  listing index (nrcrealty.ca), not a page for the address. "Great Gulf" not printed.
- **EMPTY** — no City by-law, notice or addressing-list entry renaming Temple Manor or
  changing its suffix; the August 2026 list's only "ADDRESS CHANGE" is 185 Sun Pac
  Boulevard. The September 2026 list is not yet published. Record silent on why the
  file reissued the 25 records.
- **INFERENCE** — the old rows' street type "MANOR" made the file read "2 Temple
  Manor" where the road's name is "Temple Manor Road"; the reissue brings the file to
  the name in use. Printed as the file catching up, not as a rename.

## 4. The "Unit 2" additions and the City's two-unit register

- **FACT** — City of Brampton, Additional Residential Units page: "To be legal, second
  units, third units and Garden Suites must be registered with the City of Brampton";
  "Unregistered units may face enforcement actions and potential insurance
  consequences"; "As of May 2023, the by-law allows for a maximum of 3 units (including
  the principal dwelling) on a property"; links a "Map of registered Additional
  Residential Units". The page gives no count of registered units.
  https://www.brampton.ca/EN/residents/Building-Permits/second-dwelling
- **FACT** — Office consolidation, "BY-LAW 157-2022 — A By-law to require the
  registration of Additional Residential Units (ARUs) in the City of Brampton, and to
  repeal By-law 87-2015, as amended (amended by By-law 70-2023)", 9 pages; title line
  read from the PDF on 2026-10-22.
  https://www.brampton.ca/EN/City-Hall/Bylaws/All%20Bylaws/Additional%20Residential%20Units%20(ARUs)%20Registration%20By-law%20157-2022.pdf
- **FACT** — August 2026 Municipal Addressing List, attached "REGISTERED TWO-UNIT
  DWELLINGS" report, 10 pages, "Printed: September 08, 2026", covering August 1–31,
  2026: 237 entries, every one "<number> <street>, Unit #2" (e.g. "9 Agar Lane, Unit
  #2", "276 Albright Rd, Unit #2"), with registration dates in August.
  https://www.brampton.ca/EN/residents/Building-Permits/homeowners/Municipal%20Addressing%20List/August.pdf
- **Store cross-check** — of the 237 August entries, 227 match a Unit 2 the file added
  between 31 July and 31 August (by civic number, street and unit); 9 match a Unit 2
  added in September; 235 are on file at 30 September. So a registration in the City's
  August report was in the address file within the same month. Only 35 of September's
  246 Unit 2 additions share a street name with any August entry — September's are a
  different set.
- **INFERENCE, stated as such in the article** — September's 246 Unit 2s are the same
  kind of record as August's 237; the City's September report is not published yet, so
  the match cannot be made for September.
- **EMPTY** — no statement anywhere of how many ARUs Brampton registers per month or
  per year. The monthly counts in the store (Jul 265, Aug 243, Sep 246) are the only
  figures.

## 5. 370 Main Street North

- **FACT (directory)** — shopping-canada.com lists "Kingspoint Plaza" at "370 Main St
  N, Brampton, Ontario L6V 1P8", "60 stores, restaurants, services".
  https://www.shopping-canada.com/shopping-malls-centers/ontario/brampton/kingspoint-plaza
- **SNIPPET** — a listing for 365 Main St N says it is "directly across from Kingspoint
  Plaza"; a nearby-businesses list puts a Domino's at 370 Main St N. Consistent, not
  printed.
- **EMPTY** — no site plan, development application or notice for 370 Main Street
  North; the City's Main Street North Development Permit System page and a 2022 staff
  report on a Solmar/Bristol Place tower application do not name 370. Record silent on
  why the unit points were re-placed and ten unit numbers retired.
  https://www.brampton.ca/en/Business/planning-development/projects-studies/Pages/main-street-north.aspx

## 6. The park records at McVean Drive and Blue Jay Avenue

- **FACT** — OpenStreetMap reverse geocode of 43.79645, −79.72957 (the retired 10800
  McVean Dr point): nearest feature "5, Blue Jay Avenue, Brampton … L6P 1W9".
  https://nominatim.openstreetmap.org/reverse?lat=43.79645&lon=-79.72957&format=json
- **EMPTY** — no park tagged in OpenStreetMap within 400 m; no City parks page for
  10800 McVean Drive; a search for "Blue Jay Park" Brampton finds nothing from the City
  (only a Coquitlam park and Blue Jays-branded ball diamonds elsewhere).
- **SNIPPET, do not print** — a law firm's collision write-up places "Blue Jay Park"
  near McVean Drive and Countryside Drive. Not a City source; the park's name is not
  printed.

## 7. Retirements with nothing behind them

- **SNIPPET, do not print** — By-law 029-2020 is said to concern lands "known
  municipally as 9416 Highway 50" (west side of Highway 50, north of Old Clarkway
  Drive) and permit "Mixed Use Commercial/Retail development"; the PDF is a scanned
  image and could not be read. Not printed.
  https://www.brampton.ca/EN/City-Hall/Bylaws/2020/029-2020.pdf
- **EMPTY** — 7715 Kennedy Rd, 8069 Mississauga Rd, 61-11615 McVean Dr, 21-811 Bovaird
  Dr W, 37-2730 North Park Dr, 5-15A Fisherman Dr, 10 Kennedy Rd N, 58-8887 The Gore
  Rd: nothing. Record silent.

## 8. The other splits

- **EMPTY** — 2 Dewside Dr, 25 Newkirk Crt, 37 Rainforest Dr, 8887 The Gore Rd:
  nothing beyond listings. 15 Eamont St appeared in an earlier year's March addressing
  list as "M1927 BLK 1 15 Eamont Street" (new complete commercial building) per a
  search summary; that URL now serves a different year — **SNIPPET**, not printed.
- **EMPTY** — 245 Queen St E: nothing for the address; the neighbours 241 and 253 Queen
  St E have tower proposals on UrbanToronto, not used (different lots).

## Not researched

5405 Countryside Dr and 314-50 Sunny Meadow Blvd (single moves, no address change);
the McLaughlin Rd N site-plan renumbering; the PROP_CODE_DESC recodes; the Sunday
oscillations (source behaviour, described from the store).
