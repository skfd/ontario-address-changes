# Research notes — County of Wellington, 2026-10

Raw findings behind `articles/researched/wellington-2026-10.md`. Notes, not prose.
Window: net 2026-09-30 → 2026-10-20 (store snapshots 89 → 107); 2 snapshots inside the
month (13 and 20 Oct). 30 pull days in October, 0 failed. Research done 2026-11-10.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found.

No open flag for wellington (`python run.py flags`). Two flags dated 2026-10-13
(mass-added 3,256 / mass-removed 3,262) are `reviewed`, verdict `bug`, and print under
HELD in the brief.

---

## 0. Store-side findings

**The brief's NET, street lists, "new streets", "splits" and the entities checklist
still contain the held 13 Oct event**, although its header says HELD is excluded. Only
the `rows:` line (42,958 → 42,953, −5) and the GROSS line for 20 Oct are clean. The
breakdown below comes from diffing snapshots 89, 100 and 107 in the store and pairing
each removed row with an added row on the same number, unit and point whose street is
the old street cut to 20 characters.

The held event (not news, not in any count):
- From snapshot 100 (13 Oct) every text field in the feed is cut at 20 characters.
  3,253 records on 124 street names changed `WC_FullNam` only by losing their tail
  (`St Andrew Street West` → `St Andrew Street Wes`, 156 records; `Winston Churchill
  Boulevard` → `Winston Churchill Bo`, 78; `East-West Garafraxa Townline` → `East-West
  Garafraxa`). 383 of them also lost the tail of `WC_Sign`. By township: Centre
  Wellington 1,564, Wellington North 526, Guelph-Eramosa 352, Puslinch 340, Erin 195,
  Minto 151, Mapleton 125. Because the street is part of the tracker's identity, each
  reads as one removal plus one addition.
- The 26 "significant" modifications are the same cut in another field: `UrbanCentre`
  `Wellington Road 124 and Lake Rd` → `Wellington Road 124` on 26 addresses (Wellington
  Road 124, Randell Drive, Wellington Road 32). Not a place rename.
- All 15 "new streets" on the checklist are cut names of existing streets. Both
  "splits" (170A/170B and 172A/172B `Frederick Street Wes`) are rows on file since the
  first snapshot under `Frederick Street West`; no split happened.
- Public site: the flags hold the day's additions and removals, so
  `docs/wellington/report-2026-10-13.html` shows 0 new, 0 retired and the 26
  `UrbanCentre` edits. **The six real retirements and the two renumberings sit inside
  the held removals/additions and appear on no public daily report**; the article says
  so in its methodology note. The 20 Oct report shows 4018 Concession 7 and the 33 Scott
  Street flip.
- Still cut at the last read: no non-skipped snapshot after 107, same content hash
  through 10 Nov.
- **33 Scott Street** (Fergus): longitude flipped −80.36438 → −80.36437 on 13 Oct and
  back on 20 Oct. It has done this four times since June. Rounding jitter; it is the
  whole of the 20 Oct "1 removed" and one of its "2 added".

What actually changed (3,256 − 3,253 = 3 added, 3,261 − 3,253 = 8 removed in the net
diff; two of each are the same point renumbered):

| Date | What | Where |
|---|---|---|
| 13 Oct | **338, 346, 362, 370, 378, 394 Wellington Street** removed, nothing in their place | Guelph-Eramosa, beside Everton |
| 13 Oct | **9490 Concession 6 North → 9491**, identical point | Wellington North |
| 13 Oct | **121 Main Street North → 129**, identical point | Mount Forest, Wellington North |
| 20 Oct | **4018 Concession 7** added | Puslinch |

1 new address, 6 leaving, 2 number changes in place: 1 − 6 = −5 ✓ (42,958 → 42,953).

## 1. Wellington Street beside Everton — LEAD

Store: the six removed rows were all on file since the first snapshot (11 Jun 2026),
all even-numbered, in a line about 190 m long on the south-west side of the street.
None carried an `UrbanCentre`; the odd numbers across the road (339, 347, 363, 371,
379, 395, about 40 m away) carry `Everton` and are all still on file. 300 Wellington
Street, 113 m south-east on the same side, also has no urban centre and remains. After
13 Oct the street has no even number above 300. Market Street in Everton has 110–160
on file since the first snapshot, unchanged.

- **FACT** — Wellington Advertiser, "Council okay with Everton subdivision plan
  extension", published 18 July 2013: a plan of subdivision "originally approved by the
  county in 2008" "removed five vacant lots west of Wellington Road 49 (Wellington
  Street)" and "created five new lots on the north side of Market Street"; owner Robert
  Eilers asked for an extension of a plan "expected to expire on Oct. 3"; Guelph-Eramosa
  council "unanimously approved a resolution supporting a three-year extension".
  https://www.wellingtonadvertiser.com/council-okay-with-everton-subdivision-plan-extension
  Confidence: high on what the page says. No plan or file number on it.
- **FACT** — Wellington Advertiser, "Township approves Everton lot swap and boundary
  change" (byline Chris Daponte): council approved Eilers's proposal to "swap the
  designation on ten lots and alter the boundary of Everton", removing rural residential
  zoning from "five existing lots on the west side of Wellington Street (County Road
  49)" and applying it to five proposed lots north of the Market Street road allowance;
  conditions include "prohibiting future multi-lot development on the west side of
  Wellington Street by designating those lands as agricultural".
  https://www.wellingtonadvertiser.com/township-approves-everton-lot-swap-and-boundary-change
  Confidence: high on content, **low on date**. The page header says "Published January
  01, 2025" (updated 2 Feb 2026); the body gives no year. INFERENCE: that header is an
  archive placeholder, since the story describes the township approval that the 2013
  piece places around the County's 2008 approval. Not proven: the Wayback Machine's
  only capture is from 8 June 2026 and web.archive.org could not be fetched. Do not
  print a year for it; the article says the page's date does not fit its story.
- **INFERENCE** — the six even numbers that left are on the side and stretch those
  articles describe (west of Wellington Street, outside the hamlet label). Not
  established: the articles count **five** lots and the file dropped **six** numbers;
  neither article gives a civic number; nothing found dated 2026. The article says the
  record matches in place and not in count, and that nothing says why now.
- **EMPTY** — `"Wellington Street" Everton` with each of 338/346/362/370/378/394: only
  a terminated listing for 339 (odd side, still on file). Guelph/Eramosa severance,
  zoning and consent searches for Everton in 2026: nothing.

## 2. 121 → 129 Main Street North, Mount Forest

Store: same point (−80.73607, 43.98196); neighbours 109 (12 m), 103, 135 (30 m). The
file also holds 121 and 129 Main Street **South** in Mount Forest, and a separate 129
Main Street North in Rockwood (Guelph-Eramosa, on file since June) — keep "in Mount
Forest" on every mention.

- **FACT** — the County's business directory lists Walsh's Health and Lifestyle Centre
  at "129 Main Street North Mount Forest".
  https://www.wellington.ca/business-development/business-directory/walshs-health-and-lifestyle-centre
- Other directories (wwhealthline, Cortico, Medimap) put the same pharmacy at 129 Main
  St **S**, which the file also has. Conflicting, so not used in the article.
- **EMPTY** — `"121 Main Street North" "Mount Forest"`: nothing. No notice, by-law or
  listing explains the number change.

## 3. 9490 → 9491 Concession 6 North, Wellington North

Store: same point; nearest neighbour 9496, 74 m away; the run is 9468, 9491, 9496,
9508, 9513.

- **EMPTY** — both numbers searched with Wellington North: only other roads (9490
  Wellington Road 16, 9490 Wellington Road 6 in Minto) and other numbers on the
  concession. Nothing public.

## 4. 4018 Concession 7, Puslinch

Store: new 20 Oct, between 4010 (83 m) and 4024 (49 m); run now 3994, 3996, 4010,
4018, 4024, 4040.

- **EMPTY** — `"4018 Concession 7" Puslinch`: nothing. A vacant-land listing exists for
  3996 Concession 7 Road (225 m away), which is a different address and is not used.

## 5. The layer itself

- **FACT** — the County's layer definition (name "Address Points") gives every text
  field, including `WC_FullNam`, `WC_Sign` and `UrbanCentre`, a length of 20, and its
  `editingInfo` reads schema last edited 2026-10-20 05:38 UTC, data last edited
  2026-10-20 05:40 UTC (epoch ms 1792474727927 / 1792474818261). Read 2026-11-10.
  https://services8.arcgis.com/qu8yojONWhklwVA3/arcgis/rest/services/Wellington_County_Base_Data_view/FeatureServer/0?f=json
- Before 13 Oct the store held street names up to 29 characters and an urban centre of
  31, so the limit is new. Nothing public from the County says why.
- The data-edit time matches the store's last kept snapshot (20 Oct).
