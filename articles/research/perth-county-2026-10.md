# Research notes — County of Perth, 2026-10

Raw findings behind `articles/researched/perth-county-2026-10.md`. Notes, not prose.
Window: snapshots 2026-09-08 → 2026-10-07 (one snapshot inside the month). 30 pull days
in October, 0 failed. Research done 2026-11-08.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found.

No open flag for perth-county (`python run.py flags`); nothing HELD in the brief.

---

## 0. Store-side findings

Snapshots: id 2 (09-08, 18,701 rows) → store reads 10-03..10-06 identical (skipped,
hash d13b7c1d) → id 7 (10-07, 18,717, hash 600a828b) → identical every read 10-08..11-02
→ next change 11-03 (November's). So the County published one change in October, first
read on the 7th.

Net 09-08 → 10-07: added 59, removed 43, modified 15; gross = net; rows +16.

Identity is synthesized from Full_Add + rounded lon/lat, so a moved point reads as a
removal plus an addition. Pairing added/removed by identical full address:

- **38 re-keys** (same full address, same roll, point moved):
  - 25 MCNALLY DRIVE (85–98, 100, 128–164 by 4s, 178–190 by 4s) and 10 FEATHERSTONE
    STREET EAST (380–470 by 10s), all North Perth, all on one roll 314041000110205,
    moved 3–9 m. McNally has 46 numbers on file now (21 untouched); Featherstone St E 25
    (15 untouched). All on file since the first read 2026-08-20.
  - 2917 FOREST ROAD (Perth East) 57 m; 1712 PERTH ROAD 123 (Perth South) 6 m;
    5995 PERTH LINE 20 (West Perth) 3 m.
- So **21 addresses new to the file**, **5 genuinely gone**: 21 − 5 = 16 ✓.

New 21 by township (`Inc_Muni`):
- North Perth 9: 170 Main St Atwood Units A/B, 172 Main St Atwood Units A/B, 514 Boyne
  Ave, 1098 Twamley St W, 6093 Perth Line 88, 8319 Fairlane Rd, 9334 Road 165.
- Perth East 6: 3972A/B and 3974A/B Byron St, 5047 Line 52, 6980 Road 129.
- Perth South 4: 1720A/B Perth Road 123, 3186A/B Road 122.
- West Perth 2: 5996 Perth Line 20, 6639 Line 32.

Gone 5: 172 Main St Atwood, 1720 Perth Road 123, 3186 Road 122 (split parents);
154 Boyne Ave; 2891 Road 164.
Net by township: North Perth +7, Perth East +6, Perth South +2, West Perth +1 = +16 ✓.

Splits (store):
- 170 and 172 Main St Atwood: all four units on roll 314036000809100 (172's old roll).
  No plain 170 ever on file (parent none); plain 172 retired same snapshot. 168 Main
  untouched. `--near 170 ... UNIT A`: 126 James St Atwood 42 m, 175 King St Atwood 61 m.
- 3972A/B and 3974A/B Byron St: all on roll 311001000105500; no plain 3972 or 3974 ever
  on file; 3963–3971 on file since 08-20. `--near`: 2173 Andrew St 42 m, 3970 Tannahill
  St 103 m, 3971 Burns St 114 m.
- 1720 Perth Road 123 → 1720A/B, same point (<1 m), same roll 312014000510620.
- 3186 Road 122 → 3186A/B, within ~15 m of the old point, same roll 312009000613905.

Same-spot renumber the brief misses (identity changed, so not in "Renumbered"):
- 154 BOYNE AVENUE → 514 BOYNE AVENUE, identical coordinates (43.72997, -80.96236), same
  roll 314042000812276. `--near 514`: 525 Riverview Dr 51 m, 485 Victoria Ave S 52 m,
  540 Ann St 71 m. INFERENCE: 514 fits its 500-range neighbours; whether 154 was a typo
  the file does not say. Don't call it a correction.
- 2891 ROAD 164 → 5996 PERTH LINE 20, 61 m apart, same roll 313018001503432.
  `--near 5996`: 2888 Road 164 77 m, 2884 Martyn St 86 m. The 5995 Perth Line 20 point
  moved 3 m the same day.

15 modifications, all `Property_Number` (roll) only:
- 33 MURRAY COURT Units 1–12 (Perth East): one shared roll 311034000207719 replaced by
  twelve, 311034000207763–774 (not in unit order: Unit 3 →766, Unit 4 →765, etc.).
  `--near`: 67 Main St S 39 m, 1 Llana Heights 43 m, 44 Arena Dr 94 m.
- 193 Queen St Atwood, 2687 Road 149, 5678 Perth Line 55: one roll each changed.

## 1. McNally Drive and Featherstone Street East, Listowel — Countryside Meadows

- **FACT** — REW listing, Lot 20 Featherstone Street E, Listowel (MLS X12774518, Kempston
  & Werth Realty; fetched 2026-11-08, "Days on REW: 272"): "Welcome to Countryside
  Meadows, a thoughtfully designed new subdivision by PK Homes Inc … Located on the north
  end of Listowel". https://www.rew.ca/properties/lot-20-featherstone-street-e-listowel-on
  Confidence: high on the text (direct fetch).
- **FACT** — Intercity Realty listing, Lot 14 McNally Drive (X12774448, "The Amber",
  townhome; page "Last updated … 4th of November 2026"; fetched 2026-11-08): same
  "Welcome to Countryside Meadows, a thoughtfully designed new subdivision by PK Homes
  Inc … north end of Listowel"; "City: North Perth (Listowel)".
  https://intercityrealty.com/property/X12774448/lot-14-mcnally-drive-north-perth-listowel.html
  Confidence: high (direct fetch). Other lots (9, 70) seen in search only. Listings use lot numbers, not civic numbers — can't match a
  listing lot to a file number.
- INFERENCE: the 35 nudged points sharing one roll = one parent parcel not yet split
  into lots. The file says nothing about why the points moved. Don't claim surveyed lots.

## 2. 170/172 Main Street, Atwood (North Perth)

- **EMPTY** — "170 Main Street" / "172 Main Street" Atwood: no listing, consent or
  severance found. A 2020 Midwestern Newspapers item on a Main Street Atwood rezoning
  gives no street number; can't tie it. Not used.

## 3. 3972/3974 Byron Street (Perth East)

- **FACT (location)** — a listing for 3966 Byron Street names the place Shakespeare:
  https://royallepagetriland.com/listing/3966-byron-street-shakespeare-ontario-40693052
  (search-result title "3966 BYRON Street Shakespeare"; fetch returned 403). Not
  confirmed, so the article says only "Perth East" (store `Inc_Muni`), not Shakespeare.
- **EMPTY** — 3972 / 3974 Byron: no severance, consent or listing found.

## 4. 33 Murray Court (Perth East)

- Listings found by search title "33 MURRAY Court Unit# 1 Milverton" and REW
  "9-33 Murray Court, Perth East" (https://www.rew.ca/properties/9-33-murray-court-perth-east-on).
  Fetch of the detail pages failed (403/429), so the search summary's details (condo,
  built 2024) are NOT verified. Use only "listed for sale unit by unit", or nothing.
- **EMPTY** — why the twelve units got their own rolls in October.

## 5. Not searched further

Single rural numbers (Perth Line 88, Fairlane Rd, Road 165, Line 52, Road 129, Line 32),
1098 Twamley St W, 1720 Perth Road 123, 3186 Road 122, 154/514 Boyne Ave — quick searches
on the larger items came back empty; record treated as silent.
