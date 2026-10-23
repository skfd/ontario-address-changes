# Research notes — County of Wellington, 2026-09

Raw findings behind `articles/researched/wellington-2026-09.md`. Notes, not prose.
Window: net 2026-08-29 → 2026-09-30 (store snapshots 63 → 89); 11 snapshots inside
the month (9, 11, 15, 16, 17, 18, 22, 24, 28, 29, 30 Sep). 30 pull days in September,
0 failed. Research done 2026-10-23. First article for this city.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found.

No open flag for wellington (`python run.py flags`); nothing HELD in the brief.

---

## 0. Store-side findings

Layer: County of Wellington base data (`Wellington_County_Base_Data_view`). Covers the
seven lower tiers (Centre Wellington, Erin, Guelph-Eramosa, Mapleton, Minto, Puslinch,
Wellington North); Guelph is separate. No combined address field, no stable record id:
identity is synthesized from number + street + unit + rounded position, so a moved
point reads as one retirement plus one addition.

Net: rows 42,928 → 42,958 (+30); 46 added, 16 removed, 0 modified. Gross 49 / 19.

Of the 46 "added", **11 are existing addresses whose point moved** (re-keyed):
8563 Concession 6 (Mapleton, 82 m), 161 Division St (Rockwood, 5 m), 92 and 94 King St S
(Harriston, 6 / 4 m), 149 and 157 Sideroad 18 (Fergus, 19 / 25 m), 5113 and 5127
Trafalgar Rd (Erin, 5 m each), 900 Watson Rd S (Puslinch, 5 m), 6688 Wellington Rd 109
(Minto, 39 m), 6949 Wellington Rd 7 (Centre Wellington, 9 m).

So **35 addresses new to the file**, **5 addresses leaving**: 35 − 5 = 30 ✓.

The five that left, each replaced on or near the same spot:
- **7438 Middlebrook Rd** (Centre Wellington, gone 9 Sep) → 7438A on the identical point,
  7438B 24 m away. Brief: suffix split, parent retired.
- **135 Kertland St** (Elora, gone 9 Sep) → 131 on the identical point, 137 11 m away.
  Tracker does not count it as a split or renumber.
- **19 Gilkison St** (Elora, gone 16 Sep) → 17 Gilkison St on the identical point.
- **7385 Concession 6 North** (Wellington North, gone 16 Sep) → 9392 Concession 6 North
  5 m away; same day 7385 *Sideroad 3 East* appears 242 m away (nearest other address
  7388 Sideroad 3 E). INFERENCE: the number moved to the side road and the
  concession-road point got a concession-road number; the file does not say.
- **415 Maiden Lane** (Fergus, gone 30 Sep) → same day 420 St George St W 21 m away and
  415 St Patrick St W 60 m away (nearest: 175 Maiden Lane 44 m, 399 St Patrick St W 72 m).

New addresses by township: Centre Wellington 24, Erin 3, Wellington North 3, Minto 2,
Puslinch 2, Mapleton 1 (29B Booth St E, Moorefield), Guelph-Eramosa 0.
Net: CW +20, Erin +3, WN +2, Minto +2, Puslinch +2, Mapleton +1.

Gross vs net gap (3 each way):
- 149 Sideroad 18 moved twice: a new point on 15 Sep for one day, another on 16 Sep.
- 8450 Eramosa-Garafraxa Townline (CW) read **8452** from 16 to 28 Sep, back to 8450 on
  29 Sep, same point. Not in net.

Out of window, noted for October: from snapshot 100 (13 Oct) street names truncate to
20 characters (`St David Street Nort`, `Eramosa-Garafraxa To`). Not this article.

## 1. Sideroad 18, Fergus — 145 to 157 odd — LEAD candidate

Store: 16 Sep (snap 79) 145, 151, 153, 155 new; 149 and 157 (on file since the first
read) moved 19 / 25 m the same day. Seven odd numbers within ~46 m, RoadClass URB,
UrbanCentre Fergus (149's row has no UrbanCentre value). Nearest other address:
146 Stafford St, 37 m; 33 Vincent St 111 m.

Searches:
- `"Sideroad 18" Fergus development townhouses` → Wellington Advertiser, council approves
  12 singles + 37 townhouses at **961 St. David St. N.** between Sideroads 18 and 19
  (https://www.wellingtonadvertiser.com/council-approves-another-development-on-hwy-6-just-north-of-fergus).
  **NOT this site**: 961 St David St N is on file, ~794 m from 145 Sideroad 18. Do not use.
- `"145|151|153|155 Sideroad 18" Fergus` → EMPTY (only 104 Sideroad 18 listings).
- Wellington County Land Division Committee notices 2026 (B7, B9, B10, B12, B16, B21,
  B22-26) → none on Sideroad 18. EMPTY.
- `"Sideroad 18" Fergus "Stafford Street"` → EMPTY.

Verdict: public record silent.

## 2. 6734 Wellington Road 16 — Units 1–5, parent remains

Store: 18 Sep (snap 81) Units 1–5 appear; plain 6734 still on file. Unit points are
204–526 m from the plain 6734 point, spread ~390 m apart from each other. Nearest
address on any other road: 8365 Sideroad 15 at 716 m. RoadClass CTY.

Searches:
- `"6734 Wellington Road 16" Centre Wellington` → EMPTY (6716 Wellington Rd 16 listing,
  bungalow near Lake Belwood — different property).
- ARU context: Centre Wellington allows up to two ARUs plus the original dwelling
  (https://www.wellingtonadvertiser.com/centre-wellington-residents-can-have-up-to-two-arus-plus-original-dwelling).
  FACT as headline; five units exceeds that, so it does not explain this. Not used.

Verdict: public record silent. Do not guess (campground, farm, etc.).

## 3. 7438 Middlebrook Road — 7438A / 7438B

Searches: `"7438 Middlebrook Road" Elora severance`, `"Middlebrook Road" Centre Wellington
consent application` → EMPTY. Only nearby hit: BlueTriton demolition permit at
7334 Middlebrook Rd (different property). Not used.

## 4. Kertland St (135 → 131 + 137), Gilkison St (19 → 17), Elora

`"135 Kertland Street" Elora` → EMPTY (a museum record of an 1862 house at Kertland and
Colborne, no number — not usable). Gilkison not searched beyond the Kertland query's
neighbourhood; low yield expected. Silent.

## 5. Maiden Lane → St George St W / St Patrick St W, Fergus

`"415 Maiden Lane" Fergus` → EMPTY. `St Patrick Street West Fergus Maiden Lane development`
→ only the James Square right-of-way story (299 St Patrick St W), unrelated. Silent.

## 6. Trafalgar Road, Erin — 5125 between 5113 and 5127

24 Sep: 5125 new; 5113 and 5127 moved 5 m each the same day. Nearest other road:
9406 Sideroad 5, 236 m. `"Trafalgar Road" Erin 5125|5113|5127` → EMPTY (road-work and
listings for other numbers). Silent.

## 7. Concession 6 North / Sideroad 3 East, Wellington North

`"9392 Concession 6 North" | "7385 Sideroad 3 East" | "7385 Concession 6 North"` → EMPTY.
Silent.

## Not searched

Single rural numbers (6638 Fifth Line, 5174 Fourth Line, 6348 Fourth Line E, 5961 Jones
Baseline, 7373 McLean Rd W, 7385 Sideroad 3 E, 7697 Sideroad 8 E, 5021 Tenth Line, 4562
Victoria Rd S, 983 Watson Rd S, 7693 WR17, 8344 WR19, 5792 WR2, 6965 WR7, 325 Brunswick
St, 29B Booth St E, 59 John St). Searches for single numbers in this county have come
back empty throughout; returns had stopped.
