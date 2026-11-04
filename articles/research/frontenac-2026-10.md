# Research notes — County of Frontenac, 2026-10

Raw findings behind `articles/researched/frontenac-2026-10.md`. Notes, not prose.
Window: net 2026-09-28 → 2026-10-31; 6 snapshots inside the month (10-07, 10-08, 10-13,
10-19, 10-29, 10-31); 30 pull days, 0 failed. No open flags for frontenac; the one
October flag (10-07, 395 rows, doubled space in Location) was reviewed `technical` on
10-07 and is held out of every number. Research done 2026-11-04.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **SNIPPET** = seen only in a search-engine summary; the page could not be
fetched — do not print as fact. **EMPTY** = searched, nothing found.

Source caveat: frontenac has no stable row id; `datasets/frontenac.toml` synthesizes the
key from number + street + unit + rounded lon/lat. A moved point or a corrected
StreetName therefore shows as one removal plus one addition. Qualifier is not in the
key, so a number gaining a letter is a modification, not a split.

---

## 0. Store-side findings

Net: rows 22,397 → 22,408 (+11); added 15, removed 4, significant 2. Gross: 15 / 4 / 20.
Net and gross agree on additions and removals, so nothing arrived and left inside the
month.

Three of the four removals are the same address re-keyed:

| Removed (last seen) | Added (first seen) | What changed | Township |
|---|---|---|---|
| 8078 ROAD 509 (09-28) | 8078 ROAD 509 (10-07) | point moved 89.6 m | North Frontenac |
| 1585 LEGGAT LAKE ROAD (10-07) | 1585 LEGGAT LAKE ROAD (10-08) | point moved 1.9 m | Central Frontenac |
| 1033 PRIMROSE LANE, StreetName PRICE ROAD (10-13) | 1033 PRIMROSE LANE, StreetName PRIMROSE LANE (10-19) | StreetName corrected, coordinates identical | South Frontenac |

The fourth, 57 OAK SHORES CRESCENT (South Frontenac, on file 06-11 to 10-13), has no
replacement. 55 and 59 are still on file either side of it.

So 12 of the 15 additions are points with no predecessor:
- Central Frontenac (7): 1038B PRANGER COURT, 1276 BLUEBERRY ROAD, 1575 LEGGAT LAKE
  ROAD, 1599 CLARENDON ROAD, 949 CROW LAKE ROAD (10-08); 1136 POINT LANE (10-29);
  1146 STEIGER ROAD (10-31).
- South Frontenac (3): 1127 BEACH LANE, 184A BURRIDGE LAKE ROAD, 2171 KEELEY ROAD (10-19).
- North Frontenac (2): 1060 TURKEY LANE, 1170 HAMILTON HILLS LANE (10-13).
- Frontenac Islands: none.

Two net modifications (Full Address + Qualifier, same key, same coordinates):
- 1038 PRANGER COURT → 1038A (10-08), the day 1038B appeared 88.9 m away. Nearest address
  on another street to 1038B: 1038C PLEASANT HILL LANE, 42 m; then 28539 HIGHWAY 7, 261 m.
  The court's other four numbers are 1026A–D, so every number on it now carries a letter.
- 184 BURRIDGE LAKE ROAD → 184B (10-19), the day 184A appeared 24.4 m away. Nearest
  address on another street to 184A: 14 LOWER LAKE LANE, 359 m.
- The brief's `Address splits: (none)` is correct by its definition: the original kept its
  key, so these read as a modification plus an addition.

Gross significant 20 = the two above + 18 labels on 10-08 where the space between number
and letter closed ('1050 A PENYCK LAKE LANE' → '1050A PENYCK LAKE LANE'), Qualifier
unchanged. Net strips those because their field set matches the held 10-07 event
(`month_digest.py`, held fieldsets stripped for the whole month), which is why net says 2.
The 18: 1050A Penyck Lake; 1060A/B, 1064A/B/C Morrison; 1075A Woodcock; 2378B Ducharme;
2838B McLean; 3203A/B McGarvey; 4784A Opinicon; 50A/B Howe Island Baseline; 5112A/B and
5270A Battersea; 8951A Road 509.

Primrose Lane is the brief's only "new street" and it is not a new road: the single point
has been on file since 09-28 with Location PRIMROSE LANE and StreetName PRICE ROAD, as the
September article said. Price Road's "loss" and Primrose Lane's "debut" are that row. Only
Primrose Lane row in the file; Price Road keeps 32. Nearest other address: 4338 MILLER
ROAD, 210 m.

1575 LEGGAT LAKE ROAD arrived 10-08, 56.8 m from 1585, the day 1585 was nudged.

## 1. Primrose Lane (South Frontenac)

- EMPTY — `"Primrose Lane" South Frontenac township Ontario`. Hits were Primrose Lane in
  Newmarket, Old Primrose Lane in Toronto and one in Warminster, England: the wrong-city
  trap, none used.
- EMPTY — `South Frontenac council October 2026 street naming by-law private lane civic
  address`: Halifax and other municipalities only.

## 2. 1038 Pranger Court (Central Frontenac)

- EMPTY — `"Pranger Court" Central Frontenac Ontario`: no mention of the street at all.
- EMPTY — `Central Frontenac township civic address change 2026 new civic number
  application severance`: nothing on a civic-number change.
- Context, not used — Frontenac News, Apr 2025, council on severances:
  https://fn.nfshost.com/central-frontenac-news/item/17973-cf-council-wants-to-increase-severances-to-stimulate-growth
  Seen in search summary only; nothing ties it to this address.

## 3. 184 Burridge Lake Road (South Frontenac)

- EMPTY — `"Burridge Lake Road" South Frontenac 184`. Listings exist for 137 and for a
  vacant parcel on the road, nothing for 184.
- EMPTY — South Frontenac news and public notices, pages 1–4, 2026-08-21 to 2026-11-02
  (https://www.southfrontenac.net/news/): about 20 consent, zoning and minor-variance
  notices, none on Burridge Lake Road, Oak Shores Crescent, Primrose Lane, Price Road,
  Keeley Road or Beach Lane. "Beach Island" on Buck Lake (PL-BDJ-2026-0119) is a different
  name. Read by a fetch agent; 2025 notices not covered.
- FAILED — https://www.southfrontenac.net/en/news/notice-of-road-closing.aspx returned
  404, so its contents are unknown. It surfaced on a Burridge Lake Road search. Not used.

## 4. 57 Oak Shores Crescent (South Frontenac)

- EMPTY — `"Oak Shores Crescent" Frontenac Ontario` and `"57 Oak Shores" Crescent
  Tichborne South Frontenac`: listings for 39, 51, 55, 65, 123 and 143, none for 57.
  Nothing on a demolition, merger or lot change. A retirement is a record leaving the
  file; the file does not say why.

## 5. Leggat Lake Road (Central Frontenac)

- Context, not used — the road and lake are near Sharbot Lake
  (https://geogratis.gc.ca/services/geoname/en/geonames/FBXBO.html). Nothing on 1575 or
  on the 1585 nudge.

## 6. Civic addressing rules

- EMPTY — `South Frontenac civic addressing by-law`: other municipalities' by-laws only.
  Nothing here says who issues lettered numbers in Frontenac, so the article does not say.

## 7. Not searched

Single numbers on established roads (Blueberry, Clarendon, Crow Lake, Keeley, Beach, Point,
Steiger, Turkey, Hamilton Hills) and 8078 Road 509: no street or cluster to search, and the
checklist did not list them.
