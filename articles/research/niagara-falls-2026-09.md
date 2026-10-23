# Research notes — Niagara Region (slug niagara-falls), 2026-09

Raw findings behind `articles/researched/niagara-falls-2026-09.md`. Notes, not prose.
Window: net 2026-08-12 → 2026-09-03; one snapshot kept inside the month (09-03); 30 pull
days, 0 failed. August was also read all 30 days with 0 failed and no snapshot kept after
08-12, so the 09-03 changes landed between the 2 and 3 September reads. Research done
2026-10-23.

Conventions: **FACT** = the linked page says it (fetched directly). **INFERENCE** = a
reading, not the source's. **EMPTY** = searched, nothing found.

Source caveat: the layer is the Region's, region-wide (Niagara Falls, Fort Erie, Port
Colborne, Welland, Pelham, St. Catharines, West Lincoln...), despite the slug. Identity is
GSmartID, so a re-addressed point is seen as one record changing. No `full` field, so
`lookup.py --near` does not work; placement is by the `Municipality` property only.
`location_min_move_m = 25`.

Flag queue: `python run.py flags` on 2026-10-23 shows 4 open flags (guelph, simcoe), none
for niagara-falls. Brief has no HELD section.

---

## 0. Store-side findings

Net 08-12 → 09-03: rows 208,004 → 208,079 (+75); added 75, retired 0, renumbered 1,
significant 20, split_events 21. Gross identical (one snapshot). First article for this
dataset. August brief: +46 (07-03 → 08-12).

Additions by Municipality: Niagara Falls 44, Fort Erie 20, Port Colborne 7, Welland 1,
Pelham 1, St. Catharines 1, West Lincoln 1. GSmartIDs 11542525–11542599, one unbroken run.

**3411 Whispering Woods Trail → 3–22 Butternut Crescent, Fort Erie.** GSmartIDs
11531047–11531066 (consecutive). Before: Full_StreetNo 3411, StreetName Whispering Woods,
StreetType Trail, Unit 3…22. After (09-03): Full_StreetNo 3…22, StreetName Butternut,
StreetType Crescent, no Unit. Coordinates unchanged to 5 dp (e.g. 11531047 at
-79.04706, 42.87679 before and after). Plain 3411 Whispering Woods Trail (11519641) still
active. No 1 or 2 Butternut on file. Butternut Crescent's first appearance in Fort Erie's
part of the file; other Butternuts pre-exist (Butternut Court, Lincoln, 11 rows; Butternut
Boulevard, Niagara Falls, 74 rows), which is why the brief lists no new street. These are
the brief's "20 Address Number; Street; StreetType; Unit" modifications. Still as-is on
the 10-01 read.

**745 Crescent Road, Fort Erie (+18).** Units 101, 102, 104, 105, 201–207, 301–307 (no
103), all at the same point as the plain 745 (11512111, on file since the first read).
GSmartIDs 11542573–11542590.

**2487A–D Killaly Street East, Port Colborne (+4).** GSmartIDs 11542591–11542594, four
points ~60 m apart along the road, east of 2477 (11315666). No plain 2487 on file before.
INFERENCE: four frontages, not one building. On the 10-01 read (October's business) the
same four ids read 2487, 2489, 2491, 2493, same points.

**Niagara Falls units.** 18 properties gained Unit 1 and 2 (15) or Units 1–3 (5311 Bridge
St, 6736 McMicking St, 6915 Harovics Lane), plain number still on file in every case:
11743 Niagara River Pkwy, 6304 Ker St, 6336 Jewel Common, 6589 Alexa Common, 6648 Dunn St,
6826 Stokes St, 7303 Majestic Trail, 7728 Watson St, 7745 Secretariat Ct, 7887 Seabiscuit
Dr, 8049 Tad St, 8703/8727/8775 Harlyn Common, 9122 Kudlac St. Plus 5672 Dorchester Rd
unit 11 gained 11A and 11B (unit 11 still on file; building has units 1–67). 6632 Ash St
gained a lone Unit 2 (plain 6632 on file, no Unit 1). 18 + Dorchester + 745 Crescent +
Killaly = brief's 21 split events.

**7411 → 7407 Marvel Drive, Niagara Falls.** GSmartID 11526822, same point. Odd side on
file runs …7399, 7401, [7411→7407], 7413, 7415… No other 7407 or 7411 on file.

Other single additions: 4080 Elizabeth Rd and 2417 Nigh Rd (Fort Erie), 8121 McLeod Rd and
9234 Ort Rd (Niagara Falls), 113 Humboldt Pkwy and 201/205 Wellington St (Port Colborne),
689 Lyons Creek Rd (Welland), 433 Sixteen Rd (Pelham), 11 Manhattan Ct Unit 1 (St.
Catharines; plain 11 and Unit B already on file), 6225 Vaughan Rd (West Lincoln). Not
researched.

Sub-floor nudges, not counted: 117 Humboldt (Port Colborne) ~7 m; 5464 and 5470 Lewis
(Niagara Falls) swapped coordinates. Left out of the article.

## 1. Web

- **Butternut Crescent / The Oaks at Six Mile Creek.** FACT: listing for 6 Butternut
  Crescent: "Welcome to The Oaks at Six Mile Creek, an exclusive adult-oriented community
  by Blythwood Homes in the charming town of Ridgeway"; "This to-be-built interior
  townhome"; "As a condominium townhome…". https://filipesells.ca/property/6-butternut-crescent-fort-erie-x13440220/
  — high confidence it is the same street (Fort Erie, L0S 1N0).
- FACT: REW development page: "The Oaks is a Blythwood Homes community", "124 units",
  townhome, "Now Selling", "located in historic Ridgeway". Photo caption says "Whispering
  Woods Drive" (store says Trail; store wins). https://www.rew.ca/developments/6694/the-oaks-at-six-mile-creek-fort-erie-on
- Search summaries also showed listings for 7 and 8 Butternut Crescent (viewhomes,
  squareyards); viewhomes 403s, not used. A search summary quoted directions "Whispering
  Woods Trail to Butternut Cres." but the page (keyhomes) returned 410 — not used.
- EMPTY: no Town of Fort Erie council / street-naming record for Butternut Crescent found.
- EMPTY: "3411 Whispering Woods" — nothing for the number; only other Whispering Woods
  Trail listings (Blythwood bungalows, Ridgeway).
- EMPTY: "745 Crescent Road" Fort Erie — listings for other Crescent Road numbers only; no
  site plan or application found.
- EMPTY: "2487 Killaly" Port Colborne — nothing.
- EMPTY (not searched further): 7407/7411 Marvel Drive.
- EMPTY: Harlyn Common — listings for 8719 and 8723 only (incl. a "1-8719" rental), none of
  the three numbers in the file this month.
- **Niagara Falls ADU rule.** FACT: City page: "A maximum of 2 ADUs can be located on a
  parcel of urban residential land"; same for rural; three dwelling units per lot total;
  "ADUs cannot be severed or sold separately from the main dwelling, but may be rented."
  https://www.niagarafalls.ca/building-planning-and-business/building-and-renovating/additional-dwelling-units-secondary-units/
  — this is the rule, not evidence that any of the 18 is an ADU; the file says only "Unit".
