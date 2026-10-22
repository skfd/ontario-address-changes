# Research notes - City of Burlington, 2026-09

Window 2026-08-28 -> 2026-09-28. Snapshots kept 15, 16, 25, 28 Sep. Net +8 (11 added, 3
removed), 1 unit split, 1 status change. Research run 2026-10-22, fanned out to four
agents (Guelph Line; New St + Glenwood; Plains Rd + layer metadata; Chamberlain + Enfield).
Burlington's Committee of Adjustment does not publish decisions online (agendas on
events.burlington.ca, decisions by Routine Disclosure request), so "nothing found" below
means nothing *indexed*, not nothing filed.

## Store facts the article leans on (verified with lookup.py / sqlite, 2026-10-22)

- The month's twelve new rows carry consecutive City property-record numbers
  (PROPERTYRSN) 106775-106786: 106775 0000 Enfield; 106776-77 541 Chamberlain Units 1, 2;
  106778-80 3188, 3190, 3186 New St; 106781 3340 Guelph Line; 106782 3350 Guelph Line;
  **106783 never appears in any snapshot through 22 Oct** (max RSN on file 106794);
  106784 6701 Guelph Line; 106785 6671 Guelph Line; 106786 884 Glenwood.
- 3350, 6671 and 6701 Guelph Line each left and returned in one update with a new RSN
  (17774->106782 on 16 Sep; 15745->106785 and 15743->106784 on 25 Sep). Point moves:
  3350 236 m north (old dot between 3324 and 3353, new dot 197 m past 3383); 6671 4 m;
  6701 362 m south (old dot 317 m north of 6783, new dot between 6724 and 6774, 94 m
  from each). New 3340 sits 82 m from 3324, 98 m from 3353, 144 m from where old 3350 was.
  Identity here is synthesized from address + 5 dp geometry, so a moved dot re-keys
  regardless; the new RSN is the City's doing, not the tracker's.
- 3186/3188/3190 New St (15 Sep, Pending, ward 4): 3186 is 37 m from 3180 and 8 m from
  3192; 3188 is 3 m from 3192; 3190 is 6 m from 3192 and 10 m from 3194. Spacing 6-7 m.
  3192 remains on file unchanged.
- 884 Glenwood Ave (28 Sep, Pending, ward 1): between 880 (43.30666,-79.84438) and 886
  (43.30682,-79.84511); 881 and 885 across the street.
- 541 Chamberlain Rd Units 1 and 2 (15 Sep): PROPCODE 20 "Tenant", Active; parent 541
  remains; the only unit rows on Chamberlain Rd. File has 1,977 Tenant rows.
- 0000 Enfield Rd (15 Sep): Property, Active, no NAME, no ward value (the only new row
  without one); 33 m from 619 Wickens Ave, 81 m from 1076 King Rd, 1.2 km from 331/332
  Enfield Rd. File has 141 active 0000 points, 30 of them named (e.g. 0000 Guelph Line =
  Centennial Bikeway).
- 500 Plains Rd E: two points. RSN 105045, PROPCODE 140 "Address", Pending since the
  11 Jun baseline, flipped to Active on 28 Sep (the month's one status change). A second
  point RSN 106746, PROPCODE 10 "Property", Active, appeared 20 Aug about 50 m away.
- Vocabulary on file at 28 Sep: PROPSTATUS 1 Active 60,169 / 3 Pending 187. PROPCODE
  10 Property 56,920; 20 Tenant 1,977; 140 Address 768; 180 Secondary Building 240;
  190 Tenant Non-Res 253; 100 Park 138; 90 Creek Block 40; 160 Block 16; 22 School
  Lease 2; 40 Road 2. Four of the month's additions are Pending (the New St trio, 884
  Glenwood).

## Findings

### 884 Glenwood Ave / 880 Glenwood Ave
- **880 Glenwood Avenue, consent B-004-2024 + minor variance A-012-2025** - Committee of
  Adjustment. Consent "to sever a parcel of land for the creation of one new residential
  lot"; retained ~4,022.9 m2, severed ~787.8 m2. Variance to permit a 0.85 m south-east
  side yard for the existing dwelling (2.902 m required) and two hammerhead-driveway
  exceptions on the retained parcel, "required to facilitate Consent application
  B-004-2024". On the agendas of 8 April 2026 and 20 May 2026.
  https://events.burlington.ca/meetings/Detail/2026-04-08-1730-Committee-of-Adjustment/49c0617e-5c8c-4abf-a912-b41d01251c9b
  https://events.burlington.ca/meetings/Detail/2026-05-20-1300-Committee-of-Adjustment/f6ceb750-4ba6-4815-a356-b44a014d3b1f
  Confidence: high on identity (events.burlington.ca, Aldershot). Details from search
  snippets - both agenda pages exceed the fetch size limit. **Decision not found.** That
  884 is the severed lot is inference; no source says so.
- 884 Glenwood on its own: nothing found. Queries: `"884 Glenwood" Burlington Ontario`;
  `"880 Glenwood" OR "886 Glenwood" OR "884 Glenwood" Burlington Aldershot`. Only
  street-browse pages (Royal LePage, Redfin) listing the numbers.

### 3186 / 3188 / 3190 / 3192 New St
- **3188 New Street, MLS W13550254** - new-construction freehold row/townhome by Coral
  Gable Homes (Tarion), listed $1,299,999, 3+1 or 4 bed / 3 bath, ~2,253 sq ft above
  grade; "construction is well underway", buyer may "personalize many of the interior
  finishes". Listed per homli "July 10, 2026"; a keyhomes copy returned HTTP 410 on
  2026-10-22 (removed). Postal code L7N 1M8, Roseland, "Dynes and New St".
  https://homli.ca/burlington-real-estate/3188-new-street/W13550254 (fetched; address,
  postal code, neighbourhood confirmed, details gated)
  https://rlpburloak.ca/listing/3188-new-street-burlington-ontario-w13550254/ (403;
  details from snippet)
  Confidence: high on Burlington ON. Brokerage differs between sources. A freehold
  townhome at 3188 implies attached neighbours at 3186/3190 - inference, not stated.
- 3192 New St: nothing found (consent, part-lot control, site plan, demolition, listing).
  Queries: `"3192 New Street" Burlington`; `"3192 New St" OR "3192 New Street" Burlington
  severance OR consent OR townhomes OR demolition`; burlington.ca / events.burlington.ca
  / escribe restricted searches for 3186/3188/3190/3192. Only unrelated New St items
  (2421-2431, 2360-2368, 5111).
- 3186, 3190 New St: nothing found beyond the implied neighbours.
- Context: 3198 New St listed as a custom-built 4-bed at $1,799,900
  (https://meadowtownerealty.com/listing/3198-new-street-burlington-ontario-40691336) -
  adjacent infill, no stated link.

### 541 Chamberlain Rd
- **Lower units "A" and "B"** - two separate 2-bed/1-bath lower-level rentals at $2,100
  each, "brand-new, never-lived-in lower-level suite", in-suite laundry; keyhomes:
  "Apartment in basement, Separate entrance", lot 46 x 110.06 ft, L7L 2V2 (Shoreacres).
  https://www.zolo.ca/burlington-real-estate/541-chamberlain-road/a
  https://www.zolo.ca/burlington-real-estate/541-chamberlain-road/b
  https://www.rew.ca/rentals/7428521/a-541-chamberlain-road-burlington-on
  https://www.rew.ca/rentals/7428516/b-541-chamberlain-road-burlington-on
  Confidence: high on Burlington ON; listing pages 403/410 to fetch, so listing dates
  unconfirmed (snippet only).
- **Upper unit, MLS W13827094** - 4-bed/2-bath "stunningly renovated main-floor
  residence", $3,499/month, price change 14 Oct 2026, updated 21 Oct 2026, age 31-50
  years, basement "No" (not part of this unit).
  https://www.squareyards.ca/lease/on/halton/burlington/shoreacres/unit-upper-541-chamberlain-road
  Confidence: high, fetched directly.
- **City ARU rules** - "Zoning Checklist, FAQs, and Handout for Additional Residential
  Units" (rev February 2025): "Up to three Additional Residential Units are permitted on
  a parcel of urban residential land where one Detached Dwelling, Semi-Detached Dwelling,
  Street Townhouse, or Townhouse is permitted." Zoning By-law Amendment 2020.494, Part 1
  s. 2.21(u). Says nothing about addressing.
  https://www.burlington.ca/en/planning-and-development/resources/Zoning-Clearance-Certificates/Zoning-FAQ-for-ARU.pdf
  City ARU page: a building permit is needed; incentive program of forgivable loans,
  grants and fee waivers.
  https://www.burlington.ca/en/building-and-renovating/additional-residential-units.aspx
  Confidence: high, both fetched.
- Building permit / CoA record for 541 Chamberlain: nothing found (Burlington publishes
  no permit index; ARUs are as-of-right so no CoA item expected). Whether each ARU gets
  its own unit point is not documented on burlington.ca; only Milton's by-law 033-2025
  turned up, which is not Burlington's.

### Guelph Line (3340, 3350, 6671, 6701)
- Committee of Adjustment / planning items for any of the four: nothing found. CoA page
  https://www.burlington.ca/en/planning-and-development/committee-of-adjustment.aspx
  lists 2026 meeting dates (incl. 2 and 23 Sep 2026) and says past agendas/minutes are
  available by Routine Disclosure request. Queries: `"3350 Guelph Line" Burlington`;
  `"3340 Guelph Line" Burlington`; `"6701 Guelph Line" Burlington`; `"6671 Guelph Line"
  Burlington`; `"Guelph Line" "committee of adjustment" Burlington 2026 consent`. Only
  older unrelated Guelph Line items (1396, 2022; 420, 2020).
- 3350 Guelph Line (L7P 0S7) - listings: rural estate, 1978 house, 7 bed, 4,385 sq ft,
  with a detached 3-bedroom coach house; acreage printed as 26 acres on some pages and
  "43-acre" on another; MLS 40723355 and W12181809; REW "Last updated 2025-08-30"; a
  Zolo snippet reports a sale in Aug 2025. Royal LePage page now "cannot be found".
  https://www.zolo.ca/burlington-real-estate/3350-guelph-line
  https://www.rew.ca/properties/3350-guelph-line-burlington-on
  https://invidiata.com/properties/3350-guelph-line-burlington
  Confidence: Burlington confirmed (postal code, Bruce Trail). Sale date snippet-only.
  Coach house + acreage discrepancy is suggestive of a second dwelling/parcel split
  matching the new 3340 - a lead, not a fact; no source states a severance.
- 6701 Guelph Line (L7P 0A6) - listings: vacant agricultural land, lot "555.52 x
  2229.67 Feet", described as ~90 acres; Zolo snippet shows a 2020 sale; a Century 21
  page (404 on fetch, snippet only) said the property "cannot be subdivided or severed
  as it is under conservation". No house in any listing.
  https://www.zolo.ca/burlington-real-estate/6701-guelph-line
  https://www.karenpaul.com/listing/6701-guelph-line-burlington-l7p-0a6/
  Confidence: Burlington confirmed; dates and the "cannot be severed" line are
  snippet-only. Not used in the article beyond "vacant land per listings".
- 6671 and 3340 Guelph Line: nothing found anywhere (consistent with 3340 being a brand
  new number).
- Burlington civic-addressing / rural numbering policy or by-law: nothing found (three
  agents tried; results were other municipalities and Burlington VT/WA).

### 500 Plains Rd E
- **Northshore (National Homes)** - 8-storey condo at 500 Plains Rd E, L7T 0C8, paired
  with "498 Plains Rd E Townhouses"; condos.ca: "Built in 2025", "8 floors / 188 units",
  HCC-811, "Date Registered: Nov 24, 2025", LaSalle neighbourhood.
  https://condos.ca/burlington/498-plains-road-e-townhouses-498-plains-rd-e-500-plains-rd-e
  Confidence: high on the address/building; registration date as printed, unverified.
- Planning history used 484-490 Plains Rd E: 2018 OPA/ZBA (National Homes, 2 x 8-storey
  + 117 stacked towns, 397 units, neighbourhood meeting 17 Jan 2018)
  https://www.mariannemeedward.ca/posts-to-be-added/public-meeting-jan-17-2-8-storeys-plus-117-towns-484-490-plains-rd-e ;
  sales launch Storeys 14 Mar 2023 (490 Plains Rd E, 153 units phase 1)
  https://storeys.com/northshore-490-plains-road-east-burlington-condo-development/ ;
  UrbanToronto "North Shore", 387 units, status Complete
  https://urbantoronto.ca/database/projects/north-shore.43306 ; groundbreaking Business
  Wire 2023-11-30 (403, snippet only). Unit counts conflict across sources (397/387/386/
  188/153) - not reconciled. That 484-490 became 498/500 is inference.
- Resale/rental listings at 500 Plains Rd E since May-June 2026 (units 207, 217, 310,
  314, 318; PH01 for rent June 2026), e.g.
  https://www.rew.ca/properties/318-500-plains-road-e-burlington-on
- No source explains a 28 Sep 2026 trigger. The flip trails registration by ~10 months
  and listings by ~4; it reads as the City's records catching up, which the file does
  not say either. City development page for 484-490: nothing found. Local press: nothing.

### 0000 Enfield Rd
- **OpenStreetMap** - Enfield Road in Burlington is two disconnected segments: the
  numbered 300-500 block (way 150682568) and a separate ~250 m stub (way 10157191,
  highway=unclassified) from King Road at 43.32560,-79.83285 south-west to
  43.32382,-79.83546; its node at 43.32420,-79.83498 is ~10 m from the City's point.
  https://www.openstreetmap.org/way/10157191
  Confidence: high for geometry (nodes fetched). The 1.2 km figure is the street being
  split, not the point being misplaced.
- Surroundings per OSM within 150-400 m: industrial and residential land use, the CN
  Oakville Subdivision main line and yard tracks, King Road rail underpass, Wickens Ave,
  Kingswood Pl. No park, trail, stormwater, hydro or construction feature at the point;
  nearest park Maplehurst Park ~400 m SW. Confidence: moderate (OSM coverage of small
  City parcels is incomplete).
- City park / acquisition / trail at Enfield-King-Wickens: nothing found. Queries:
  `"Enfield Road" "King Road" Burlington Aldershot`; `"Wickens Avenue" Burlington park`;
  `site:burlington.ca Enfield Road`; `Burlington Ontario Aldershot "Enfield" park OR
  parkette OR stormwater OR trail "King Road" 2025 OR 2026`. Nearby but unrelated: King
  Road closure 11 Mar-8 Apr 2026; Penta Properties 1200 King Rd subdivision (zoning July
  2026). Neither mentions Enfield.

### Layer metadata / what "Pending" means
- Layer 0 REST JSON (fetched 2026-10-22): description "City of Burlington Addresses";
  copyrightText "City of Burlington"; every field `"domain": null` - PROPSTATUSCODE /
  PROPSTATUSDESC / PROPCODE / PROPDESC carry no coded-value list. No editingInfo.
  https://mapping.burlington.ca/arcgisweb/rest/services/COB/AddressPoints/MapServer/0?f=pjson
  Parent service: "City of Burlington Municipal Addresses"; keywords "open data,
  Burlington Ontario, Address, Property".
  https://mapping.burlington.ca/arcgisweb/rest/services/COB/AddressPoints/MapServer?f=pjson
  Confidence: high.
- Navigate Burlington hub item https://navburl-burlington.opendata.arcgis.com/datasets/address-points
  is client-rendered; description/data dictionary not retrievable by fetch (403 on the
  API). Gap, not a null.
- No City page defines Pending/Active/Tenant/Property/Address. Closest text: Site Plan
  Application Guidelines say an applicant whose address "is not yet known or assigned"
  should consult Development Planning staff
  https://www.burlington.ca/en/planning-and-development/resources/Site-Plans/Site-Plan-Application-Guidelines.pdf
