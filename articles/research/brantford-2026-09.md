# Research notes — City of Brantford, 2026-09

Raw findings behind `articles/researched/brantford-2026-09.md`. Notes, not prose.
Window researched: net 2026-08-31 → 2026-09-18; three snapshots kept inside the month
(09-01, 09-05, 09-18); 30 pull days, 0 failed. Research done 2026-10-22.

Conventions: **FACT** = the linked page says it (fetched directly). **INFERENCE** = a
reading, not the source's. **SNIPPET** = seen only in a search-engine summary; the page
itself could not be fetched — do not print. **EMPTY** = searched, nothing found.

Source caveat: brantford publishes no stable row id (OBJECTID and OBJECTID_1 are both
sequential), so `datasets/brantford.toml` synthesizes the identity key from number +
street + unit + rounded lon/lat. The tracker's `full` column is the source's FULLADDRESS
string, `number` is STREETNUM. No unit column; units are embedded in STREETNUM as
"<unit>-<number>" and split out by `unit_from_number`. None of September's rows has a
unit. The layer has 9 fields and no domains; the item description is one line ("City of
Brantford Site Addresses"), so there is no published statement of what a point represents.

---

## 0. Store-side findings (this repo, not the web)

Net, 08-31 → 09-18: rows 38,986 → 38,999 (+13); added 13, removed 0, nothing else.
Gross equals net. No splits, renames, renumberings, status, boundary or place events.
First Brantford article; no earlier month to compare except by brief: August was +5 net
on 191 in / 186 out (a churn month, 162 of each on 08-12); July −2.

Snapshots kept (store `snapshots`, non-skipped): id 43 2026-09-01 (38,987 rows),
id 45 2026-09-05 (38,998), id 46 2026-09-18 (38,999). Skipped reads 09-04, 09-23, 09-24,
09-26, 09-27, 09-30 (content unchanged). Previous kept snapshot 2026-08-31 (38,986).

Day by day:
- 09-01: +1 — 209 CAMPBELL ST (N3S 5B5).
- 09-05: +11 — 137, 139, 141 GILLESPIE DR (N3T0K3); 24, 27, 28, 29, 31 TURNBULL DR and a
  row labelled 36 TURNBULL DR (N3T0K4); 6, 8 WILMOT RD (N3T0K8).
- 09-18: +1 — 486 KING GEORGE RD (N3T 5L8).

**West Brant cluster (11 rows, 09-05).** All within 165 m of each other (max pairwise
span). `--near 24 TURNBULL DR`: 143 Gillespie Dr 82 m, 24 Cheevers Rd 99 m, 2 Wilmot Rd
121 m, 17 Cahill Dr 141 m, 142 Holder Dr 182 m, 393 Blackburn Dr 207 m. Street state
before and after (all pre-existing rows on file since the first read, 2026-06-11):
- TURNBULL DR before: evens 2–22, 34, 36, 38, 40; odds 7–25, 33, 35. New: 24, 28 (even),
  27, 29, 31 (odd), plus the row labelled 36 (see below). 26, 30, 32 still absent as
  labels.
- GILLESPIE DR before: …133, 135, 143, 145…; new 137, 139, 141.
- WILMOT RD before: 1, 2, 3, 4, 5, 7, 9, 10…; new 6, 8.
- All new numbers sit inside existing number runs — a fact about the sequence, not
  about lots or construction.

**The row labelled 36 TURNBULL DR (09-05).** Source props: FULLADDRESS "36 TURNBULL DR",
STREETNUM "26", STREETNUMIN 26, POSTALCODE "N3T0K4"; coords 43.10808, −80.30259. The
pre-existing 36 TURNBULL DR (since 06-11): STREETNUM "36", STREETNUMIN 36, POSTALCODE
"N3T 0K4"; coords 43.1073, −80.30279. Distance between the two points: 88.2 m. The new
point is 13 m from 24 and 15 m from 28 Turnbull (and 26 m from 22); the old 36 is 8 m
from 34 and 8 m from 38. Both rows are active. The tracker keys on number+street+unit+
position, so they are two records; the site's daily report and the brief show the new
one as "36 TURNBULL DR" because the tracker displays FULLADDRESS. The file does not say
which field is right. Active duplicate FULLADDRESS strings in the whole file: 2 (this
one and 890 COLBORNE ST, pre-existing, not September's).

**Postal-code spacing.** The 11 West Brant rows carry POSTALCODE with no space
("N3T0K4"); the file's convention is "N3T 0K4". Active rows with a space-less postal
code: 22 of 38,999 (11 from before September; 1,035 active rows have a blank postal
code). August's 191 additions: 0 without a space. 209 Campbell and 486 King George carry
the space. Observation only; the file does not say how the rows were entered.

**209 CAMPBELL ST (09-01).** Odd side; 201 Campbell 27 m, 199 40 m, 195 63 m, 200 Elgin
St 79 m. Odd numbers on file 191–201 then 209; 203, 205, 207 absent; no even number
between 190 and 230 on file. `--near`: 200 Elgin St 79 m, 103 Maitland St 135 m,
365 Rawdon St 152 m, 224 Bruce St 175 m.

**486 KING GEORGE RD (09-18).** Even side between 466 and 504. Same-road distances:
493 (odd side) 90 m, 483 98 m, 481 148 m, 504 155 m, 477 183 m, 466 313 m, 506 313 m,
460 416 m. Nearest active address on any other street *in the City's file*: 441A
Powerline Rd 891 m, then 396 Governor's Rd E 980 m. (`lookup.py --near` prints nothing
for it — beyond its radius.) The parcel is near the City's northern boundary; County of
Brant addresses are not in this file, so "nearest" is scoped to the City's file.

**Flags.** No open or reviewed flag for brantford. Nothing held inside September.

---

## 1. Turnbull Drive, Gillespie Drive, Wilmot Road — council record

- **FACT** — City Council minutes, 24 August 2021 (video-conference meeting, Mayor Davis
  presiding; 41-page PDF served by the City's meeting calendar). Item 12.2.8 "Road
  Dedication By-law, Gillespie Drive, Turnbull Drive and Wilmot Road [Financial Impact –
  none], 2021-398": "That Report 2021-398 … BE RECEIVED" and that by-laws be presented
  "to declare and dedicate Block 102, Registered Plan 2M-1928, City of Brantford, as part
  of the Public Highway, to be known as Gillespie Drive"; "Block 101 … Turnbull Drive";
  "Block 103 … Wilmot Road". Section 15 BY-LAWS lists them as 156-2021 (Gillespie),
  157-2021 (Turnbull), 158-2021 (Wilmot), each "(2021-398) (Committee of the Whole –
  Operations and Administration Report #2021-08-03)". Motion "THAT By-law 154-2021
  through to and including By-law 172-2021 … BE TAKEN as read a third time, be finally
  passed and signed by the Mayor and Clerk" — recorded vote of 3rd reading of all by-laws
  not separated: YES (10), CARRIED (10 to 0).
  https://calendar.brantford.ca/meetings/Detail/2021-08-24-1800-City-Council/846a87e6-a893-4cfb-adac-ae7601255889
  (fetched with curl + browser UA; the URL returns the minutes PDF; WebFetch got 403.)
- **FACT, same minutes** — item 12.3.11 "Extension to a Draft Approved Plan of
  Subdivision 29T-17505 – 599 Shellard Lane (Empire Wyndfield West Phase 8)", 2021-489,
  request by Armstrong Planning on behalf of Empire Communities Ltd. to extend the
  draft-plan expiry, approved. **Nothing fetched says Plan 2M-1928 is Phase 8** — same
  meeting, separate item. Do not bridge them in the article.
- **EMPTY** — the staff report 2021-398 itself (eScribe `filestream.ashx?DocumentId=…`)
  is behind eScribe's "Verifying your browser" wall (403/JS challenge to both WebFetch
  and curl). Why the streets carry these names is not in the minutes and was not found
  elsewhere. Search for Brantford street naming honours found Rudd and Leary streets
  (Wyndfield West Phase 8B, Afghanistan casualties, signs unveiled 24 May 2024) — not
  these three. https://www.brantford.ca/news/posts/city-of-brantford-honours-fallen-soldiers-with-street-naming-and-vmp-rededication-ceremony/
- **SNIPPET, do not print** — Empire Communities "Wyndfield Fall Update 2023"
  (empirecommunities.com/blog/wyndfield-fall-construction-update-2023/): "Phase 8A1 is
  almost complete, with 90% of homes on Gillespie Dr."; Phase 8A2 homes on Bellhouse
  Ave., Piley Rd., blocks on "Baskett St., Wilmont Rd., and Monteith Drive". Live URL
  404; web.archive.org not reachable from here. Every "Phase 8A" claim traces only to
  this snippet.
- **FACT, context only (not printed)** — ConstructConnect certificate of substantial
  performance F9-78690: "Wyndfield Phase 8B-1", owner Empire Communities Inc.,
  contractor Terracon Underground Limited, substantial performance 18 July 2023, signed
  12 February 2024; premises "bounded by Wyndfield West Phase 8A to the west".
  https://canada.constructconnect.com/dcn/certificates-and-notices/8B483A57-C8DB-491C-9FA8-4AC66CF76AE6

## 2. 8 Wilmot Road — rental listing

- **FACT** — REW rental listing, MLS X13716494, $3,200/month, house (detached), 5
  bedrooms in the details and "4 bedroom" in the text. Description: "Stunning 4 bedroom
  detached home by Empire Communities on a premium 42' lot backing onto greenspace",
  "approximately 3,100 sq. ft. of living space with over $30,000 in premium upgrades".
  Page shows "Days on REW: 49 Days" and "Updated 27 days ago" as read on 2026-10-22; no
  listing date is printed. **Do not subtract** — print the page's wording.
  https://www.rew.ca/rentals/7499484/8-wilmot-road-brantford-on
- Other copies of the same listing (point2homes, meadowtownerealty, zolo) returned 403;
  search summaries add "0 to 5 years old" (Zolo) — SNIPPET, not printed.
- **EMPTY** — no listing, permit or planning item found for 6 Wilmot Rd, 137/139/141
  Gillespie Dr, or 24/27/28/29/31 Turnbull Dr. Searches for "36 Turnbull Drive" return
  only 2, 8, 14 and 40 Turnbull (resales/rentals; 14 Turnbull "built in 2016" per a
  listing — SNIPPET).

## 3. 486 King George Road

- **FACT** — Squareyards listing page (URL says "brantford-twp" and "king-george-road-e"):
  MLS X12458189, $199,000, status shown as Sold; "about 4 acres", roughly 180 ft frontage
  by 900 ft depth; "designated Core Natural and zoned 'N - Core Natural'"; "Residential
  development is not permitted under the current zoning"; marketed as a recreational
  retreat or land investment; "not a residential building lot"; "Last Updated: 01 Sep,
  2026". Listing courtesy Royal LePage Real Estate Associates.
  https://www.squareyards.ca/sale/on/brant/brantford-twp/486-king-george-road-e
- **Conflict (notes only)** — a search summary of another copy says "Status: For Sale",
  "Price drop by $51,000", "Listed 9 days ago"; the keyhomes page
  (keyhomes.ca/property/ontario/brant/28980698, title "486 King George Road, Brant,
  Ontario N3T 5L8" — postal code matches the file) returns HTTP 410 Gone. Print only the
  fetched squareyards wording; do not state when it sold or whether it sold.
- **EMPTY** — no consent, variance, site plan or permit for 486 King George Rd in
  Brantford Committee of Adjustment results (2026 schedule found; April 8, 2026 agenda
  items are Wood St and billboard signs). https://www.buildbrantford.ca/planning-and-development-services/committee-of-adjustment/
- **FACT, not printed** — the 2017 Brant→Brantford boundary transfer (c. 2,454–2,700 ha,
  effective 1 Jan 2017, northern boundary extended to Governors Road) exists in press
  coverage, but nothing fetched ties King George Rd 486 to it. Left out of the article.
  https://kitchener.ctvnews.ca/boundary-deal-brant-county-ceding-2-454-hectares-to-brantford-1.2725969

## 4. 209 Campbell Street

- **EMPTY** — nothing for 209 Campbell Street, Brantford: no listing, no permit, no
  Committee of Adjustment item. Search results are all 301 Campbell St (rental) or other
  streets. The record is silent.

## 5. City of Brantford permit and addressing records

- **EMPTY** — the City's monthly "Report on Construction Activity" PDFs on brantford.ca
  stop at 2021 in search results (e.g. BuildingReport-MAR2021.pdf); the old
  Brantford.ca/BuildingReports shortcut now lands on a general building-and-construction
  page with no reports. No 2026 permit list to check September's addresses against.
  https://www.brantford.ca/business-and-development/building-and-construction/
  (2026 "summary reports" that do turn up are the County of Brant's, on brant.ca — wrong
  municipality for these addresses.)
- **EMPTY** — no City of Brantford civic-addressing by-law or policy found. The County of
  Brant's By-law 141-23 is the County's, not the City's; not used.

## 6. Licence and layer

- **FACT** — City of Brantford Open Data Licence page: "This is version 1.0 of the Open
  Government Licence – Brantford"; attribution wording "Contains information licensed
  under the Open Government Licence – Brantford." Matches the brief's attribution line.
  https://www.brantford.ca/your-government/open-data/open-data-licence/
- **FACT** — ArcGIS item 8fa270cb0c174bd99b52a11260f60f15: title "City of Brantford
  Site Addresses 2", description "City of Brantford Site Addresses", licenseInfo "See
  Licence", owner CoBOpenData, created 2018-11-29, modified 2026-09-14. Layer
  OP_Site_Addresses2/0: 9 fields (OBJECTID, OBJECTID_1, FULLADDRESS, STREETNUM,
  STNUMSUFF, STREETNAME, STREETTYPE, POSTALCODE, STREETNUMIN), no domains, empty
  copyright. https://services.arcgis.com/aji2lCmjXt0KpGzI/arcgis/rest/services/OP_Site_Addresses2/FeatureServer/0?f=pjson

## Not researched

Why Turnbull, Gillespie and Wilmot carry those names (the staff report is behind the
eScribe wall); 890 Colborne St duplicate (pre-existing, not September's); the 11
pre-September rows without a postal-code space.
