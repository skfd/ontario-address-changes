# Research notes — County of Frontenac, 2026-09

Raw findings behind `articles/researched/frontenac-2026-09.md`. Notes, not prose.
Window: net 2026-08-18 → 2026-09-28; 7 snapshots inside the month (09-02, 09-04, 09-22,
09-23, 09-24, 09-25, 09-28); 30 pull days, 0 failed. No open flags for frontenac.
Research done 2026-10-23.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **SNIPPET** = seen only in a search-engine summary; the page could not be
fetched — do not print as fact. **EMPTY** = searched, nothing found.

Source caveat: frontenac has no stable row id; `datasets/frontenac.toml` synthesizes the
key from number + street + unit + rounded lon/lat. A renumbered address, a moved point,
or a corrected StreetName therefore shows as one removal plus one addition.

---

## 0. Store-side findings

Net: rows 22,381 → 22,397 (+16); added 20, removed 4, modified 6. Gross: 21 / 5 / 6.
The extra gross pair is 125 Inspiration Lane re-keyed between 09-23 and 09-28 (below).

All four net removals have a replacement in the additions:

| Removed (last seen) | Added (first seen) | Coordinates | Township |
|---|---|---|---|
| 5758 ROAD 38 (09-22) | 125 INSPIRATION LANE (09-23) | identical, 44.44305 -76.66605 | South Frontenac |
| 1148 NINE MILE POINT ROAD (09-04) | 63 LUCAS POINT LANE (09-22) | identical, 44.17585 -76.49952 | Frontenac Islands |
| 1213 CRONK ROAD (08-18) | 1179 CRONK ROAD (09-02) | identical, 44.65818 -76.77699 | Central Frontenac |
| 122 FULLER ROAD WEST (08-18) | 122 FULLER ROAD WEST (09-02) | moved 63 m | Frontenac Islands |

So 16 of the 20 additions are points with no predecessor:
- South Frontenac (10): 107, 109, 111, 126 INSPIRATION LANE (09-28); 123 OLD THIRTEEN
  ISLAND LAKE ROAD, 4320 ELLERBECK ROAD, 118 TWELFTH CONCESSION ROAD, 4280 STAGE COACH
  ROAD, 86 HALL LANE (09-23); 1033 PRIMROSE LANE (09-28).
- Central Frontenac (3): 2493 and 2503 CROW LAKE ROAD, 1079 CALVERT LANE (09-02).
- Frontenac Islands (3): 5 16TH LINE ROAD (09-04), 173 SUNRISE LANE (09-22), 51 REED'S
  BAY ROAD (09-24).
- North Frontenac: none.

Inspiration Lane detail:
- 125 first appeared 09-23 with Location "125 INSPIRATION LANE" but StreetName still
  "ROAD 38"; on 09-28 it was reissued with StreetName "INSPIRATION LANE" (new key), and
  107, 109, 111, 126 arrived the same day.
- `lookup.py --near "107 INSPIRATION LANE"`: 5768 ROAD 38 at 66 m, 4789 HOLLEFORD ROAD
  127 m, 3984 BOYCE ROAD 162 m. Points span ~200 m east-west.

1033 PRIMROSE LANE: first seen 09-28 with Location "1033 PRIMROSE LANE" but StreetName
"PRICE ROAD" (which is why the brief lists Price Road as gaining an address). Only
Primrose Lane row in the file. Nearest other address: 4338 MILLER ROAD, 210 m. The
StreetName was corrected to PRIMROSE LANE on 10-19 (October, after the window).

Six modifications, all Location only: a doubled space removed —
1141 NINE MILE POINT ROAD, 7181 HINCHINBROOKE ROAD NORTH, 718 REED'S BAY ROAD (09-24);
370 DRISCOLL ROAD, 124 7TH LINE ROAD, 1334 HOWE ISLAND DRIVE (09-25). Editorial.

## 1. Inspiration Lane (South Frontenac)

- EMPTY — `"Inspiration Lane" South Frontenac`: no township, county or press mention.
  Only unrelated Inspiration Lanes elsewhere.
- EMPTY — `"Inspiration Lane"` restricted to southfrontenac.net / frontenaccounty.ca:
  one unrelated park map (Tett Park), no mention.
- EMPTY — South Frontenac street-naming by-law for Inspiration Lane or Primrose Lane.
- FACT (context) — South Frontenac runs a private-lane upgrade subsidy and won an AMO
  award for it in 2020: https://www.southfrontenac.net/en/resources/en/resources/news/20200817-PJMarshall-TwpofSouthFrontenacNRFINAL.pdf
  (search summary; not tied to Inspiration Lane). Not used in the article: nothing says
  Inspiration Lane is a private lane.
- SNIPPET — 2017 Frontenac News piece says 545 of the county's 981 private lanes are in
  South Frontenac: https://www.frontenacnews.ca/south-frontenac-news/item/11158-private-roads-to-play-major-role
  (403 on fetch). Not printed.

## 2. Lucas Point Lane (Frontenac Islands)

- EMPTY — `"Lucas Point Lane" Frontenac Islands`. The lane already had 7 addresses on
  file since June (34–183), so it is not a new street; one point moved onto it.
- SNIPPET — Frontenac Islands' street naming policy PDF, summarised by search as making
  naming of new streets (and private roads) the township's responsibility:
  https://frontenacislands.ic15.esolg.ca/en/living-here/resources/Policy-Street-and-Road-Naming-Township-of-Frontenac-Islands.pdf
  404 on fetch 2026-10-23. Not printed.

## 3. Cronk Road (Central Frontenac)

- EMPTY — nothing public on a renumbering of 1213 to 1179. A listing for 1147 Cronk
  Road, Parham exists (https://condos.ca/addresses/1147-cronk-road-parham) — confirms
  the road is near Parham, nothing about 1179/1213. Not used.

## 4. Primrose Lane, 122 Fuller Road West

- EMPTY for both. Nothing searched beyond names; record silent.
