# Research notes — County of Lambton, 2026-10

Raw findings behind `articles/researched/lambton-2026-10.md`. Notes, not prose.
Window: net measured 2026-09-30 → 2026-10-29 (store snapshots 22 → 50). Seven snapshots
kept inside the month: 10-01, 10-02, 10-09, 10-15, 10-23, 10-28, 10-29 (ids 23, 24, 31,
37, 45, 49, 50). Vault: 30 pull days, 0 failed. No lambton flag open or held in the month
(`run.py flags`: 16 open, none lambton). Research done 2026-11-06.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **SNIPPET** = seen only in a search-engine summary; the page itself could not
be fetched — do not print. **EMPTY** = searched, nothing found. **STORE** = this repo's
`data/lambton/lambton.db` (or `data/sarnia/sarnia.db` where named), not the web.

---

## 0. Store-side findings

### Brief vs what happened

- Brief: net +37 / −6, gross the same (no churn), rows 56,984 → 57,015 (+31). No splits,
  renames, renumberings, status or boundary events. Nothing held.
- The identity key is synthesized and the point's position counts (a ~1 m shift re-keys
  7429 Mud Creek), so a moved point lands as one out, one in.
- STORE, pairing the six "retired" keys against the additions:

| Out | In | Move | pointtype | Snapshot |
|---|---|---|---|---|
| 34 Alberta St | 34 Alberta St | 30 m | Unknown → Driveway Entrance | 10-02 |
| 10026 McCordic Ln | same | 32 m | Unknown → Driveway Entrance | 10-15 |
| 10030 McCordic Ln | same | 48 m | Unknown → Driveway Entrance | 10-15 |
| 10038 McCordic Ln | same | 71 m | Unknown → Driveway Entrance | 10-15 |
| 7429 Mud Creek Tr | same | ~1 m | Unknown → Unknown | 10-15 |
| 7433 Mud Creek Tr | *none with that number* | — | — | 10-15 |

- So 37 − 5 = **32 new**, 6 − 5 = **1 retired**, net +31, which matches the rows line.
- 7433 Mud Creek Trail / 10034 McCordic Lane: 10034 has one row ever (snapshot 37), in the
  gap between 10030 and 10038. It sits 55 m from 7433's last point and carries the
  2026-02-17 approved/active stamp of the older rows around it, not an October one.
  INFERENCE: the same point re-addressed from Mud Creek to McCordic. The file has no field
  linking them. Printed as a stated possibility; counted as 1 new + 1 retired.
- `approveddate`: all 31 other new rows carry a date of the day before or the morning of
  the snapshot that first shows them (09-30 → 10-01; 10-02 → 10-02; 10-08 → 10-09;
  10-14 → 10-15; 10-22 → 10-23; 10-27 → 10-28; 10-29 → 10-29). The moved rows keep
  2026-02-17. September's caution stands: the field is not the date an address was first
  given. Scope any claim to this month's new numbers.

### The 32 new

- 10-01 (23): **Boswell St, Township of St. Clair — 15**: 2465, 2467, 2469, 2471, 2472–2479,
  2481, 2483, 2485. **Melwood Dr, Township of St. Clair — 7**: 1571–1576, 1578. All approved
  2026-09-30 within about 15 minutes, pointtype Driveway Entrance. 86 Main St W, Lambton
  Shores (approved 09-30).
  - Boswell on file before: 57 numbers at snapshot 1, up to 2464 and 2468. Melwood: 15
    numbers at snapshot 1, 1549–1570.
  - `--near`: 2465 Boswell → 2472 Courtright Line 53 m, 2455 Jane St 101 m, 1570 Traxler Ct
    108 m. 1578 Melwood → 2485 Boswell 21 m, 2494 Courtright Line 60 m. One contiguous
    block: the Boswell run ends where the Melwood run ends.
- 10-02: 32 Alberta St, Lambton Shores (approved 10-02), about 10 m from 34's new point.
- 10-09: 1708 and 1709 Bickford Line, St. Clair (approved 10-08). Point pair, about 27 m
  apart. `--near` finds no other street close by.
- 10-15: 10296 Grand Oaks Dr, Lambton Shores (approved 10-14), 56 m from 10157 Sumac Ct;
  10034 McCordic Ln (above).
- 10-23: 3172 Churchill Line, Plympton-Wyoming (approved 10-22).
- 10-28: 7024 Wisbeach Rd, Warwick (approved 10-27), 219 m from 8746 Birnam Line.
- 10-29: 220 and 373 George St, City of Sarnia (approved 10-29).

### George Street against the City's own file

- STORE (`sarnia.db`): the City of Sarnia dataset has carried 220 George St and 373 George
  St since its first snapshot (11 June 2026). City and county points: 373 within a few
  metres, 220 about 36 m apart. Sarnia's file has not changed since 20 August.
- STORE: neither number was ever in the county file before 10-29.
- So the two numbers are new to the county layer, not new to Sarnia. 353 George is in the
  City's file (from 08-20) and still not in the county's; not an October event, left out.

---

## 1. Boswell Street and Melwood Drive, Brigden

- FACT: Zoocasa, 1552 Melwood Dr: "This newly built 3-bedroom, 3-bathroom home is nestled
  on a quiet dead-end street in the heart of Brigden". Listed June 2025 (cancelled), then
  expired January 2026. No builder or subdivision named. 1552 was on file from snapshot 1.
  <https://www.zoocasa.com/saint-clair-on-real-estate/1552-melwood-dr>
- EMPTY: builder, subdivision name, plan number, lot count for Boswell or Melwood, across
  general search and `stclairtownship.ca`.
- EMPTY: St. Clair council highlights for 15 June and 10 Aug 2026 mention no Brigden or
  subdivision item.
  <https://www.stclairtownship.ca/council-highlights-june-15-2026/>
  <https://www.stclairtownship.ca/council-highlights-aug-10-2026/>
- FACT, NOT PRINTED: 5 Oct 2026 highlights: "Approved a one-year extension to the Draft
  Plan Approval for the Beckwith Developments Inc. Subdivision." No location given, and a
  draft plan still being extended is not an obvious match for lots already numbered.
  Nothing ties it to Brigden.
  <https://www.stclairtownship.ca/council-highlights-regular-meeting-october-5-2026/>
- 2431 Boswell St listings show an older house in Brigden; not relevant.
- Michigan's St. Clair Township dominates the results; all discarded.

## 2. 220 George Street, Sarnia

- FACT: Sarnia News Today, 20 Jan 2026: "Former Central United Church, located at 220
  George St." Council received and filed the heritage designation request, so no
  designation proceeds. Property to be sold by Xoana Corporation Inc. (Anthony Mota) to
  Heikal Group Inc. (Mostafa Heikal, Angels Childcare); proposal: part of the building
  "adaptively reused for daycare purposes" with "residential intensification on the
  remainder of the property". Sale "expected to close in March". Whether it closed: not
  stated.
  <https://sarnianewstoday.ca/sarnia/news/2026/01/20/denied-heritage-request-paves-way-for-new-ownershipof-former-central-united-church>
- SNIPPET: 2021 approval for 15 residential units under Xoana (search summary of
  <https://sarnianewstoday.ca/sarnia/news/2021/07/13/apartments-planned-former-church>).
  Not fetched, not printed.
- EMPTY: any 2026 rezoning or site-plan item for 220 George; any confirmation of the sale.
- Nothing links the county's new point to the church plans. The article puts them side by
  side and says so.

## 3. 373 George Street, Sarnia

- EMPTY: exact-address search returned other George St numbers only.
- Indwell's supportive housing proposal is 353 George St, not 373: refused by the Committee
  of Adjustment 10 Feb 2026, under appeal at the OLT, merit hearing set for 22 Sept
  (outcome not found). No page mentions 373. Left out.
  <https://sarnianewstoday.ca/sarnia/news/2026/05/21/indwell-supporters-await-update-on-proposed-george-street-development>
  <https://www.windsornewstoday.ca/sarnia/news/2026/04/24/city-council-to-debate-next-move-in-indwells-olt-appeal>

## 4. 10296 Grand Oaks Drive, Lambton Shores

- FACT: HouseIndex, MLS X12996956: vacant land, listed 2026-04-14, status Sold at $429,000
  (no sale date given), 130.9 × 160 ft, cross street Grand Oaks Drive and Sumac Court;
  description says Southcott Pines, Grand Bend.
  <https://houseindex.ca/mls/listing/lambton-shores/10296-grand-oaks-drive/X12996956>
- REW confirms Land/Lot. <https://www.rew.ca/properties/10296-grand-oaks-drive-lambton-shores-on>
- Only 206 days on market is shown, so the sale may have come late; do not say "sold in
  spring". Print "listed in April".

## 5. 32 and 34 Alberta Street, Lambton Shores

- SNIPPET: search summaries say 34 is a custom build by Cloverwood Homes (CA$1,124,900)
  and 32 sold 2025-12-15 at $1,099,000, R1, with another listing at $1,149,900. All of
  evrealestate (429), sothebysrealty (404), pine.ca (403), terrystevens (404) and houseful
  (banner only) failed. Do not print.
- EMPTY: any severance or planning item for either number.

## 6. McCordic Lane and Mud Creek Trail, Lambton Shores

- EMPTY: nothing on a civic-number change or on McCordic Lane at all. "Mud Creek Trail"
  hits are Saskatchewan and elsewhere, none in Lambton Shores.
- Locality not printed: Port Franks is a guess from coordinates. `--near` 10034: 9970
  Edward St 168 m, 7441 Sanderson Rd 212 m, 7340 Outer Dr 226 m.

## 7. The rest

- 86 Main St W, Lambton Shores: EMPTY. 37 m from 15 Lakeside Circle. Grand Bend bridge
  closure notice for Main St W exists but says nothing about this number; left out.
- 1708/1709 Bickford Line: EMPTY.
- 3172 Churchill Line, 7024 Wisbeach Rd: single rural numbers, store only.
