# Research notes — County of Hastings, 2026-10

Raw findings behind `articles/researched/hastings-2026-10.md`. Notes, not prose.
Window: snapshots 2026-09-29 → 2026-10-31 (21 snapshots inside the month, 10-01 .. 10-31;
30 pull days, 0 failed). No open flags for hastings. Research done 2026-11-06.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found. **DROPPED** = found but failed a check.

Source caveat, as in September: hastings publishes no stable row id, so
`datasets/hastings.toml` synthesizes the identity key from number + street + unit + rounded
lon/lat. A point moved by more than about a metre reads as one retirement and one addition.

---

## 0. Store-side findings (this repo, not the web)

Brief: rows 31,336 → 31,357 (+21); net added 315, removed 294, 22 "split events", no
modifications of any kind. Gross = net. All 315 additions still on file at 11-06.

Pairing added and removed rows by identical label (full + unit + unit type), nearest first:
- **284 pairs**: same address, point moved. Median 34 m, min 1 m, max 444 m (81 Ruddy Ln,
  CARL, 10-22). 30 over 100 m. 275 of 284 kept the same roll (RnoTXT2); the other 9 are six
  16 Alice units, 12 Alice St, 30 Nicklaus Dr, 5259 Old Hastings Rd.
- By code: BANC 139, BANG 38, DUNG 29, TYEN 22, MCCL 17, FARA 16, CARL 6, MAYO 5, WICK 4,
  WOLL 4, HERS/HUNG/TUDO/RAWD 1 each.
- By street: Hastings St North (BANC) 74 (10-09: 11, 10-10: 33, 10-19: 30; median 15 m, max
  164 m at 337); Shannonville Rd (TYEN) 22 on 10-07; Alice St (BANC) 14 on 10-09; Highway 28
  (DUNG) 13 on 10-19; Fairway Blvd (BANC) 12; Dog Point Rd, Maple Blvd (BANG) 9 each on
  10-23; Mink Lake Rd (MCCL) 9 on 10-28.
- **No overlap with September**: none of these 284 labels was in September's moved set.
  Mink Lake Rd appears in both months with different numbers.
- Baker St (September's watch item): no row in October's diff.
- Left over: **31 additions, 10 retirements**, which is the +21.

The 10 labels that left:
- Plain base rows with units still on file: 303 Hastings St North (and its stray APT 303),
  16 Alice St. 3 rows.
- Relabelled on the same roll, 5 rows: **73 Crystal Beach Rd → 73A** (0 m, 10-01; 73B new,
  43 m away, same roll …1005600); **15 Cleak Ave → 15A** (12 m, 10-10; 15B already on file,
  moved 10-10); **36987 Highway 62 → 36987B** (61 m, 10-22; 36987A on file since June, own
  roll); **574 → 548 Airport Rd** (397 m, 10-07, roll …2034110); **11863 → 11864B Highway 62**
  (464 m, 10-01, roll …2012600; 11864A arrived the same day on a new roll …2014100).
- **592 and 697 Ingram Rd** (WOLL), last seen 10-02, absent 10-03. 592 shares roll …2517350
  with 593 Ingram, still on file. 697's roll …2517600 is on no other row at any time. 230 and
  249 Ingram moved the same day. Only 697 is an address with nothing left behind it.

The 31 new labels: the six relabel rows above, 11864A, 303 APT 103 and APT 107, 16 Alice
UNIT 202, then **21 single numbers**: 223 Bateman, 47 Charles, 127 Hazzards, 27 Iroquois,
527 Kamaniskeg Lake, 331 Maines, 1708 Melrose, 142 Moores, 140 Mudcat, 792 Musclow-Greenview,
7775 Old Hastings, 17 Palmateer, 496 Pine Point, 537 Pine View Ridge, 29 Red Oak, 260 and 430
Robinson, 430 South Baptiste Lake, 756 St. Ola, 563 Steenburg Lake North, 415 Vine.
- 8 of the 21 are on a roll another address already held (47 Charles/55; 127 Hazzards/11
  Hazzards + 15124 Hwy 62; 331/289 Maines; 140/20+90 Mudcat; 792/814 Musclow-Greenview;
  17/39 Palmateer; 430/420 South Baptiste Lake; 415/423 Vine).
- 260 and 430 Robinson Rd share one roll, 789 m apart, both 10-16.
- 7775 Old Hastings Rd and 563 Steenburg Lake North Rd carry no roll.
- Nearest unpaired retirement to any of the 21 is over 1.8 km: none is a hidden move.

The 22 "splits" (brief lists 15; all 22 pulled by raising TOP_N in a throwaway run):
- 17 have every child already on file: moved points. 12, 20, 24, 61, 8 Hastings St North and
  1 Fairway Blvd read `parent retired`, but the plain base is still active at a new point.
  **The brief's `retired` is wrong for those**: the tracker closed the old key, the address
  stayed. Checked each in the store.
- 5 touch a new label: 303 Hastings (2 of 32), 16 Alice (1 of 8), 15 Cleak (15A; a relabel),
  11864 Highway 62 (a renumber plus one new), **73 Crystal Beach (the only address that
  became two)**.

Stacked points: 9 old points carrying 2+ labels spread to 2+ new points, 60 rows: 303 Hastings
(30 → 2), 16 Alice (7 → 7), 12 Hastings St N (7 → 7), 61 Hastings St N (4 → 4), 30933 Hwy 28,
817 Mayo Lake Rd (3 → 3 each), 775 and 849 Bay Lake Rd, 47 Snow Rd (2 → 2 each).
12A–12F now run in a line about 15 m long; 24 Hastings St N moved as one stack and stayed one.

**303 Hastings St North** (roll 126200002012450, all rows). The only 303 on any Hastings
street in the store (no South). `--near`: 6 York River Dr 120 m, 29 Eagles Nest Cr 165 m.
- To 10-17: 32 rows on one point (-77.85886, 45.08026): plain 303, APT 101, 102, 104, 105,
  106, 108–112 (10), APT 201–220 (20), APT 303.
- From 10-19 (no 10-18 snapshot): 32 rows on two points. APT 101–112 (12) at (-77.85837,
  45.08059), 53 m from the old point; APT 201–220 (20) at (-77.85796, 45.08074), about 89 m
  from it and 36 m from the first. New: APT 103, 107. Gone: plain 303, APT 303.

**16 Alice St** (`--near`: 2 Madawaska St 87 m, 124 Hastings St North 145 m). To 10-08: plain
16 and 7 units on one point and one roll (…2011001). From 10-09: 8 units, 8 points, 8 rolls
(…2011001 to …2011008); moves 22–44 m; UNIT 202 new; plain 16 gone.

## 1. Web

- **303 Hastings Street is York River Heights.** FACT:
  https://www.hastings.ca/communities/services/housing-services/bancroft-properties-0 —
  "York River Heights Senior Citizen Complex Corporation Non-Profit Housing"; "Main Office:
  303 Hastings Street, Bancroft, Ontario K0L 1C0"; applicants "65 years of age or older";
  "The building has 24 one-bedroom and 8 two-bedroom units. There are ground level entrances
  to apartments on the ground floor." 24 + 8 = 32 is arithmetic, not the page's. The page
  says "the building", singular; storeys and year built not given. Whether the file's two
  points are two buildings is unknown and not printed. The hastingscounty.com
  mirror 403'd, and a snippet of it gave a different phone number; not used.
- **16 Alice Street, Unit 202 was on sale before the file had it.** FACT: REW page
  https://www.rew.ca/properties/202-16-alice-street-bancroft-on — "Apt/Condo", "located at
  202-16 Alice Street, Bancroft, ON", last updated 2026-07-09.
  DROPPED: "co-op" and "31–50 years old" came only from search snippets; every page behind
  them 403'd or 404'd (teamrealty, kimalldread, homesbykahlon, coldwellbanker).
- **County 9-1-1 addressing and GIS work.** FACT, context only: 9-1-1 Sub-Committee agenda,
  4 Feb 2026,
  https://opencouncil.ca/wp-content/uploads/2025/06/HC-9-1-1-Sub-committee-04-Feb-2026-Agenda-Pdf.pdf
  - p. 36, NG911 Readiness Update 2026: geospatial routing "requires significant updates to
    Geographic Information System (GIS) data".
  - p. 37: "The legacy 9-1-1 network will be decommissioned by March 2027".
  - p. 40, HQ911 2025 Projects and Achievements: County 9-1-1 staff "completed joint 9-1-1
    information sessions that were held at each municipal office, specifically for staff
    working with addressing."
  - p. 41: "This transition continues to require extensive updates to Geographic Information
    System (GIS) data and processes". Report approved 26 January 2026.
  - p. 44: the County's role includes "managing the 9-1-1 addressing and signage system".
  None of it mentions moving address points or any street. **Not evidence of cause**; printed
  as context with that said.
- County or Town notice of the October moves, Hastings St North renumbering or re-survey:
  EMPTY (three searches; hits were other jurisdictions and sale listings).
- Later 2026 9-1-1 Sub-Committee agendas: not reached. opencouncil's committee page lists
  none; the civicweb portal was not followed.
- 548 / 574 Airport Rd: EMPTY (only 168, 314, 1073 Airport Rd listings).
- 73, 73A, 73B Crystal Beach Rd: EMPTY (a Crystal Beach Lane campground in Madoc turned up;
  a different street name, DROPPED).
- 260 / 430 Robinson Rd: EMPTY (only 24 Robinson Rd listings).
- 592 / 697 Ingram Rd: EMPTY (only 727 and 1386).
- Not searched: the other single numbers. The article gives no reason for them and claims no
  search.

Place names: `MUNICIPALI` has no coded-value domain (see September's notes), so codes are not
expanded. "Bancroft" is printed for 303 Hastings St and 16 Alice St, where a source says so;
the 139 are described by the code those two carry.
