# Research notes — United Counties of Leeds and Grenville, 2026-09

Raw findings behind `articles/researched/leeds-grenville-2026-09.md`. Notes, not prose.
Window: net 2026-08-04 → 2026-09-01; one snapshot inside the month (09-01); 30 pull days
(09-01 .. 09-30), 0 failed. No open flags for leeds-grenville. Research done 2026-10-23.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found.

Source cadence: the counties republish roughly monthly — kept snapshots 06-11, 07-07,
08-04, 09-01, 10-06. Every September change landed in the one 09-01 republication; the
rest of September read the same file. Gross = net (44 / 9 / 73 / 17).

Identity: keyed on the source `Id` (stable). A record keeps its Id through renumbering,
so renumbers show as modifications, not add+remove.

---

## 0. Store-side findings

Net: rows 54,142 → 54,177 (+35); added 44, removed 9, modified 73 significant + 17
location-only.

### The August id mix-up, undone on 09-01
- 08-04 file: ids 1200045135–41 carried copies of seven existing addresses — 215, 217,
  219 Reuben Cres (North Grenville), 855 Coyote Ln, 79 and 115 Benson Park Rd, 457 Lyndhurst
  Rd (Leeds and the 1000 Islands). Meanwhile the original ids of 215 Reuben (1200019699),
  855 Coyote (1200010056), 79 Benson Park (1200006245), 115 Benson Park (1200030663) and
  459A Lyndhurst (1200030568) were missing from the August file. Id 1200044752
  (660 Veenstra Grove, Gananoque, since June) read 650 Pine Street.
- 09-01: ids 1200045135–41 became 101, 103, 105, 107, 109, 111 and 100 Old Whaley Drive,
  each with its own coordinates; the originals returned on their old ids; 1200044752 is
  660 Veenstra Grove again and 650 Pine St has a new id (1200045163, same point).
- 459A Lyndhurst Rd (July) came back as **457** Lyndhurst Rd, same roll 081281602022300,
  ~14 m away. So a renumber hidden inside the mix-up.
- 215/217/219 Reuben Cres all carry roll 071971901039400 (one property, three numbers).
  217 and 219 first appeared 08-04; 215 has been on file since June. Not researched
  further.
- Effect on the brief: 8 of the 44 "added" were already on the August file as addresses —
  five on their original ids that had gone missing (215 Reuben, 855 Coyote, 79 and 115
  Benson Park, 457 Lyndhurst ex-459A), three re-issued under fresh ids (217, 219 Reuben
  → 1200045133/34; 650 Pine → 1200045163); and the seven new
  Old Whaley numbers are counted as modifications. By address, 43 addresses on file at
  09-01 were on neither the July nor the August file (incl. 5 + 4 units). Not used as a
  headline number — the article keeps the brief's 44/9/+35 and explains.

### Old Whaley Drive (North Grenville, GEOTOWNSHP "Oxford on Rideau Twp")
- Debuted 08-04 with 20 numbers (102–130, mostly even + 115, 119, 121–127). 09-01 added
  100, 101, 103, 105, 107, 109, 111 → 27 numbers. ARN "Not yet available" on all.
- All 20 August records had township typo "Oxford on Rideau **Two**" in ADDRESS911; fixed
  to "Twp" on 09-01 (these are 20 of the 73 modifications).
- Nearest other streets (store, active): 2200 County Road 20 at 54 m, 7 Rachelle Cres
  174 m, 4 Smith Rd 361 m.

### 235 James Street West, Prescott — split
- Base 235 (roll 070802002016100) on file since June, still there ("remains"). Units 1–5
  arrived 09-01, same roll, TYPE "Unit".
- Nearest: 485 Centre St 52 m.

### 130 Henry Street East, Prescott
- Base 130 since June (roll 070801001003800) remains. Four new records 09-01, labels
  130-A..130-D, ADDRESS911 "Unit A..D, 130 Henry Street East"; UNITNUM empty, so the
  tracker's unit column is blank (brief shows four identical "130 Henry Street East").

### 240, 242, 244, 246 Water Street West, Prescott
- New 09-01 with four separate rolls (070802002003803, …3800, …4002, …4000) but **no
  CIVICNUM and no ADDRESSAGOL** — the file's full-address field was empty; only LABEL and
  ADDRESS911 carried the numbers. Filled in on the 10-06 republication (October).
- Nearest: 249 King St W 29 m.

### St John Street, Merrickville-Wolford — 8 removed
- Removed: 826, 828, 856, 858, 928, 932, 968, 972 St John St — four pairs. Ids in the
  1200043647–72 block, ARN "Not yet available", on file since the tracker began
  (2026-06-11). The block 1200043634–716 is the whole new St John / Wallace St run
  (720–1059 St John, 140–172 Wallace); 83 ids, the other 75 remain on file (store count).
- Nothing replaced them; no other address on the street was added.
- Location-only: 751, 753, 755, 757, 825, 831 St John and 140–146, 167, 169 Wallace moved
  3–7 m (same block).

### Other
- 1 Snake Island (Leeds and the 1000 Islands): one of two records with that address
  retired; the other (roll 081281201018800) remains, ~16 km away. Two different islands?
  Not researched; article says the file kept the other one.
- Ranges collapsed to single numbers (Rideau Lakes): 2416-2430 R24 → 2430; 286-372 County
  Rd 8 → 372; 476-528 Summers Rd → 476; 32-34 Sand-Birch Island → 32; 43-43A King St → 43;
  1158-1172 Davis Lock Rd → 1158 (+ new 1172); 255-259 UB2 → 259 (+ new 255, 257).
- Renumbered in place: 5975 → 5575 County Road 15 (Augusta); 6660 → 6659 Island 201 Big
  Rideau Lake; Jones Court (Augusta): 20 → 23, 22 → 25, 22A → 22 (rolls kept), plus a new
  20 with no roll.
- Suffix restyles: 13A → 13-A, 13C → 13-C Whitefish Lake Rd; 3904A/C → 3904-A/C Freeland
  Rd. 5195 Salem Rd → 5195-A (+ new 5195-C, same roll).
- 981 Highway 15 (Rideau Lakes) split in two on 09-01, same roll: the old record now reads
  981-B in its number field and 981-A on its label; the new record the reverse. Data
  inconsistency in the source; noted, not used.
- Location: 135/137 Old River Rd 74/66 m, 558 Ritz Rd 58 m — no story.

## 1. Merrickville Grove (St John / Wallace St, Merrickville)
- FACT — North Grenville Times, 13 Nov 2019, "New urban subdivision planned for
  Merrickville": Park View Homes' Merrickville Grove, west of St. Lawrence St, would open
  an unbuilt section of St. John St (Sophie Lane to Bruce St W) and an unbuilt section of
  Wallace St linking St. John and St. Lawrence; 67 two-storey townhomes, 16 bungalow
  townhomes, 15-unit apartment (98 homes). https://ngtimes.ca/?p=22641
- FACT — North Grenville Times, 23 Sep 2020, "Council moves ahead with Merrickville Grove
  Subdivision": now 99 units, fewer bungalow townhomes; council approved the draft plan
  with conditions, Deputy Mayor Cameron opposed; goes to the County.
  https://ngtimes.ca/?p=28196
- FACT — listing for 752 St. John St (still on file): Park View Homes, "Merrickville
  Grove", 2-storey townhome, marked sold 18 Aug 2026.
  https://www.wahi.com/ca/en/real-estate/on/leeds-and-grenville/merrickville-wolford/752-st-john-st-merrickville-wolford-k0g1n0-ontario-canada
  (listing site; inconsistent pre-construction/sold wording — used only for "Park View
  Homes, Merrickville Grove").
- INFERENCE (printed as geography, not as a sourced fact) — the eight removed numbers
  belong to Merrickville Grove: they sit in the same id block as the new St John/Wallace
  run, on the unbuilt St John stretch the 2019 piece names, ~69 m from Wallace St, and
  752 St John (same run) is listed as Merrickville Grove. No source names the eight.
- EMPTY — why eight numbers came off. Nothing on the eight addresses. INFERENCE (not
  printed): a lot-layout revision; do not say so.

## 2. 235 James Street West, Prescott
- FACT — current MLS listing X13639696: "Turnkey legal 5-unit apartment building";
  "Originally a duplex, this property has been comprehensively transformed into a modern
  income-producing asset"; one 3-bed, two 2-bed, two 1-bed suites.
  https://www.rew.ca/properties/235-james-street-w-prescott-on (REW shows 80 days on
  site as of 10-23; listing date not shown — not printed). Price differs between
  syndicators; not printed.
- EMPTY — no Town of Prescott permit / planning record found.

## 3. Old Whaley Drive, North Grenville
- EMPTY — `"Old Whaley Drive" North Grenville`; `"Old Whaley"` + Kemptville / Oxford Mills /
  County Road 20; `site:pub-northgrenville.escribemeetings.com Whaley`; "Whaley
  subdivision". Nothing: no street-naming by-law, plan of subdivision or listing.
  (Search turned up the 7-lot Archstone subdivision in Oxford Mills — different place
  name, not linked to this street; not used.)

## 4. 130 Henry Street East, Prescott
- EMPTY — `"130 Henry Street East" Prescott`: only Brooklyn's 130 Henry St.

## 5. 240–246 Water Street West, Prescott
- EMPTY — nothing on these numbers. Search returns Prescott Place condos at 235 Water St W
  across the road (57-unit townhouse condominium) — unrelated to the new numbers; not used.
