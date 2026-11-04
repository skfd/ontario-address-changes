# Research notes - City of Cornwall, 2026-10

Window 2026-09-25 -> 2026-10-27. Snapshots kept 2, 6, 7, 15, 17, 24, 27 Oct. Net +12
(15 added, 3 removed), 2 unit splits, 4 location moves, 16 other edits. No open flags for
cornwall. 30 pull days, none failed. Research run 2026-11-04.

## Store facts the article leans on (verified with lookup.py / sqlite, 2026-11-04)

Lookup spans read "last seen", so a row ending 2026-10-17 left on the 24 Oct snapshot.

- **The 15 additions**: A-21 and A-23 Portland Dr; A-502 and A-504 Walton St; A, B, C-506
  Walton St; A-2703 Ross Av; A, B, C, D-205 Baldwin Av; A-11 Pine St; 189 Woodland Dr;
  1692 Woodward Ct. Thirteen are lettered units on numbers already on file; only the last
  two are new numbers.
- **Baldwin / Second corner, 24 Oct.** Before: 624 Second St E (AddressID 11714), 626 Second
  St E (11715), 207 Baldwin Av (11716), 205 Baldwin Av (11717), all POLY_ID 4858, postal
  K6H 4J3 on the Baldwin rows, on file since the 11 Jun baseline. After: 624, 626 and 207
  gone and stayed gone; 205 kept its AddressID, moved 5 m, and gained Units A-D (24400-24403),
  also POLY_ID 4858. FLOOR: A 1, B 2, C 2, D 1. A and B share one point, 2 m from where 624
  and 626 stood; C and D sit 1-3 m from where 205 and 207 stood. The file does not map old
  numbers to units. 622 Second St E next door is a separate polygon (4859) and stays.
- **502 / 504 Walton St, 15 Oct.** Both POLY_ID 3512. Each gained one Unit A, both FLOOR 2
  (24394, 24395). 502 itself gained FLOOR 1 and 504 moved 6 m. So four addresses on that
  polygon, the count the listing gives for 504.
- **506 Walton St, 15 Oct.** POLY_ID 3513. Units A, B, C (24396-24398) all on one point, no
  FLOOR. Base moved 2 m. Near 300 Belmont St (14 m) and 303 Carleton St (24 m).
- **21 / 23 Portland Dr.** AddressID 23765 was labelled 21, 23766 labelled 23 with ST_NUMBER
  **29**. 6 Oct: 23765 relabelled 23, 23766 relabelled 29, and A-23 / A-29 appear (24392,
  24393). So for one snapshot the file had no 21 and a second 29 beside the real 29 (18288).
  7 Oct: 23766 relabelled 21, and A-29 became A-21; 21 and 23 are back at their original
  spots with the record numbers swapped. Units are FLOOR -1. The only rows with two spans in
  the month are these four. The brief's gross `renumbered: 1` does not name its row (the
  JSON lists only net renumberings, none), so the article does not attribute it.
- **Portland Dr floors, 7 Oct**: A-27, A-49, A-51, A-55, A-57 (on file since baseline) went
  from no FLOOR to -1. These are the brief's five FLOOR edits. A-29 was left blank. 14 unit
  addresses on the street at month end. 15 and 17 Portland Dr are not on the file at 27 Oct.
- **2703 Ross Av, 17 Oct**: Unit A (24399), FLOOR -1, base moved 4 m. 25 m from 190 McKenzie St.
- **11 Pine St, 24 Oct**: Unit A (24404), no FLOOR.
- **189 Woodland Dr, 2 Oct**: new, postal K6H 0K1, 76 m from 210 Ruby Dr. 179 Woodland
  arrived 29 Jul.
- **1692 Woodward Ct, 27 Oct**: new, postal K6J 0B7. 1691 is the only other address on the
  court. 92 m from 1264 Wesburke Av.
- **North end, 24 Oct**: AddressIDs 24090-24097 (3141/3143 Ross, 3140/3142 Poirier, 3141/3143
  Duval, 3130/3132 Leger), on file since baseline with POLY_ID 0, got real POLY_IDs
  (19434-19440). 24097 was labelled 3132 DUVAL AV with STREET = LEGER; now 3132 LEGER AV,
  same point. These are the brief's 7 POLY_ID + 1 Full Address;POLY_ID edits, not new houses.
- Total on file 20,695 -> 20,707. Flat at 20,707 through the 4 Nov read.

## Web searches

| Entity | Found | URL | Confidence |
|---|---|---|---|
| 205 Baldwin Av | "FULLY--RENTED FOURPLEX in the heart of "Le Village"", "4 HYDRO METERS"; off market, sold $449,900, added "4 years ago", MLS 1312138. Structured field says Townhouse, contradicting the text | https://www.ovlix.com/property/2IEEaX-205-Baldwin-Avenue-Cornwall-ON | medium: aggregator, page read; old listing, undated |
| 205 Baldwin Av | later listing, $519,900, expired, also "fourplex" | https://realtris.ca/listings/X10371412/205-baldwin-avenue-cornwall-cornwall-on-k6h-4j3 | search snippet only, page 403s; not used |
| 207 Baldwin Av | nothing under this number | - | silent |
| 624 / 626 Second St E | nothing under these numbers; no listing ties them to 205 Baldwin | - | silent |
| Second St E demolitions | Seaway News column on downtown demolitions, undated, no addresses | https://cornwallseawaynews.com/local/cornwalls-evolving-downtown | not tied to this corner; not used |
| 504 Walton St | Property Type "Fourplex", 12 bed, 4 bath, 2-storey, status Sold; no mention of 502 or of unit numbering | https://property.ca/addresses/504-walton-st-cornwall | medium: page read |
| 504 Walton St | Multifamily, 12 bed, 4 bath; page last updated 2026-10-15, the file's change date. Treated as coincidence, not used | https://www.rew.ca/properties/504-walton-street-cornwall-on | page read |
| 504 Walton St | MLS X13017804, $700,000, four units of 3 bed / 1 bath | https://teamrealty.ca/listing/504-walton-street-cornwall-ontario-x13017804/ | snippet only, 403s; Royal LePage copy is gone; not used |
| 502 / 506 Walton St | nothing under these numbers (507-509 Walton is a separate triplex) | - | silent |
| 15 and 17 Portland Dr | Committee of Adjustment file A-27-26, notice 14 Aug 2026, hearing 26 Aug 2026; Lot 19, Plan 52M-58; semi-detached dwelling with an additional residential unit in the basement of each half. Outcome not found | https://www.cornwall.ca/en/news/posts/notice-of-public-hearing-committee-of-adjustment-city-of-cornwall-application-for-minor-variance-file-a-27-26/ | high for address and date (page read); the basement wording is from the search excerpt of the same page. Different lots from 21/23 |
| 74, 80 Portland Dr | listings describe semi-detached duplexes with lower units | https://realtris.ca/listings/X12310435/80-portland-drive-cornwall-cornwall-on-k6h-0j5 | snippet only; not used |
| 21 / 23 Portland Dr | one Zolo page with an inconsistent title; nothing on a lower unit | - | silent |
| 2703 Ross Av | semi-detached; listings disagree on bedrooms, price and postal code | https://wahi.com/ca/en/real-estate/on/stormont-dundas-and-glengarry/cornwall/eamers-corners/2703-ross-ave-cornwall-k6k1e6-ontario-canada | medium: snippet only; not used |
| 11 Pine St | nothing | - | silent |
| 189 Woodland Dr | nothing for 189; other Woodland numbers are listed, 151 as a house to be built | - | silent |
| 1692 Woodward Ct / Woodward Court | nothing; no public hit for the street at all | - | silent |
| 3130/3132 Leger, Duval, Poirier | nothing | - | silent |
| Cornwall additional-unit rules | Zoning By-law 127 has an additional-unit section; 2020 presentation says units need a building permit. Nothing on civic numbering | https://www.cornwall.ca/media/svaf2iih/cornwall-zbl-final-online-poh-2-presentation_may-2020_for-web.pdf | not used: does not explain any one address |
| "Cornwall HAF progress report", Cornwall planning hits | **wrong Cornwall** (Town of Cornwall, PEI; Cornwall, UK) | cornwallpe.ca, plota.co.uk | discarded |

"Eamers Corners" appears only in listing URLs, so the article places streets by the store's
neighbours instead. Nothing public says why any address changed in October; the listings
describe buildings, not the file's edits.
