# Toronto, April 2026 — public-record research

Retrieval notes for the April 2026 monthly article. Facts and inferences are labelled
separately. Every claim carries a URL. Searches that returned nothing are recorded as
such.

City of Toronto, Ontario confirmed in every source cited below (ward names, former
municipality, planning district or community-council district checked in each case).

Two open-data endpoints did a lot of the work and are worth reusing:

- Development Applications — `https://open.toronto.ca/dataset/development-applications/`
  (CKAN datastore resource `8907d8ed-c515-4ce9-b674-9f8c6eefcf0d`)
- Committee of Adjustment Applications — `https://open.toronto.ca/dataset/committee-of-adjustment-applications/`
  (active `51fd09cd-99d6-430a-9d42-c24a937b0cb0`, closed-since-2017 `9c97254e-5460-4799-896f-c7823413c81c`)
- Building Permits, Active — `https://open.toronto.ca/dataset/building-permits-active-permits/`
  (resource `6d0229af-bc54-46de-9c2b-26759b01dd05`)
- Building Permits, Cleared since 2017 — `https://open.toronto.ca/dataset/building-permits-cleared-permits/`
  (resource `a96c0ba4-3026-402b-b09d-5b1268b8f810`)
- Demolition and Replacement of Rental Housing Units — `https://open.toronto.ca/dataset/demolition-and-replacement-of-rental-housing-units/`
  (resource `3ad8e86d-f166-4279-85e8-69b752248c16`) — this one carries actual
  **rental demolition permit issue dates**, which nothing else does.

The first four were last refreshed 27 August 2026 when queried; the rental-demolition
register 3 August 2026.

Note on `secure.toronto.ca`: council agenda-item pages (`/council/agenda-item.do`,
`/council/report.do`) return HTTP 403 to automated fetches. The URLs are still valid in
a browser and are cited below; where a fact came from them it is because a City PDF or a
search index quoted them, and that is flagged.

---

## 1. Secord Avenue — 10–18 and 40–50 retired 2 April 2026

**What I searched.** `"Secord Avenue" Toronto East York development application`;
`"Secord Ave" Toronto rezoning demolition Main Street Danforth`; `"Secord Avenue"
Toronto "Toronto Community Housing" OR "affordable housing" redevelopment 2026`;
`"Secord Avenue" Toronto urbantoronto development` (domain-limited to urbantoronto.ca);
`"40 Secord" OR "42 Secord" OR "50 Secord" Toronto demolition townhouses`;
`"Bela Square" Toronto Secord Avenue townhouses demolition 2026 construction start`;
Toronto Development Applications open data filtered to `STREET_NAME = SECORD`;
Committee of Adjustment open data (active + closed-since-2017) filtered to
`STREET_NAME = SECORD`.

### FACT — the exact retired range appears verbatim in a City staff report

The City's December 2024 rental-housing-demolition decision report for 90 Eastdale
Avenue and 2 Secord Avenue contains this decision-history paragraph (quoted verbatim
from the PDF):

> On July 16, 2013, City Council approved the application for a Rental Demolition permit
> under the Municipal Code to demolish 22 residential rental townhouse units located at
> 90 Eastdale Avenue (Units 92-108 and 101A) and 2 Secord Avenue (**Units 8-18 and
> 40-50**) to replace them with 24 three-bedroom stacked townhouses.

Source: *90 Eastdale Avenue and 2 Secord Avenue – Rental Housing Demolition Application
– Decision Report – Approval*, Toronto and East York Community Council, dated
18 December 2024, Ward 19 Beaches-East York —
https://www.toronto.ca/legdocs/mmis/2025/te/bgrd/backgroundfile-251764.pdf

The 2013 council item it cites is 2013.TE25.16 —
https://secure.toronto.ca/council/agenda-item.do?item=2013.TE25.16 (403 to automated
fetch; the URL is printed inside the PDF above, which is how it is cited here).

The eleven addresses retired from the file on 2 April 2026 are 10, 12, 14, 16, 18, 40,
42, 44, 46, 48, 50 Secord Ave. The 2013 permit's Secord range is "Units 8-18 and 40-50".

**Discrepancy, recorded not explained:** 8 Secord Ave is inside the 2013 permit range but
was *not* retired — it is still on the address file. I have no source that reconciles this.

### FACT — the surviving evens 20–38 are the *next* phase, not this one

Same report, summary section, verbatim:

> This report reviews and recommends approval of the Rental Housing Demolition
> Application which proposes to demolish 31 townhouse rental dwelling units located at
> 90 Eastdale Avenue and 2 Secord Avenue. The 31 townhouse units are subject to
> secondary addresses inclusive of **20-38 Secord Avenue** and 48-88 Eastdale Avenue.

So the evens that stayed on the file (20–38) are precisely the units approved for a
*future* demolition, not yet carried out.

### FACT — application numbers, dates and decision path

From the same report and from the Development Applications open dataset:

| Item | Value |
|---|---|
| Rental Housing Demolition application | **24 123653 STE 19 RH** |
| Related Zoning By-law Amendment | **24 123646 STE 19 OZ** |
| ZBA submitted | 8 March 2024 (open data `DATE_SUBMITTED`) |
| RH application submitted | 8 April 2024 (report, "Decision History") |
| Tenant meeting | 9 September 2024 |
| Staff report | 18 December 2024 |
| Community Council (statutory public meeting) | 14 January 2025, adopted without amendment |
| To City Council | 5 February 2025 |
| ZBA status in open data (Aug 2026) | "Council Approved" |
| Ward | 19 — Beaches-East York (matches the file's ward for these points) |

- Community Council agenda item: 2025.TE19.10 —
  https://secure.toronto.ca/council/agenda-item.do?item=2025.TE19.10
- Zoning report: https://www.toronto.ca/legdocs/mmis/2025/te/bgrd/backgroundfile-251767.pdf
- Notice of public meeting (Rental Housing Demolition and Conversion):
  https://secure.toronto.ca/nm/api/individual/notice/5669.do
- Notice of application under the Planning Act, 90 Eastdale / 2 Secord:
  https://secure.toronto.ca/nm/api/individual/notice/5804.do
- Application Information Centre file for 24 123646 STE 19 OZ:
  http://app.toronto.ca/AIC/index.do?folderRsn=RehUeFAvbwH5UNv71hfqvw%3D%3D
- News: "Community Council approves plan for 40-storey residential building on Eastdale
  Avenue", *Beach Metro Community News*, 16 January 2025 —
  https://beachmetro.com/2025/01/16/community-council-approves-plan-for-40-storey-residential-building-on-eastdale-avenue/

### FACT — the earlier applications on the same site

Development Applications open data, `STREET_NAME = SECORD` (3 records, all "2 SECORD
AVE", all Ward Beaches-East York):

- **08 231740 STE 31 OZ**, submitted 23 December 2008, Closed. Description: "OPA
  application to permit the demolition of 9 rental townhouse blocks containing 52 -3
  bedroom dwelling units so as to permit the construction of 2 above grade residential
  towers … Existing units to be retained 687, 365 proposed."
- **10 119850 STE 31 OZ**, submitted 18 February 2010, Closed. Description: "Rezoning
  application to include the replacement of 22 existing units on the site with new
  stacked townhouses, to add one new residential condominium building, being 24 storey
  building with 251 units …"
- **24 123646 STE 19 OZ** — as above.

### FACT — the project and its build dates

The site is DBS Developments' **Bela Square**, in the Taylor-Massey neighbourhood, north
of Danforth Ave near Main St.

- Phase 1, 94 Eastdale Ave (7-storey, 80 units): completed May 2024.
- Phase 1, 100 Eastdale Ave (35-storey, 404 units): occupancy began March 2025.
- Phase 2 (the 40-storey tower replacing the remaining 31 townhouses): approved; the
  developer "is unsure of when construction will start."

Source: RENX, "In Toronto's Main-Danforth, Bela Square is an entirely new concept" —
https://www.renx.ca/index.php/dbs-second-bela-square-apartment-building-opens-in-toronto

Also: UrbanToronto project database, Bela Square Phase 2 (primary address 88-90 Eastdale
Ave, Toronto M4C 5A2; status Pre-Construction; DBS Developments and Achille
Developments; Arcadis) — https://urbantoronto.ca/database/projects/bela-square-phase-2.55664
and https://urbantoronto.ca/news/2024/04/40-storeys-proposed-bela-square-second-phase-east-york.55677
and the Bela Square Phase 1 entry https://urbantoronto.ca/database/projects/bela-square.31626

Phase 1 LPAT approval: "On May 24, 2019, The Local Planning Appeal Tribunal (LPAT)
approved Zoning By-law and Official Plan Amendment applications for Phase 1 to permit a
35-storey tower consisting of 404 units on the north end of the block and a 7-storey
apartment building consisting of 80 units, including 22 rental replacement units, on the
western side of the block." (quoted from backgroundfile-251764.pdf).

### FACT — the demolition permit date, from the City's rental-demolition register

The City publishes *Demolition and Replacement of Rental Housing Units* —
https://open.toronto.ca/dataset/demolition-and-replacement-of-rental-housing-units/
(CKAN resource `3ad8e86d-f166-4279-85e8-69b752248c16`, refreshed 3 August 2026). It has
two rows for this site, and they are decisive:

**Row 1 — the Phase 1 demolition (the eleven retired addresses)**

| Field | Value |
|---|---|
| IBMS Address | `90 EASTDALE AVE` |
| Address of Existing Rental Building | `2 Secord Avenue` |
| RH File Number | **12 269076 STE 31 RH** |
| Ward (post-2018) | 19 |
| City Council Approval Date | **2018-07-23** |
| Link to Staff Report | https://secure.toronto.ca/council/agenda-item.do?item=2018.TE34.21 |
| Type | Demolition – 6 Rental Units or More |
| Total rental homes for demolition | **22** (10 affordable, 12 mid-range) |
| Total rental homes replaced | 28 |
| **Date the Rental Demolition Permit was Issued** | **25 March 2021** |
| Date the 2nd Rental Demolition Permit was Issued | 23 July 2024 |
| Rental homes subject to rental demolition permit(s) | 22 |

The "22" matches the 22 townhouse units of the 2013 approval — 90 Eastdale (Units 92-108
and 101A) plus 2 Secord (Units 8-18 and 40-50).

**Row 2 — the Phase 2 demolition (the surviving evens 20–38, not yet demolished)**

| Field | Value |
|---|---|
| IBMS Address | `90 Eastdale and 2 Secord Avenue` |
| Address of Existing Rental Building | **`20-38 Secord Avenue and 48-88 Eastdale Avenue`** |
| RH File Number | **24 123653 STE 19 RH** |
| City Council Approval Date | **2025-02-05** (confirms the Council date) |
| Link to Staff Report | https://secure.toronto.ca/council/agenda-item.do?item=2025.TE19.10 |
| Total rental homes for demolition | 31 (17 affordable, 1 mid-range, 13 high-end) |
| Total rental homes replaced | 35 |
| Date the Rental Demolition Permit was Issued | **N/A** — none issued |

So: Phase 1's demolition permit issued **25 March 2021**; Phase 2's has **not been issued
at all** as of the dataset's 3 August 2026 refresh. That is exactly the split the address
file shows — 10–18 and 40–50 gone, 20–38 still there.

**Note a discrepancy in the record itself:** the 2024 staff report attributes the 22-unit
approval to City Council on **16 July 2013** (item 2013.TE25.16); this dataset records
the council approval for RH file 12 269076 STE 31 RH as **23 July 2018** (item
2018.TE34.21). Both are City sources. I did not reconcile them — the RH file number
`12 …` suggests a 2012 application that ran a long course. Cite whichever you use, and
say which.

### INFERENCE (labelled) — what this most likely means for the file

The eleven addresses retired on 2 April 2026 match, number for number apart from 8
Secord, the townhouse units covered by the Phase 1 rental demolition permit — whose
permit was **issued 25 March 2021** — and which were cleared to build Bela Square Phase 1
(94 Eastdale completed May 2024; 100 Eastdale occupancy March 2025). The inference is
that the 2 April 2026 retirement is the address file catching up on a physical demolition
that happened roughly **five years earlier**, not a new event on the ground in April 2026.

The complementary inference: the evens that stayed (20–38) are the Phase 2 units, whose
demolition permit has not been issued, so the buildings are still standing and still
addressed.

**What is NOT established:** the date the buildings actually came down. A permit issued
25 March 2021 is a licence to demolish, not proof of the date of demolition. Searched the
Development Applications, Committee of Adjustment and Building Permits (active and
cleared-since-2017) open datasets for `STREET_NAME = SECORD` — no demolition permit record
at 10–50 Secord Ave in any of them; the rental-demolition register above is filed under
90 Eastdale Ave.

**Timing gaps:** rental demolition permit issued 25 March 2021 → ~5.0 years before the
file change. 2nd rental demolition permit 23 July 2024 → ~1.7 years before. City Council
approval of Phase 2, 5 February 2025 → ~14 months before. Phase 1 occupancy March 2025 →
~13 months before.

**Confidence: confirmed** for the address range appearing verbatim in the 2013 permit as
quoted in a 2024 City report, for the 25 March 2021 demolition-permit date, for the
absence of a Phase 2 demolition permit, and for all application numbers and dates.
**Confidence: likely** for the causal link between the Phase 1 demolition and the April
2026 retirement. **Nothing found** for the physical demolition date.

**Nothing found** for: Toronto Community Housing involvement on Secord Ave; a Crescent
Town assembly; any 2026-dated news item about Secord Ave; any Committee of Adjustment
application on Secord Ave at all (0 records in both the active and closed-since-2017
datasets).

---

## 2. Everwood Gardens, Commerce Trail and 2650 St Clair Ave W

**What I searched.** `"2650 St Clair Avenue West" Toronto development application`;
`"Everwood Gardens" "Commerce Trail" Etobicoke York Community Council agenda item 2026`.

### FACT — both names come from one City street-naming report, and it is explicit

*Naming of 2 Private Streets for a Development at 2650 St. Clair Avenue West*, report to
Etobicoke York Community Council from the Director, Engineering Support Services,
**dated 30 January 2026**, Ward 5 — York South-Weston.

https://www.toronto.ca/legdocs/mmis/2026/ey/bgrd/backgroundfile-284282.pdf

Verbatim recommendations:

> 1. Approve the name "Commerce Trail" for a proposed private street at 2650 St. Clair
>    Avenue West, shown as PART 1 on Attachment No.1 Sketch No. PS-2025-052
> 2. Approve the name "Everwood Gardens" for a proposed private street at 2650 St. Clair
>    Avenue West, shown as PART 2 on Attachment No.1 Sketch No. PS-2025-052

Other facts from the same report:

- The naming application was received from the developer on **7 November 2025**.
- "This is the first time that this issue is before Community Council."
- Both are **private** streets, not public ones.
- Names circulated to and acceptable to Toronto Police Service, Toronto Fire Services and
  Toronto Paramedic Services. Councillor Frances Nunziata (Ward 5 York South-Weston)
  supports the naming. Community Councils hold delegated authority to decide street
  naming.
- Applicant rationale, verbatim: Commerce Trail "reflects the historical economic
  significance of the St. Clair Avenue West area … Once part of the city's thriving
  Stockyards District, the neighbourhood supported meatpacking, rail-based logistics, and
  manufacturing industries"; Everwood Gardens "combines 'ever,' suggesting longevity and
  continuity, with 'wood,' evoking trees, greenery, and a connection to nature."
- Signage cost estimated at $1,200, payable by the applicant.
- City street-naming policy: https://www.toronto.ca/city-government/planning-development/street-naming/

This is a direct match to the file: Ward York South-Weston, former municipality York, two
new street names, addresses first seen 13 April 2026.

### FACT — the development at 2650 St Clair Ave W

*2650-2672 St. Clair Avenue West – Zoning By-law Amendment and Draft Plan of Subdivision
Applications – Request for Directions Report*, Etobicoke York Community Council, dated
**24 June 2020**, Ward 5 – York South-Weston. Planning application numbers
**18 208427 WET 11 OZ** and **18 208431 WET 11 SB**.

https://www.toronto.ca/legdocs/mmis/2020/ey/bgrd/backgroundfile-148358.pdf

Verbatim details:

> These applications propose to amend the former City of York Zoning By-law No. 1-83 and
> City-wide Zoning By-law No. 569-2013 and seek Draft Plan of Subdivision approval to
> redevelop the site of the former Danier Leather factory, municipally known as
> 2650-2672 St. Clair Avenue West.

> The townhouses would be in five blocks (Blocks A to E), having a total of 98
> three-bedroom units. Each block is proposed to be 4-storeys (12.75 metres in height) …

> The Draft Plan of Subdivision application proposes to establish a new public road to
> the west of the existing commercial building extending from St. Clair Avenue West to
> the existing public lane to the north …

The 2-storey building fronting St Clair Ave W (6,500 m² GFA, the former Danier outlet) is
retained and renovated for commercial/office use. 388 parking spaces. The owner had
appealed to LPAT for non-decision as of the 2020 report.

Marketing pages describe the project as "2650 St. Clair Avenue West Townhomes" by
**Dunpar Homes**, 98 back-to-back townhomes (third-party, not a City source):
https://precondo.ca/2650-st-clair-ave-west-townhomes/ ;
https://www.gta-homes.com/toronto-condos/2650-st-clair-ave-west/

### FACT — the site is under permit and the lead permits were issued in January 2026

Building Permits – Active Permits open data
(https://open.toronto.ca/dataset/building-permits-active-permits/, resource
`6d0229af-bc54-46de-9c2b-26759b01dd05`): **662 active permit records** at STREET_NUM 2650
/ STREET_NAME ST CLAIR. They are the six townhouse blocks of the 2020 subdivision, by
block letter and model name:

| Folder | Block | Description in permit |
|---|---|---|
| 23 192840 | Block A | "16 back-to-back townhouses" |
| 23 192883 | Block B | "16 back-to-back townhouses" |
| 23 193111 | Block C | "18 back-to-back townhouses" |
| 23 193153 | Block D | "8 back-to-back townhouses" |
| 23 193212 | Block E | "18 back-to-back townhouses with parking garage for the 18 townhouses" |
| 23 193276 | Block F | "20 back-to-back townhouses" |

- All six folders applied **23–24 August 2023**.
- Drain/site-service permits issued **18 September 2025**.
- The "New Building – Lead" permits (23 193111 B01, 23 193153 B01, 23 193212 B01) and the
  bulk of the New Building / HVAC / plumbing permits were **issued 16 and 22 January 2026**.
- Revisions applied 17–18 February 2026 were **issued 24 and 30 April 2026** and
  1 May 2026.
- An older permit at the same address, 17 124169 BLD (issued 5 April 2017), is the
  industrial-building recladding: "Exterior recladding of Building facade … Future use
  office" — i.e. the retained Danier building.

**Timing:** the construction permits were issued 16–22 January 2026; the street names were
recommended 30 January 2026; the five addresses (15, 25, 35 Everwood Gardens; 30, 50
Commerce Trail; and 2650 St Clair Ave W itself) first appear in the file on 13 April 2026
— roughly **three months after** permit issuance and **ten weeks after** the naming report.

**Nothing found:** zero permit records under STREET_NAME EVERWOOD or COMMERCE in either
the active or the cleared-since-2017 permit dataset — expected, since the private streets
were only named in 2026 and the permits are all filed against 2650 St Clair Ave W.

### Named subdivision / masterplan?

**Nothing found** for a named masterplan or branded subdivision name covering Everwood
Gardens and Commerce Trail beyond the developer's project marketing. The City report
treats them purely as two private streets inside 2650 St Clair Ave W.

### NOT established — the exact community-council decision date

The report is dated 30 January 2026 and community councils have delegated authority, so
a decision would normally follow at the next Etobicoke York Community Council meeting
(meetings on 18 February 2026 and 31 March 2026 exist per the City's YouTube channel:
https://www.youtube.com/watch?v=oFxSvyzQvZw and
https://www.youtube.com/watch?v=OrYbhbFa6yg; a communication filed for a
February 2026 EY meeting: https://www.toronto.ca/legdocs/mmis/2026/ey/comm/communicationfile-205130.pdf).
I could not retrieve the agenda/decision item number — `secure.toronto.ca/council/report.do`
and `/council/agenda-item.do` both return 403 to automated fetches. A second search
surfaced two Etobicoke York agenda-item URLs in the same result set
(2026.EY31.3 and 2026.EY32.24) but **neither could be verified as this item** — do not
use either. **Do not state a decision date or item number without checking
`secure.toronto.ca` in a browser.**

**Timing:** the naming report is dated 30 January 2026, ~10 weeks before the addresses
appear in the file (13 April 2026). The addresses arrive as *reserved*, which is
consistent with streets named and under construction but not yet occupied — the townhouse
construction permits were issued 16–22 January 2026 (see below).

**Confidence: confirmed** for the street-naming report, its date, ward, the private-street
status, the applicant rationale, and the 2650 St Clair development. **Nothing found** for
the community-council decision item number/date, or for a subdivision brand name.

---

## 3. Rear ("R") addresses — 407R Arlington Ave, 623R Broadview Ave, 885R Caledonia Rd

**What I searched.** `Toronto address "R" suffix rear address municipal addressing
standard laneway suite`; the City's *Municipal Numbering of a Property* page; Toronto
Municipal Code **Chapter 598, Numbering of Properties** (full text, grepped for
"rear", "suffix", "letter", "alpha" — **zero hits**); the Address Points (Municipal) open
data dataset page; Committee of Adjustment open data for Arlington / Broadview /
Caledonia; Building Permits (active) open data for 407 Arlington, 623 Broadview,
885 Caledonia.

### NOTHING FOUND — no City source defines the "R" suffix

- *Municipal Numbering of a Property* (City of Toronto) —
  https://www.toronto.ca/city-government/planning-development/municipal-numbering-of-a-property/
  — lists triggers for a new address ("New construction results in an additional building
  or entrance on the property requiring a separate address") and links the Laneway Suites
  and Garden Suite programs, but **does not define any suffix**, "R" or otherwise.
  Contact for addressing: municipaladdress@toronto.ca / 311.
- Toronto Municipal Code **Chapter 598, Numbering of Properties** —
  https://www.toronto.ca/legdocs/municode/1184_598.pdf — sections 598-1 through 598-9.
  No occurrence of "rear", "suffix", "letter" or "alpha" anywhere in the chapter.
  §598-3.B says only: "Where a new building is erected, the Deputy City Manager shall
  assign to the building a municipal address conforming to the municipal addresses of the
  other properties on the street … according to the official record."

  (Useful side-fact from the same chapter, §598-2: "The 'One Address Repository' component
  of the City's corporate data base … is the official record of the municipal addresses of
  properties within the City", and §598-2.D requires each address to carry one of the
  former-municipality identifiers "former Toronto," "East York," "York," "North York,"
  "Etobicoke" or "Scarborough" — which is where the file's former-municipality field
  comes from.)

**Do not assert that "R" is Toronto's documented convention for a rear structure.** No
source found says so.

### FACT — two of the three R addresses have a laneway/garden-suite building permit

From Building Permits – Active Permits open data
(`https://open.toronto.ca/dataset/building-permits-active-permits/`, resource
`6d0229af-bc54-46de-9c2b-26759b01dd05`, refreshed 27 Aug 2026):

**407 Arlington Ave** (11 permit records at this address):

| Permit | Type | Structure type | Work | Applied | Issued | Description |
|---|---|---|---|---|---|---|
| 25 104277 BLD | Small Residential Projects | **Laneway / Rear Yard Suite** | **New Laneway / Rear Yard Suite** | 2025-01-14 | **2025-05-12** | "Proposal for a laneway suite at the rear of 4 Unit-Detached" |
| 25 104109 BLD | New Houses | 3+ Unit – Detached | New Building | 2025-01-13 | 2025-02-07 | "Propose new 3-storey fourplex" |

(plus matching DRN/HVA/PLB service permits under both folders)

And from Building Permits – Cleared since 2017 (resource
`a96c0ba4-3026-402b-b09d-5b1268b8f810`), one further permit at 407 Arlington Ave:

| Permit | Type | Structure type | Work | Applied | Issued | Completed | Description |
|---|---|---|---|---|---|---|---|
| **25 104153 DEM** | Demolition Folder (DM) | SFD – Detached | Demolition | 2025-01-13 | 2025-02-10 | **2026-07-24** | "Propose new 3-storey fourplex" |

So 407 Arlington Ave is: existing detached house demolished (permit issued Feb 2025,
cleared July 2026), replaced by a 3-storey fourplex, **plus** a laneway suite at the rear.

**623 Broadview Ave** (5 permit records):

| Permit | Type | Structure type | Work | Applied | Issued | Description |
|---|---|---|---|---|---|---|
| 25 222205 BLD | Small Residential Projects | **Laneway / Rear Yard Suite** | **New Laneway / Rear Yard Suite** | 2025-09-08 | **2026-01-19** | "Proposal for new garden suite" |
| 25 222205 BLD (rev 01) | same | same | same | 2026-04-23 | 2026-05-08 | "REV01: Proposed revision as per drawings (correction to lot boundary)" |

Also, Committee of Adjustment (closed-since-2017 dataset), 623 Broadview Ave:

- **A0755/25TEY**, in 2025-10-06, Toronto East York panel, status **Deferred**: "To
  construct a new two-storey detached ancillary building (containing one garden suite
  with a south side porch and second storey deck), in the rear yard, abutting Tennis
  Crescent."
- **A1024/19TEY**, in 2019-09-24, heard 2020-01-29, **Withdrawn**: "To construct a new
  rear two-storey ancillary building containing a dwelling unit."

**885 Caledonia Rd — nothing found.** Zero records in Building Permits, both the active
and the cleared-since-2017 datasets, whether filtered on STREET_NUM 885 / STREET_NAME
CALEDONIA or free-text searched for "885 CALEDONIA". Zero Committee of Adjustment records
at 885 Caledonia in either the active or closed-since-2017 datasets. (Caledonia Rd has
8 active and 33 closed CoA records overall, none at 885.) Zero Development Applications
at 885 Caledonia (Caledonia Rd has 43 city-wide, all at other numbers). So 885R Caledonia
Rd has **no public-record explanation at all** in the City's own datasets.

### Timing

- 407R Arlington added to the file 27 April 2026; its laneway-suite permit was issued
  12 May 2025 — the address arrives **~11.5 months after** permit issuance.
- 623R Broadview added 27 April 2026; its garden-suite permit was issued 19 January 2026
  — the address arrives **~3.2 months after** permit issuance.
- 885R Caledonia added 3 April 2026; no permit record found to compare.

### City programs (background, with sources)

- Laneway Suites (Changing Lanes) program —
  https://www.toronto.ca/city-government/planning-development/planning-studies-initiatives/changing-lanes-laneway-suites-in-toronto/
- Garden Suites program —
  https://www.toronto.ca/city-government/planning-development/planning-studies-initiatives/garden-suites/
- 2017 City background report, *Laneway Suites: A new housing typology for Toronto*
  (26 May 2017) — https://www.toronto.ca/wp-content/uploads/2017/10/97ac-Laneway-Suits.pdf

**Both program pages were fetched and checked.** Neither the Changing Lanes (laneway
suites) page nor the Garden Suites page contains anything about how a suite gets a
municipal address — no suffix, no separate-address rule, no "R", no municipal numbering
at all. So the answer to "what does the laneway/garden-suite program say about how these
get addressed?" is: **nothing**.

The City's own permit data uses the structure type "Laneway / Rear Yard Suite" — that
phrase is the closest official language found to "rear address", and it comes from the
permit dataset, not from an addressing policy.

**Confidence: confirmed** that 407 Arlington and 623 Broadview each have a City building
permit for a laneway/rear-yard suite (and that 623 Broadview's is described as a garden
suite in both the permit and a Committee of Adjustment application).
**Confidence: nothing found** for any City document defining the "R" suffix, and for any
permit or CoA record at 885 Caledonia Rd.
**Inference (labelled, not asserted):** that the R-suffixed address is how the City
numbers these rear suites. Two of three cases line up; no policy source confirms the rule.

---

## 4. Sandown Lane, Scarborough Southwest — 170 and 172 added 2 April 2026

**What I searched.** `"Sandown Lane" Toronto Scarborough new street naming`; Development
Applications open data `STREET_NAME = SANDOWN` (0 records); Committee of Adjustment open
data `STREET_NAME = SANDOWN` (0 active, 18 closed-since-2017 — none at 170 or 172);
Building Permits open data for 170 and 172 Sandown.

### FACT — Sandown Lane is not a new street on the ground

Sandown Lane is a pre-existing public laneway, documented in a 2021 walking blog:
"runs behind the buildings on the north side of Kingston Road, west of Midland Avenue in
Scarborough" — https://mcfcrandall.blog/2021/02/13/sandown-lane-cliffside/ (post dated
13 February 2021; Cliffside, Toronto). That location matches the file's coordinates
(~43.7065, -79.2522, Kingston Rd near Midland Ave) and its ward, Scarborough Southwest.

The same post's update notes two nearby Kingston Rd developments that had site plan
approval at the time of writing: an 8-storey mixed-use building at 2448-2450 Kingston Rd
(former cat hospital) and a 6-storey mixed-use development at 2380-2382 Kingston Rd
(former Wong's Martial Arts). Neither is at 170/172 Sandown; treat as context only.

Historical background on the name (Sandown Park subdivision, bounded by the CNR,
Kennedy Rd, Kingston Rd and Midland Ave) — Scarborough Historical Society, "Street Names
of Scarborough": https://scarboroughhistorical.ca/local-history/street-names-of-scarborough/

### NOTHING FOUND — no development behind 170/172 Sandown Lane

- Development Applications open data: **0 records** for STREET_NAME SANDOWN, city-wide.
- Committee of Adjustment: 0 active, 18 closed-since-2017 on Sandown — none at 170 or 172.
- Building Permits: **0 records** at 170 or 172 Sandown in either the active or the
  cleared-since-2017 dataset.
- No council street-naming report found for Sandown Lane (consistent with it being an
  existing lane rather than a newly named one).

**Note on the framing:** "new street" here means new *to the address file*, not new on the
ground. The lane predates the file by at least five years. What is new is that two
addresses (170, 172) were assigned on it, filed as *regular* rather than *reserved*.

**Confidence: confirmed** that Sandown Lane is an existing Toronto laneway in Cliffside at
the file's coordinates. **Nothing found** for what was built or approved at 170/172.

---

## 5. 152 Pinegrove Ave and 155 Poyntz Ave — the two splits

**What I searched.** `"152 Pinegrove" Toronto committee of adjustment consent severance`;
`"155 Poyntz" Toronto North York severance OR "committee of adjustment" OR demolition`;
Committee of Adjustment open data filtered to `STREET_NAME = PINEGROVE` and
`STREET_NAME = POYNTZ`; Development Applications open data (0 records for PINEGROVE;
POYNTZ records are all Willowdale towers, none at 155).

### FACT — 152 Pinegrove Ave: consent to sever, approved 11 February 2026

City of Toronto Committee of Adjustment, **Scarborough** panel:

| File | Type | In date | Hearing | Decision | Description |
|---|---|---|---|---|---|
| **B0037/25SC** | Consent | 2025-11-26 | **2026-02-11** | **Approved** | "To obtain consent to sever the property into two residential lots. The existing one-storey detached dwelling would be demolished." |
| **A0251/25SC** | Minor variance | 2025-11-26 | 2026-02-11 | **Approved** | "To construct a new three-storey detached dwelling (triplex) with front porch, two front balconies on the second and third floors, a rear deck and two rear balconies … Cross-reference Consent" |
| **A0252/25SC** | Minor variance | 2025-11-26 | 2026-02-11 | **Approved** | (same wording as A0251/25SC — the second of the pair) |

Three further placeholder records at 152 Pinegrove (one CO, two MV) with in-date
2025-10-08 and no file number carry no decision.

Source: Committee of Adjustment Applications, City of Toronto Open Data —
https://open.toronto.ca/dataset/committee-of-adjustment-applications/ (closed-since-2017
resource `9c97254e-5460-4799-896f-c7823413c81c`, refreshed 27 Aug 2026).

**Timing:** the severance was approved 11 February 2026; 152A/152B Pinegrove appear in the
address file in April 2026 — about **two months later**.

### FACT — 155 Poyntz Ave: consent to sever, approved 14 August 2025

City of Toronto Committee of Adjustment, **North York** panel:

| File | Type | In date | Hearing | Decision | Description |
|---|---|---|---|---|---|
| **B0002/25NY** | Consent | 2025-02-03 | **2025-08-14** | **Approved** | "To obtain consent to sever the property into two residential lots. Application Nos. B0002/25NY, A0073/25NY & A0077/25NY will be considered jointly." |
| **A0073/25NY** | Minor variance | 2025-02-03 | 2025-08-14 | **Approved** | "To construct a new detached dwelling with an integral garage and a rear deck." |
| **A0077/25NY** | Minor variance | 2025-02-03 | 2025-08-14 | **Approved** | "To construct a new detached dwelling with an integral garage and rear deck." |

Three placeholder records at 155 Poyntz (two MV, one CO) with in-date 2024-09-26 and no
file number carry no decision.

**Timing:** the severance was approved 14 August 2025; 155A/155B appear in the address
file in April 2026 — about **eight months later**.

**Both cases:** severance (consent) plus two new dwellings, exactly matching the file's
"original still on file, plus A and B" pattern.

**Confidence: confirmed** for both, with file numbers, hearing dates and decisions from
the City's own open data. The link to the April 2026 address split is an **inference**,
though a strong one given the shape and the dates.

---

## 6. Items not researched / researched incidentally

- **Bazalgette Dr cluster (27–34, retired 2 April / re-added 3 April under new ids).**
  Not on the assignment list, but checked while running the datasets: **0 records** in
  Development Applications, **0** in Committee of Adjustment (active and
  closed-since-2017), and **0** in Building Permits (active and cleared-since-2017) for
  STREET_NAME BAZALGETTE. Nothing found anywhere. Consistent with a records-keeping
  reissue rather than a development.
- **Secord Ave building permits.** Also checked: **0 records** at 10, 12, 40 or 50 Secord
  in either permit dataset — no demolition permit surfaced for the eleven retired units.
- **155 Poyntz Ave and 152 Pinegrove Ave building permits.** 152 Pinegrove has a single
  cleared permit, 18 265223 DRN, a 2018 back-water-valve installation — unrelated.
  155 Poyntz has none. The severances in §5 are the only records.
- **9 Don River Blvd, place name "Parking Lot - Earl Bales Park".** Not researched; not on
  the assignment list. (Development Applications has 2 records on "DON RIVER" but they
  were not inspected against number 9.)

---

## Method notes for whoever writes the piece

1. The `secure.toronto.ca` 403 means agenda-item and meeting-agenda URLs cannot be
   verified programmatically. They are stable, public URLs in a browser. Two facts in
   §1 (the 2013 item number, the January 2025 community-council date) come from a City
   PDF and a news article respectively, not from those pages.
2. WebSearch result summaries were wrong at least once in this session (a summary claimed
   "20-38 Secord Avenue" was the demolished set; the source PDF says the opposite —
   20-38 is the *surviving*, next-phase set). Every load-bearing quote above was pulled
   from the raw PDF or raw JSON, not from a search snippet.
3. The open-data route (CKAN `datastore_search` with a `filters` JSON on STREET_NAME /
   STREET_NUM) is far more productive than web search for individual addresses, and is
   itself citable. Reuse it.
