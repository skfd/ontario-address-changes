# Research notes - City of Kingston, 2026-10

Window: 2026-09-29 -> 2026-10-30 (16 snapshots). Net +122 rows (77,583 -> 77,705).
Brief: 134 added / 12 removed / 3 significant / 1 location, by ADDRESS_ID. Gross significant 13.
30 pull days, 0 failed. Flags: `run.py flags` shows nothing open for kingston; nothing HELD.

## From the store (verified with lookup.py and direct queries on data/kingston/kingston.db)

- **1239 Centennial Dr, 2026-10-03.** All 87 of the day's additions. Units 101-107, 201-215,
  301-315, 401-415, 501-515, 601-615 (82) plus LL1-1 to LL1-5 (5). The plain 1239 (ID 107370,
  K7P 0E9) on file since the tracker began. Unit IDs 109018-109107, three gaps (109067,
  109098, 109100). The first snapshot (06-11) already held IDs up to 109531, including
  neighbours of this run, so these numbers are older than records that were public in June;
  the units reached the public layer only on 10-03. The unit records carry no postal code.
  Confidence: high.
- **1245 Centennial Dr.** Base ID 107369, the number right before 1239's. K7P 0E9. 82 units on
  file since 06-11 (IDs 107723-107805 range), same pattern as 1239: 101-107, then 15 a floor
  on floors 2-6. No LL units. The two sit about 64 m apart (1239 at -76.56018,44.26967; 1245
  at -76.55951,44.26997). 1 - 497 Cataraqui Woods Dr is 64 m from 101 - 1239.
- **163 Brock St -> 3 Montreal St.** Units 1, 2, 3 of 163 Brock (IDs 53825-53827) last on
  10-08. On 10-09 3 Montreal St and Units 1-4 appear (IDs 110030-110034), 8-10 m from where
  the units stood; the plain 163 Brock stays (ID 17229) and its point moves about 6 m the same
  day. No 3 Montreal St before this. 10-10: base gains K7L 3G7, and Units 1-4 lose their unit
  labels, so five identical "3 MONTREAL ST" records; 10-17: labels restored. That is 9 of the
  10 edits between net 3 and gross 13 (10-10: 5, 10-17: 4); the tenth is 429 Victoria's postal
  code on 10-15. Confidence: high on the file. That the apartments were re-addressed is a
  match of place and count, not a source statement.
- **291 and 295 Ontario St.** 291 (ID 108948, no postal code) last on 10-01. On 10-02, 295 (ID
  13207, K7K 2X7) moves 162 m, from -76.47840,44.23270 to -76.47645,44.23229, about 3 m from
  291's old point. Nearest other addresses: 1 Queen St 167 m, 2 Princess St 223 m. 282 and 285
  Ontario remain. Confidence: high.
- **1173 and 1177 Montreal St.** IDs 19368, 19367 (adjacent), 17 m apart, last on 10-21, gone
  on 10-23, not back through 11-06. Nothing new on the spot. 1168 and 1179 remain. Only 1177
  had a postal code. The only two retirements with nothing beside them.
- **Victoria St 427/429, 10-14 (last seen 10-10).** Units 3, 4 of 427 and Unit 2 of 429 out;
  Units 1, 2 of 427 and plain 429 in, on the same points. Plain 427 kept. Relabel, not loss.
- **443 Johnson St, 10-14.** Unit B out, Units 1 and 2 in, same point.
- **2818 Hwy 15.** Units 1, 2 arrived 09-23 (in September's article), last on 09-29, gone 10-01.
  Plain 2818 remains. Eight days on file.
- So of 12 retirements: 3 Brock (moved round the corner), 3 Victoria + 1 Johnson (relabels),
  1 Ontario (295 on its point), 2 Hwy 15 (September's units undone), 2 Montreal (actually gone).
- **Units 1 and 2.** Twelve houses gained both with no earlier unit: 131 Johnson, 96 Regent,
  1394 Thornwood (10-02); 90 Byron, 9 Cataraqui (10-14); 35 Holland, 514 Division, 61 Yonge
  (10-19); 63 Livingston (10-24); 798 Arundel, 2228 Swanfield (10-28); 353 Frontenac (10-30).
  All bases remain. 427 Victoria and 443 Johnson also show as Units 1 and 2 but replace older
  labels. 19 "splits" in the brief = these 14 + 1239 Centennial, 80 Queen, 3 Montreal,
  676 King W, 21 Grange.
- **676 King St W, 10-08.** Units 1-4, IDs 110026-110029; plain 676 remains.
- **21 Grange St, 10-14.** Units 1-3; about 45 m from 676 King W by the file's points.
- **80 Queen St, 10-21.** Units 101-104, 201 (IDs 110054-110058). Plain 80 and Unit 301 on file
  since June. Unit 202 arrives 11-06, November's file. 25 m from 212 Wellington St.
- **1375 Monarch Dr, 10-30.** K7P 0S2, the only brand-new single number that isn't a
  re-address. Near Swallowdale Crt, Davenport Cres, Holden St.
- **Other edits.** 1620 Bath Rd's main record got its full-address text back 10-02 (lost 09-25).
  "131 - 129 Charles St" lost its unit field 10-05. 2 King St W: direction field WEST -> W 10-14.
- Additions: 87 + 47 elsewhere, none on a new street. Busiest day 10-03.

## From outside

- **The Grove, site.** CityFlats: 1245 Centennial Dr, "at the intersection of Centennial Drive
  and Cataraqui Woods Drive", 5.4 acres, "recently rezoned to accommodate five residential
  apartment buildings totaling 597 units". First building under construction, completion Q1
  2027; "Planning for the second building is well advanced, with construction expected to
  commence in Q3 2026." 1239 not mentioned. Undated, (c) 2026.
  https://cityflats.ca/assets/the-grove/ Confidence: high (owner's page, read in full).
- **The Grove, phases.** insauga, 19 Jan 2026: five-phase, 410 rental apartments; first building
  The Cedar, occupancy February 2027. Second building not named.
  https://www.insauga.com/new-rental-community-in-kingston-ontario-selects-property-management-firm/
  Confidence: high that it says so. 410 conflicts with CityFlats' 597; neither explained.
- **Pre-leasing.** projectnewhome: pre-leasing for 1 March 2027, 1245 Centennial Dr, K7P 0E9.
  https://www.projectnewhome.com/projects/the-grove-kingston-6576
- **82 units.** ForRent lists The Grove at 82 units, 6 storeys, built 2026.
  https://www.forrent.com/on/kingston/the-grove/r6f99w0 Confidence: medium, seen in search results
  only, page 403s automated fetches; other listing sites give 27 and 597. Matches 1245's 82 on file.
- **1239 Centennial Dr:** no source names it anywhere. Silent. That it is The Grove's second
  building is an inference from the IDs, postal code, spacing and floor pattern; say so.
- **163 Brock St.** Wahi copy of the 2025 MLS listing (X12088627): "MEDICAL CLINIC AND FOUR
  RESIDENTIAL APARTMENTS OPPOSITE HOTEL DIEU HOSPITAL", 1,900 sq ft medical office; "The Seller
  will lease-back until June 30, 2026."
  https://wahi.com/ca/en/real-estate/on/frontenac/kingston/sydenham/163-brock-st-kingston-k7l1s2-ontario
  Confidence: high that the listing says it (read directly). LoopNet dates it on market
  2025-04-22 (403 to fetches). Sale outcome not found. Nothing on why a Montreal St address.
- **676 King St W.** Dec 2025 listing, street-level commercial with "two well-proportioned,
  self-contained apartments" in a residential building behind.
  https://property.ca/addresses/676-king-street-w-kingston Confidence: high that it says so
  (read directly). Listings differ on price and size; not used. Nothing explains four units.
- **Unit numbers.** City ARU page: "We will assign a new unit number to assist emergency services,
  home delivery, and mail services according to the building permitting and zoning review
  process, to recognize your additional residential unit". No cap given on the page.
  https://cityofkingston.ca/building-and-renovating/building-permits/additional-residential-units-arus
  Confidence: high. The file does not mark any of the twelve houses as having an ARU.
- **80 Queen St.** Broker's sublease brochure for Suite 300, about 7,499 sq ft, K7K 6W7.
  https://images.loopnet.fr/d2/TpxCQ7MMbKm1zWnOFU5HDxNtcc1M3uv09Y8yylXPeyg/80%20Queen%20St%20Suite%20300%20Sublease%20Brochure.pdf
  Confidence: medium, seen in search results only, PDF 403s fetches. Nothing on 101-104 or 201.
- **Searched, silent:** 291/295 Ontario St (nothing names either); 1173/1177 Montreal St
  (Kingstonist's Montreal St corridor zoning piece and the John Counter intersection project
  mention neither; not used); 3 Montreal St; 427/429 Victoria St; 2818 Hwy 15.
- Not searched in depth: 21 Grange St, 1375 Monarch Dr, the twelve houses one by one.
- Also unusable: 1400 Bath Rd listings (a separate site with an easement to Centennial Dr).
