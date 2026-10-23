# Research notes - City of Kingston, 2026-09

Window: 2026-08-28 -> 2026-09-29 (16 snapshots). Net +77 rows (77,506 -> 77,583).
Brief: 141 added / 64 removed / 260 significant mods by ADDRESS_ID.

## From the store (verified with lookup.py and direct queries on data/kingston/kingston.db)

- **Indian Rd -> Aki Rd.** 62 Indian Rd addresses (81-301) last seen 2026-09-03; 44 Aki Rd
  rows appeared 2026-09-04 and 18 more on 2026-09-05. Same 62 numbers, points within
  ~11 m of the old ones, but brand-new ADDRESS_IDs 109898-109959 (one consecutive run),
  so the brief counts 62 retirements + 62 additions and "Street renames: (none)". Aki Rd
  rows arrived with no POSTAL_CODE; postal codes filled in on 2026-09-17 (60 of 62 equal
  to the Indian Rd code). Confidence: high.
- **32 Indian Rd -> 345 McMahon Ave.** 32 Indian Rd (ID 11602) last on 2026-08-28; 345
  McMahon Ave (ID 109895) first on 2026-09-03 at the same point (~7 m apart:
  -76.52804,44.24958 vs -76.52813,44.2496). Nearest neighbours of 345 McMahon: 52
  Hampstead Heath 33 m, 1343 Princess St 55 m. Confidence: high on the file; the link to
  the staff recommendation below is a match of place, not a source statement.
- **Aki Rd location** (--near 81 Aki Rd): 36 Gretna Green 43 m, 29 Hampstead Heath 84 m,
  40 Strathcona Cres 90 m, 1373 Princess St 198 m.
- **1620 Bath Rd, 2026-09-25.** 120 records that all read plain "1620 BATH RD" (no unit)
  since the tracker began in June got unit numbers 101-112, 201-212 ... 901-912,
  1001-1012 (ten floors x 12). "1102 - 1620 BATH RD" (ID 90645) retired the same day.
  Base record 42844 lost its FULL_ADDRESS on 09-25 (restored 2026-10-02, next month).
  Same day the postal codes swapped: 1620 Bath Rd records K7M 0C1 -> K7M 0E5; all 121
  1610 Bath Rd records K7M 0E5 -> K7M 0C1. Accounts for 120 of the "Full Address;
  POSTAL_CODE; Unit" mods and 121 of the 122 postal-only mods. Confidence: high.
- **ID reuse, 2026-09-03.** IDs 109788-109799, which in August carried units at 1209
  Johnson St, 109 Morenz Cres, 596 MacDonnell St, 1037 Montreal St, 48 Gibson Ave (units
  existed from 2026-08-21), were rewritten to new unit addresses at 352 MacDonnell St,
  729 Selkirk Rd, 1184 Montreal St, 1261 Max Cres, 1312 Turnbull Way and 1369 Tremont Dr,
  and the August units were reissued under new IDs 109876-109894 (27 Baker St too). So
  the brief's "splits" at 1209 Johnson, 109 Morenz, 27 Baker, 596 MacDonnell, 1037
  Montreal are reissues, not new units. Also 109787 (unit 1 of 1209 Johnson in August)
  became 1377 Butternut Creek Rd on 2026-09-11. Confidence: high.
- **New units at existing houses.** By address string, 24 houses gained Unit 1 and Unit 2
  (e.g. 418 Knightsbridge Rd, 928 Hudson Dr, 54 Dauphin Ave, 441 Albert St on 09-08; 29
  and 31 Rideau St 09-10/11; 212 and 240 Mill Pond Pl 09-11; 310 University Ave 09-22;
  2818 Hwy 15 09-23), 729 Selkirk Rd and 60 Joseph St gained Units 1-3; 213 King St E
  added units 7-12 to its existing 1-6 (09-09); 322 Queen St added 7 and 8 (09-29).
  All bases remain.
- **Single new numbers:** 14B and 14C Red Patch Ave (09-04, beside 14 and 14A), 1008 Unity
  Rd (09-10), 1377 Butternut Creek Rd (09-11), 37 Lakewatch Lane (09-18).
- **778 Progress Ave.** Units 1-6 appeared 2026-09-08 (IDs 109968-109973); on 09-17 the
  unit labels were stripped and the base gained postal K7M 9E4, leaving seven identical
  "778 PROGRESS AVE" records on one point. Confidence: high on the file; the file does
  not say why.
- **1265 Unity Rd** moved ~100 m on 2026-09-08, same ID and number.
- Flags: `run.py flags` shows nothing open for kingston.

## From outside

- **Council vote.** City of Kingston news, 17 Jun 2026: Council voted at its 16 June
  meeting to rename Indian Road to Aki Road, "an Ojibwe word meaning earth/land/ground";
  Indian Road Park becomes Odamino Park ("to play"); next steps are sign changes and
  compensation for residents. No effective date given.
  https://www.cityofkingston.ca/news/posts/name-of-residential-road-in-kingston-deemed-to-be-outdated-and-derogatory-set-to-change/
  Confidence: high (primary source).
- **McMahon Avenue.** City project page, Project Update June 2026: staff also recommended
  renaming the southern portion of Indian Road, which connects to Princess Street, as
  McMahon Avenue. The page presents it as a recommendation; I found no source saying it
  was approved. https://getinvolved.cityofkingston.ca/renaming-of-indian-road/news_feed/project-update-june-2026
  Confidence: high that it was recommended; approval unconfirmed.
- **Vote count and history.** Kingstonist, 17 Jun 2026: eight to five; first brought to
  Council in 2017; June 2025 motion started the process.
  https://www.kingstonist.com/news/kingston-city-council-votes-in-favour-of-name-change-for-indian-road/
- **Cost/compensation.** YGK News, 19 Jun 2026: approx. 62 addresses; $250 per affected
  household; budget $46,250.
  https://ygknews.ca/2026/06/19/kingstons-indian-road-to-be-renamed-aki-road/
  Confidence: medium-high (local outlet; matches the store's 62).
- A search summary claimed completion "by the first quarter of 2027" (attributed to CFRC);
  the CFRC page 404'd and no other source carried it. Not used.
- **1610 Bath Rd** is "Westside Stories I - Affordable Housing", 1610 Bath Rd, K7M 0C1
  (South East Healthline). https://www.southeasthealthline.ca/displayService.aspx?id=74493
  After 09-25 the file gives 1610 that same code. Nothing found about 1620 Bath Rd
  (no listing, no development page). Silent.
- **213 King St E**: nothing found on what the six added units are. Silent.
- Not searched in depth: the 24 two-unit houses (no source per address; the file does not
  say whether these are secondary suites), 778 Progress Ave, Lakewatch Lane.
