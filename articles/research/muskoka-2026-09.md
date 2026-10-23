# Research notes — District Municipality of Muskoka, 2026-09

Raw findings behind `articles/researched/muskoka-2026-09.md`. Notes, not prose.
Window: net 2026-08-29 → 2026-09-27; eight snapshots inside the month (09-16, 09-17,
09-18, 09-23, 09-24, 09-25, 09-26, 09-27); 30 pull days (09-01 .. 09-30), 0 failed.
No open flags for muskoka; nothing HELD. Research done 2026-10-23.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found.

Identity: `datasets/muskoka.toml` synthesizes the key from number + street + unit +
`PropertyNum` (assessment roll number), with geometry off. A roll-number change or a new
number therefore shows as one retirement plus one addition, never as a modification.
`location_min_move_m = 2` (the service wobbles up to ~1.4 m between republishes).

Licence: custom terms, no reuse grant. The brief's attribution line is a plain source
statement; quote few addresses.

---

## 0. Store-side findings

Rows 66,471 → 66,498 (+27). Brief: added 44, removed 17, location 87, 2 split events.
Gross added/removed = net (44 / 17); gross location 95 vs net 87.

### Mackenzie Drive, Huntsville — 14 out, 14 in, same addresses (re-key)
- 30, 32–39, 42, 44–46, 48 Mackenzie Dr (14 records). Until 08-29 all fourteen carried
  one roll number, 444202000401515. From 09-16 each carries its own,
  444202000401537 … 444202000401550. Numbers, street, coordinates unchanged (≤1 m).
- So the brief's 14 added + 14 removed on Mackenzie Dr are the same addresses re-keyed.
  Real arrivals in the month: 30; real departures: 3.
- `--near 30 Mackenzie Dr`: 31 Greaves Av 99 m, 57 Yonge St S 175 m, 20 Goodwin Dr
  185 m, 34 Walter St 234 m.
- INFERENCE (not printed as fact): one roll splitting into fourteen consecutive rolls is
  the pattern of a parcel being divided into separately assessed lots. Nothing public
  confirms it.

### 1291 Skeleton Lake 2 Road, Muskoka Lakes — split, parent `none`
- No plain 1291 has ever been on file. "1291 Skeleton Lake 2 Rd Unit 1" on file since
  06-11 (roll 445302001806500); on 09-16 it was nudged ~19 m and seven records appeared
  on the same roll: Unit "1 01" … "1 05", "1 HOUSE", "1 Marina Bldg" (the file's own
  labels). Spread ~110 m north–south.
- Other 1291 units (4, 6, 10, 14 … 48) have been on file since June, each on its own roll.
- `--near` returns no other street nearby.

### 1180 Woodroffe Road, Muskoka Lakes — split, parent remains
- 1180 Woodroffe Rd on file since 06-11 (roll 445304000703400), still active.
  Units A–F first on 09-16, all on the parent's roll, in a row ~75 m long about 55 m
  north of the parent point.
- `--near 1180 Woodroffe Rd Unit A`: 8126 Lake Joseph Rd 253 m.

### Other addresses that left
- **1047 → 1049 Mahoney Ln** (Bracebridge): same roll (441805000400400), ~4 m apart;
  1047 last 08-29, 1049 first 09-16. A renumbering shown as retirement + addition.
- **1633 Walkers Point Rd** (Muskoka Lakes): the old record (roll 445308000400100) closed
  08-29. On 09-16 "1633 Walkers Point Rd Unit 1" appeared on that same roll ~80 m south,
  and a new plain 1633 on a different roll (445308000312200) a few metres from it.
  Also new that day: 1571 Walkers Point Rd.
- **1102 Woodroffe Rd Unit 0** (Muskoka Lakes): retired after 08-29; Units 2–12 of 1102
  remain.

### The rest of the real arrivals (16)
- Muskoka Lakes: 1001 Woodroffe Rd (09-16; 98 m from 8009 Lake Joseph Rd), 1263 Three
  Mile Lake 1 Rd Unit 6, 1571 Walkers Point Rd (all 09-16); 1011 and 1013 Currie St,
  1050 Hudson Point Rd Unit 9, 1295 Windermere Rd, 2901 Muskoka Rd 118 W (09-25).
- Lake of Bays: 1608 and 1652 Paint Lake Rd, 3704 Muskoka Rd 117 (09-16).
- Bracebridge: 1111 Caribou Rd (09-25). Gravenhurst: 1090 Jones Rd (09-16).
  Huntsville: 72 South Mary Lake Rd (09-16).
- By municipality of the 30 real arrivals: Muskoka Lakes 23, Lake of Bays 3, Bracebridge
  2 (incl. 1049 Mahoney), Gravenhurst 1, Huntsville 1.

### Location moves
- 87 records moved ≥2 m between 08-29 and 09-27; 25 of them ≥50 m, 12 under 10 m.
  By municipality: Muskoka Lakes 41, Huntsville 17, Bracebridge 13, Gravenhurst 10,
  Lake of Bays 4, Georgian Bay 2.
- Largest: 1032 Redwood Rd Units 5, 3 and 1 (361, 267, 181 m); 157 and 179 Longs Lake Rd
  in Huntsville (254, 233 m); 4182 Muskoka Rd 169 Unit 34 (198 m).
- 09-16 carried 73 of the month's location edits; gross 95 vs net 87 means a few points
  moved more than once.

---

## 1. Searches

- **Mackenzie Drive, Huntsville** — `"Mackenzie Drive" Huntsville Ontario townhouses
  development`; `Huntsville "Mackenzie Drive" plan of condominium OR subdivision council`.
  EMPTY for any planning item. Results were resale listings for 5, 10, 14 Mackenzie Dr
  ([5](https://beckyhunt.locationsnorth.com/listing/5-mackenzie-drive-huntsville-ontario-x13147488/),
  [10](https://realtris.ca/listings/X10922259/10-mackenzie-drive-huntsville-huntsville-on-p1h-0a1)
  (403 on fetch), [14](https://www.wahi.com/ca/en/real-estate/on/muskoka/huntsville/14-mackenzie-dr-huntsville-p1h0a1-ontario)),
  none about 30–48 or a roll change. The Town's
  [planning notices page](https://www.huntsville.ca/news/posts/planning-notices-for-consideration-at-september-11th-planning-council-meeting-and-other-notices)
  that came up is from Aug 2024 and does not mention the street. Confidence: the record
  is silent on why the rolls changed.
- **1291 Skeleton Lake 2 Road** — `"1291 Skeleton Lake" Road 2 Muskoka Lakes marina`;
  `"Skeleton Lake Marina" address Skeleton Lake Road 2 Utterson`. EMPTY for the address.
  Listings mention a marina on Skeleton Lake reached by Skeleton Lake Road 2, but none
  ties it to 1291; the
  [Skeleton Lake cottagers' newsletter (June 2019)](https://skeletonlake.ca/news/7587477)
  names a "Skeleton Lake Marina" fishing derby, no address. Not printed as a link between
  the marina and 1291. Confidence: silent.
- **1180 Woodroffe Road** — `"1180 Woodroffe" Road Muskoka Lakes Lake Joseph`. EMPTY.
  Results were other Lake Joseph properties. Confidence: silent.
- Not searched further: Paint Lake Rd, Currie St, Walkers Point Rd, Mahoney Ln (single
  rural numbers; returns had already stopped).
