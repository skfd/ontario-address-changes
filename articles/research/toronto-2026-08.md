# Research notes — Toronto, 2026-08

Raw findings behind `articles/researched/toronto-2026-08.md`. Notes, not prose.
Window researched: snapshots 2026-07-31 → 2026-08-27. Research done 2026-09-08, by five
parallel search passes (downtown; Yonge corridor; Liberty Village and the west end;
Etobicoke, the east end and Scarborough; place names), merged here with a store-side
section on top.

Conventions: **FACT** = the linked page or record says it. **INFERENCE** = a reading, not
the source's. **SNIPPET** / *summary-level* = text seen only in a search-engine summary or
a WebFetch paraphrase of a page that could not be opened — check by hand before printing.
Every claim carries a URL. Empty searches are recorded as results.

Access notes that shaped the session: `secure.toronto.ca/council/agenda-item.do` (TMMIS)
still returns 403 to every fetch. `toronto.ca/legdocs/**.pdf`, `toronto.ca/wp-content/uploads/**.pdf`
and `omb.gov.on.ca/e-decisions/*.PDF` download fine but WebFetch cannot read them — pull
with curl and read with pypdf/pdftotext. The TEYCC decision `.htm` pages under
`toronto.ca/legdocs/mmis/<year>/te/decisions/` open normally (a way round the TMMIS 403).
Toronto CKAN `datastore_search` with `filters={"STREET_NAME":…,"STREET_NUM":…}` is reliable
on the development-applications, building-permit (active and cleared) and Committee of
Adjustment resources; `q=` full-text is rank-limited and once returned 0 for a phrase two
known records contain — don't cite `q=` empties. `datastore_search_sql` 403s. The live
Address Point layer `https://gis.toronto.ca/arcgis/rest/services/cot_geospatial27/MapServer/101`
answers `returnDistinctValues`. `parking.greenp.com` and `toronto.ca` parks facility pages
are JS shells — URL/title evidence only. CanLII (TLAB decisions since Feb 2023) 403s.
Listing sites (realtor.ca, strata.ca, condos.ca, zolo, livabl) 403/429.

CKAN resource ids used throughout (URL form
`https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=<RID>&filters=%7B%22STREET_NAME%22%3A%22<NAME>%22%2C%22STREET_NUM%22%3A%22<NUM>%22%7D`):
development applications `8907d8ed-c515-4ce9-b674-9f8c6eefcf0d`; building permits active
`6d0229af-bc54-46de-9c2b-26759b01dd05`, cleared `a96c0ba4-3026-402b-b09d-5b1268b8f810`;
Committee of Adjustment active `51fd09cd-99d6-430a-9d42-c24a937b0cb0`, closed
`9c97254e-5460-4799-896f-c7823413c81c`.

---

## 0. Store-side findings (this repo, not the web)

- **Counts recomputed from the store, 2026-07-31 (snapshot 95) → 2026-08-27 (snapshot 113).**
  Added 31, removed 24 — matches the brief. Of the 31 additions, **10** carry a `full`
  address that already had an active row at the open (second points), and **5** arrived
  `REGULAR` (1976/1978/1980/1982 Victoria Park Ave, 8R Hilltop Rd); the other 26 arrived
  `RESERVED`. Of the 24 removals, **12** still have an active row under the same `full` at
  the close. All 26 new reserved points and the four Wilson Ave removals carry ids in a
  `6008xxxx` series; the reserved points that went regular this month carry `300xxxxx` /
  `301xxxxx` ids and were all first seen on snapshot 1 (2025-04-01).
- **RESERVED → REGULAR flips: 49, not 41.** The brief's `status: 41` counts rows whose only
  changed field was `MAINT_STAGE`. Eight more flips are filed under *Other modifications*:
  seven as `Location; MAINT_STAGE` (5 and 9 Sheppard Ave E, 4763/4771/4773 Yonge St,
  2 and 4 Anndale Dr — the Hullmark block, moved 0–39 m) and one as
  `MAINT_STAGE; PLACE_NAME; PLACE_NAME_ALL` (12 Willingdon Blvd, label carried across).
  41 + 7 + 1 = 49, and 49 is what the offline draft's own bullets enumerate. All 49 had
  been reserved since snapshot 1.
- **Place-name edits: 6 listed + 2 under `Location; PLACE_NAME; PLACE_NAME_ALL`.** The two
  are 5 Leaside Park Dr (*Leaside Park* → *Leaside Park, Leaside Park Outdoor Pool*, moved
  11.7 m, 2026-08-18) and 44 Beechgrove Dr (place name changed, moved 99.6 m, 2026-08-10;
  the row could not be re-found by `full` afterwards — not chased).
- **Net location changes: none.** Gross `location: 3` = 372 Military Trl (129 m,
  *Seven Oaks Park*), 155 Transit Rd (79 m) on 2026-08-03 and 428 O'Connor Dr (51 m) on
  2026-08-18; everything else in the month's coordinate churn is under the 50 m floor.
  The 421–429A Yonge St re-versioning on 2026-08-10 is sub-10 m jitter plus
  `ADDRESS_CLASS_DESC`, an ignored field.
- **Corrections to the offline draft (`articles/offline/toronto-2026-08.md`), found while
  verifying it:** (1) it grouped 12 Willingdon Blvd with the 2157 Lake Shore Blvd W /
  Annie Craig / Marine Parade points as one 17 August cluster; the store puts 12 Willingdon
  at 43.64825, −79.51060, about 3.6 km from 2157 Lake Shore (43.62532, −79.47953). (2) it
  printed 41 reserved numbers put in service while listing 49. Both fixed surgically on
  2026-09-08; nothing else in it touched. The "north side of Edward" in one research prompt
  was my error, not the draft's — the draft never named a side.
- **`lookup.py --near` was broken this week, and why.** It took `last_id = max(snapshot ids)`
  as "active", but snapshots 120 (2026-09-07) and 121 (2026-09-08) are *skipped* pulls —
  same content hash as 119 (2026-09-05), `skipped = 1` — and skipped snapshots never appear
  in any row's `max_snapshot_id`, so nothing was "active" and every `--near` call exited
  with *no active address*. Same mechanism explains why the 28 and 31 August pulls close
  nothing: identical to the 27th, skipped, so the month's window ends at 08-27. **Not yet
  fixed** (the 2026-09-08 session could not write to the skill directory): the fix is to set
  `last_id` to the newest snapshot with `skipped == 0` instead of `max(dates)`. Every
  neighbour distance in these notes was computed against snapshot 119 directly. (`--street … --month`
  is not broken — it keeps every row whose span touches the month, which on a long-lived
  street is every row.)
- **Neighbours (nearest active address on another street, snapshot 119):** 75 Edward St →
  610 Bay St 6 m, 112 Dundas St W 37 m; 107 Edward St → 130 Elizabeth St 16 m; 4380 Bloor St W
  → 210 Markland Dr 61 m; 975 Woodbine Ave → 2078 Danforth Ave 3 m; 679 Strathmore Blvd →
  2142 Danforth Ave 45 m; 1978 Victoria Park Ave → 183 Broadlands Blvd 45 m; 5 East Liberty St
  → 15 Solidarity Way 20 m, 37 Strachan Ave 48 m; 534 Duplex Ave → 68 Roselawn Ave 19 m,
  2458 Yonge St 128 m; 2157 Lake Shore Blvd W → 60 Annie Craig Dr 61 m, 122 Marine Parade Dr
  145 m; 3986 Eglinton Ave W → 151 La Rose Ave 79 m, 75 Richview Rd 251 m; 8R Hilltop Rd →
  912 Eglinton Ave W 28 m; 355 Church St → 70 Gerrard St E 25 m, 89 McGill St 27 m;
  1996 Yonge St → 23 Glebe Rd W 40 m; 4763 Yonge St → 2 Anndale Dr 13 m, 9 Sheppard Ave E
  97 m; 1025 Yonge St → 1 Roxborough St E 20 m; 779 Adelaide St W → 241 Niagara St 17 m;
  273 Merton St → 4 Pailton Cres 92 m; 17 Dunkirk Rd → 39 Binswood Ave 18 m; 12 Wellesley St W
  → 9 St Nicholas St 37 m, 582A Yonge St 37 m; 1043 Coxwell Ave → 561 O'Connor Dr 7 m;
  803 Richmond St W → 169 Walnut Ave 28 m.

---

## 1. Yonge St at Glebe Rd W (15 Aug) — Allure Condos, 10 storeys, on the site of a seniors' home and a row of shops

**Searched:** `"1994 Yonge Street" OR "2008 Yonge Street" "Glebe Road West" development`; `"Allure" Greenpark "23 Glebe"`; `urbantoronto.ca database Allure`; `site:toronto.ca/legdocs/bylaws "Glebe Road West"`; TEYCC 2010 decision; CKAN dev-apps `q=GLEBE`, `q="Glebe Road"`; CKAN permits `STREET_NAME=GLEBE, STREET_DIRECTION=W`.

- FACT — Preliminary report, 15 Jan 2007, file 06 186968 STE 22 OZ: "On October 27, 2006 Templeton Holdings Inc. applied for a Zoning By-law amendment for 1994-2008 Yonge Street to permit the construction of an 11 storey residential apartment building"; site "situated on the south-west corner of Yonge Street and Glebe Road West… currently occupied by a single storey building and two-2 storey buildings"; "West: 3 storey seniors home". <https://www.toronto.ca/legdocs/mmis/2007/te/bgrd/backgroundfile-1168.pdf>
- FACT — Final report, 26 Jul 2010, ref 09-115302 STE 22 OZ: "This application was made on March 9, 2009"; "the applicant acquired the property to the immediate west of the development site"; proposal "to demolish a senior's residence building at 17 Glebe Street West [sic] and several retail buildings, including three residential rental units, from 1994-2008 Yonge Street"; "10-storey mixed-use building… 165 residential units, and 185 vehicular parking spaces"; Section 37 "$500,000… Up to $200,000 may be used for the beautification of the terminus of Glebe Road West". <https://www.toronto.ca/legdocs/mmis/2010/te/bgrd/backgroundfile-32465.pdf>
- FACT — TEYCC 17 Aug 2010, item TE36.14 "Final Report - 1994-2008 Yonge Street and 17 Glebe Road West - Rezoning Application": recommended "City Council amend Zoning By-law 438-86, as amended, for the lands at 1994-2008 Yonge Street and 17 Glebe Road West". <https://www.toronto.ca/legdocs/mmis/2010/te/decisions/2010-08-17-te36-dd.htm>
- FACT — CKAN development applications: OZ `09 115302 STE 22 OZ`, submitted 2009-03-09, Closed, listed at 1994, 2000, 2008 Yonge St and 17 and 23 Glebe Rd W; SA `10 319388 STE 22 SA`, submitted 2010-12-23, Closed, at 17 and 23 Glebe Rd W; description "Proposed is a 10 storey mixed-use building with 196 residential units with retail at-grade." <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&q=GLEBE&limit=100>
- FACT — UrbanToronto database: "Allure Condos", 17 Glebe Road, developer "Greenpark Homes", "Page + Steele / IBI Group Architects", 10 storeys, "130 ft / 39.62 m", 197 units, status "Complete" (no dates filled in). <https://urbantoronto.ca/database/projects/allure-condos.2944>
- FACT (listing site — do not anchor a lag on it) — Precondo: "Allure is a 10-storey boutique condominium completed in 2015." 23 Glebe Rd W, 195 units. <https://precondo.ca/r/building/23-glebe>
- FACT — No building permits on Glebe Rd W in the active-permits dataset (total 0). <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22GLEBE%22%2C%22STREET_DIRECTION%22%3A%22W%22%7D&limit=200>
- Discrepancies to carry, not resolve: unit count is 165 (final report, approval stage), 196 (CKAN), 195 (Precondo), 197 (UrbanToronto). Templeton Holdings is the 2006 applicant; Greenpark is the developer per UrbanToronto — different stages, both sourced.
- INFERENCE (high): the 15 Aug change is the file catching up on a building finished about a decade earlier — the pre-assembly lot addresses (1994, 2000, 2008 Yonge, 17 Glebe) retired, and the building's addresses (23 Glebe Rd W = the condo's marketed address; 1996/2000/2008 Yonge = presumably the Yonge retail frontage) made regular. No source names "1996 Yonge St" or ties the addressing to any 2026 event.
- Anchor the lag on the City's own dates: community council recommended the rezoning (and with it the demolitions) on 17 Aug 2010 — sixteen years to the week before the file retired those addresses. The 2015 completion is listing-level.

**Confidence: confirmed** (project, applicant/developer, storeys, approval chain). Completion year: listing-level only. Cause of the 2026 file change: inference.

---

## 2. 4759–4789 Yonge St / 5 & 9 Sheppard Ave E / 2 & 4 Anndale Dr (15 Aug) — Hullmark Centre, Tridel + Hullmark, 45 + 35 storeys, "recently completed" in March 2016

**Searched:** `"4759 Yonge" OR "4789 Yonge Street" Sheppard Anndale`; `"Hullmark Centre" 4789 Yonge Tridel`; `site:toronto.ca "4759-4789 Yonge"`; `urbantoronto.ca database "Hullmark Centre"`; Globe and Mail; CKAN dev-apps `q=ANNDALE`, `q=4789`, `q=SHEPPARD` (all empty for these numbers), `q=163756` (hit); CKAN permits `STREET_NAME=YONGE,STREET_NUM=4789` and `STREET_NAME=ANNDALE`.

- FACT — Hullmark Centre Inc. settlement offer (legdocs 2009, NYCC): "Concerning Mixed Use Redevelopment of 4759-4789 Yonge Street / OMB File No. O03145 / City of Toronto OPA & Re-zoning Application 06 163756 NNY 23 OZ"; four components — "Podium & Infrastructure… north and south subway station connections", "Link Building", "South Tower Component (residential…)", "North Tower Component (office + residential…)"; gross site "including the Anndale Drive extension and Yonge Street road widening lands (2,531.60 square metres) to be conveyed to the City". <https://www.toronto.ca/legdocs/mmis/2009/ny/bgrd/backgroundfile-20123.pdf>
- FACT — CKAN development applications: `09 198292 NNY 23 OZ`, submitted 2009-12-21, Closed, two rows with STREET_NUM `4763` and `4759-4789` YONGE: "A amendment to height limit in OPA 91 of north tower from 155 metres to 160 metres. This application includes lands from 4759-4789 Yonge Street. Previous related applications are 06 163756 NNY 23 OZ and 120530 NNY 23 SA." (The City's own application record carries the same range-style "4759-4789" address the file retired.) <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&q=163756&limit=50>
- FACT — Globe and Mail, 23 Sep 2015, John Bentley Mays: "the two-tower, mixed-use scheme called the Hullmark Centre is nearing completion"; Kirkor Architects for Hullmark Developments and Tridel; "67,000 square feet of retail, including a spacious Whole Foods"; "connected directly to the subway". <https://www.theglobeandmail.com/life/home-and-garden/architecture/the-hullmark-centre-in-torontos-north-york-a-solid-architectural-citizen/article26503927/>
- FACT — City staff report, 11 Mar 2016 (4800 Yonge St preliminary report): "On the southeast corner of Yonge Street and Sheppard Avenue East is the recently completed mixed use Hullmark Centre at 4759 - 4789 Yonge Street with a 45 storey residential and office condominium, 5 storey office condominium and 35 storey residential condominium apartment building." <https://www.toronto.ca/legdocs/mmis/2016/ny/bgrd/backgroundfile-91274.pdf>
- FACT — UrbanToronto database: "Hullmark Centre", 5 Sheppard Ave E, Tridel / Hullmark, KIRKOR, 45 and 35 storeys, 167.94 m, status "Complete". <https://urbantoronto.ca/database/projects/hullmark-centre.124>
- FACT (weaker source) — urbandb lists the south structure at "2 Annadale Street" [sic], 35 storeys, and the north structure at "5 Sheppard Avenue", 45 storeys. <https://www.urbandb.com/canada/ontario/toronto/hullmark-centre-south/index.html> / <https://www.urbandb.com/canada/ontario/toronto/hullmark-centre-north/index.html>
- FACT — Building permits at 4789 Yonge St: 44 records, earliest application 2014-08-14; latest is `26 156208 BLD`, interior alteration for a therapist clinic, applied 2026-05-06, **issued 2026-07-16**. <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22YONGE%22%2C%22STREET_NUM%22%3A%224789%22%7D&limit=200>
- FACT — No permits at 2 or 4 Anndale Dr (46 Anndale records; numbers 1, 5, 7, 15… present). <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22ANNDALE%22%7D&limit=200>
- INFERENCE (high): the "4759-4789 Yonge St" range row is the assembly-era address used through the OMB/OPA process; its retirement and the regularisation of 4763/4771/4773/4789 Yonge, 5 & 9 Sheppard E and 2 & 4 Anndale on 15 Aug is the file catching up a decade after completion. 5 Sheppard Ave E = north tower and 2 Anndale Dr = south tower per the sources above; 9 Sheppard, 4 Anndale and the three Yonge numbers are not named anywhere found.
- Most recent dated milestone: tenant fit-out permit issued 2026-07-16 (building in ordinary use). No news in 2026.

**Confidence: confirmed** (project, developers, architect, storeys, OMB file, completion window 2015–16 from a City report). File-change cause: inference.

---

## 3. 353/355/357 Church St + 89–95 McGill St → regular (15 Aug) — Alter, by Tridel, permit completed 2019-12-19

**Searched:** CKAN all four datasets for 353–357 Church, 89–99 McGill; `"355 Church Street" Toronto condo McGill development`; `site:urbantoronto.ca Alter Tridel 355 Church`; `site:toronto.ca legdocs "355 Church Street" McGill townhouse OMB settlement`; `"Gerstein Crisis Centre" "355 Church"`.

**FACT — the building is Alter, by Tridel, complete since 2019.** CKAN dev-applications: **12 162027 STE 27 OZ** (submitted 2012-04-26, addresses 355 Church and 89 McGill) "33 storey mixed-use building … 337 residential units"; Site Plan **14 173921 STE 27 SA** (2014-06-13):
> "The proposed building consists of a four storey base building containing three town-house units, 3,188 sm of office space and 271 sm of commercial space. The 29-storey residential condo tower contains 337 residential units."
Condo **16 215145 STE 27 CD** (2016-08-30). Building permit **14 257790 BLD** "To construct a 33 storey mixed use condo building containing 335 dwelling units", issued 2016-12-22, **completed 2019-12-19**.
**FACT.** By-law 837-2015(OMB), authority "Ontario Municipal Board Decisions/Orders issued on June 16, 2014 and April 15, 2015 in Board File No. PL130373", "lands known municipally in the year 2014 as 355 Church Street"; regulates "bay windows within dwelling … along the McGill Street frontage". <https://www.toronto.ca/legdocs/bylaws/2015/law0837.pdf>
**FACT.** UrbanToronto database: "Alter", 355 Church Street, Tridel, architects—Alliance, 33 storeys, 107.89 m, 340 units, Complete; last forum post Oct 15, 2018. <https://urbantoronto.ca/database/projects/alter.5835>
**FACT.** City Toronto Green Standard Tier 2 profile "89 McGill Street": Tridel, Architects Alliance, "337 luxury condominium suites and retail at grade". <https://www.toronto.ca/city-government/planning-development/official-plan-guidelines/toronto-green-standard/tier-2-project-profiles/89-mcgill-street/>
(Do not print: the 2014 staff report's "entrances to three townhouse units on McGill Street" — the PDF URL returned an HTML page; search-snippet only. 33 vs 34 storeys and 335/337/340 units differ by source.)

**FACT — the only 2026 activity at the address.** Permit 25 254045 BLD, 355 Church, "interior alterations to existing vacant suite for new crisis centre - 'Gerstein Crisis Centre'", issued 2026-02-05. City report *Establishing a Toronto Community Crisis Service Training Centre*, **18 November 2025**: lease with Family Service Toronto "for the fourth floor at 355 Church Street", up to $2.5 million for fit-out, "Q4 2026 launch". <https://www.toronto.ca/legdocs/mmis/2025/ec/bgrd/backgroundfile-260108.pdf> — present as the only 2026 event, not as a cause.

**Cross-item store finding (live datastore, fetched 2026-09-08 — after the window):** every Structure point in this month's items carries an `ADDRESS_POINT_ID_LINK` to a parent Land point: 353/357 Church → 355 Church; 91/93/95 McGill → 89 McGill; 1025 Yonge → 1027 Yonge; 73/75/85 Edward → reserved 604 Bay (id 60083950); 107 Edward → reserved 130 Elizabeth (id 60083957); 273 Merton → reserved 275 Merton (id 60083945). The *meaning* of the field is INFERENCE from the pattern — it is as undocumented as MAINT_STAGE.

**INFERENCE (moderate):** three Structure points on McGill (91/93/95) = the three townhouse units in the 2014 site plan; 353/357 Church = tower/podium entrances. **INFERENCE (high):** the 15 Aug flip is the file regularising a building occupied since 2019 — a ~6.7-year lag. **Nothing found** for a 2026 trigger.

**Confidence: confirmed** (project, developer, dates); trigger: nothing found.

---

## 4. 1025/1027 Yonge St and 1 Roxborough St E → regular (17 Aug) — Hill and Dale Residences, permit completed 2026-01-06

**Searched:** CKAN all datasets for 1025/1027 Yonge, 1/3 Roxborough St E; `"1027 Yonge Street" OR "1025 Yonge Street" Roxborough Toronto development`; `"1025 Yonge Street" Toronto`; `site:urbantoronto.ca "Hill and Dale" 1027 Yonge`.

**FACT.** CKAN Site Plan **15 132389 STE 27 SA** (2015-03-25): "To maintain existing 3-storey plus basement office building located at the southeast corner of Yonge St. and Roxborough St. East, while adding an additional 3 storeys plus mechanical penthouse." Condo **18 134997 STE 27 CD** (2018-03-27): "6-storey mixed-use building … 14 residential units … on levels 4 through 6." CoA A0686/15TEY (2015), A1199/17TEY (2017, "currently under construction").
**FACT — the milestone.** Permit **16 103087 BLD** ("3 storey addition above the existing 3 storey building", 17 units) issued 2017-11-15, **completed 2026-01-06** — seven months before the flip; also 18 142063 BLD (café, Unit 2) completed 2026-04-02.
**FACT.** UrbanToronto database: Old Stonehenge Development Corporation and Clifton Blake Group, Studio JCI, 6 storeys, 27.13 m, 17 units, Complete, last post Dec 15, 2019. <https://urbantoronto.ca/database/projects/hill-and-dale-residences.19456>
**FACT.** Globe and Mail, 18 Feb 2016, *Rosedale condo project stands out with proudly modern design*: Hill and Dale, 1027 Yonge at Roxborough St E, Old Stonehenge, JCI Studio, six storeys, 17 suites, replacing "a kind of dumb-looking, three-storey modernist office block from the 1970s". <https://www.theglobeandmail.com/life/home-and-garden/architecture/rosedale-condo-project-stands-out-with-proudly-modern-design/article28781945/>
Listing sites use both "1 Roxborough St E & 1027 Yonge St" for the building. <https://strata.ca/toronto/1-roxborough-st-1027-yonge-st-hill-and-dale-residences> (429 — title-level only). Unit count 14/15/17 differs by source.

**INFERENCE (high):** the file catching up with a building under construction in 2017, after the permit closed in January 2026. 1025 Yonge is a Structure point linked to 1027; 1 Roxborough St E switched class Structure → Land. **Nothing found** for a 2026 real-world event.

**Confidence: confirmed** (project, developer, permit close); nothing found for trigger.

---

## 5. East Liberty St / Solidarity Way / 14 Strachan Ave (17 Aug) — the 2010 King Liberty Village master plan, all built

**Searched:** `"East Liberty Street" "Solidarity Way" Toronto`; `"14 Strachan Avenue" Toronto development Liberty Village`; `"Solidarity Way" Toronto street naming`; `"Solidarity Way" site:toronto.ca`; `site:toronto.ca/legdocs/mmis/2014/te "Solidarity Way"`; `"2014.TE31" "Solidarity Way"`; `Fitzrovia Liberty Village East Liberty rental`; `urbantoronto "East Liberty" Strachan 2026 proposal`; `"Liberty House" Fitzrovia completed`. CKAN dev-apps, active permits, cleared permits, all 18 CoA resources for 5, 9, 25, 31, 35, 39, 49, 51, 55, 59 East Liberty, 14 Strachan, 15 and 25 Solidarity. Fetched and text-extracted the 2010 staff report; UrbanToronto Liberty House thread p.3; Municipal Code Ch. 950 Sch. XVI.

### The master plan — FACT (verbatim, City staff report, 10 May 2010)

Final Report, "14 Strachan Ave, 39-51 East Liberty St and 19 Western Battery Rd – Rezoning, Subdivision Applications", refs **09 115093 STE 19 OZ, 10 108633 STE 19 SB**, to Toronto and East York Community Council.
> "This application proposes to incorporate reserved lands from the former Inglis Manufacturing Facilities Lands into King Liberty Village … The intent is to allow for the construction of three residential towers at 14 Strachan Avenue and 39 to 51 East Liberty Street. Two of the towers, both being 25 storeys in height, would share a common 4 storey podium on the south side of East Liberty Street; the third tower, also having a height of 25 storeys, would have a separate 4 storey podium on the south west corner of Strachan Avenue and East Liberty Street."

> "The site municipally referred to as 39-51 East Liberty Street and 14 Strachan Avenue is located on the south west corner of East Liberty Street and Strachan Avenue. The irregularly shaped lot has an area of 1.69 hectares … A two storey building, with two billboards extending from the roof, currently exists on site."

The new road: "will intersect East Liberty Street so that it is aligned with Western Battery Road … will become the first phase of the new local road that is intended to connect to Dufferin Street." The zoning block is "Block 2A East".
<https://www.toronto.ca/legdocs/mmis/2010/te/bgrd/backgroundfile-30181.pdf>

CKAN subdivision record (verbatim): 10 108633 STE 19 SB, submitted 2010-01-22, "Draft plan of subdivision … for the creation of four additonal lots/blocks in the proposed Block 2A East area of the Inglis Lands (KLV lands) … Refer to as Phase II East Subdivision".

### What is actually at each address — FACT (CKAN, verbatim)

Every address with a record is a **completed** building, not a live project:

| Address | Record |
|---|---|
| 39 East Liberty / 15 Solidarity Way / 14 Strachan | **18 139795 STE 19 SA**, submitted 2018-04-06, Closed: "Liberty Village Block 10: Site Plan Control application for a proposed mixed-use building: 25 storeys plus MPH, 440 dwelling units, 259 parking spaces … See related Minor Variance No. A0489/17TEY". CoA A0489/17TEY (in 2017-04-28): "To modify the re-development plan of the 25-storey residential rental building, approved under Site-Specific By-law 1079-2010". Cleared permit at **14 Strachan**: 21 200173 BLD, "Interior alterations for new Starbucks", issued 2021-09-17, **completed 2023-10-11**. |
| 49 East Liberty / 25 Solidarity Way | **12 116875 STE 19 SA**, 2012-02-03: "PHASE 2 - Site plan approval for mixed use building - 27 storeys … 293 residential units"; **19 187236 STE 10 CD**, 2019-07-11: "27 Storey building with 303 residential units". |
| 51 East Liberty | **10 321108 STE 19 SA**, 2010-12-30: "new 25 storey mixed use building - 386 residential units"; **15 157818 STE 19 CD**, 2015-05-15, draft plan of condo. Latest permit: 26 205279 BLD, applied 2026-07-20, **issued 2026-08-20**, "Tim Hortons (#122593) Interior alterations". |
| 55 East Liberty | 07 244462 SHO shoring permit, issued 2009-09-03: "Permit for new 20 storey and 10 storey residential 276 units". |
| 59 East Liberty | 07 244439 DRN, issued 2009-01-20: "permit for new 5 Storey Residential Building - '57 East Liberty' - 20 Units. Phase 1B". |
| **5, 9, 25, 31, 35 East Liberty; 15 Solidarity Way** | **0 records** in every dataset. |

Reproducible: `https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&filters=%7B%22STREET_NAME%22%3A%22EAST%20LIBERTY%22%2C%22STREET_NUM%22%3A%2239%22%7D`

Names for the buildings (real-estate listings, not City sources): Liberty House = 39 East Liberty / 15 Solidarity Way, "440 condos over 25 storeys … built by Fitzrovia Capital" <https://strata.ca/toronto/39-east-liberty-street-liberty-house>; 51 East Liberty = CanAlfa's Liberty Central by the Lake, 49 = Liberty Central 2 (27 s), 59 = Liberty Towers <https://libertyvillagetoronto.com/future-residential-developments-planned-for-liberty-village>. UrbanToronto thread: "this site was sold to CentreCourt last month" (post 2018-03-21, per WebFetch summary) <https://urbantoronto.ca/forum/threads/toronto-liberty-house-84-12m-25s-fitzrovia-arcadis.10027/page-3>. **No source gives a completion year**; the Starbucks permit completion (2023-10-11) is the best City-sourced proxy that the building was occupied by then.

### 5/9/25/31/35 East Liberty — INFERENCE only

Store coords: 5 (43.63907, -79.41105), 9 (43.63903, -79.41119), 25 (43.63881, -79.41156), 31 (43.63886, -79.41219), 35 (43.63883, -79.41230), 39 (43.63881, -79.41240); all class "Structure"; 14 Strachan (retired) at 43.63860, -79.41099. They run west along the south side of East Liberty from the Strachan corner across the Liberty House footprint. **INFERENCE (moderate):** multiple street-frontage/entrance addresses of the Liberty House block, regularised together; 14 Strachan (the Starbucks address) dropped in favour of them. No source says this.

### "Solidarity Way" — when named

- **SNIPPET (page 403s — needs browser confirmation; do not print the date):** Toronto and East York Community Council, meeting 2014.TE31, 8 April 2014: "the name 'Solidarity Way' be approved to identify a proposed public street located west of Strachan Avenue, extending southerly from East Liberty Street." <https://secure.toronto.ca/council/report.do?meeting=2014.TE31&type=decisions> (item number not recoverable without a browser).
- **FACT (verbatim):** the name was already in the **May 2010 draft zoning by-law** attached to the staff report above: "the buildings on block 2A east will provide a 3 metres setback above a height of 16 metres on East Liberty Street and Solidarity Way, only". So the 2014 item reads as formal approval of a name in use since at least 2010 — **INFERENCE**.
- **FACT (verbatim):** Municipal Code Ch. 950 Sch. XVI lists "East Liberty Street | Both | Anytime | Western Battery Road/Solidarity Way and Strachan Avenue" — confirms Solidarity Way meets East Liberty opposite Western Battery Rd. <https://www.toronto.ca/legdocs/municode/toronto-code-950-16.pdf>
- Nothing found on who or what "Solidarity" commemorates.

**Confidence:** master plan and building identities **confirmed**; the 17 Aug event as file maintenance **likely** (store-only); the five low-number points **unexplained**; naming date **snippet only**.

---

## 6. 779 and 781 Adelaide St W → regular (17 Aug) — a 2015 severance; nothing built; lots for sale this week

**Searched:** CKAN all datasets (incl. CoA 2013–2016) for 777–783 Adelaide St W; `"779 Adelaide Street West" OR "781 Adelaide Street West" Toronto`; `"779 Adelaide" Toronto semi-detached OR permit`; `"781 Adelaide" Toronto sold OR construction 2025 OR 2026`.

**FACT — nothing has been built; the lots are for sale.** MLS **C13013624**, 781 Adelaide St W, $899,000, active, data as of 2026-09-08, lot 17.52 × 101.8 ft:
> "Offered as a package, 779 & 781 Adelaide Street West present two premium residential lots, perfectly positioned and primed for redevelopment."
> "The properties are ideally suited for a semi-detached development, with plans and prior building permit work already prepared by the seller."
<https://condos.kingwestcondo.com/idx/details/listing/b126/C13013624> (realtor.ca listing 29622114 403s: <https://www.realtor.ca/real-estate/29622114/781-adelaide-street-w-toronto-niagara>). Listing calls it the "Niagara neighbourhood" — attribute if used.

**FACT — the severance is from 2015.** CoA **B0093/14TEY**, 781 Adelaide St W, consent, in 2014-12-23, hearing Feb 11, 2015, Approved, "NUMBER_OF_LOTS_CREATED": 1: "To obtain consent to sever the property into two residential lots, together with various easements/rights-of-way."
**FACT — permits issued 2022, never completed.** 15 175789 DEM (demolish existing dwelling) and 15 176323 BLD "new 3 storey semi detached dwelling … (Exisitng lot to be severed into two parcels)", both applied June 2015, **issued 2022-02-17**, status Permit Issued; sibling 15 175693 BLD "Pending Cancellation".
**FACT — the house.** ACO Toronto: c.1872/1873 Gothic Revival house, "This building is at Risk", "Since approximately 2015, a demolition notice has been posted in the front window of 781 Adelaide Street West. The property is in a deteriorating condition." <https://www.acotoronto.ca/building.php?ID=13598>

**INFERENCE (high):** the 17 Aug change regularises the 2015 severance (779 = the new lot, 781 = the retained one; 781A was the old placeholder) — an ~11.5-year lag — and records no construction. **Nothing found** naming 779 in any City record; it exists only in the listing and the file.

**Confidence: confirmed** (severance, permits, unbuilt); causal reading is inference.

---

## 7. Edward St 73/75/85/107 + second points at 604 Bay / 130 Elizabeth (3 Aug) — the Toronto Coach Terminal redevelopment

**Searched:** CKAN dev-applications, active/cleared permits, CoA for 604/610 Bay, 130 Elizabeth, 63–107 Edward (odd); live address points for side-of-street; `"610 Bay Street" "130 Elizabeth Street" development application`; `"Coach Terminal" 610 Bay Street demolition OR construction 2026 Kilmer Tricon`; `"Edward Street" "610 Bay" Kilmer Tricon paramedic 2026` (empty); `site:toronto.ca legdocs "604-610 Bay Street and 130 Elizabeth Street"`.

**FACT — the side of the street** (the research prompt guessed "north"; the offline draft never said). City staff report *Construction Staging Area - 610 Bay Street and 130 Elizabeth Street*, Director, Traffic Management → Toronto and East York Community Council, **18 December 2025**, Ward 11:
> "EllisDon is constructing two affordable housing projects: a 44-storey residential tower at 130 Elizabeth Street, and a 16-storey residential tower at 610 Bay Street. The two development sites are located on the south side of Edward Street, between Chestnut Street and Bay Street."
> "The proposed sidewalk closures are required for a period of 39 months, from January 31, 2026 to April 30, 2029."
<https://www.toronto.ca/legdocs/mmis/2026/te/bgrd/backgroundfile-261275.pdf>
Corroborated by the live dataset: 73/75/85/107 Edward have `CENTRELINE_SIDE = L`; the existing 64–106 Edward (evens) are `R`; the new points sit ~30 m south of 70 Edward.

**FACT — the application.** CKAN development-applications: **25 133694 STE 11 OZ**, submitted **2025-03-24**, status Closed:
> "Application to permit a 16-storey building at 604-610 Bay Street and a 43-storey building at 130 Elizabeth Street. The proposed development integrates the designated heritage Coach Terminal building and includes 1,623 square metres of retail space and 4,809 square metres of institutional space for a Toronto Paramedic Services facility and office uses in the lower levels of the buildings, and 858 purpose-built rental dwelling units, including 245 affordable units, above. This is one of eight sites under the City of Toronto's ModernTO initiative."
Site Plan **25 197844 STE 11 SA**, submitted 2025-07-22, status "NOAC Issued" (15-storey / 43-storey, 827 units incl. 210 affordable). Hold-lift **25 244508 STE 11 OZ**, submitted 2025-10-24, Closed.
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&filters=%7B%22STREET_NAME%22%3A%22BAY%22%2C%22STREET_NUM%22%3A%22604%22%7D>

**FACT.** Notice of Public Meeting for application 25 133694 STE 11 OZ, "Location of Application: 604-610 Bay Street and 130 Elizabeth Street", "Applicant: Tricon Residential and Kilmer Group", meeting 5 June 2025. <https://www.toronto.ca/legdocs/mmis/2025/te/bgrd/backgroundfile-255494.pdf>
**FACT.** By-law 588-2025, "Enacted and passed on June 26, 2025", site-specific provisions "On lands municipally known as 604-610 Bay Street and 130 Elizabeth Street". <https://www.toronto.ca/legdocs/bylaws/2025/law0588.pdf>

**FACT — partners and timeline.** City news release, **21 November 2024**: Kilmer Group and Tricon Residential (Kilmer-Tricon) selected; 873 new homes with 290 affordable; "A new 23,000-square-foot Toronto Paramedic Services Hub"; 610 Bay completion expected Q1 2029, 130 Elizabeth Q1 2030. <https://www.toronto.ca/news/city-of-toronto-and-createto-announce-development-partners-and-vision-for-the-historic-toronto-coach-terminal-site/>
CreateTO project page: shortlist June 2022; Kilmer-Tricon preferred proponent November 2024. <https://createto.ca/projects/610-bay-street>

**FACT — where construction stood in the window.** UrbanToronto, **12 August 2026**, *Crane Rises as Demolition Wraps at Toronto Coach Terminal Redevelopment*: 130 Elizabeth "44-storey mixed-use rental and institutional tower", 147.7 m, 547 rental homes, architects—Alliance; 610 Bay "16-storey mixed-use building", 55.45 m, 280 rental homes, Studio Gang with architects—Alliance; and
> "From Edward Street, a newly erected luffing-jib crane now rises above the west parcel's excavation."
<https://urbantoronto.ca/news/2026/08/crane-rises-demolition-wraps-toronto-coach-terminal-redevelopment.61530>
STOREYS, 3 April 2025: "The facades along Edward Street and the rear of the building incorporate a series of angled projections". <https://storeys.com/kilmer-tricon-plans-toronto-coach-terminal/>

**FACT — permits (CKAN active permits).** 130 Elizabeth: demolition 25 230504 DEM issued 2025-12-03; conditional shoring permit **25 267337 SHO issued 2026-08-04** — one day after the addresses appeared; foundation part-permit applied 2026-07-27; new building 25 267337 BLD "44-storey mixed-use rental apartment building … 547 residential units, including 140 affordable" under review. 604 Bay: partial demolition 25 259053 DEM issued 2026-03-27; new building 25 267262 BLD "16-storey mixed-use rental apartment building", 280 units, Under Review; shoring applied 2026-09-02.
CoA **A0849/25TEY** (130 Elizabeth, in 2025-11-17, heard 2026-01-14, Approved, final 2026-02-05): "15-storey mixed-use building (East Block fronting Bay Street)" and "43-storey mixed-use building (West Block fronting Elizabeth Street)", "827 purpose-built rental units".

**Discrepancy for the writer:** storeys and units drift by stage — 16/43 + 858/245 (OZ), 15/43 + 827/210 (SA, CoA), 16/44 + 280+547 (permits, UT Aug 2026), 873/290 (Nov 2024 release). The article uses the OZ stage (16 and 43 storeys, 858 rental units, 245 affordable) and says so.

**INFERENCE (high):** the four Edward St numbers are pre-assigned frontages of the two towers — 73/75/85 for the Bay St (east) block, 107 for the Elizabeth St (west) block (link field, item 3) — issued the day before shoring was permitted. **Nothing found** naming 73, 75, 85 or 107 Edward St in any source.

**Confidence: confirmed** (project, applicant, application numbers, south side, construction stage). Address-number level: inference from link field only.

---

## 8. 273 Merton St (new reserved) and 275 Merton second point (3 Aug) — 267-275 Merton, 40 storeys, City land

**Searched:** CKAN all datasets for 267–275 Merton; `"275 Merton Street" Toronto development`; `"273 Merton" Toronto` (nothing for 273); `site:toronto.ca legdocs "267-275 Merton Street"`.

**FACT.** City *Decision Report - Approval, 267-275 Merton Street - Zoning By-law Amendment Application*, **10 January 2025**, Ward 12, application **24 231134 STE 12 OZ**:
> "The site is located on the south side of Merton Street in the Davisville neighbourhood just west of Mount Pleasant Road. The site is an assembly of 267 Merton Street and 275 Merton Street, a City-owned property."
> "The 275 Merton Street parcel includes a two-storey office building owned by the City of Toronto and occupied by Toronto Water."
> "128-metre (40 storeys), excluding the mechanical penthouse, mixed-use, purpose-built rental building, containing 494 dwelling units, of which 148 (30 percent) will be affordable rental units."
<https://www.toronto.ca/legdocs/mmis/2025/ph/bgrd/backgroundfile-252090.pdf> (page footer reads "269-275 Merton Street" while the title says 267-275 — note, don't interpret.)
**FACT.** CKAN: OZ submitted 2024-10-25; Site Plan **25 162380 STE 12 SA** submitted 2025-05-20, "NOAC Issued". Demolition **25 178542 DEM** at 275 ("Demolish existing 2 storey office building") issued 2025-07-10, **completed 2026-03-17**; the new-building permit **25 252134 BLD** ("40-storey … 494 dwelling units, including 148 affordable rental units, and 153 sqm of retail") is filed under **267 Merton**, applied 2025-11-10, Examiner's Notice Sent.
**FACT.** City news release, **24 October 2025**, groundbreaking: partners City, CreateTO, Collecdev-Markee; "Formerly home to a Toronto Water office building, the 275 Merton St. development repurposes City-owned land". <https://www.toronto.ca/news/city-of-toronto-createto-break-ground-on-new-purpose-built-rental-project-on-city-owned-land-with-494-new-rental-homes/>
**FACT.** City report 9 June 2025: "construction starts can be achieved in September 2025 for 267-275 Merton". <https://www.toronto.ca/legdocs/mmis/2025/ph/bgrd/backgroundfile-256217.pdf>
**FACT.** Project site: "Construction officially began in September 2025"; demolition Sept 2025–Feb 2026; above-grade Oct 2026–Jun 2028; latest update 26 June 2026. <https://www.275merton.com/>
**FACT.** UrbanToronto database: Collecdev-Markee Developments and CreateTO, gh3, 40 storeys, 135.45 m, 494 units, Under Construction, last post Aug 24, 2026. <https://urbantoronto.ca/database/projects/267-275-merton-street.56369>

**INFERENCE (high):** 273 Merton (Structure, reserved, linked to the reserved 275 Land point) is the tower's pre-assigned building address, issued ~4.5 months after demolition closed and ahead of above-grade work. **Nothing found** naming 273 Merton anywhere.

**Confidence: confirmed** (project, partners, dates); 273 by link field only.

---

## 9. Danforth Ave at Woodbine Ave (15 Aug) — Choice Properties, 35 + 10 storeys, permits applied 26–27 Aug

**Searched:** CKAN all five at Danforth 2078–2108, Woodbine 975–987, Strathmore 677–687; `"2078 Danforth" OR "2106 Danforth" Woodbine 35-storey`; storeys.com; Beach Metro; staff report (pypdf); by-law 1212-2024 (pypdf); UrbanToronto thread pages 1, 7–10; `"985 Woodbine" urbantoronto 2026`.

**FACT — the project.**
- OZ **19 122810 STE 19 OZ**, submitted 2019-03-07, Closed: "Official Plan and Zoning By-Law Amendments to permit the redevelopment of the site for a a 35-storey residential mixed-use building along Danforth Avenue and a 10-storey residential building along Strathmore Boulevard. The two buildings share an underground parking garage." Filed under 2078, 2086, 2100, 2102, 2106 DANFORTH and 985 WOODBINE; WARD_NAME Beaches-East York.
- SB **21 219361 STE 19 SB**, 2021-09-29, Closed: "Draft Plan of Subdivision for the creation of 2 blocks."
- SA **24 251716 STE 19 SA**, submitted 2024-12-18, `Under Review `: "Site Plan Control application to permit a 10- and 35-storey mixed-use building connected by a 1-storey podium, containing 601 rental dwelling units and 4,474.3 square metres of non-residential gross floor area. The application includes a privately owned public space (POPS), a grocery store, a preschool, and an institutional theatre space."
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&filters=%7B%22STREET_NAME%22%3A%22WOODBINE%22%2C%22STREET_NUM%22%3A%22985%22%7D>

**FACT — by-law 1212-2024, council 2024-11-14:** "Item TE17.8, adopted as amended by City of Toronto Council on November 13 and 14, 2024 … BY-LAW 1212-2024 To amend Zoning By-law 569-2013 … 985 Woodbine Avenue and 2078, 2086, 2100, 2102 and 2106 Danforth Avenue." <https://www.toronto.ca/legdocs/bylaws/2024/law1212.pdf>
Staff decision report 2024-10-07: "The site is immediately adjacent to the Woodbine TTC station." "The proposed non-residential uses include a grocery store and theatre space in the west building and daycare space in the east building. The application also proposes a total of 606 residential units, including 14 rental replacement units and 12 affordable rental units." <https://www.toronto.ca/legdocs/mmis/2024/te/bgrd/backgroundfile-249314.pdf>

**FACT — Committee of Adjustment variance, decided 2025-11-12.** CoA closed, 985 WOODBINE, **A0691/25TEY**, IN_DATE 2025-09-10: "To alter the development standards (as approved under Site Specific Zoning By-law 1212-2024) for a mixed-use building (10 and 35-storeys, connected by a one-storey podium), by increasing the height of the northwest and southeast corners of the 35-storey tower (Building A) by removing the chamfering … There will be a total of 601 rental dwelling units on this lot, including 14 rental replacement units and 12 affordable rental units." C_OF_A_DESCISION `Approved`, FINALDATE 2025-12-03.

**FACT — building permits applied for inside the window, 11–12 days after the addresses were reserved (most recent milestone).** Permits active, 985 WOODBINE:
- **26 226392 BLD** New Building, APPLICATION_DATE **2026-08-26**, STATUS `Application Acceptable`, DWELLING_UNITS_CREATED `436`, EST_CONST_COST `117562000`: "THE PROJECT CONSISTS OF TWO RESIDENTIAL BUILDINGS (TOWER A, AND TOWER B) CONTAINING A TOTAL OF 601 DWELLING UNITS, AND INCLUDING TWO LEVELS OF BELOW GRADE PARKING. THIS PERMIT FOR TOWER A"
- **26 226705 BLD** New Building, APPLICATION_DATE **2026-08-27**, `Application Acceptable`, DWELLING_UNITS_CREATED `165`, EST_CONST_COST `114058000`: "… THIS PERMIT FOR TOWER B AND 2 LEVELS OF UNDERGROUND GARAGE."
- plus SHO/FND/STR partial permits and STS/DRN/PLB/HVA sub-permits dated 2026-08-26/27.
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22WOODBINE%22%2C%22STREET_NUM%22%3A%22985%22%7D>

**FACT — what is on the site now, from permit text:** 985 Woodbine is a retail store — "Value Mart" (permits 09 138119 PLB, 15 204300 BLD) and, in 2024, "Your Independent Grocer" (24 152281 BLD, "install security gates in an existing retail store"); 2078 Danforth is a "Bank" (04/05 permits, "Closed - Dormant" 2026-06-08). No demolition permit on file at any of the addresses.

**FACT — press/developer (*summary-level*):** Storeys, 2025-01-20: developer "Choice Properties REIT (real estate arm of George Weston Limited)", architect "Superkul", "1.6 acres", original application "February 2019". <https://storeys.com/985-woodbine-avenue-choice-properties/> . Beach Metro, 2024-11-18: approved at council's November meeting; Councillor Brad Bradford quoted. <https://beachmetro.com/2024/11/18/woodbine-and-danforth-development-approved-by-city-with-provision-more-affordable-units-will-be-sought/> . UrbanToronto thread (title "985 Woodbine | 118.5m | 35s | Choice Properties | Superkül"), page 10, posts of 2025-12-28 and 2026-05-24: store closure "deferred from February to September 2026", "NOAC has not been issued", grocery operator signage posted May 2026. <https://urbantoronto.ca/forum/threads/toronto-985-woodbine-118-5m-35s-choice-properties-superk%C3%BCl.29773/page-10> — forum-level.

Unit count drifts across sources: 646 (Beach Metro / Dec 2023 scheme), 606 (staff report, Oct 2024), 601 (SPA, CoA and both permits). Use 601 and note the drift.

**FACT — Strathmore Blvd 677–687: 0 records in all five datasets.** The new Strathmore numbers have no paper of their own.

**INFERENCE:** the file's 15 Aug batch (two Strathmore numbers for the 10-storey building on Strathmore, a new 975 Woodbine 3 m from 2078 Danforth for the tower, and re-pointed 985 Woodbine / 2106 Danforth) is the address set for the two-block subdivision, reserved just before the permit applications landed. No source assigns numbers to buildings.

**Confidence: high** — CKAN, by-law and staff report agree; the permits fall inside the window.

---

## 10. Bloor St W at Markland Dr (15 Aug) — Hazelview's 210 Markland Drive infill, severed into three lots Dec 2025

**Searched:** CKAN all five resources at Bloor 4370–4400 and Markland 206–214; `"210 Markland Drive" Etobicoke development`; `"210 Markland" Hazelview council approved`; `site:toronto.ca legdocs "210 Markland Drive"`; `urbantoronto "210 Markland"`; pypdf of the staff report; scan of 2025 by-laws 30–74 for "Markland".

**FACT — application 22 217986 WET 02 OZ, submitted 2022-10-17.** CKAN Development Applications, 210 MARKLAND DR:
> "Revised proposal to retain the existing 13-storey residential building on site and to develop three new buildings with heights of 12, 9, and 10 storeys respectively . 484 residential units are proposed … full movement access from Markland Drive and right-in-right-out access from Bloor Street West. The proposal also includes 1591 sq/m parkland dedication at the northeast corner of the site connecting to Millwood Park to the immediate east"
STATUS `Closed`; WARD_NAME `Etobicoke Centre`; COMMUNITY_MEETING_DATE 2023-05-24.
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&filters=%7B%22STREET_NAME%22%3A%22MARKLAND%22%2C%22STREET_NUM%22%3A%22210%22%7D>
- Companion subdivision application **22 217995 WET 02 SB**, same date, STATUS `Under Review ` — description is the *earlier* scheme ("four 12-storey apartment buildings, while retaining the 13-storey existing building").

**FACT — staff decision report, 2024-12-18, to Etobicoke York Community Council:**
> "The existing 13-storey residential building on site, which contains 152 rental dwelling units (the "existing building"), will be retained."
> "The site is generally rectangular in shape with an area of 17,438 square metres, and with frontage on Bloor Street West (135 metres), Markland Drive (115 metres), and Silverthorne Bush Drive (165 metres). To the east, the site has frontage on Millwood Park."
> "Further engagement took place with the Markland Wood Homeowners Association (MWHA) throughout the application review process."
<https://www.toronto.ca/legdocs/mmis/2025/ey/bgrd/backgroundfile-251683.pdf> ("Markland Wood" is therefore usable — it is in the City's report.)

**FACT — by-law enacted 2025-02-05.** By-law 54-2025: "Authority: Etobicoke York Community Council Item EY19.1, as adopted by City of Toronto Council on February 5, 2025 … To amend Zoning By-law 569-2013, as amended, with respect to the lands municipally known in the year 2024 as 210 Markland Drive." <https://www.toronto.ca/legdocs/bylaws/2025/law0054.pdf>
(*Summary-level*, from search index of 2025.EY19.1: EYCC on 2025-01-09 amended Building A from 9 to 8 storeys — TMMIS page not opened; do not print.)

**FACT — the site was severed into three lots at Committee of Adjustment, decided 2025-12-04 (most recent milestone).** CoA active, 210 MARKLAND DR, file **B0031/25EYK**, IN_DATE 2025-06-27, WORK_TYPE `Sever Lot`:
> "To obtain consent to sever the property into three lots. The existing 13 storey Apartment Building will remain."
HEARING_DATE 2025-12-04, C_OF_A_DESCISION `Approved`, NUMBER_OF_LOTS_CREATED `2`, STATUSDESC `Conditional Consent`. (An earlier identical filing, SYS_ID 5662090, was `Cancelled` the same day it was filed.)
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=51fd09cd-99d6-430a-9d42-c24a937b0cb0&filters=%7B%22STREET_NAME%22%3A%22MARKLAND%22%2C%22STREET_NUM%22%3A%22210%22%7D>

**FACT — developer, *summary-level*.** Hazelview's own page: "Hazelview Investments", "three new mid-rise buildings plus one retained existing 13-storey tower", "approximately 424,000 square feet of new purpose-built rental housing", status "Entitlement". <https://www.hazelview.com/private-real-estate-investing/development-management-v2/developments/210-markland-drive> . Storeys.com, 2025-02-07: "The infill development would add 484 new units to the site plus 3,530 sq. ft of non-residential space". <https://storeys.com/developments-approved-toronto-february-2025/> . UrbanToronto thread title: "210 Markland | 46m | 12s | Hazelview | Diamond Schmitt". <https://urbantoronto.ca/forum/threads/toronto-210-markland-46m-12s-hazelview-diamond-schmitt.34514/>

Storey counts appear three ways across sources; the article cites the application record's 12, 9 and 10 and the by-law.

**FACT — no building permits yet at the new numbers.** Permits active/cleared at 4380–4390 Bloor: 0 records (only hit in the 4370–4400 range is 4370 Bloor St W, 2004 irrigation permit, "Installation of irrigation services at Millwood Park"). Permits at 210 Markland: 3 cleared, all maintenance on the existing tower (latest: 22 162337 BLD balcony repairs, COMPLETED 2026-07-31). Dev apps at 4380–4390 Bloor and 208/212 Markland: 0.

**INFERENCE:** five new reserved addresses + a re-pointed 210 = one address per new building/lot after a three-lot severance and a by-law that gives frontage on both Bloor and Markland. No source states which building gets which number.

**Confidence: high** on what/who/when (CKAN + by-law + report); the address-to-building mapping is inference.

---

## 11. 3986 Eglinton Ave W (15 Aug, reserved, Etobicoke Centre) — nothing at the address; an emergency exit building filed 250 m away

**Searched:** CKAN all five resources at 3980–3990 Eglinton (with STREET_DIRECTION check); full scan of Eglinton W 3800–4200 and all of Richview Rd in dev apps, CoA and permits; `"3986 Eglinton Avenue West" Toronto`; Metrolinx ECWE Scarlett/portal/what-we're-building/open-house pages; `Metrolinx "Richview Road" emergency exit building`.

**File row (store):** 3986 Eglinton Ave W, ADDRESS_CLASS_DESC `Structure`, MAINT_STAGE `RESERVED`, no PLACE_NAME, coords 43.68399, -79.52273, WARD_NAME Etobicoke Centre.

**FACT — nothing at 3986 itself.** Dev apps 0, permits active 0, permits cleared 0, CoA active 0, CoA closed 0. Web search for the address: nothing. The 3986 Eglinton Ave **E** trap was checked — nothing either way.

**FACT — an ECWE emergency exit building is being permitted at 75 Richview Rd, ~250 m away — and the permit text confirms July's "EEB1" label.**
- Site Plan application **26 209163 WET 02 SA**, STREET_NUM `0` RICHVIEW RD, DATE_SUBMITTED **2026-07-27**, STATUS `Under Review `, WARD Etobicoke Centre:
  > "Proposed emergency exit building,  ancillary building which provides a route for emergencyegress from the tunnel and facilitates maintenance access."
  <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&filters=%7B%22STREET_NAME%22%3A%22RICHVIEW%22%7D>
- Building permit **26 229667 BLD** (New Building), 75 RICHVIEW RD, APPLICATION_DATE **2026-09-01**, STATUS `Application Acceptable`:
  > "Proposed construction of an Emergency Exit Building (EEB-1) at 75 Richview Road for the ECWE"
  (plus STS/HVA/PLB sub-permits same day). This date is *after* the window.
  <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22RICHVIEW%22%2C%22STREET_NUM%22%3A%2275%22%7D>
- Same day (2026-07-27) the same City planner filed **26 209400 WET 02 SA** at 4200 Eglinton Ave W ("Proposed two separate above grade buildings with a combined gross floor area of 8330 m2") — the ECWE station site where permit 25 159310 BLD reads "Proposal for the construction of Transit Station for ECWE".

**FACT — Metrolinx context (*summary-level*):** the Scarlett portal is "along the north side of Eglinton Avenue West, just west of Scarlett Road" and is "the transition point between the 1.5-kilometre elevated segment of the line and the western underground portion of the route". <https://www.metrolinx.com/en/projects-and-programs/eglinton-crosstown-west-extension/what-were-building/extraction-shaft-and-portal> . No Metrolinx page fetched names Richview Rd or any Eglinton address for an EEB.

**INFERENCE (medium, not printed as fact):** 3986 Eglinton Ave W could be a transit-related reservation — a new *Structure* point, Etobicoke Centre, 19 days after the EEB site-plan filing, ~250 m from 75 Richview Rd. Counter-evidence: EEB-1 already has an address (75 Richview Rd) and the row carries no PLACE_NAME (July's station entrances did). The article writes 3986 as a silence with a sourced neighbour and does not call it an EEB.

**Confidence:** nothing found at the address; the 75 Richview Rd filing is **confirmed**.

---

## 12. Victoria Park Ave 1974–1982 (6 Aug) — a private road with a Nov 2024 fire-route by-law; what stands on it, unknown

**Searched:** CKAN all five at 1970–1984; full scan of Victoria Park 1900–2050 in dev apps + CoA; `"1974-1982 Victoria Park"`; fire-route by-law and Chapter 880 Schedule A (pypdf); `"1970 Victoria Park" townhouse developer`; listing sites (403/429).

**File rows (store):** old row `1974-1982 Victoria Park Ave` (LO_NUM 1974, HI_NUM 1982, class `Land`, ADDRESS_POINT_ID 12104356, coords 43.74976,-79.3128) ends 2026-08-03; new `1974` keeps the same ADDRESS_POINT_ID 12104356 (class `Land`, coords 43.74909,-79.31263, 75.8 m from the old point); 1976/1978/1980/1982 are new IDs 6008399x, class `Structure`, REGULAR, spread over ~110 m north–south. Neighbours on file since 2025-04-01: 1966, 1968A–C, 1970A–C, 1972A–C, 1972R (even side) and the range `1973-1991` (odd side).

**FACT — 0 records in every dataset at 1974, 1976, 1978, 1980 and 1982** (dev apps, permits active, permits cleared, CoA active, CoA closed).

**FACT — the range is a designated fire route on a private road, by-law 1172-2024.** Municipal Code Chapter 880 Schedule A lists:
> "1970 Victoria Park Avenue [Added 2024-04-05 by By-law 296-2024]"
> "1974-1982 Victoria Park Avenue [Added 2024-11-01 by By-law 1172-2024]"
and, as a separate legacy entry with no by-law note, "1980 Victoria Park Avenue *" and "Victoria Park Avenue and Van Horne Avenue (plaza) *".
<https://www.toronto.ca/legdocs/municode/1184_880_a.pdf>
Draft bill (NYCC, 2024-10-03): "That part or those parts of the private road or roads shown on the site plans filed with the Fire Chief … (a) 1974-1982 Victoria Park Avenue". <https://www.toronto.ca/legdocs/mmis/2024/ny/bgrd/backgroundfile-249209.pdf>

**FACT — the adjacent 1970 project is a 67-unit townhouse subdivision.** Dev apps at 1970 VICTORIA PARK: 13 172109 NNY 34 OZ (2013-05-22, Closed) "Change in Zoning to permit 67 townhouse dwelling units in 3 storey buildings"; 13 172935 NNY 34 SA (2013-05-23, Closed) "Construct 67 townhouse dwelling units."; 20 233432 NNY 16 PL (2020-12-23, Closed) "Part lot control exemption application to create 67 townhouse lots"; 20 233440 NNY 16 CD (Draft Plan of Common Element condominium). All WARD_NAME Don Valley East. The OZ record is also filed under 1966, 1968 A–E, 1970 A–F, 1972 A–C — the address list stops at 1972. 417 cleared permits at 1970 (conditional permits for Blocks A/B/C, models A1–E2, applied 2015-06-09, ISSUED 2023-01-06/09); none mention 1974–1982.
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&filters=%7B%22STREET_NAME%22%3A%22VICTORIA%20PARK%22%2C%22STREET_NUM%22%3A%221970%22%7D>

**FACT — the odd side (1973-1991) is a different, old proposal:** 15 270704 ESC 37 CD (2015-12-31, Closed) "Magnus Opus Developments (Victoria Park) Corporation, owners of … 1955, 1961, 1967, 1973, 1979, 1985 and 1991 Victoria Park Avenue". Not this side of the street.

**Nothing found:** what physically occupies 1974–1982 (the record says "private road"; it does not say townhouses, plaza, or anything else), the builder of the 1970 project (listing sites 403/429; resale listings labelled "Parkwoods-Donalda" are listing-level and not used), and any 2025–26 event that explains the August restatement.

**INFERENCE:** a fire route designated in Nov 2024 for "1974-1982" as one private road, sitting directly north of a 67-lot townhouse subdivision whose own fire route was designated seven months earlier, reads like a further block of the same or a sister project being addressed out individually — but no source says so.

**Confidence:** high that it's a private road with a Nov 2024 fire-route by-law; low on what's built there — write "the public record is silent on what stands on it".

---

## 13. 552, 554, 556, 558 Wilson Ave (gone between 31 Jul and 3 Aug) — public record silent on these four numbers

**Searched:** `"552 Wilson Avenue" OR "556…" OR "558…"`; `"550 Wilson Avenue" OR "554…" OR "560…"`; `"Wilson Avenue" 552… "York Centre" townhouses OR "site plan" OR rezoning`; `"50 Wilson Heights" Housing Now … Block 2 Block 3 Block 4`; `"155 Transit Road" Toronto TTC`; CKAN dev-apps `STREET_NAME=WILSON` (78 records) and `STREET_NAME=WILSON HEIGHTS` (9); permits `STREET_NAME=WILSON` (92) and `STREET_NAME=WILSON HEIGHTS` (50); CoA active and closed for WILSON.

- FACT — **Nothing found** at 552–558 Wilson Ave in any dataset: no development application (the 540–600 records are 545/555 Wilson — The Station condos, 2008–09; 470–530 Wilson — Nordic, 2016–18; 570/590 Wilson — see below), no building permit (540–600 hits are only 545 and 570), no Committee of Adjustment file. <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&filters=%7B%22STREET_NAME%22%3A%22WILSON%22%7D&limit=1000> ; <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22WILSON%22%7D&limit=1000>
- Store — the four points (ADDRESS_CLASS "Structure", MAINT_STAGE RESERVED, ward York Centre, ids 30159028–31 consecutive) ran 2025-04-01 .. 2026-07-31 at 43.7346–43.7347, -79.44845 → -79.4489: north side of Wilson Ave, between 530 Wilson (-79.4462) and 570 Wilson / Wilson Station (-79.4509), just west of **2 and 10 Wilson Heights Blvd** (both still RESERVED) and beside the **50 Wilson Heights Blvd** points (43.73538, -79.44911 regular; a second RESERVED point at 43.73563, -79.44891). Nearest other streets: 65 Ansford Ave 32 m, 10 Wilson Heights Blvd 67 m, 565 Wilson Ave 74 m. In the same 2026-08-03 snapshot the rows for 75 and 79 Billy Bishop Way and 155 Transit Rd were re-issued with moved coordinates — a cleanup pass on the station block, not a demolition. No new street or address appeared within 300 m in that snapshot.
- FACT — the land they sat on: Housing Now at 50 Wilson Heights Blvd, "northwest corner of Wilson Avenue and Wilson Heights Boulevard", 8 acres, former commuter lot; Tridel and Greenwin selected; "1,484 homes, with 520 affordable rental homes"; status "Under Construction". <https://createto.ca/projects/50-wilson-heights-boulevard>
- FACT — Decision report, 21 Nov 2024 (24 211509 NNY 06 OZ): Block 1 "is the most south-westerly block of the overall lands abutting the north side of Wilson Avenue"; "East: 50 Wilson Heights (Block 2) will be the site of 3, 17-storey mixed-use residential buildings with 765 rental units". <https://www.toronto.ca/legdocs/mmis/2024/ph/bgrd/backgroundfile-250893.pdf>
- FACT — City news release, 26 Nov 2024: groundbreaking; rental construction "anticipated to begin spring 2025", "first occupancy expected early 2029". <https://www.toronto.ca/news/city-of-toronto-and-createto-break-ground-on-new-mixed-use-transit-oriented-housing-project-with-520-affordable-rental-homes/>
- FACT — Building permits are all filed under **50 Wilson Heights Blvd**, not Wilson Ave: Tower A "531 rental units, 286 affordable housing" (`24 254305 BLD`, examiner's notice); Tower A foundation conditional permit issued **2025-12-17**; Tower A and Tower C structural-framing partial permits applied **2026-03-11 / 2026-03-13**, under review; Tower B 116 units, Tower C 120 units. <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22WILSON%20HEIGHTS%22%7D&limit=100>
- FACT (area context only, ~550 m west): rezoning `26 128829 NNY 06 OZ` at 570 Wilson Ave and draft plan of subdivision `26 128887 NNY 06 SB` at 590 Wilson Ave, both submitted **2026-03-12**, "up to 63 storeys (195 metres)", "9,529 dwelling units", "1 future Wilson station development block", community meeting 2026-07-14. <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&q=128829&limit=20> ; <https://haveyoursay.toronto.ca/city-planning-development-review-community-consultations/590-wilson-avenue> — not a cause of the removal; different parcel.
- INFERENCE (low): 552–558 were address reservations along the Housing Now site's Wilson Ave frontage, dropped because the buildings are being permitted under 50 Wilson Heights Blvd. No source says this; nothing was withdrawn, refused or built under those numbers.

**Confidence: nothing found** on the four numbers themselves; the surrounding project is confirmed.

---

## 14. 4003 and 4005 Dundas St W (retired 7 Aug) — demolished by January 2024; sold out of receivership March 2026

**Searched:** `"4003 Dundas Street West" OR "4005 Dundas Street West" Toronto`; `3775-4005 Dundas Street West receivership sale 2026 buyer demolition`; `"4003-4005 Dundas" City Council 2020 demolition`. CKAN all datasets for 4003, 4005, and 3775/3779/3803 (2019+). Fetched the 2020 staff report (text-extracted), TDB Advisory docket, RENX, Storeys, Gord Perks page, UrbanToronto database.

**FACT (verbatim, City staff report, 25 Feb 2020, "Non-Residential Demolition Application – 3775, 3379 [sic], 3803, and 4003-4005 Dundas Street West", Ward 4):** "the application for demolition of four (4) non-residential buildings … (Application No. 19-264181 DEM, 19-264205 DEM, 19-264218 DEM, & 19-264231 DEM) are submitted to City Council" … "the commercial buildings at 3775, 3779, 3803, and 4003-4005 Dundas Street West would be demolished and the site re-developed for the purposes of a new thirteen (13) storey mixed-use building containing 297 rental and affordable-rental residential units with grade related retail" … "a rezoning of the site was approved in July of 2017 with the adoption of site specific By-law 827-2017" … "on October 2, 2019, City Council approved the project under the Open Door Affordable Housing Program and the project is enrolled in the federal CMHC Rental Construction Financing program." <https://www.toronto.ca/legdocs/mmis/2020/te/bgrd/backgroundfile-147715.pdf>

**FACT (CKAN, verbatim):** cleared permit at **4003 Dundas St W**: **19 264231 DEM**, "Demolition Folder (DM)", applied 2019-12-23, **issued 2021-02-10, completed 2024-01-26**, "Proposed demolition of the entirety of the existing one-storey commercial building, including footings and foundations", proposed use "Mixed-Use Rental Apartment". **4005 has no permit record** (it shares the OZ/SA records only). Dev apps: 12 295537 WET 13 OZ (2012-12-18, Closed) "13-storey mixed-use building with 297 rental apartment units"; 12 295562 WET 13 SA, status "Under Review", description begins "INACTIVE". No new application or permit at 3775/3779/3803 since 2019. Reproducible: `…datastore_search?resource_id=a96c0ba4-3026-402b-b09d-5b1268b8f810&filters=%7B%22STREET_NAME%22%3A%22DUNDAS%22%2C%22STREET_NUM%22%3A%224003%22%7D`

**FACT (receivership docket, per WebFetch summary of TDB Advisory):** debtors "3803 DSW TAS LP, 3803 DSW MR LP, 3803 DSW Urban Properties Inc."; receiver TDB Restructuring appointed **6 March 2025** (Ontario Superior Court); "Approval and Vesting Order (Real Property)" **20 March 2026**; Receiver's Second Report 11 May 2026; "Order of the Court (Approval and Discharge)" **19 May 2026**. <https://tdbadvisory.ca/insolvency-case/3775-4005-dundas-street-west-toronto-ontario/>. Storeys (18 Mar 2025, per summary): debt $17,505,744 to Cameron Stephens Mortgage Capital; TAS's approved scheme 13 s / 297 rental / SvN. <https://storeys.com/tas-dundas-street-west-receivership/>. RENX (7 Apr 2026, per summary): buyer **Cogir Real Estate** "through Dundas West Project Limited Partnership and 10361968 Canada Inc."; site "Vacant development site"; "Cogir declined to comment for this article, so it is not known whether it plans to continue with the previous development proposal or redesign the project." <https://renx.ca/cogir-acquires-dundas-west-property-in-receivership-sale> (the summary's "transaction approved March 20, 2025" conflicts with TDB's 2026-03-20 — treat as a summary error; cite TDB.) UrbanToronto database "3775 Dundas West": developer COGIR, architect SvN, 13 s, 297 units, "Pre-Construction", "As of April 2026 the property is acquired by Cogir" <https://urbantoronto.ca/database/projects/3775-dundas-west.36763>. Councillor's page: "Demolition has taken place at the corner of Humber Hill Ave and Dundas St W … The Site Plan application has yet to be completed." <https://www.gordperks.ca/3775_4005_dundas_st_w>

**Store fact worth a line:** 3775 and 3803 Dundas St W remain active; only 4003/4005 came off — two of the four demolished commercial addresses.

**INFERENCE (high):** the buildings were gone by January 2024 (permit completion) and the address points outlived them by ~31 months; the retirement follows the site changing hands (vesting order March 2026, receiver discharged May 2026) — but no source ties the addressing to either event.

**Confidence: confirmed** (demolition, project, receivership, buyer); timing link **inference**.

---

## 15. Duplex Ave 530–538 (27 Aug) — five houses on the severed lots of 60 and 64 Roselawn Ave; the permits named the numbers in 2023

**Searched:** `"Duplex Avenue" 530…538 Toronto`; `"530 Duplex Avenue" OR "534…" OR "536…"`; `"538 Duplex" … new custom built`; `"C2C Design Build" Duplex Avenue`; `"60 Roselawn Avenue" OR "64 Roselawn Avenue"`; `TLAB "22 127860"`; CKAN dev-apps `q=DUPLEX` and `STREET_NAME=ROSELAWN`; CKAN permits `STREET_NAME=DUPLEX`, `STREET_NAME=ROSELAWN, STREET_NUM=60` and `=64`; CoA active + closed-since-2017 for DUPLEX and ROSELAWN.

- Store — the five points sit ~6–7 m apart on the west side of Duplex Ave at the Roselawn Ave corner (530 at 43.71067, -79.40131). Nearest other streets: 68 Roselawn Ave 19 m, 35 Castlefield Ave 50 m, 2458 Yonge St 128 m. The rows for **60 Roselawn Ave** (43.71069, -79.40127) and **64 Roselawn Ave** (43.71068, -79.4014) — the same spot — run 2025-04-01 .. **2026-09-01**, i.e. they were retired after the window closed (September's article).
- FACT — CoA consent `B0012/21NY` (60 Roselawn) and `B0013/21NY` (64 Roselawn), IN_DATE **2021-02-23**: "To obtain consent to sever each property (60 and 64 Roselawn Ave.) into five undersized parts for the purpose of lot additions to create five new houses fronting Duplex Avenue. Related Committee of Adjustment files include B0013/21NY, A0186/21NY, A0187/21NY, A0188/21NY, A0189/21NY, and A0190/21NY." Hearing **2022-03-08**, decision "Approved", appeal expiry 2022-04-04; STATUSDESC "Approved with Conditions" (B0012) and "TLAB Appeal" (B0013). <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=51fd09cd-99d6-430a-9d42-c24a937b0cb0&filters=%7B%22STREET_NAME%22%3A%22ROSELAWN%22%2C%22STREET_NUM%22%3A%2260%22%7D&limit=100> and the same URL with `%2264%22`.
- FACT — North York Community Preservation Panel minutes, 10 May 2021, item 4.5.3.1 "60-64 Roselawn Ave.": "An Application was submitted to the North York Committee of Adjustment (NY CofA) on February 21, 2021 for severance and minor variances to permit six semi-detached dwellings. No hearing is scheduled at present. A heritage nomination was previously submitted by Alex Grenzebach." <https://www.toronto.ca/legdocs/mmis/2021/pb/comm/communicationfile-135491.pdf> (Six semis in 2021 vs five detached as built — the scheme changed.)
- FACT — Building permits filed under 60 Roselawn: `23 182180 BLD` "LOT A - Pending address is 530 Duplex Ave. Proposal to construct a new 3 storey SFD-detached dwelling", applied 2023-07-31, **issued 2023-12-08**, builder "12362741 CANADA CORPORATION"; revision 01 "changes to the back elevation" issued **2026-03-18**. `23 189644 BLD` "LOT C - Pending address is 534 Duplex Ave", applied 2023-08-16, **issued 2024-06-26**, builder "C2C DESIGN BUILD LTD"; revision 02 (floor layout, internal heights) applied 2025-04-09, issued **2026-03-19**. Both status "Inspection". <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22ROSELAWN%22%2C%22STREET_NUM%22%3A%2260%22%7D&limit=100>
- FACT — Demolition permit under 64 Roselawn: `23 182148 DEM` "Proposal to demolish the existing 2 storey SFD-dwelling. See also 22 127860 TLAB.", applied 2023-07-31, **issued 2024-07-11**, dwelling units lost 1. <…same URL with `%2264%22`>
- FACT — Listing for 538 Duplex Ave (Batori Group): "Detached 4-Storey"; "A rare boutique collection of architecturally designed detached homes by C2C Design Build Ltd."; "Tarion warranty"; list price $2,538,000; "This property has sold." <https://www.batorigroup.com/listings/538-duplex-ave/>
- FACT — No development application, permit or CoA record carries a Duplex Ave number in 520–545. <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22DUPLEX%22%7D&limit=500>
- Not found: the TLAB outcome for file 22 127860 (search empty; TLAB decisions before Feb 2023 aren't on CanLII). INFERENCE (high): permits issued Dec 2023 / Jun 2024 mean the appeal was resolved in the applicant's favour by then.
- INFERENCE (medium): lots B, D, E (532, 536, 538) are absent from the *active*-permits dataset, which drops completed permits; 538 has already sold — consistent with those three being closed out.
- INFERENCE (high): the 27 Aug reserved→regular flip is the City activating the "pending" addresses the 2023 permits named, ~5.5 years after the severance was filed; the parents (60/64 Roselawn) then left the file on 1 Sep.

**Confidence: confirmed** (severance, builder, permits, pending-address link to 530/534, sale of 538). Two homes' permits and the TLAB outcome unverified.

---

## 16. 60 Huntington Ave — 60A/60B reserved (17 Aug), 60 remains — refused by the Committee of Adjustment, appealed; outcome not found

**Searched:** CKAN all five at 58–62 Huntington; `"60 Huntington" TLAB fourplex consent`; `"60 Huntington" "B0003/25SC"`; CoA Scarborough agenda 2025-10-08 (pypdf); TLAB hearings/decisions page; CanLII TLAB index (403 twice); `"60 Huntington Avenue" Scarborough Toronto 2026`. Boston "Huntington Avenue" hits discarded.

**FACT — a severance + fourplex application was refused by the Committee of Adjustment on 2025-08-13 and appealed to TLAB.** CoA active, 60 HUNTINGTON AVE, all IN_DATE 2024-12-31, HEARING_DATE 2025-08-13, WARD `20`:
- **B0003/25SC** (Consent, `Sever Lot`): "To obtain consent to sever the existing lot into two new residential lots. Cross reference Minor Variance applications A0006/25SC and A0005/25SC being considered jointly." C_OF_A_DESCISION `Refused`, NUMBER_OF_LOTS_CREATED `1`, STATUSDESC **`TLAB Appeal`**.
- **A0005/25SC** and **A0006/25SC** (Minor Variance, `New R Building`): "To construct a new three-storey fourplex. Cross reference Consent and Minor Variance Applications A0006/25SC and B0003/25SC being considered jointly." Both `Refused`, `TLAB Appeal`.
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=51fd09cd-99d6-430a-9d42-c24a937b0cb0&filters=%7B%22STREET_NAME%22%3A%22HUNTINGTON%22%2C%22STREET_NUM%22%3A%2260%22%7D>
(STATUSDESC is as-of the dataset refresh; it does not say the appeal is still open.)

**FACT — the appeal is listed on the Scarborough CoA agenda of 2025-10-08**, under "4. Toronto Local Appeal Body (TLAB) — TLAB Appeal: … 2. 60 Huntington **Drive** – B0003/25SC A0005/25SC A0006/25SC Refused by Committee, appealed by Owner". (The agenda's "Drive" is a typo — the CoA records say AVE.) <https://www.toronto.ca/wp-content/uploads/2025/09/9855-CommitteeofAdjustment-Scarborough-Hearing-Agenda-October-8-2025.pdf>

**FACT — no permits at 60.** Dev apps 0; permits active 0; permits cleared 0 at 60 (the only Huntington hits are 62 Huntington, a 2017 basement second suite, closed 2019). CoA closed 0.

**Nothing found — the TLAB outcome.** The City's TLAB page says decisions since 2023-02-01 are on CanLII; CanLII returned 403 to every fetch. Web search found no decision.

**INFERENCE:** 60A and 60B appearing as reserved while 60 stays is *consistent with* TLAB having allowed the two-lot severance — but no source says the appeal was decided, let alone allowed. Zolo's "Kennedy Park" is listing-level; use the ward.

**Confidence:** high on the refused-and-appealed history; the August trigger is unsourced — needs a browser check on CanLII before any claim beyond "under appeal".

---

## 17. 41 and 43 Wineva Ave — second reserved points (6 Aug) — a severance approved 1 Apr 2026

**Searched:** CKAN all five at 41 and 43 Wineva; `"41 Wineva" OR "43 Wineva"`; `"41 Wineva" Committee of Adjustment 2026`.

**FACT — a consent to sever 41 Wineva into two lots, with a three-unit houseplex on each, was approved 2026-04-01.** CoA active, 41 WINEVA AVE, **B0012/24TEY**, IN_DATE 2024-02-12, `Sever Lot`:
> "To obtain consent to sever the property into two undersized residential lots, and to maintain and create new easements/rights-of-way."
HEARING_DATE 2026-04-01, C_OF_A_DESCISION `Approved`, STATUSDESC `Conditional Consent`, WARD `19`.
Companion variances (CoA closed, FINALDATE 2026-04-22, both `Approved`):
- **A0190/24TEY**: "To convert the existing two-storey semi-detached dwelling with two dwelling units into a two-storey semi-detached dwelling (houseplex) with three dwelling units … The existing rear garage (attached to the houseplex) with three parking spaces will remain with one parking space allocated to this lot (and two parking spaces allocated to the north abutting conveyed lot, Parts 1, 2, 3 and 6, Draft R-Plan)."
- **A0189/24TEY**: same conversion, "Parking will be provided in the existing rear garage (attached to the houseplex on the south abutting retained lot, Parts 4, 5, and 7, Draft R Plan) with two parking spaces allocated to this lot."
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=51fd09cd-99d6-430a-9d42-c24a937b0cb0&filters=%7B%22STREET_NAME%22%3A%22WINEVA%22%2C%22STREET_NUM%22%3A%2241%22%7D>
Hearing agenda listing the three files: <https://www.toronto.ca/wp-content/uploads/2026/03/97be-CommitteeofAdjustment-Toronto-East-York-Agenda-April-1-2026.pdf> (title-level; not opened).

**FACT — 0 records** at 41/43 Wineva in dev apps, permits active, permits cleared. All CoA files are under 41; nothing is filed under 43.

**INFERENCE:** the two reserved points beside 41 and 43 are the two lots of the April 2026 conditional consent (retained south lot + conveyed north lot). Whether 43 is the "north abutting conveyed lot" is not stated in the record. "The Beaches" appears only on listing sites — use the ward (Beaches-East York).

**Confidence:** high on the cause; the 41↔43 lot mapping is inference.

---

## 18. 12 and 16 Wellesley St W — new reserved points (6 Aug) — a retail-unit severance finalised 24 Aug 2026

**Searched:** CKAN CoA (all years) and permits for 6–16 Wellesley St W; `"12 Wellesley Street West" OR "16 Wellesley Street West" Toronto 2026`; `8 Wellesley Residences CentreCourt retail heritage row houses`; `"8 Wellesley" CentreCourt occupancy 2025 OR 2026`.

**FACT — a consent to sever a ground-floor retail unit, finalised inside the window.** CKAN Committee of Adjustment, **B0021/26TEY**, 12 Wellesley St W, type CO / "Sever Lot", in **2026-02-18**, hearing 2026-05-13, **Approved**, appeal expiry 2026-06-08, **FINALDATE 2026-08-24**, condition expiry May 19, 2027:
> "To obtain consent for a stratified severance of an existing retail unit located on the ground floor (including the heritage wall located along the west façade of the building), into two parcels (units), for separate ownership. Also, to maintain the existing easements/rights-of-way."
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=9c97254e-5460-4799-896f-c7823413c81c&filters=%7B%22REFERENCE_FILE%23%22%3A%22B0021%2F26TEY%22%7D>

**FACT — the building is finished.** Permit **21 116610 BLD** (10 Wellesley St W), "55-storey mixed-use building with 600 dwelling units", issued 2022-12-20, **completed 2025-09-05**; heritage-retention permit 21 117722 BLD "Heritage Retention at 10-16 Wellesley Street West" completed 2025-12-23; demolition permits for 12 and 16 Wellesley St W (21 119514/119516 DEM) completed July 2025. CentreCourt, 21 July 2023: design "retains and restores the heritage facade at 10 through 16 Wellesley Street West in order to be used for retail and lobby space". <https://centrecourt.com/news/looking-at-two-years-of-progress-on-8-wellesley/>

**FACT (store).** The two new 6 Aug points are Land-class, RESERVED, with no link field, alongside the existing REGULAR 12 (Land) and 16 (Structure) points. (July's article had 10–16 Wellesley retired; the store shows 12's reserved point 30123253 went regular on 2026-07-09 and a fresh reserved point 60084113 appeared on 2026-08-06.)

**INFERENCE (moderate-high):** the consent created two parcels out of one retail unit; two new reserved Land points appeared 18 days before the consent was finalised. Do not assert which parcel gets 12 vs 16 — no source says.

**Confidence: likely** — mechanism inferred; the consent record itself is confirmed.

---

## 19. 17 and 19 Dunkirk Rd — reserved → regular, old 19 retired (18 Aug) — a 2021 severance, houses built 2023–25

**Searched:** CKAN all five at 15–21 Dunkirk; `"19 Dunkirk" OR "19A Dunkirk" OR "17 Dunkirk" Toronto`.

**File rows (store):** 17 Dunkirk RESERVED 2025-04-01..2026-08-17 → REGULAR from 2026-08-18; 19 Dunkirk had two rows (one REGULAR, one RESERVED) to 2026-08-17 → one REGULAR from 2026-08-18; 23 Dunkirk also re-versioned the same day. Ward Beaches-East York.

**FACT — a 2021 severance of 19 Dunkirk into two lots, approved 2022-03-30.** CoA closed, 19 DUNKIRK RD, IN_DATE 2021-08-10, HEARING_DATE 2022-03-30:
- **B0086/21TEY** (`Sever Lot`): "To obtain consent to sever an existing residential lot into two residential lots." `Approved`, NUMBER_OF_LOTS_CREATED `1`, FINALDATE 2024-09-17.
- **A1083/21TEY**, **A1084/21TEY**: "To construct a new three-storey semi-detached dwelling and a rear semi-detached ancillary building (semi-detached garage)." Both `Approved`, FINALDATE 2022-10-24.
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=9c97254e-5460-4799-896f-c7823413c81c&filters=%7B%22STREET_NAME%22%3A%22DUNKIRK%22%2C%22STREET_NUM%22%3A%2219%22%7D>

**FACT — demolition and two new-house permits, and the City's own permits call the lots 19A and 19B.**
- **22 147104 DEM**, applied 2022-05-16, issued 2022-10-17, COMPLETED 2023-06-26, `Closed`: "Proposal to demolish the existing 1 storey SFD-detached dwelling." DWELLING_UNITS_LOST `1`.
- **22 152366 BLD** (New Houses, `2 Unit - Semi-detached`), applied 2022-05-27, ISSUED 2023-04-25, STATUS `Inspection`: "PART 1 - West Lot, 19A Dunkirk RoadProposal to construct a new 3 storey semi dwelling with 2 units and semi-detached garage in the rear of lot." BUILDER_NAME `PETER JOSEPH POSPISIL`, EST_CONST_COST `390,000`.
- **22 152417 BLD**, applied 2022-05-27, ISSUED 2023-04-28, `Inspection`: "PART 2 - East Lot, 19B Dunkirk RoadProposal to construct a new 3 storey semi dwelling with 2 units …" DWELLING_UNITS_CREATED `2`.
- Revisions 01 to both issued 2024-04-19; HVAC permits issued 2024-04-25 / 2024-05-21; drain permits COMPLETED **2025-08-12** (cleared). Most recent dated event in the record: drains closed 2025-08-12; the BLD permits are still `Inspection`.
<https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22DUNKIRK%22%2C%22STREET_NUM%22%3A%2219%22%7D>

**FACT — nothing filed under 17 or 15/21 Dunkirk** in any dataset; dev apps 0 at all numbers.

**Sourced discrepancy worth a sentence:** the permits name the two halves "19A" (west) and "19B" (east); the address file gave them **17** and **19** — the file's numbering stands, the permit's is the builder's working label.

**INFERENCE:** the 18 Aug flip from reserved to regular marks the City finalising the two addresses for the finished semi pair some 2–3 years after the permits issued; the record does not say what prompted it that week.

**Confidence:** high on cause (severance + rebuild); the trigger for the August date is unsourced.

---

## 20. 8R Hilltop Rd — new regular address (3 Aug) — a laneway suite permitted 25 Jun 2026; and Carpark 131 next door

**Searched:** `"8 Hilltop Road" Toronto laneway OR garden suite`; `"Carpark 131" OR "Green P 131" Eglinton Avenue West`; `Toronto address "R" suffix rear laneway suite "Municipal Addressing"`; `open.toronto.ca "Address Points" LO_NUM_SUF suffix "R"`. CKAN all datasets for 8 and 8R Hilltop, 912 Eglinton W. Fetched Municipal Code Ch. 598 (Numbering of Properties), the City's Municipal Numbering page, Ch. 950 Sch. 34, TPA facilities report.

**FACT (CKAN, verbatim) — 8 Hilltop Rd:**
- CoA **A0606/24NY**, IN_DATE **2024-12-09**, hearing **2025-11-06**, decision **"Approved"**: "To construct a new multiplex building in conjunction with a new laneway suite. Please note this application was previously deferred Thursday, February 6, 2025." Zoning "RD (f15.0; d0.6) (x1335)". (Committee of Adjustment dataset, "Closed Applications since 2017", filters `STREET_NAME=HILLTOP, STREET_NUM=8` — <https://open.toronto.ca/dataset/committee-of-adjustment-applications/>)
- **26 148922 BLD**, "Small Residential Projects", structure type **"Laneway / Rear Yard Suite"**, work "New Laneway / Rear Yard Suite", applied 2026-04-23, **issued 2026-06-25**, description "New Laneway Suite", PROPOSED_USE "Garden Suite", units created 1, est. cost $250,000, 97.2 m² residential.
- **26 148877 BLD**, "New Houses", "3+ Unit - Detached", applied 2026-04-23, **issued 2026-07-09**: "Proposal for demolishing existing SFD and construct a new Fourplex", 4 units, $1,500,000, builder **"8 HILLTOP HOLDINGS LIMITED"**.
- **26 148899 DEM**, issued 2026-07-09: "Proposed demolition of a detached single-family dwelling to construct a new 4-unit houseplex and a laneway suite."
Reproducible: `…datastore_search?resource_id=6d0229af-bc54-46de-9c2b-26759b01dd05&filters=%7B%22STREET_NAME%22%3A%22HILLTOP%22%2C%22STREET_NUM%22%3A%228%22%7D`. The records say "laneway suite" and "Garden Suite" in the same folder — quote both, don't pick. **8R** itself has 0 records (permits are filed under 8). 8R appeared in the file **39 days** after the suite permit issued and 25 days after the fourplex/demolition permits.

**FACT — 912 Eglinton Ave W:** Ch. 950 Sch. 34 (verbatim): "131 Hilltop 912 Eglinton Avenue West" — the car park is literally named "Hilltop". <https://www.toronto.ca/legdocs/municode/toronto-code-950-34.pdf>. TPA report (verbatim): "131 | 912 Eglinton Ave W | Surface | Owned | 26 … Serves businesses within Upper Village BIA along Eglinton Ave W." <https://www.toronto.ca/legdocs/mmis/2024/pa/bgrd/backgroundfile-244114.pdf>. Store: 8R (43.70093, -79.42824) is 28 m from 912 Eglinton (43.70075, -79.42800) — the suite backs onto the Green P lot. **INFERENCE (moderate):** the rear suite's frontage is the lane/lot behind, hence the R suffix rather than a lane address.

**"R" suffix — nothing found.** Municipal Code Ch. 598 says only "Where a new building is erected, the Deputy City Manager shall assign to the building a municipal address conforming to the municipal addresses of the other properties on the street" and names the "One Address Repository" as "the official record of the municipal addresses of properties within the City" <https://www.toronto.ca/legdocs/municode/1184_598.pdf>; the Municipal Numbering page says only "If the property is proposing a new laneway or garden suite … An active application requesting a building permit or a building permit with the ground floor plan showing the entrance of the new building is required." <https://www.toronto.ca/city-government/planning-development/municipal-numbering-of-a-property/>. Neither mentions letter suffixes.

**Confidence: confirmed** (CoA + three permits, builder, dates); suffix convention **nothing found**.

---

## 21. 29 Blackthorn Ave — retired 15 Aug — nothing found

**Searched:** `"29 Blackthorn Avenue" Toronto`; `"29 Blackthorn Ave" Toronto`. CKAN dev apps, active permits, cleared permits, all 18 CoA resources for 29, plus 25/27/31/33 Blackthorn.

**Nothing found.** 0 records at 29 in every City dataset (neighbours: only a 2000 "Not Accepted" basement permit and a 2002 porch permit at 33, "SFD - Semi-Detached"). Web: only 291 Blackthorn and street-level pages.

Store facts only: 29 was class **"Land Entrance"** (point 30018972, 43.67536, -79.45863, Ward Davenport), sitting between 27 (43.67524, -79.45869) and 31 (43.67545, -79.45828), both class "Land" and still active. Same day, 35 Blackthorn's point moved ~10 m west. **INFERENCE (weak):** a redundant entrance point removed during local clean-up. Don't gloss "Land Entrance" — no source defines it.

**Confidence: nothing found** (strong negative across four City datasets).

---

## 22. 2157 Lake Shore Blvd W, 59/60 Annie Craig Dr, 122 Marine Parade Dr (17 Aug) — the Ocean Club block; a hotel approved, not started

**Searched:** `"2157 Lake Shore Boulevard West" Toronto`; `"Annie Craig Drive" development Humber Bay Shores 2026`; `"2157 Lake Shore" hotel Ontario Land Tribunal settlement`; `"2157 Lake Shore Boulevard West" settlement report December 2023`. CKAN all datasets for 2157 Lake Shore, 120/122/124 Marine Parade, 59/60 Annie Craig. Fetched the 2023 staff report, OLT decision, torontonewswire, UrbanToronto forum p.2.

**FACT (CKAN, verbatim):**
- 08 223121 WET 06 OZ, submitted 2008-11-19 (also filed against **59 and 60 Annie Craig**): "Official Plan Amendment and Zoning By-law Amendment Application to propose a mixed use development".
- 11 276514 WET 06 SA, 2011-09-16: "three buildings, two residential and one commerial. The proposed 10 storey and 39-storey building will have a combined total of 516 dwelling units."
- 11 295644 BLD, issued 2014-11-13: "To construct new 10 storey residential building and 39 storey mixed use building … 516 units (Building A and Building B)". These are built (Ocean Club, per listings).
- **20 126617 WET 03 OZ**, DATE_SUBMITTED **2020-03-16**, STATUS **"Council Approved"**: "Official Plan and Zoning By-law Amendment application to permit a 13-storey (43.4 metres, excluding Mechanical Penthouse) hotel building . The proposal as revised would include 167 hotel suites and one level of underground parking … as well as a restaurant on the ground floor (157 square metres)."
- **No building permit for the hotel exists** — active permits at 2157 Lake Shore stop at 2014.
- **26 157353 WET 03 SA**, submitted **2026-05-08**, Closed: "Administrative Site Plan Control Application Amendment to 11 276514 WET 06 SA59 -60 Annie Craig Drive." Reproducible: `…datastore_search?resource_id=8907d8ed-c515-4ce9-b674-9f8c6eefcf0d&filters=%7B%22STREET_NAME%22%3A%22ANNIE%20CRAIG%22%2C%22STREET_NUM%22%3A%2259%22%7D`
- 59 Annie Craig is a restaurant address (Scaddabush sign permit 19 104347 DST; 2024 "TIS Dining" alterations completed 2025-09-22) with a 2026 permit 26 155252 BLD issued 2026-06-24 "reconfigure and combine the second floor men's and women's change rooms".

**FACT (verbatim, staff report 4 Jan 2023):** "On February 8, 2020, an Official Plan and Zoning By-law Amendments application was submitted to permit the development of a 13-storey hotel building with 154 suites and a ground floor restaurant at 2157 Lake Shore Boulevard West." … "On August 19, 2022, the applicant appealed … to the Ontario Land Tribunal (OLT) due to Council not making a decision". Site history: the 2010 by-laws permitted a "Five-storey office/commercial building, on the parcel of land fronting Lake Shore Boulevard West" — the hotel parcel. Parking for the hotel is partly "provided on the adjacent site (60 Annie Craig Drive)". <https://www.toronto.ca/legdocs/mmis/2023/ey/bgrd/backgroundfile-230806.pdf> (Submission-date discrepancy, CKAN 2020-03-16 vs report 2020-02-08 — report both.)

**FACT (verbatim, OLT decision, primary source):** OLT-22-004312, "2599302 Ontario Ltd. v. Toronto (City)", issue date **1 February 2024**: "to facilitate the development of a 13-storey hotel building consisting of 154 guest suites"; "THE TRIBUNAL ORDERS THAT: 1. The appeals are allowed, in part, and the draft Official Plan Amendment and draft Zoning By-Law Amendment … are hereby approved in principle." <https://www.omb.gov.on.ca/e-decisions/OLT-22-004312-FEB-01-2024.PDF>. Suite counts vary by source (154 / 156 / 165 / 167).

Press (per WebFetch summary, 11 Dec 2023): Stay Inn Hospitality; site "Previously occupied by the Silver Moon Motel, demolished in 2008". <https://torontonewswire.com/stay-inn-hospitality-moving-closer-to-building-a13-storey-hotel-at-humber-bay-shores/>. UrbanToronto: developer Stay Inn Hospitality, architect Arcadis, 13 s, status "Pre-Construction". <https://urbantoronto.ca/database/projects/2157-lake-shore-boulevard-west.42196>

**122 Marine Parade Dr:** nothing found anywhere (0 CKAN records; store has no other 120s on Marine Parade — jumps 76 → 122).

**INFERENCE (moderate):** the 17 Aug regularisation of 2157 Lake Shore / 59 / 60 Annie Craig / 122 Marine Parade is the Ocean Club block's addressing being tidied, most plausibly downstream of the 2026-05-08 administrative site-plan amendment (three months prior); it is **not** the hotel starting — no permit exists. **Do not** say the hotel is under construction.

**Confidence:** hotel history **confirmed** (primary sources); the Annie Craig SPA link **likely**.

---

## 23. Place names

### 1091 Eastern Ave — "Ashbridge's Bay Sports Hub, Toronto Water Pumping Station" (19 Aug) — council 30 July 2026; 20 days

**Searched:** `"Ashbridge's Bay Sports Hub" Toronto`; `"1091 Eastern Avenue" Toronto pumping station`; `"Main Sewage Treatment Playground" renamed council "MM" motion Fletcher July 30 2026`; `"MM43.84" toronto.ca legdocs` (no legdocs PDF surfaced). Fetched Beach Metro, CP24, blogTO, City news release, Fletcher's end-of-term page, ACO Toronto, the 2008 heritage-listing PDF.

**The renaming — FACT**
- Council adopted the rename on **30 July 2026**, the last council meeting of the term. blogTO: adopted "July 30, 2026", "Councillor Paula Fletcher, seconded by Mayor Olivia Chow". <https://www.blogto.com/city/2026/08/sewage-playground-toronto/>
- Item number **2026.MM43.84**; "a baseball diamond, rugby field, two basketball courts" and "11 dedicated pickleball courts". CP24, published 4 Aug 2026. <https://www.cp24.com/local/toronto/2026/08/04/toronto-renaming-main-sewage-treatment-playground/> (CP24's "corner of Emdaabiimok Avenue and Lake Shore Boulevard" is not used; the City's own release says Eastern and Coxwell.)
- Why, in the motion's words as quoted by Beach Metro (6 Aug 2026): "This well-used park is located on land owned by Toronto Water and serves as an important community space… The new name should be reflective of the area and the great wide-range facilities available." Also: the park is "home to a Toronto Water Pumping Station." <https://beachmetro.com/2026/08/06/city-flushes-name-of-main-sewage-treatment-playground-park-now-to-be-called-ashbridges-bay-sports-hub/>
- Fletcher's own page (31 July 2026): "We also renamed it as the Ashbridge's Bay Sports Hub so that it better reflects the amenities for players across the city." <https://www.councillorpaulafletcher.ca/end_of_council_term_update_july_2026>
- **SNIPPET (403'd TMMIS page — do not print the wording):** the operative text directs the General Manager, Toronto Water, to update the "wayfinding name". <https://secure.toronto.ca/council/agenda-item.do?item=2026.MM43.84>

**The trigger — FACT.** City news release, **10 July 2026**: 11 dedicated pickleball courts opened at "Main Sewage Treatment Playground, Eastern Avenue and Coxwell Avenue", "$1.05 million investment through the Mayor's Back on Track program". <https://www.toronto.ca/news/city-of-toronto-opens-one-of-its-largest-dedicated-pickleball-facilities/>

**The pumping station — FACT (primary: 2008 heritage listing).** "Located in Pump House Park near the southwest corner of Eastern Avenue and Coxwell Avenue, the pumping stations at the Ashbridge's Bay Treatment Plant that were designed in 1911 and 1971 have cultural heritage value." The 1911 one is "Building M"; "the Mid-Toronto Interceptor Pumping Station (now called Building T) was constructed according to 1971 plans prepared by Gore and Storrie Limited". *Reasons for Listing: 1091 Eastern Avenue*, 2008. <https://www.toronto.ca/legdocs/mmis/2008/pb/bgrd/backgroundfile-14751.pdf>. ACO Toronto gives the newer building as 1975 and "slated for replacement". <https://www.acotoronto.ca/building.php?ID=2855>. So 1091 Eastern Ave is the plant's *pumping stations* in Pump House Park — distinct from the treatment plant proper at 9 Leslie St.

**Lag:** council 30 July → file 19 Aug = **20 days**. The "Pumping Station" half of the label was already there from 11 May, before the motion existed. The shortest lag this series has recorded (July's Sheppard Ave W demolitions were ~1 month).

**Confidence: confirmed** (date, item, mover, facilities, pumping-station identity). Operative wording: snippet only.

### 4995 Keele St — "Keele Reservoir & Toronto Azzurri Youth Sport Village" (18 Aug) — the label is the City parks page's title

**Searched:** `"Toronto Azzurri Youth Sports Village" Keele reservoir opening`; `"Toronto Azzurri" "Keele" reservoir council lease agreement legdocs`; `"Toronto Azzurri" "4995 Keele" lease 2035 OR 2036 "MM23.20"`; two opening-year searches.

- FACT — the file's new label is verbatim the title of the City's Parks facility page (JS shell; title/URL only). <https://www.toronto.ca/explore-enjoy/parks-recreation/places-spaces/parks-and-recreation-facilities/location/?id=1685&title=Keele-Reservoir-&-Toronto-Azzurri-Youth-Sport-Village=>
- FACT — the club's page: "The Toronto Azzurri Soccer club in partnership with the City of Toronto has developed and is operating a community based soccer/sports complex on the Keele/Steeles Reservoir lands… After 12 years of hard work, fundraising and sponsorship contributions, the Toronto Azzurri are proud to announce the realization of the 5000 square foot LiUNA feildhouse [sic]." No date. <https://www.torontoazzurri.com/page/show/6844378-liuna-clubhouse>
- FACT — address as the club gives it: "Toronto Azzurri Youth Sport Village 4995 Keele Street Carmen Principato Way Toronto Ontario M3J 3B2". <https://dukeheights.ca/featured-member-toronto-azzurri-soccer-club/>
- **SNIPPET (403'd TMMIS page — do not print any lease date):** 2024.MM23.20 — a lease renewal at 4995 Keele St, original lease "dated January 1, 2006". <https://secure.toronto.ca/council/agenda-item.do?item=2024.MM23.20>. A club announcement's "December 26, 2036" end date conflicts with the item's 2035 — unresolved.
- **Nothing found:** an opening date or year for the village or clubhouse; any 2026 event.

**Confidence: likely** on what it is and the City partnership; lease dates **unverified** (snippets only).

### 912 Eglinton Ave W — "Carpark 131" (3 Aug); 803 Richmond St W — "Carpark 53" (17 Aug); 12 Willingdon Blvd — "TPA Carpark 503"

- FACT — Municipal Code ch. 950, Schedule XXXIV: "131 Hilltop 912 Eglinton Avenue West"; "53 Walnut 803 Richmond Street West"; "503 Willingdon 12 Willingdon Boulevard". <https://www.toronto.ca/legdocs/municode/toronto-code-950-34.pdf>
- FACT — TPA *Appendix A: Off-Street Parking Facilities Owned/Managed by Toronto Parking Authority* (2024): "131 912 Eglinton Ave W Surface Owned 26 … Serves businesses within Upper Village BIA along Eglinton Ave W."; "53 803 Richmond St W Surface Owned 48 … Serves Queen West retail/commercial. Site is encumbered by significant Toronto Water infrastructure. Designated by TPA Board for Residential Overnight Parking."; "503 12 Willingdon Blvd Surface Owned 64 … Serves Royal York Station/ Businesses along Bloor St W in The Kingsway BIA." <https://www.toronto.ca/legdocs/mmis/2024/pa/bgrd/backgroundfile-244114.pdf>
- Green P pages exist (JS shells; URL only): <https://parking.greenp.com/carpark/131_912-eglinton-avenue-west/> · <https://parking.greenp.com/carpark/53_803-richmond-street-west/> · <https://parking.greenp.com/carpark/503_12-willingdon-blvd/>
- **Nothing found:** any closure, opening or redevelopment of 131 or 53 (a search snippet claiming 131 is "owned by TTC with development potential flagged by CreateTO" is contradicted by the TPA's own table — discard). The 2019 CBC "People or parking?" story is about a different lot at Caledonia and Eglinton. Nothing found on any 2026 construction at 503 beyond a Green P URL slug reading "partial-construction-reduced-spaces".
- **12 Willingdon Blvd is at Royal York station, in The Kingsway** — about 3.6 km from the 2157 Lake Shore Blvd W points the offline draft grouped it with. The only thing tying it to them is the same-day reserved→regular swap (old point 20102975 retired, 30139050 regularised, label carried across).

**Confidence: confirmed** exists, all three; no event to lag against.

### 1043 Coxwell Ave — "Royal Bank Canada" dropped (18 Aug) — silent

**Searched:** `RBC branch "1043 Coxwell" Toronto`; `RBC branch closing Coxwell O'Connor Toronto 2026`; `"1043 Coxwell Avenue" Toronto`; RBC locator; `RBC "Coxwell" branch closing OR closed OR consolidat … 2025 OR 2026`. Grepped the 6ixretail March 2026 closures piece (no Coxwell mention).

- FACT — directory listings still show an RBC branch at 1043 Coxwell Ave, M4C 3G4 (Coxwell & O'Connor). <https://www.yellowpages.ca/bus/Ontario/Toronto/RBC-Royal-Bank/7092861.html> — a listing, not proof of current operation.
- FACT — 2026 Toronto bank-closure coverage names downtown Yonge St closures only. <https://6ixretail.com/2026/03/changing-role-bank-branch-toronto-closures/>
- **Nothing found:** any closure, relocation or consolidation notice. The public record is silent on why the label went.

### 15 Leaside Park Dr — "Thorncliffe Tennis Club" (case restyle); 5 Leaside Park Dr — "Leaside Park, Leaside Park Outdoor Pool"

- FACT — Tennis Ontario lists "Thorncliffe Park Tennis Club", 15 Leaside Park Drive, six lit hard courts in Leaside Park. <https://www.tennisontario.com/clubs/get-on-the-court/find-a-club/thorncliffe-park-tennis-club>. The club calls itself Thorncliffe **Park** Tennis Club; the file's restyle fixed the case, not the name.

### 5 Merrill Ave — "Merrill Park"

- FACT — City Parks facility page "Merrill Park", id=2478 (JS shell; title/URL only). <https://www.toronto.ca/explore-enjoy/parks-recreation/places-spaces/parks-and-recreation-facilities/location/?id=2478&title=Merrill-Park>. 2024 parks classification attachment: "Merrill Park Parkette Etobicoke York 5". <https://www.toronto.ca/legdocs/mmis/2024/cc/bgrd/backgroundfile-250425.pdf>
- Store: the label "Merrill Park" has been on 5 Merrill Ave continuously since 2025-04-01; the 15 Aug event is a twin-point swap, not a naming. Not the east-end Merrill Bridge Road Park.

---

## 24. What do MAINT_STAGE = RESERVED / REGULAR mean? — no published definition

**Searched:** CKAN `package_show` for the dataset (notes, limitations, every resource description); the readme resource; datastore field `info.notes`; the open.toronto.ca page; ArcGIS Address Point layer metadata; U of T and York library catalogue pages; City "Municipal Numbering of a Property" page; `"MAINT_STAGE"` web searches (three variants).

**Nothing found. No published definition exists.**
- Package notes describe attributes only generically: "Each address point is described with a series of attributes including street number, street name, address type, feature class and real world coordinates." Every resource `description` is null; every datastore field's `info.notes` is empty. <https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show?id=address-points-municipal-toronto-one-address-repository>
- The only readme, `readme-address-feature-codes.txt`, is a list of GENERAL_USE codes — and the `limitations` note says those codes were nullified 29 July 2021. <https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/abedd8bc-e3dd-4d45-8e69-79165a76e4fa/resource/921563fc-aeab-4e1f-82bd-c7bdae6dc26a/download/readme-address-feature-codes.txt>
- ArcGIS layer "Address Point" (description: "Point representation of authorized addresses within the City of Toronto"): `MAINT_STAGE` string(10), `domain: null`. <https://gis.toronto.ca/arcgis/rest/services/cot_geospatial27/MapServer/101?f=pjson>
- City page: "The City of Toronto's Land and Property Surveys team is responsible for assigning and maintaining street names and property addresses across the city" — no status vocabulary. <https://www.toronto.ca/services-payments/building-construction/city-owned-land-and-property-surveys/municipal-numbering-of-a-property/>

**FACT (empirical, live layer, 2026-09-08):** exactly two values exist — `REGULAR` 517,771 points, `RESERVED` 7,711; `ADDRESS_STATUS` is null everywhere. The offline draft's gloss ("a number that has been assigned but is not yet in service") is a reading of the word, not a City definition; the researched article says so.

---

## Cross-cutting observations for the writer

1. **The lag is the story again, and this month it runs to sixteen years.** Yonge/Glebe: community council recommended the rezoning on 17 Aug 2010; the shops' addresses came off on 15 Aug 2026. Hullmark Centre: "recently completed" in a March 2016 City report; regularised 15 Aug 2026. Alter: permit completed 19 Dec 2019; regularised 15 Aug 2026. Adelaide 779/781: severed 2015, nothing built, lots for sale in September 2026. Dundas W 4003/4005: demolished by 26 Jan 2024; retired 7 Aug 2026.
2. **The shortest lag this series has seen: 20 days.** Ashbridge's Bay Sports Hub — council 30 July, file 19 Aug. And one item where the file moved *first*: 12/16 Wellesley St W reserved 6 Aug, consent finalised 24 Aug.
3. **Addresses ahead of buildings:** Edward St (shoring permit 4 Aug, one day after), 985 Woodbine (permits applied 26–27 Aug, 11 days after), 273 Merton (demolition closed March, above-grade from October), Markland (severed Dec 2025, no permits yet).
4. **A City record named the number before the file did.** Permit 23 182180 BLD, filed under 60 Roselawn Ave in 2023: "Pending address is 530 Duplex Ave." First time in this series.
5. **Do not print:** the 2014 Solidarity Way naming date; MM43.84's operative wording; any Azzurri lease date; "Humber Bay Shores"; CP24's Emdaabiimok/Lake Shore location; Hazelview's storey range; Precondo's 2015 as a City fact; that 3986 Eglinton Ave W is an EEB; that 779/781 Adelaide were built; that the 2157 Lake Shore hotel has started; "Niagara neighbourhood" without attributing the MLS listing; "north side of Edward".
6. **Usable sourced neighbourhood names:** Davisville (Jan 2025 Merton report), Markland Wood (Dec 2024 report), King Liberty Village (2010 report), Rosedale (Globe headline), The Kingsway (TPA table). Everything else: ward names.

## Explicitly not researched

The 421–429A Yonge St re-versioning of 10 Aug (sub-10 m jitter plus an ignored field), the sub-50 m coordinate churn on Sonnet Crt, Sonic Way, O'Connor Dr and Walnut Ave, and the 372 Military Trl / 155 Transit Rd / 428 O'Connor Dr moves — location noise or gross-only, none of it in the net figures.
