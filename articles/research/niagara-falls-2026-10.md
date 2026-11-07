# Research notes — Niagara Region (slug niagara-falls), 2026-10

Raw findings behind `articles/researched/niagara-falls-2026-10.md`. Notes, not prose.
Window: net 2026-09-03 → 2026-10-01; one snapshot kept inside the month (10-01, store
snapshot 23); 30 pull days 10-01..10-31, 0 failed; next change on file is 11-05. So every
change below landed between the 3 September snapshot and the 1 October read, and the
rest of October changed nothing. Research done 2026-11-07.

Conventions: **FACT** = the linked page says it (fetched directly). **INFERENCE** = a
reading, not the source's. **EMPTY** = searched, nothing found.

Source caveat (as in September): the layer is the Region's, region-wide, despite the slug.
Identity is GSmartID. No `full` field, so `lookup.py --near`/`--addr` do not work; placement
by the `Municipality` property and a hand-rolled nearest-street query on coordinates.
`location_min_move_m = 25`.

Flag queue: `python run.py flags` on 2026-11-07 shows open flags for guelph, simcoe,
mississauga only; none for niagara-falls. Brief has no HELD section.

---

## 0. Store-side findings

Net: rows 208,079 → 208,286 (+207); added 213, retired 6, renumbered 7, location 3,
split_events 5. Gross identical (one snapshot). September was +75.

Additions by Municipality: Niagara Falls 196, St. Catharines 4, Lincoln 4, Grimsby 2,
Fort Erie 2, Wainfleet 2, Pelham 1, Port Colborne 1, Welland 1 (= 213).

**The Montrose Road block (Niagara Falls).** 182 of the 213 additions, GSmartIDs
11542626–11542811 (every one of the 182 inside that run; four ids unused), all first seen 10-01:
- Forestgate 60 (7404–7573), Wintergreen 35 (7424–7548), Springland 28 (7427–7545),
  Kingbird 15 (3658–3686), Grasslands 11 (3653–3675), Craftsman 9 (3655–3673), Rove 6
  (3662–3682) — all StreetType **Common**, all seven names new to the file.
- Montrose Road 18 (3666–3758, even numbers), StreetType Road, a column of points at
  lon −79.1247 along the road frontage, lat 43.1180–43.1192.
- No units on any of the 182.
- Centroid ≈ 43.119, −79.123. Nearest existing streets (hand query on active rows):
  Monastery (7526, ~98 m), Mount Carmel (~147 m), South Wood, Bernadette, Trinity.
- **3736 Montrose Road** (GSmartID 11536035, on file since the first read, at 43.11882,
  −79.12400, inside the new block's frontage) retired on the same snapshot. Parent-style
  retirement; the file says nothing about what it was.
- **3770 Montrose Road** (11490331, 43.11723, −79.12389, just south of the block) is still
  on file, unchanged.
- Niagara Falls had 454 Common-type addresses on 10-01; the City's file already uses
  *Common* for private condominium-type roads (Harlyn Common, Emerson Common in this
  month's splits). INFERENCE: these are private roads; not stated by any source found.

**Splits** (parent remains, all units 1–2 or 1–3): 18 Princess St (St. Catharines,
Units 1–3), 5352 Stanley Ave, 6598 Emerson Common, 7356 Majestic Trail, 9248 Griffon St
(Niagara Falls, Units 1–2). Same shape as September's eighteen.

**Renumbered:**
- 2487A/B/C/D Killaly St (Port Colborne) → 2487, 2489, 2491, 2493, same ids and points.
  Already flagged as "belongs to October" in the September piece.
- 122-122A Livingston Ave (Grimsby, id 11463870) → 122. **A second record, 11474985, has
  read plain 122 at the identical point (43.19769, −79.5755) since the first read** — so
  122 Livingston is now on the file twice. The brief also shows 250 Livingston as an
  addition.
- 84 → 86 Millpond Rd (Niagara-on-the-Lake), 266 → 272 Westcott Rd (Welland), in place.

**Retired (6):** 2 Balmoral Ave (Grimsby), 6 Shore Blvd (St. Catharines), 8455 Stanley Ave
and 3736 Montrose Rd (Niagara Falls), 9282 Twenty Rd (West Lincoln), 870 Forks Rd
(Welland). All were *Active* on their last read. Re-key test (nearest new 10-01 addition
to each retired point): 870 Forks → new 860 Forks 6 m away; 2 Balmoral → new 17 Rosslyn
Ave 5 m away; 8455 Stanley → new 5362 Progress St 32 m away; 3736 Montrose → Wintergreen
points 10 m away (the block); 6 Shore and 9282 Twenty have nothing new within 3 km. These
explain the brief's unnetted Forks +1/−1; Stanley's third addition is 8559 Stanley.
Block id range 11542626–11542811 has four unused ids: 11542681, 11542784, 11542797,
11542798. Monastery Dr points lie at lat 43.1196–43.1220, north of the block (max 43.1195).

**Location moves:** 3227 Culp Rd (Lincoln) 81 m, as new 3235 Culp Rd appears ~115 m northwest of its new spot;
91 McMaster Ave 76 m and 74 Ross St 52 m (Welland, ending ~70 m apart).

**September follow-up:** plain 3411 Whispering Woods Trail (11519641) is still on file
beside the twenty Butternut Crescent addresses that used to be its units.

---

## 1. Montrose Road block = Forest Gate, former Canadian Tire plaza

- FACT — insauga (Don Redmond, published 2023-03-06): "developer Forest Gate Group will
  build 26 semi-detached homes, 109 townhouses and 140 stacked townhouse apartments at
  3770 Montrose Rd."; site is "the former Canadian Tire plaza on Montrose Rd."; council
  "lifted the holding order on the site at last week's meeting"; rezoned from commercial
  the year before; "With 270 units in total"; "in the Carmel neighbourhood".
  https://niagara.insauga.com/new-niagara-falls-development-gets-okay-to-build-townhouses-semis/
  Confidence: high on developer/site/holding lift; the article's own counts don't add up
  (26+109+140 = 275 vs "270"; caption says 129 townhouses). Quote "about 270".
- FACT — SkyriseCities thread (started 2023-12-11): "subdivision of condo-townhomes and
  semi-detached dwellings designed by One Riser Design for Forest Gate on the east side of
  Montrose Road, south of Monastery Drive, west of the Queen Elizabeth Way and north of
  Thorold Stone Road". Matches the store: block is east of Montrose, south of Monastery.
  https://toronto.skyrisecities.com/forum/threads/toronto-3770-montrose-road-11m-3s-forest-gate-one-riser.37129
- FACT — Historic Niagara Public Library photo, "Montrose Road, 3770 - Canadian Tire
  store", 2005. https://historicniagara.ca/s/All/item/245251
- INFERENCE (store vs source): the 182 numbers sit on the 3770 Montrose site described
  above; "Forestgate" echoes the developer's name. No source ties the street names to the
  project. The 182 numbers are fewer than the ~270 planned units; whether stacked units
  will get unit numbers later is not on record.
- EMPTY — "3736 Montrose Road": no listing or record found. What it was is not known.
- EMPTY — street names Forestgate / Wintergreen / Springland / Kingbird / Grasslands /
  Craftsman / Rove: no by-law, council item or listing found. City of Niagara Falls street
  name index exists on niagaraopendata.ca (not queried).
- Not fetched: public presentation linked from the Skyrise thread,
  https://niagarafalls.civicweb.net/document/49537/

## 2. Killaly Street East, Port Colborne

- EMPTY — "2487 Killaly Street" Port Colborne: only vacant-lot listings on rural Killaly
  St E (Sherkston area) for other parcels. Nothing on the four numbers.

## 3. Not searched (supporting items, store-only in the piece)

122 Livingston duplicate, Millpond/Westcott renumbers, six retirements, Culp/McMaster/Ross
moves, the five splits. Article reports them as what the file shows, no cause.
