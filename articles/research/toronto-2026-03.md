# Toronto address changes, March 2026 — external research notes

Retrieval and citation only. Facts are separated from inference. Every fact carries a URL.
Compiled 2026-08-28. City open-data extracts pulled the same day (datasets last refreshed
2026-08-27).

## Sources used throughout

City of Toronto open data, downloaded and grepped locally:

- Development Applications — https://open.toronto.ca/dataset/development-applications/ (26,432 rows)
- Committee of Adjustment Applications (Active + Closed since 2017) — https://open.toronto.ca/dataset/committee-of-adjustment-applications/ (36,540 rows)
- Building Permits – Active Permits — https://open.toronto.ca/dataset/building-permits-active-permits/
- Building Permits – Cleared Permits since 2017 — https://open.toronto.ca/dataset/building-permits-cleared-permits/
- Toronto Centreline (TCL) — https://open.toronto.ca/dataset/toronto-centreline-tcl/
- Address Points (Municipal) – Toronto One Address Repository — https://open.toronto.ca/dataset/address-points-municipal-toronto-one-address-repository/ (the tracker's own source)

The Committee of Adjustment CSV carries no per-application URL; CofA file numbers below
(e.g. `B0033/24SC`) are cited against that dataset landing page. Development applications
carry an Application Information Centre (AIC) link, quoted verbatim.

Note on coordinates: the Development Applications CSV `X`/`Y` are MTM zone 10 on a NAD27
datum (EPSG:2019). Reprojecting with the NAD83 equivalent puts every Toronto point ~220 m
too far south — worth knowing if anyone re-checks the geography.

---

## 1. 1226–1250 Queen St E (eleven addresses retired 6 March 2026)

**What I searched**

- Development Applications, all Queen St E numbers 1200–1270 (both parities).
- Committee of Adjustment, Queen St E 1200–1270 E.
- Building Permits (active + cleared since 2017), Queen St E 1220–1260 E, checking the
  `DEMOLITION` column.
- Web: "1226 Queen Street East Toronto development application Leslieville"; "Queen St E
  Leslieville Greenwood Coxwell demolition development 2026"; `"1226" OR "1250" "Queen
  Street East" Toronto Leslieville demolition fire 2026`; `"1244 Queen St E" OR "1246
  Queen St E" OR "1248 Queen St E" Toronto`; blogTO/UrbanToronto queries for a demolished
  Queen East strip between Greenwood and Coxwell.

**Nothing found — the even side**

There is **no development application, no Committee of Adjustment application and no
building or demolition permit** filed against 1226, 1228, 1230, 1232, 1234, 1236, 1240,
1244, 1246, 1248 or 1250 Queen St E in any of the four City datasets above. No news
coverage of a fire, demolition or assembly on that stretch was found in four web searches.
The only demolition permit anywhere on this block is on the **odd** side: `16 176237 DEM`,
"demolish existing 1 storey automotive repair shop" at 1249 Queen St E, applied 2016-06-17,
issued 2016-07-20 (Building Permits – Cleared).

**Facts found about the site itself**

- 1238 Queen St E — still on file, and the only address on that frontage carrying a place
  name (`PLACE_NAME = Avondale Retirement Residence`) — is **Chartwell Avondale Retirement
  Residence**, a 79-suite retirement residence that has operated in Leslieville for over
  20 years. Chartwell's own page describes it as "nestled above a retail complex" with a
  dental clinic, banks and a bakery. https://chartwell.com/on/toronto/avondale
- Retail space in that complex is marketed by **unit letter under the single number 1238**,
  not by separate street numbers — e.g. "Unit F-1238 Queen St E" listed for lease.
  https://www.zolo.ca/toronto-real-estate/1238-queen-street-east/unit-f
- Two sign permits confirm ground-floor commercial tenants under 1238: `20 202973 DST`
  (CHARTWELL, applied 2020-10-06, cancelled) and `22 239474 DST` (H&R BLOCK, applied
  2022-12-14, issued 2022-12-21) — Building Permits – Cleared.
- Building permit **`26 109780 BLD`, "Proposal for interior building renovations –
  retirement home", 1238 Queen St E, applied 2026-01-27, issued 2026-05-22**, with matching
  plumbing, HVAC (`26 109780 PLB` / `HVA`) and sprinkler (`26 140205 FSU`, applied
  2026-04-08) permits. https://open.toronto.ca/dataset/building-permits-active-permits/
  *Date gap: applied ~5 weeks before the 6 March retirement; issued ~2.5 months after it.*
- In the City's Address Points source data the ten points 1228–1250 carry consecutive
  `ADDRESS_POINT_ID` values 14205472–14205481 (descending with increasing street number);
  1226 is the odd one out at 8408355. Consecutive IDs indicate the ten were created as one
  batch. https://open.toronto.ca/dataset/address-points-municipal-toronto-one-address-repository/
- The retirement removed an interleaved run, not a contiguous parcel: 1238 and 1242 Queen
  St E stayed on file between the retired numbers, as did 1220, 1256, 1256A and 1260.

**Inference (not fact)** — the eleven look like legacy per-storefront points along the
Avondale complex frontage that the City consolidated under 1238 (and 1242), rather than a
demolition. The supporting evidence is the unit-lettered leasing convention, the batch-
created IDs, the survival of 1238/1242, and the total absence of any demolition record. No
document says this.

**The adjacent project is on the other side of the street — do not conflate.** 1233–1251
Queen St E (odd side, ~40 m south) is a live redevelopment:

- ZBA `22 123730 STE 14 OZ`, filed 2022-03-17, 9-storey mixed-use, 142 units —
  http://app.toronto.ca/AIC/index.do?folderRsn=wdqsT0eH14vayzZ%2BPrZnRg%3D%3D
- Site Plan `22 123729 STE 14 SA`, filed 2022-03-17, NOAC Issued —
  http://app.toronto.ca/AIC/index.do?folderRsn=nAz%2BaUnaluNUoOpG2I0PTQ%3D%3D
- Holding-symbol removal `24 124851 STE 14 OZ`, filed 2024-03-12 (By-law 1292-2023) —
  http://app.toronto.ca/AIC/index.do?folderRsn=zC7IlS18YXZ0QX%2B8DPB36Q%3D%3D
- Earlier ZBA/SPA at 1249–1251 Queen St E, `17 247432 STE 32 OZ`, filed 2017-10-13,
  6-storey mid-rise — http://app.toronto.ca/AIC/index.do?folderRsn=tovop4whVFpZVIiyhDesRQ%3D%3D
- Building permit `24 194251 BLD`, "Proposal for a nine-storey mixed-use building. A total
  of 149 dwelling units are proposed.", 1233 Queen St E, applied 2024-08-07; conditional
  foundation permit issued 2026-01-29; conditional structural permit issued 2026-08-19.
- Project identity: 1233 Queen East, Core Development / Woodbourne, Studio JCI, 9 storeys,
  co-living rental. https://urbantoronto.ca/forum/threads/toronto-1233-queen-east-35-7m-9s-core-development-studio-jci.33338/
  and https://www.parvisinvest.com/investments/properties/1233-queen-street-east
- Heritage: City notice of intention to designate 1233–1235 Queen St E (2022) —
  https://www.toronto.ca/legdocs/mmis/2022/pb/bgrd/backgroundfile-229442.pdf

*Confidence: **nothing found** for a real-world cause of the eleven retirements; the site
identification (Chartwell Avondale at 1238) is **confirmed**; the consolidation explanation
is **inference only**.*

---

## 2. YZD Lane / 81 YZD Lane (new street, first seen 2026-03-03)

**What I searched** — Development Applications (`YZD` and `DOWNSVIEW` street names);
Toronto Centreline; web: `"YZD Lane" Toronto Downsview street name`; `Rogers Stadium "81
YZD Lane" Toronto address`; `"YZD Lane" street naming Toronto council report toronto.ca`.

**Facts**

- **YZD Lane is a real entry in the City's own street network**, not a placeholder. Toronto
  Centreline record: `LINEAR_NAME_FULL = "YZD Lane"`, `LINEAR_NAME_ID = 30296`,
  `CENTRELINE_ID = 60052961`, `FEATURE_CODE_DESC = "Other"`, **`JURISDICTION = PRIVATE`**,
  address range `81–81` on the odd side only, `ADDRESS_L = None`.
  https://open.toronto.ca/dataset/toronto-centreline-tcl/
  (Retrieved via the CKAN datastore search on resource `ad296ebf-fca6-4e67-b3ce-48040a20e6cd`;
  exactly one matching record city-wide.)
- **81 YZD Lane is Rogers Stadium**, the 50,000-capacity temporary concert venue on the
  former Downsview Airport lands. Live Nation's venue page gives the address as
  "81 YZD Lane (former Downsview Airport lands). Toronto, ON M3K0A1".
  https://www.livenation.com/venue/KovZ917ARzt/rogers-stadium-events
  Ticketmaster venue listing: https://www.ticketmaster.ca/rogers-stadium-tickets-toronto/venue/132627
- **Address discrepancy, recorded not adjudicated:** Wikipedia gives Rogers Stadium's
  address as "105 Carl Hall Road", operator Live Nation, opened **29 June 2025**, capacity
  50,000, intended lifetime five years with demolition expected around 2030.
  https://en.wikipedia.org/wiki/Rogers_Stadium
  *Date gap: the stadium opened ~8 months before 81 YZD Lane entered the address file
  (absent from the 2026-02-27 snapshot, present 2026-03-03).*
- **YZD is the developer's brand for the whole district.** Northcrest Developments unveiled
  "YZD" as the identity of the 370-acre former Downsview Airport redevelopment on
  2024-08-17; the name is a nod to the airport's aviation code. Master plan by KPMB and
  Henning Larsen, landscape by Michael Van Valkenburgh Associates and SLA, planning by
  Urban Strategies; PSP Investments is a partner; the Hangar District is the first phase.
  https://urbantoronto.ca/database/projects/yzd.51564 ,
  https://www.yzd.ca/ , https://www.northcrestdev.ca/
- The address point in the file is classed `Land Entrance` and `REGULAR` (not `RESERVED`).

**Nothing found** — no City Council or community council street-naming report for "YZD
Lane" surfaced in two searches, including a `site:toronto.ca` style query against the
street-naming pages. The City's street-naming policy page is
https://www.toronto.ca/city-government/planning-development/street-naming/ ; nothing on it
names YZD Lane. Consistent with `JURISDICTION = PRIVATE`, a private road name may not
require a council naming by-law — but that is **inference**, not something a document says.
No development application in the City dataset uses "YZD" as a street name.

*Confidence: **confirmed** that YZD Lane is in the City centreline as a private street
carrying only No. 81, and that 81 YZD Lane is used as Rogers Stadium's address. **Nothing
found** on a council naming record.*

---

## 3. Diamond Jubilee Promenade / 476 Front St E (added 25 March 2026)

**What I searched** — Toronto Centreline (`Diamond Jubilee`); Parks and Recreation
Facilities datastore (`Diamond Jubilee`); Development Applications and CofA, Front St E
440–520; Building Permits, Front St E 460–490; web: `"Diamond Jubilee Promenade" Toronto`;
`"Diamond Jubilee Promenade" Waterfront Toronto West Don Lands naming park`; `"Diamond
Jubilee Promenade" site:toronto.ca`.

**Facts**

- **Diamond Jubilee Promenade is a City of Toronto park.** It appears in a 2024 City
  Council attachment listing every park by name, ward, operational district and
  classification, as: `DIAMOND JUBILEE PROMENADE | 13 | Toronto East York | Neighbourhood`
  (page 8 of the PDF; verified by extracting the text myself).
  https://www.toronto.ca/legdocs/mmis/2024/cc/bgrd/backgroundfile-250430.pdf
  A web search associated this file with the 2024 council item on the audit of Parks Branch
  operations (2024.AU6.1, "Citywide Parks List and Classification"); `secure.toronto.ca`
  returns HTTP 403 to automated fetches, so the parent item is **unconfirmed**.
- It has its own City parks facility page (location id 3584), which lists a splash pad and
  a drinking fountain (from `https://www.toronto.ca/data/parks/live/facilities/3584.json`).
  Page: https://www.toronto.ca/explore-enjoy/parks-recreation/places-spaces/parks-and-recreation-facilities/location/?id=3584
  The page is JavaScript-rendered and did not fetch as text.
- Location: on Front Street East between Cherry Street and Bayview Avenue, two minutes'
  walk from the 504 King stop at Cherry St / Front St E.
  https://www.walkscore.com/score/diamond-jubilee-promenade-toronto-on-canada
- The surrounding public realm is **Waterfront Toronto's Front Street Promenade** in the
  West Don Lands: "Front Street is the main pedestrian thoroughfare in the new West Don
  Lands. Designed by … PFS Studio, this new section of Front Street is defined by a linear
  park, or promenade, located on the north side of the street."
  https://www.waterfrontoronto.ca/our-projects/front-street-promenade
  The tracked point 476 Front St E sits on the north side of Front St E (43.65345,
  -79.35514), between 474 and 482.
- The adjoining lands are the Canary District / West Don Lands Pan Am blocks addressed
  475 Front St E; e.g. Committee of Adjustment minor variance **`A0300/18TEY`**
  (SYS_ID 4340491), "To modify the redevelopment plan for Phase 2 of the West Don Lands
  approved by Site-specific By-law 4-2011 …", filed 2018-03-20, approved 2018-08-29
  (https://open.toronto.ca/dataset/committee-of-adjustment-applications/), and building
  permits at 475 Front St E repeatedly labelled "Canary district block 12" /
  "PAN-AM. BLOCKS 1 & 14".

**Nothing found**

- Diamond Jubilee Promenade is **not** in the Toronto Centreline (0 matches) — it is not a
  street, which is consistent with the file attaching it as a `PLACE_NAME` on a Front St E
  address rather than creating a new street.
- It is **not** in the Parks and Recreation Facilities open dataset (0 matches).
- No development application, CofA application or building permit is filed against
  476 Front St E specifically.
- No council report naming the promenade was found in two searches. (Toronto's Platinum
  Jubilee page notes the City marked the Diamond Jubilee in 2012 —
  https://www.toronto.ca/news/platinum-jubilee-of-her-majesty-the-queen-2022/ — but does
  not mention this promenade, so it is **not** evidence of when or why it was named.)

*Confidence: **confirmed** that it is a City park (Ward 13, Toronto East York,
"Neighbourhood" classification) on the Front Street promenade in the West Don Lands;
**nothing found** on a naming decision or a dedication date.*

---

## 4a. 2424–2440 Dundas St W (four added, 2440 retired) — one development, confirmed

**Facts**

- **Zoning By-law Amendment `23 124848 STE 04 OZ`, filed 2023-03-20**, 2400 and 2440 Dundas
  St W: "Zoning By-law Amendment for three towers. The proposal will have 6372.4 square
  metres of non-residential floor area and a total of 1,214 dwelling units. A 1,043 square
  metre public park is proposed along Dundas Street West and a new private road will provide
  vehicular and pedestrian access to the existing GO/UP Station pick-up/drop-off loop to the
  south." Status: Closed.
  http://app.toronto.ca/AIC/index.do?folderRsn=q3NTqW7XR%2FvcAKSvQtPMbA%3D%3D
- **Site Plan `25 184214 STE 04 SA`, filed 2025-06-26**, Phase 1 of 2400–2440 Dundas St W:
  37-storey tower on a 3-storey podium (Tower A), 447 purpose-built rental units, 11
  affordable secured in kind under s.37(6); "The existing grocery store will be re-located
  to the second floor of this building". Status: Under Review.
  http://app.toronto.ca/AIC/index.do?folderRsn=EaVRaQdkWKpBjN4XKExbHg%3D%3D
- **Site Plan `25 184923 STE 04 SA`, filed 2025-06-27**, Phase 2: two towers at 25 and 42
  storeys on a 2-storey shared podium, 56 affordable rental units, a new public park, a
  POPS, and a surface easement to the relocated Metrolinx pick-up/drop-off at 2376 Dundas
  St W. Status: Under Review.
  http://app.toronto.ca/AIC/index.do?folderRsn=tzpa3AbOR4gLYdn4w3ca0A%3D%3D
- **Consent `B0042/24TEY`** (SYS_ID 5469281), 2440 Dundas St W, filed 2024-07-05, heard
  2024-11-20, **Approved**: "To obtain consent to sever the lot into two lots for a
  mixed-use phased development and to maintain an existing easement/right-of-way."
  https://open.toronto.ca/dataset/committee-of-adjustment-applications/
- **Minor variance `A0225/26TEY`** (SYS_ID 5802956), 2440 Dundas St W, **filed 2026-03-26**,
  heard 2026-05-27, Approved: alters development standards for the 37-storey Phase 1 tower
  approved under site-specific Zoning By-law 1419-2024 — raising Tower A by 1 m and the
  stepped podium by 0.7–2.9 m, and reducing the required share of three-bedroom units.
  *Filed in the same month as the address changes.*
- Demolition permit **`26 153556 DEM`**, 2440 Dundas St W, "Demolition of an existing 2
  storey commercial building", 1,623 m² demolished, **applied 2026-05-01, issued
  2026-07-14** — i.e. ~5 weeks and ~3.5 months *after* the March address changes.
- Site identity: the Dundas–Bloor FreshCo/Shoppers plaza beside Dundas West Station and
  Bloor GO. Developer **Fora Developments** (formerly listed as Collecdev), architect
  Giannone Petricone. https://www.blogto.com/real-estate-toronto/2023/02/2400-dundas-west-toronto/ ,
  https://urbantoronto.ca/forum/threads/2400-dundas-street-w-collecdev-s.32082 ,
  https://2400dundas.com/
  FreshCo's own listing confirms the store's address is 2440 Dundas St W.
  https://www.yellowpages.ca/bus/Ontario/Toronto/FreshCo/100406364.html

**Inference** — that 2440 Dundas St W coming off the file while 2424/2428/2430/2432 went on
reflects the approved severance and phasing of this development. The consent, the by-law,
the phased site plans and the March 2026 variance are all facts; the causal link to the
address change is not stated anywhere.

*Confidence: **confirmed** one development; the address-change linkage is **likely**.*

## 4b. 70–76 Perth Ave (four added) — one development, confirmed

**Facts** — all at 72 Perth Ave, Ward Davenport:

- ZBA `18 170127 STE 18 OZ`, filed 2018-06-01 —
  http://app.toronto.ca/AIC/index.do?folderRsn=37F7XrE1QstTsbxAgvz5qg%3D%3D
- Site Plan `21 226455 STE 09 SA`, filed 2021-10-15, NOAC Issued: "The revised Site Plan
  Control application now proposes an 18-storey residential building with 19,485 square
  metres of total gross floor area and 262 residential units, including 13 affordable
  housing units." — http://app.toronto.ca/AIC/index.do?folderRsn=WBRRSvg2r561doTNFSmoxA%3D%3D
- ZBA `25 108495 STE 09 OZ`, filed 2025-01-24: "Zoning By-law Amendment for a 18-storey
  purpose-built rental apartment building containing 262 residential units." Status: Closed.
  http://app.toronto.ca/AIC/index.do?folderRsn=51StyTatoIBp3aOx0Yr8mw%3D%3D
- Minor variances `A0892/22TEY` (filed 2022-08-08, heard 2022-11-02, Approved — units from
  108 to 128 plus height for a geothermal system, referencing SPA 21 226455) and
  `A0199/24TEY` (filed 2024-02-23, heard 2024-04-24, Approved — height from 11 to 16
  storeys, under site-specific By-law 182-2022).
  https://open.toronto.ca/dataset/committee-of-adjustment-applications/
- Project: **72 Perth**, Castlepoint Numa + Hazelview Investments (50/50), Studio JCI,
  18 storeys, **255 rental homes including 51 affordable** delivered with WoodGreen
  Community Services under the City's Rental Housing Supply Program; geothermal heating and
  cooling. **Ground broken 22 May 2026**, initial occupancy December 2028.
  https://urbantoronto.ca/database/projects/72-perth.45042 ,
  https://urbantoronto.ca/news/2026/05/ground-broken-255-unit-rental-72-perth-junction-triangle.61054 ,
  https://www.toronto.ca/news/city-of-toronto-breaks-ground-on-255-new-rental-homes-in-davenport-including-51-affordable-homes/ ,
  https://www.hazelview.com/private-real-estate-investing/development-management/developments/72-perth-avenue
  *Date gap: the four addresses appear ~11 weeks before the groundbreaking.*
- In the file, 70/74/76 Perth Ave are `RESERVED`, and a second `RESERVED` point for 72 Perth
  Ave appears alongside the existing `REGULAR` one.

**Inference** — the four are the addressing of the 72 Perth building. Not stated in any
document; note that the older townhouse site plan `16 122757 STE 18 SA` (filed 2016-03-02)
covers 12–68 Perth Ave with A/B suffixes and stops short of 70.

*Confidence: **confirmed** one development at 72 Perth; the 70/74/76 linkage is **likely**.*

## 4c. 1452–1458 King St W (four added) — nothing found

**What I searched** — Development Applications (King St W 1400–1500, plus Maynard, Dunn,
Spencer and Jameson Aves); Committee of Adjustment (King St W 1440–1470); Building Permits
active + cleared (King St W 1440–1470); web: UrbanToronto/torontotoday for 1452/1458/1464
King St W.

**Nothing found.** No development application, CofA application or building permit exists
for 1452, 1454, 1456 or 1458 King St W. The four points are `RESERVED` in the file.

**Nearby, but not tied to these numbers (fact + explicit non-link)** — `24 253913 STE 04 OZ`,
filed 2024-12-27, status **Council Approved**, at **1464 King St W and 10–12 Maynard Ave**:
"OPA & Rezoning to permit the development of a 13 storey mixed use building with ground-floor
retail and daycare uses and a proposed temple with religious residences."
http://app.toronto.ca/AIC/index.do?folderRsn=d%2BsHIMhI3SEn0qzeVONBdg%3D%3D
This is the Kagyu Monastery project by the Karma Sonam Dargye Ling congregation in "Little
Tibet"; the existing site holds a detached house, a 19-unit low-rise and the temple.
https://www.torontotoday.ca/local/real-estate-housing/city-approves-13-storey-tower-buddhist-temple-parkdale-12659001 ,
https://urbantoronto.ca/news/2025/03/mid-rise-monastery-rentals-proposed-block-apart-south-parkdale.58216
The UrbanToronto article names the site as "1464 King Street West and 10–12 Maynard Avenue"
and **does not mention 1452–1458**. In the tracked file, 1458 King St W (-79.43791) and
1464 King St W (-79.43797) are about 5 m apart. Any connection between the approved project
and the four new numbers is **inference with no supporting document**; I would not assert it.

*Confidence: **nothing found**.*

---

## 5. Address splits — 6 Shorncliffe Rd, 33 Reidmount Ave, 372 Glen Park Ave

### 6 Shorncliffe Rd (Etobicoke; 6A–6E added, no plain "6" ever on file) — nothing found

**What I searched** — Development Applications (all Shorncliffe); Committee of Adjustment
(Shorncliffe ≤ 20); Building Permits active + cleared (Shorncliffe ≤ 20); web: `"6
Shorncliffe" Toronto Etobicoke townhouses development`.

**Nothing found.** No application or permit of any kind is on record for 6 Shorncliffe Rd.
Web hits for "6 Shorncliffe" all resolve to **6 Shorncliffe *Avenue*, Forest Hill** — a
different street in central Toronto — and were discarded per the city/street check.

**Nearby context only, no claimed link** — the large Shorncliffe master plan is on the
**east** side of the road, anchored at 15/25 Shorncliffe Rd and 5415 Dundas St W:

- ZBA `18 272108 WET 03 OZ`, filed 2018-12-27: "Amend the zoning to permit a mixed used
  project including residential, retail and offices uses comprised of 4 base buildings with
  eight tower components." — http://app.toronto.ca/AIC/index.do?folderRsn=7Aqqq1FSnGQsUtFiKi9a5g%3D%3D
- Draft Plan of Subdivision `19 264584 WET 03 SB`, filed 2019-12-24, **Draft Plan
  Approved**: "A Draft Plan of Subdivision application to create a J-shaped public street
  that connects Dundas Street West to Shorncliffe Road that will service 4 development
  blocks and a public park." — http://app.toronto.ca/AIC/index.do?folderRsn=ZBohaUvVXNx07BCq7W1CCA%3D%3D
- Self-storage / industrial condo redevelopment at 37 Shorncliffe Rd, `23 113750 WET 03 OZ`,
  filed 2023-02-14 — http://app.toronto.ca/AIC/index.do?folderRsn=wCgLfTiYPwcikUfZhVdDnw%3D%3D

The five new points sit at 43.6315–43.6317 / -79.5446 to -79.5447, i.e. **west** of 15
Shorncliffe Rd and just north of 10 Shorncliffe Rd, on a separate lot from the master-plan
site. All five are `RESERVED`.

*Confidence: **nothing found** for 6 Shorncliffe Rd itself.*

### 33 Reidmount Ave (Agincourt; 33A–33D added, 33 retained) — confirmed

**Facts**, all from https://open.toronto.ca/dataset/committee-of-adjustment-applications/ :

- **Consent `B0033/24SC`** (SYS_ID 5488417), 33 Reidmount Ave, filed **2024-08-02**, heard
  **2025-02-12**, **Approved**, `NUMBER_OF_LOTS_CREATED = 2`: "To obtain consent to sever
  the property into two residential lots. Cross-reference Minor Variance Applications
  A0168/24SC and A0169/24SC."
- Minor variances **`A0168/24SC`** (SYS_ID 5487792) and **`A0169/24SC`** (SYS_ID 5487767),
  both filed 2024-08-01, heard 2025-02-12, Approved: "To construct a new two-storey
  detached dwelling. The existing one-storey detached dwelling will be demolished."

*Date gap: the consent was approved 2025-02-12, ~13 months before the March 2026 split
appeared in the address file.*

**Nothing found** — no building permit for 33 Reidmount Ave in either permit dataset, and no
development application (the Development Applications dataset has zero Reidmount rows).

**Inference** — in the file 33A and 33C are classed `Land` while 33B and 33D are classed
`Structure`, which reads as two severed lots each with a front dwelling and a rear
structure. That mapping is my reading of the class codes against the consent wording, not
something the City states.

*Confidence: **confirmed** severance; the A/B/C/D-to-lot mapping is **inference**.*

### 372 Glen Park Ave (North York; 372A–372D added, 372 retained) — confirmed

**Facts**, all from https://open.toronto.ca/dataset/committee-of-adjustment-applications/ :

- **Consent `B0025/25NY`** (SYS_ID 5714984), 372 Glen Park Ave, filed **2025-09-26**, heard
  **2026-01-08**, **Approved**, `NUMBER_OF_LOTS_CREATED = 2`: "To obtain consent to sever
  the property into 2 residential lots with a fourplex and accessory garden suite on each
  lot. File numbers B0025/25NY, A0408/25NY & A0409/25NY will be jointly considered."
- Minor variances **`A0408/25NY`** (SYS_ID 5715139) and **`A0409/25NY`** (SYS_ID 5714996),
  both filed 2025-09-26, heard 2026-01-08, Approved (A0409 shown as "Approved with
  Conditions"): "To construct a new Fourplex dwelling with a Gardenn Suite at the rear of
  the property." Ward 08, North York.

*Date gap: heard and approved 2026-01-08, ~2.5 months before the March 2026 split appeared
in the file.*

**Nothing found** — no development application and no building permit for 372 Glen Park Ave.

**Inference** — 372A and 372C are classed `Land`, 372B and 372D `Structure`, matching two
lots each with a fourplex and a rear garden suite. Again, my reading, not the City's.

*Confidence: **confirmed** severance; the suffix-to-lot mapping is **inference**.*

---

## Cross-cutting negatives worth recording

- No demolition permit anywhere on the even side of Queen St E between 1220 and 1260.
- "Diamond Jubilee Promenade" and "YZD Lane" behave oppositely in the City's own street
  network: YZD Lane is a centreline record (private jurisdiction), the promenade is not in
  the centreline at all.
- Of the six address clusters investigated, four (Dundas, Perth, Reidmount, Glen Park) have
  a matching City planning record; two (1452–1458 King St W, 6 Shorncliffe Rd) have none in
  any of the four City datasets checked.
