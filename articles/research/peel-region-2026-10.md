# Research notes - Regional Municipality of Peel, 2026-10

Window: net 2026-06-11 -> 2026-10-24. The October 24 snapshot is the first change since
June 11 (July-September were read every day and came back identical), so everything below
is four and a half months of edits landing on one day. Searched 2026-11-08.

## Store facts (verified against data/peel-region/peel-region.db, snapshots 1 -> 40)

- Added 2,707 by MUNICIPALITY: Mississauga 1,268, Brampton 861, Caledon 578.
- Retired 78: Mississauga 55, Brampton 16, Caledon 7.
- New streets and municipality (cross-streets from the nearest pre-existing addresses):
  - ALIZA ST (124, 6201-6377), MALIYAH LANE (100), ANATIG BLVD (89), STANDING LANE (58):
    Mississauga, all within ~100 m of Ninth Line (6252, 6400, 6500 Ninth Line).
  - ARTIST LANE (75, 5120-5220): Mississauga, 50 m from 1711 Barbertown Rd.
  - DOCKVIEW DR (44) and JIM TOVEY BLVD (44 new, 1 already on file): Mississauga, next to
    Hydro Rd and Rangeview Rd, ~210 m from Lakeshore Rd.
  - HISTORY CIR (84), THORNBIRD CRES (67): Brampton, near All Nations Dr / Coastal Dr.
  - MUSTAFA CRES (46): Brampton, 27 m from 8646 Mississauga Rd. MAHA CRES (43): Brampton,
    61 m from 5759 Mayfield Rd. BRASSTOWN VALLEY TRAIL (+48, 3 already on file): Brampton.
  - SPEERS AVE (84), HEWSON TERR (71), SAINT RITA DR (50), DAMARA RD (44): Caledon, near
    Sweetgum Pl, Beech Hill Rd, Tim Manley Ave; Hewson near McLaughlin Rd.
- Renames: PLANTERS WOOD CRT -> PLANTER'S WOOD (44, Mississauga) - punctuation restyle;
  ERNEST BLASON -> ERNEST BIASON (2) - an L/I typo corrected; GREEN LAKE -> GREEN LAKES (2);
  FAIRBIRCH -> FAIR BIRCH (1).
- 4330 / 4350 Ebenezer Rd, Brampton: units 49-57 (plus one base row) moved 4330 -> 4350 and
  units 70-78 (plus one base row) moved 4350 -> 4330, same ids kept - the two numbers swapped
  between two groups of units.
- Splits: 12538 Kennedy Rd (Caledon) 20 units, base on file; 168 Queen St S (Mississauga) 15
  new units alongside units already on file; 25 William St (Brampton) units 1-12; 399 Healey
  Rd (Caledon, industrial) units 101-107, base retired the same day.
- Retired: 8 on Dixie Rd, Mississauga (2046-2101, beside Sherway Dr / Feldwood Rd / North
  Service Rd); 7 at 60 Dundas St E, Mississauga (base + units 1, 6, 6B, 9, 48, 52); 3 on
  Mona Rd (1148, 1154, 1274).
- Ward field blanked: 1,622 existing addresses lost their WARD value (brief's boundary count
  1,603 excludes the rows that also moved); Mississauga 1,314, Brampton 272, Caledon 36; 1,614
  residential. Most new addresses also carry no ward (2,512 of 2,707). File does not say why.
- STREETTYPE recodes: SWEETGUM PLACE->PL (31), CULLINGTREE PLACE->PL (25), SWEET MAPLE
  DRIVE->DR (25), all Caledon - abbreviation restyles.

## Outside record

- Jim Tovey: Mississauga Ward 1 councillor 2010-2018, died January 2018, credited with the
  Lakeview waterfront plan. https://globalnews.ca/news/3967468/mississauga-councillor-jim-tovey-dead/
  (high). Jim Tovey Lakeview Conservation Area opened 2026:
  https://www.mississauga.ca/city-of-mississauga-news/news/new-conservation-area-brings-new-life-to-mississaugas-waterfront (high).
  No source found naming "Jim Tovey Boulevard" or "Dockview Drive" or recording the naming
  decision - SILENT. Do not state the street is named for him.
- Lakeview Village:
  https://www.mississauga.ca/?p=123454 (fetched: "Developing parks in Lakeview Village", calls it "a 177-acre mixed-use development on the eastern edge of Mississauga's waterfront"; placing Dockview/Jim Tovey
  inside it rests on store cross-streets Hydro Rd / Rangeview Rd, not on a source naming them).
- Ninth Line lands: https://www.mississauga.ca/ninthline - "Shaping Ninth Line", City study completed 2018, vision for the Ninth Line Lands (fetched, high).
  Anatig Boulevard appears on City of Mississauga application drawings for Ninth Line sites,
  e.g. https://www.mississauga.ca/wp-content/uploads/2026/05/29115557/Site-Concept-Plan-1-OZ-26-6-W9-April-2026.pdf
  (medium - names the street; which plan the 89 addresses belong to is not confirmed).
  Aliza, Maliyah, Standing: SILENT.
- 60 Dundas St E, Mississauga: former Gold Star Plaza, reported demolished
  https://www.insauga.com/end-of-an-era-as-long-time-mississauga-plaza-is-demolished/ ;
  OLT approved redevelopment Jan 2025, three towers 16-29 storeys
  https://urbantoronto.ca/news/2025/03/multi-tower-proposal-recommended-approval-cooksville.58196
  (high on both). The retirement is consistent with it; the file does not say why.
- Dixie Rd 2046-2101: no application or news found - SILENT.
- Thornbird Cres: tenant listing describes a new freehold townhome in Caivan's Arbor West
  https://tenant.ca/listings/idx-W13747470--26-thornbird-crescent-brampton-on (medium; listings
  show the street lived in before the Region's file carried it). History Cir: SILENT.
- Speers Ave, Caledon: new-build listings, under construction, near McLaughlin / Mayfield /
  Tim Manley https://listo.ca/house-for-sale/caledon-real-estate/W13022420/152-speers-avenue-rural-caledon-caledon-on-L7C1Z9
  (medium). Hewson, Saint Rita, Damara: SILENT.
- Ward blanking: Mississauga election 2026-10-26 under the existing 11 wards
  (https://www.mississauga.ca/city-of-mississauga-news/news/mississauga-gets-ready-for-the-2026-municipal-election/);
  no source links the blanked ward field to any boundary change - SILENT. Do not connect it.
- Ebenezer swap, Planters Wood, splits, Mona Rd: not searched beyond the store / nothing found.
