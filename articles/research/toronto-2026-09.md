# Research notes — Toronto, 2026-09

Raw findings behind `articles/researched/toronto-2026-09.md`. Notes, not prose.
Window researched: snapshots 2026-08-27 → 2026-09-30 (17 snapshots). Research done
2026-10-03, by four parallel search passes (station rename; Carlaw Ave and the east end;
new lanes; splits, labels and withdrawn reservations), merged here with a store-side
section on top.

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
Written below as e.g. BPc(CARLAW,445).

Access notes: the TEYCC meeting 34 (8–9 July 2026) decision pages were not found at the
usual `legdocs/mmis/2026/te/decisions/2026-07-0{8,9}-te34-dd.htm` URLs (404); TMMIS
(`secure.toronto.ca`) still 403s. Outcomes of TE34.4 and TE34.6 therefore seen only as
"confirmed" in By-law 914-2026, not as decision text.

---

## 0. Store-side findings (this repo, not the web)

- **Brief re-run 2026-10-03:** net added 24, removed 129, status 181 (RESERVED→REGULAR),
  location 12, place_name 8, renumbered 1, splits 4; rows 525,469 → 525,364 (−105).
  Gross status 184. No events held (brief `HELD` empty); `tools/article_due.py --city toronto
  --month 2026-09` returns `status: due`, which it only does with no open Toronto flag in the
  month. Matches the offline draft. Derived figures in the offline draft recomputed from the
  store (identity-key diff 113 → 136): 63 removals whose `full` stays active, 66 gone (10 of
  them reserved); 8 additions whose `full` was already on file (2 of them replacing a removed
  row), 16 new; 194 RESERVED→REGULAR, 55 with a same-`full` row removed, 178 first seen on
  snapshot 1, top street Florence Ave 7, Etobicoke-Lakeshore 48 of 194; 19 Structure Entrance
  removals. All match.
- **Offline draft spot-checked against the store:** Carlaw ids (439=13971685, 447=13971686,
  451–463=13971687–13971693, so nine consecutive), last seen 2026-09-11 (snapshot 123),
  gone 09-14 — correct. Lavender/Lowell/Cree ids 30026322–30026334, last seen 09-15, gone
  09-16 — correct. Station place names — correct. Lanes — correct.
- **60 and 64 Roselawn Ave** were last seen on the 2026-09-01 snapshot and are absent from
  09-03 (snapshot 118). August's researched article said they "came off the file on
  1 September"; strictly they were last *on* it on 1 September and off by the 3rd. Not
  in the offline September draft at all (they are two of the 129 removals).
- **Station points (snapshot 138):** 1175 Eglinton Ave E (43.71996, −79.33914) Land,
  RESERVED; 817 Don Mills Rd (43.72139, −79.33881) Land, REGULAR, nearest 1180 Eglinton Ave E
  67 m; 6 Gervais Dr (43.72175, −79.33694) Structure Entrance, REGULAR, nearest 825 Don
  Mills Rd 117 m, 1180 Eglinton Ave E 131 m. Both new-label points sit north of Eglinton;
  817 east of Don Mills.
- **770 Don Mills Rd still carries PLACE_NAME "Ontario Science Centre"** at month end
  (two row versions active since the June rebuild, one RESERVED, one REGULAR).
- **Carlaw:** all 13 retired points were Structure Entrance, at lat 43.6681–43.6687,
  lon −79.3427/−79.3428 — the east side of Carlaw north of Gerrard. Still active nearby:
  **425 Carlaw Ave** (Land, 43.66806, −79.34266) — the number the City's Gerrard Station
  site-plan file uses (see §2); 471 Carlaw Ave (Structure); even side 456–466 (Land).
- **855 Gerrard St E** lost *Gerrard - Carlaw Parkette* between the 09-11 and 09-14
  snapshots — the same snapshot as Carlaw.
- **255 Morningside Ave** lost *Morningside Library* on 09-23; 4279 Lawrence Ave E
  (Structure) carries it.
- **First-seen dates:** 349A/349B Melrose St 09-01; 55A Bywood Dr, 917A/917B Victoria Park
  Ave, 784/786 Spadina Rd (and a RESERVED second point at 782) 09-03; 888 Dundas St W and
  188 Claremont St 09-03; 2A–2C Northampton Dr 09-14 (REGULAR, class Structure).

---

## 1. Science Centre Station → Don Valley Station (file: 15 Sep 2026)

**Searched:** "Science Centre Station renamed Don Valley Station Eglinton Crosstown";
"Line 5 Eglinton opening date 2026"; "\"817 Don Mills\" OR \"6 Gervais\" Toronto"; "TTC Don
Valley station entrances Gervais Drive"; "Ontario Science Centre 770 Don Mills Road site
2026"; "\"Don Valley station\" September 2026"; "Line 5 Eglinton full service date 2026".

- FACT — blogTO, Fri 28 Mar 2025: Metrolinx renaming the station before opening; reason
  its "proximity to the Don Valley Parkway, Don River, and the Don Valley itself"; at
  Don Mills Rd and Eglinton Ave. <https://www.blogto.com/city/2025/03/ttc-station-changing-name-before-opening>
- FACT — Wikipedia: name Science Centre chosen to "reflect its proximity to the Ontario
  Science Centre"; after the June 2024 closure, "Metrolinx announced that the station would
  be renamed Don Valley" on 28 Mar 2025; station "opened on February 8, 2026".
  <https://en.wikipedia.org/wiki/Don_Valley_station>
- FACT — Global News, 20 Jun 2024: Metrolinx then: "At this time, there is no new name
  change to the current Science Centre ECLRT station." Quotes Paul Calandra, April 2023:
  "We'll change the name of the subway stop for them." <https://globalnews.ca/news/10576942/science-centre-rename-eglinton-lrt>
- FACT — Wikipedia: province announced immediate closure of the Ontario Science Centre on
  21 Jun 2024, citing an engineering report on roof-collapse risk (RAAC panels).
  <https://en.wikipedia.org/wiki/Ontario_Science_Centre>
- SNIPPET — relocation to Ontario Place announced 18 Apr 2023; new building broke ground
  May 2026, due 2029. <https://www.ontariosciencecentre.ca/about-us/ontario-science-centre-relocation>,
  <https://www.cp24.com/local/toronto/2026/05/25/construction-of-new-ontario-science-centre-begins/>
- FACT — Wikipedia (Line 5): "A phased opening began on February 8, 2026"; later service
  from 5 Apr 2026. <https://en.wikipedia.org/wiki/Line_5_Eglinton>
- FACT — TTC station page: address "1175 Eglinton Avenue East" (matches the reserved point);
  "Don Mills Road Entrance – East side of Don Mills Road, 75 metres north of Eglinton Avenue
  East"; "Gervais Drive Entrance – West side of Gervais Drive, 45 metres north of Eglinton
  Avenue East". <https://www.ttc.ca/subway-stations/don-valley-station>
- FACT — Metrolinx Ontario Line page: future interchange, entrances at "southwest and
  northeast corners". <https://www.metrolinx.com/en/projects-and-programs/ontario-line/what-were-building/don-valley-station>
- INFERENCE (medium-high) — 817 Don Mills Rd and 6 Gervais Dr are the two TTC entrances:
  position (north of Eglinton; 817 on the east side of Don Mills) matches the TTC's
  descriptions; no source names either address.
- EMPTY — nothing ties 15 Sep 2026 to an announcement or service change. No TTC board or
  Council decision found; the rename was Metrolinx's.
- Lags: Metrolinx rename → file: 28 Mar 2025 → 15 Sep 2026, ~17½ months. Opening → file:
  8 Feb 2026 → 15 Sep 2026, ~7 months.

**Confidence:** high (who, when, why, opening); entrances = inference; trigger = silent.

---

## 2. Carlaw Ave 439–469, odd (file: off between 11 and 14 Sep) — Riverdale Shopping Centre, demolished for the Ontario Line's Gerrard portal

**Searched:** CKAN all five resources at CARLAW 439/445/449/455/463/467/469/471/425 and
GERRARD 855; web: "449 Carlaw" Metrolinx demolition Ontario Line; "471 Carlaw" Toronto;
Gerrard Carlaw Parkette Ontario Line; "Riverdale Shopping Centre" Carlaw Gerrard No Frills.

- FACT — Metrolinx notice, 15 Nov 2024: "449 Carlaw Avenue (formerly the Riverdale Shopping
  Centre) is the future site of the Gerrard Tunnel Portal".
  <https://assets.metrolinx.com/image/upload/v1731967831/Images/Metrolinx/Ontario%20Line/2024-11-15_Notice_449Carlaw_Works_Nov2024.pdf>
- FACT — BPc(CARLAW,445): `25 122049 DEM` "Demolition of 449 Carlaw Avenue is necessary as
  part of the Ontario Line – Pape Tunneling Underground Stations project at the Gerrard
  Portal"; applied 2025-02-26, issued 2025-03-19, **completed 2025-12-15**; proposed use
  "Ontario Line – Gerrard Tunnel Portal".
- FACT — blogTO, Apr 2024: the plaza at Gerrard and Carlaw closing — No Frills (closing
  20 April), Dollarama, a Mobil station, Kal Tire, Work Authority, Little Caesars, Carpet
  Mill (31 May) — for Gerrard Station. <https://blogto.com/city/2024/04/gerrard-carlaw-toronto-shopping-plaza-closing>
- FACT — BPa(CARLAW,449): `25 201515 DST` secant retaining wall "within Metrolinx-owned lands
  at 449 Carlaw Avenue", issued 2025-09-26; `25 270560 DEM` "north wing wall … northeast side
  of the Gerrard and Carlaw" for the Gerrard Station building, issued 2026-02-24.
- FACT — BPa(CARLAW,445): `25 120004 BLD` (not yet issued) describes Gerrard Station as "an
  elevated, non-terminal station on the Ontario line".
- FACT — DA(CARLAW,425): `24 252705 STE 14 SA`, filed 2024-12-20, under review, "Site Plan
  Control Placeholder for Gerrard Station". (425 Carlaw is still on the file — §0.)
- SNIPPET — demolition "began on March 24", expected to wrap July 2025 (Metrolinx site-walk
  deck). <https://assets.metrolinx.com/image/upload/v1746198036/Images/Metrolinx/Ontario%20Line/PapeRiverdale_March_25_2025_Site_Walk_Deck.pdf>
- EMPTY — no DA or CoA records at 439–471; no permits at 439, 455, 463, 467, 469; nothing at
  all at 471 Carlaw.
- INFERENCE (high) — the 13 entrance points were the plaza's storefront doors; they left the
  file nine months after the demolition permit was completed. Consecutive ids (§0) fit: the
  doors of one building issued as a batch.
- 471 Carlaw — record silent.

**Gerrard - Carlaw Parkette (855 Gerrard St E; label off same snapshot)**
- FACT — Metrolinx construction notice: "As early as November 7, 2025, the Gerrard-Carlaw
  Parkette and dog off-leash area (DOLA) will be closed temporarily … until the completion
  of Gerrard Station construction (expected in 2030)." Replacement DOLA at the southeast
  corner. <https://assets.metrolinx.com/image/upload/v1762207184/Images/Metrolinx/Ontario%20Line/TGP-OLN_EGS-Construction_Notice-DOLA_Closure__UpdateNov7__Final.pdf>
- FACT — BPa(GERRARD,855): `25 267734 DEM` "south wing wall located on the southwest side of
  the Gerrard and Carlaw" for Gerrard Station, issued 2026-01-28.
- FACT — TEYCC report, 19 Jun 2026: South Head House in the southwest quadrant, North Head
  House northeast; station works 2026–2030. <https://www.toronto.ca/legdocs/mmis/2026/te/bgrd/backgroundfile-288482.pdf>
- FACT (2021) — Metrolinx: a neighbouring property used for construction "will be added to
  the parkette" afterwards, ~500 m² more. <https://www.metrolinx.com/en/discover/metrolinx-announces-more-park-space-for-ontario-line-east>
- EMPTY — no renaming or merger found.
- INFERENCE (medium) — label dropped because the parkette is a station work site; the file
  does not say so.

**Confidence:** high on the plaza, the portal and the demolition; parkette closure high,
reason for the label drop medium.

**Smaller east-end/other entrance retirements**
- 920 / 924A St Clair Ave W (15 Sep): EMPTY in all CKAN resources. Store: same snapshot,
  922/924/928 reclassed Structure Entrance → Structure and 918–928 moved ~8 m. Next-door
  910–916 condo demolitions completed 2022–23 (DA `17 162972 WET 17 SA`, BPc `22 193201 DEM`).
  INFERENCE: address-point maintenance on one building. Confidence medium, store-only.
- 194A / 196 / 198 Neville Park Blvd (24 Sep): EMPTY. 194 rebuilt as a detached house,
  permit `12 276919 BLD` completed 2020-10-19 (BPc(NEVILLE PARK,194)). Low confidence of any
  link. Not used.

---

## 3. The three new lanes — each over a finished laneway suite

**Searched:** `"Palmira Lane" Toronto`; `"Sunday Mews" Toronto lane naming`; `"Ciamaga Lane"
Toronto`; `"Palmira Lane" OR "Sunday Mews" TEYCC 2026 decision`; `Ciamaga lane naming Barton
Euclid 2018 Gustav Ciamaga TE31.1`; `"Palmira Lane" by-law 2026`; `Toronto laneway suite
address requires named lane`; BPa/BPc at EUCLID 363/768, LOGAN 189/185, BARTON 89, COLLEGE 507.

**Palmira Lane (363R Euclid Ave → 168 Palmira Lane, 3 Sep)**
- FACT — staff report to TEYCC, 29 May 2026: "Approve the name 'Palmira Lane' for an existing
  public lane located south of College Street, east of Euclid Avenue"; applied for by a
  resident through Councillor Dianne Saxe's office; Palmira "a traditional women's name in
  Italian and Portuguese communities", meaning "pilgrim", to "honour the many stories of the
  women in this community that came bravely across the sea"; signage ~$300.
  <https://www.toronto.ca/legdocs/mmis/2026/te/bgrd/backgroundfile-288315.pdf>
- FACT — notice, item TE34.4, heard 9 Jul 2026. <https://www.toronto.ca/legdocs/mmis/2026/te/bgrd/backgroundfile-288356.pdf>
- FACT — By-law 914-2026 confirms the proceedings of TEYCC meeting 34 including TE34.4 (says
  the item was dealt with, not what was decided). <https://www.toronto.ca/legdocs/bylaws/2026/law0914.pdf>
- FACT — BPc(EUCLID,363): `24 121658 BLD` "Laneway / Rear Yard Suite", "new 2-storey laneway
  suite"; applied 2024-03-04, issued 2024-04-08, **completed 2025-04-07**.
- Lag: community council 9 Jul → file 3 Sep = 56 days. Suite completed ~17 months before.
- Confidence: high on name/meaning/permit; adoption seen only via the confirming by-law.

**Sunday Mews (189R Logan Ave → 32 Sunday Mews, 3 Sep)**
- FACT — staff report to TEYCC, 28 May 2026: lane "east of Logan Avenue, west of Morse
  Street"; resident application 22 Sep 2025; the name honours "the bright, idyllic days of
  rest shared with family and friends; baking bread, strolling along tree-lined paths, and
  enjoying the quiet charm of Leslieville"; "'Mews' refers to multi-use lanes that
  accommodate both vehicles and homes – just like this lane does today"; Councillor Paula
  Fletcher supportive; signage ~$600. <https://www.toronto.ca/legdocs/mmis/2026/te/bgrd/backgroundfile-288308.pdf>
- FACT — notice, TE34.6, heard 9 Jul 2026. <https://www.toronto.ca/legdocs/mmis/2026/te/bgrd/backgroundfile-288309.pdf>
  Confirmed in By-law 914-2026 (same caveat).
- FACT — BPc(LOGAN,189): `22 126116 BLD` "Laneway / Rear Yard Suite", "demolish existing frame
  garage and build new laneway suite"; applied 2022-03-23, issued 2022-09-12, **completed
  2025-05-14**. No suite permit at 185 Logan.
- Lag: 56 days from community council.
- Confidence: high; adoption via the confirming by-law only.

**Ciamaga Lane (new 51 Ciamaga Lane, 14 Sep)**
- FACT — By-law 383-2018 (item TE31.1, TEYCC 4 Apr 2018) names the lane.
  <https://www.toronto.ca/legdocs/bylaws/2018/law0383.pdf>
- FACT — staff report, 14 Mar 2018: 13 Seaton Village lanes named at the request of the
  Seaton Village Residents Association; "named after Mr. Gustav Ciamaga, (April 10, 1930 -
  June 4th, 2011) a long-time resident at 762 Markham Street"; composer; set up Brandeis
  University's electronic music studio; directed the University of Toronto Electronic Music
  Studio from 1965; Dean 1977–84; Principal of the Royal Conservatory 1983–84.
  <https://www.toronto.ca/legdocs/mmis/2018/te/bgrd/backgroundfile-113290.pdf>
- FACT — BPc(EUCLID,768): `24 235109 BLD` "New Laneway / Rear Yard Suite", "demolish existing
  garage and construct a two-storey laneway suite with garage on main level and laneway
  suite on second floor"; applied 2024-11-05, issued 2024-12-09, **completed 2026-06-22**.
- EMPTY — no permits at 89 Barton Ave.
- INFERENCE (medium-high) — 51 Ciamaga Lane (23 m from 768 Euclid) is that suite's address;
  arrived 12 weeks after the permit closed, eight years after the lane was named.

**Policy:** EMPTY — no City source found saying a laneway suite needs a named lane to be
addressed (Changing Lanes 2018 reports <https://www.toronto.ca/legdocs/mmis/2018/te/bgrd/backgroundfile-114362.pdf>
silent on addressing). SNIPPET — Post City: City began naming laneways in 2013 to help EMS
<https://postcity.com/?p=38363>. Do not claim a rule.

---

## 4. Splits and new numbers — Committee of Adjustment trail

**Searched:** all five CKAN resources at each address below; store lookups.

- **784 / 786 Spadina Rd (+ reserved 782), 3 Sep.** FACT — CoA-A(SPADINA,782): consent
  **B0077/25TEY** "To obtain consent to sever the property into three undersized residential
  lots and to create new easements/rights-of-way"; filed 2025-12-17, heard **2026-06-03**,
  Approved; "Conditional Consent", conditions expire 9 Jun 2027; Ward 12. CoA-C: A0934–A0936/25TEY
  each "to construct a new four-storey attached apartment building", final 2026-06-24.
  BPa: three permits applied 12–13 Aug 2026, each "four-storey building with six townhouse
  units"; `26 221724 DEM` applied 2026-08-18 "demolish existing single family dwelling and
  sever lot into three residential lots". Earlier scheme (2016 rezoning for a semi pair;
  2018 permits cancelled 2024-07-08). INFERENCE high: 784/786 are the new lots.
- **2 Northampton Dr → 2A/2B/2C (REGULAR), 14 Sep.** FACT — BPc(SHAVER,102): `24 158975 BLD`
  "new 3 story fourplex building", issued 2024-09-04, **completed 2026-09-17**, 4 units
  created; `24 159007 DEM` demolishing the house, completed 2025-05-13. Nothing at all filed
  under Northampton. INFERENCE medium: the corner fourplex's units got Northampton numbers;
  the file moved three days before the permit closed.
- **349 Melrose St → 349A/B (reserved), 1 Sep.** FACT — CoA-C(MELROSE,349): **B0007/26EYK**
  "sever the lot into two undersized residential lots", filed 2026-01-29, heard 2026-05-14,
  Approved, final **2026-09-17**. BPa: `26 196296 BLD` ("Retained Lot") issued 2026-09-21.
  File 16 days ahead of finality.
- **55 Bywood Dr → 55A/B (reserved), 3 Sep.** FACT — CoA-A(BYWOOD,55): **B0017/25EYK** "sever
  the lot into two residential lots", filed 2025-04-22, heard 2025-07-10, Approved; still
  "Conditional Consent" with condition expiry 18 Jul 2026. No permits. Whether conditions
  were cleared: not in open data — hand-check. Not printed beyond "approved July 2025".
- **917 Victoria Park Ave → 917A/B (reserved), 3 Sep.** FACT — CoA-C(VICTORIA PARK,917):
  **B0001/24SC** "sever the existing lot into 2 parcels", filed 2023-12-18, heard 2024-09-18,
  Approved, final **2026-09-01**. File two days later.
- **890 → 888 Dundas St W; 188 Claremont St appears, 3 Sep.** FACT — CoA-C(DUNDAS,890):
  A0933/25TEY, rear one-storey addition with canopies and patios for a ground-floor
  restaurant at 890, with "892 Dundas Street West" and "190 Claremont Street" on the lot;
  final 2026-04-01. BPa: `25 226201 BLD` restaurant shell, addition "with an awning that
  encroaches towards Claremont", issued 2026-04-30. Nothing filed under 888 or 188.
  INFERENCE medium; renumbering reason unsourced.
- **60 / 64 Roselawn Ave (off by 3 Sep)** — from August's notes (§15 of
  `toronto-2026-08.md`): CoA **B0012/21NY** and **B0013/21NY**, filed 2021-02-23, "sever each
  property (60 and 64 Roselawn Ave.) into five undersized parts for the purpose of lot
  additions to create five new houses fronting Duplex Avenue", approved 2022-03-08
  <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=51fd09cd-99d6-430a-9d42-c24a937b0cb0&filters=%7B%22STREET_NAME%22%3A%22ROSELAWN%22%2C%22STREET_NUM%22%3A%2260%22%7D&limit=100>;
  demolition permit `23 182148 DEM` (64 Roselawn) issued 2024-07-11; 530–538 Duplex went
  regular 27 Aug 2026.

---

## 5. Labels

- **Morningside Library off 255 Morningside Ave (23 Sep).** FACT — TPL branch page: opened in
  Morningside Plaza 1968, moved into the new Morningside Mall 1979, "Reopened 30 May 2006 at
  4279 Lawrence Ave. E." <https://tpl.ca/locations/MS/>. 255 Morningside today is a retail
  plaza (permits for salons, restaurants, banks — BPa(MORNINGSIDE,255)); a 2022 rezoning for
  18/28-storey towers (518 units) closed (DA); consent B0052/24SC to sever the site postponed
  (CoA-A). SNIPPET: 255 = "Morningside Crossing", the old mall site — unconfirmed, don't
  print. INFERENCE high: a label twenty years out of date removed.
- **Kensington Community School, 401 College St.** FACT — TDSB school at 401 College St,
  M5T 1S9. <https://schoolweb.tdsb.on.ca/kensington/About-Us>. SNIPPET: part of a 2025 TDSB
  accommodation review. Not printed.
- **Carpark 137, 77 Gough Ave** — EMPTY (Green P pages are JS-only; no CKAN record).
- **7 Ashtonbee Rd, Enbridge label** — EMPTY (only a cancelled 2017 shade-structure permit).

---

## 6. Withdrawn reservations (16 Sep)

- FACT — BPc(LAVENDER,54) and (LAVENDER,56): `15 229948 BLD` and `15 229968 BLD`, each "new
  semi-detached house", applied 2015-09-29, **Cancelled 2017-05-09**.
- EMPTY — no CoA or DA at 48–56 Lavender Rd, 29 Lowell Ave, 46/48 Cree Ave.
- Lavender Rd records carry M6N (York); Cree Ave M1M (Scarborough) — far apart, one id run.
- INFERENCE (medium): at least 54/56 Lavender were held for an infill scheme cancelled in
  2017; the reservation outlived it by nine years. Lowell/Cree: silent.

---

## Lag table (for the article)

| What | Record date | File | Lag |
|---|---|---|---|
| 917 Victoria Park severance final | 2026-09-01 | 2026-09-03 | 2 days |
| 102 Shaver fourplex permit completed | 2026-09-17 | 2026-09-14 | file 3 days early |
| 349 Melrose severance final | 2026-09-17 | 2026-09-01 | file 16 days early |
| Palmira Lane / Sunday Mews at community council | 2026-07-09 | 2026-09-03 | 56 days |
| Ciamaga Lane suite permit completed (768 Euclid) | 2026-06-22 | 2026-09-14 | 12 weeks |
| 782 Spadina severance approved | 2026-06-03 | 2026-09-03 | 3 months |
| Don Valley Station opened | 2026-02-08 | 2026-09-15 | 7 months |
| 449 Carlaw demolition permit completed | 2025-12-15 | 2026-09-14 | 9 months |
| Gerrard-Carlaw Parkette closed | 2025-11-07 | 2026-09-14 | 10 months |
| Science Centre → Don Valley rename announced | 2025-03-28 | 2026-09-15 | ~17½ months |
| 54/56 Lavender Rd permits cancelled | 2017-05-09 | 2026-09-16 | 9 years 4 months |
| Morningside Library moved to 4279 Lawrence E | 2006-05-30 | 2026-09-23 | 20 years — **not printed**: 255 Morningside = old mall site unconfirmed (DA 22 205463 ESC 25 OZ doesn't say) |
| 6 Gervais Dr class (store) | Structure snap 1–124 | Structure Entrance from 125 | verified |
| 770 Don Mills Rd distance from 1175 Eglinton Ave E (store) | | | ~360–395 m |
