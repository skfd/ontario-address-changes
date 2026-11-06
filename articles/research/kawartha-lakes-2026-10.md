# Research notes — City of Kawartha Lakes, 2026-10

Raw findings behind `articles/researched/kawartha-lakes-2026-10.md`. Notes, not prose.
Window: snapshots 2026-08-01 → 2026-10-26 (2 kept inside the month: 10-03, 10-26; September
kept none, so the 3 October snapshot carries everything since 1 August; 30 pull days, 0
failed). Research done 2026-11-06.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found. **UNREACHABLE** = the page that might answer
could not be read, so the record is unknown there, not silent. **UNVERIFIED** = seen only
in a search summary; page could not be fetched — do not print.

No open flag for kawartha-lakes in 2026-10 (`python run.py flags`: 16 open, none this city);
nothing HELD in the brief. `article_due` lists the month as `due`.

---

## 0. Store-side findings

Net 08-01 → 10-26: rows 44,205 → 44,261 (+56); added 63, removed 7; gross = net.
By snapshot: 10-03 added 48, removed 7; 10-26 added 15, removed 0.

### Re-keys: 6 of 63 "added" and 6 of 7 "removed" are the same addresses

`AddressID` is the identity key. Ten addresses changed ID at the same coordinates.

| Address | ID on 08-01 | ID on 10-03 | Shows in brief as |
|---|---|---|---|
| 191 Pontypool Rd | 101216 | 101288 | added |
| 22 Maple Ave | 101217 | 101280 | added |
| 160B Pleasant Point Rd | 101218 | 101277 | added |
| 1108B Sandy Hook Rd | 101219 | 101289 | added |
| 28 Lees Rd | 101220 | 101291 | added + removed |
| 4413D Hwy 35 | 101221 | 101290 | added + removed |
| 245 Kawartha Lakes Rd 46 | 101240 | 101216 | removed |
| 1676 Peniel Rd | 101241 | 101217 | removed |
| 121D Albert St N | 101239 | 101218 | removed |
| 165 Peniel Rd | 101242 | 101219 | removed |

IDs 101216–101219 therefore show as four "modifications" that jump 19–42 km and change
address entirely (brief's "Other modifications" rows). Those are ID reuse, not moves.
The config comment calls AddressID persistent; this month it was not, for these ten.

Corrected: 57 new addresses, 1 retired, net +56 (matches the brief's net).

### The one real retirement

313 Fox Rd (ID 618, on file since the first read, gone by 10-03). Its point was identical to
312 Fox Rd's (44.32458, -78.55958); 312 is still on file. No span returns later.

### New addresses carrying ARUApproved = Yes: 21 of the 57

INFERENCE: `ARUApproved` means additional residential unit approved; the file does not expand
the name, but the City uses ARU for that term and these rows fit (§1).

Suffixes: B ×10, D ×7, C ×1, none ×3 (1831 Heights Rd, 28 Horseshoe Cres, 34 Dunbar Dr).
Distance from plain-numbered address: 15 of 17 measurable sit 7–44 m away; 88B Childs Rd
124 m, 1793D Kawartha Lakes Rd 121 109 m. 1159D Killarney Bay Rd has no plain 1159 on file.

Places: Lindsay 5, Fenelon Twp 3, Verulam Twp 2, Bobcaygeon 2, and one each in Eldon, Somerville,
Bexley, Ops, Emily, Dalton Twps, Pontypool, Oakwood, Mariposa Estates.

Records with ARUApproved = Yes: 90 on 08-01, 123 on 10-26 (+33 = 21 new + 12 existing addresses
that gained the flag on the 10-03 snapshot). These are records, not units: a house and its
unit can both carry the flag. On 10-26, seven existing parents gained MultiUnitLot only.
File-wide suffixes on flagged rows: B 52, C 23, D 15, none 33. The file does not say what the
letters mean. D points sit further from the parent (median 32 m vs B 15 m), which proves nothing.

### Sanderson Drive, Lindsay

10-03: seven new records, IDs 101304–101310 in one run: 58, 60, 64, 66, 68, 112, 116. Old 58
(ID 100316) became 62, moved 3 m. So the new numbers on the street are 60, 62, 64, 66, 68,
112, 116. 110 and 114 moved 3–4 m. Nearest other streets from 62: 61 Sylvester Dr 84 m,
53 Debois St 116 m. ID 101311 (698 Hwy 7A) follows the run but is elsewhere.

### Direction changes (brief: "street renames", 19 addresses)

- **William St → William St North**, Lindsay, 13: 437, 440, 442, 444–450 (all), 454, 456, 460.
  Editorial shape per `references/verifying.md`. Joins 386 other William St North records.
  459 William St, Lindsay, kept the bare name, 88 m from 450. The other 31 bare William St
  records are Bobcaygeon's own street.
- **Church St → Church St East**, Omemee, 3: 49, 51, 53. Omemee's other five were already East,
  so no bare Church St is left there.
- **George St North → George St South**, Omemee, 3: 14, 15, 17. These sit south of King St East.
  Until then the file held two 15 George St Norths; the other is still there north of King.
  Unchanged: 13 George St North at 44.29817, south of King, 34 m from 15 George St South,
  and a second 13 George St North at 44.30003, north of King, about 220 m away.

### Renumbering

20 Byrne Court → 4 Byrne Court, same point. Street's others: 5, 8, 12. Was the southernmost
of them, so 4 fits the order and 20 did not (INFERENCE from coordinates; no reason on file).

### Moves

28 location changes; no `location_min_move_m` for this city; most are small. Six over 100 m,
five in Emily Twp: 124 Meadowview Rd 896 m, 372 Hayes Line 687, 884 St Luke's Rd 406, 801 Peace
Rd 369, 836 Hayes Line 195; plus 694 Hwy 7A (Manvers) 102. Figures from the brief.

---

## 1. Additional residential units

- **FACT** City's ARU guide: "All ARUs must be registered under By-law 2020-162."
  "Unregistered ARUs are considered illegal." Each ARU on a lot is registered individually.
  Inventory used by "emergency services agencies", solid waste, planning.
  https://www.kawarthalakes.ca/media/u3qdmu5c/aru-guide-2023.pdf — read in full (7 pages).
- **FACT** Same guide, FAQ: "Upon completion of registration, a municipal address will be
  assigned to the ARU."
- **FACT** Same guide: "Up to two ARUs for every primary residential unit", one in the building
  and one in an accessory building; one, inside the house, in the Oak Ridges Moraine Area.
- **EMPTY** The guide says nothing on suffix letters. "2023" is the file name only; no printed date.
- **EMPTY** No City addressing by-law or suffix rule found. Hamilton's and Prince Rupert's turned
  up and do not apply here.
- Notes only: PTBO Today, 30 Apr 2025: 138 residential permits in Kawartha Lakes including 12
  ARUs, in what reads as Q1 2025 (period not stated for permits).
  https://www.ptbotoday.ca/?p=88927
- Notes only: Lindsay Advocate, 1 Nov 2020: public meeting on official plan amendments to
  permit ARUs. https://lindsayadvocate.ca/city-to-hold-public-meeting-on-amendments-for-additional-residential-units/
- **UNREACHABLE** kawarthalakes.ca ARU web pages tried by guessed URL: both 404.

## 2. Sanderson Drive

- **FACT** 66 Sanderson Dr: rental listing dated 8 Jan 2026, leased 28 Jan 2026, possession
  2026-01-15; "newly built" Rivera townhome by Tribute Communities; "community of Lindsay
  Heights". https://property.ca/listings/x12677578 — single agent listing, good for dates.
- **UNVERIFIED** 127, 108, 98, 43, 68 Sanderson listings: search summaries only; debbiegrant
  and comfree pages gone (404/410), getaldo 404. Do not print.
- **Not linked to Sanderson:** Canadian Mortgage Professional, 22 Sep 2021: Greybrook and Tribute,
  over 2,600 homes on land east of Hwy 35 in Lindsay. Names neither Sanderson nor Lindsay Heights.
  https://www.mpamag.com/ca/news/general/more-than-2600-new-homes-to-rise-in-lindsay-ontario/310805
- **EMPTY** No plan of subdivision, phase or City file found for the street.

## 3. Direction changes

- **EMPTY** No by-law, notice or council item for William St North, Church St East or George St
  South. Search hits were other cities, or the 2026 budget's $2.7 million Colborne/William
  intersection (https://www.kawarthalakes.ca/media/osvpigpb/kl-tax-insert-jan-2026_accessible.pdf),
  search summary only and not about these addresses.
- Notes only: The Standard, "Apr 23" with no year: proposed updates to the street naming policy,
  including renaming rules. Silent on direction suffixes.
  https://www.thestandardnewspaper.ca/post/new-naming-rules-aim-to-reflect-community-culture-and-growth-in-kawartha-lakes
- Weak: cartogiraffe describes Church St East as a street in Omemee. Directory, not used.
  https://www.cartogiraffe.com/canada/ontario/central+ontario/church+street+east/

## 4. Single addresses

- **EMPTY** 313 Fox Rd: every hit was 81 Fox Rd listings.
- **EMPTY** Byrne Court: no result names the street.
- **Not searched individually:** the Emily Twp moves; the file has no reason for them and no
  named thing to search. Unrelated: The Standard's Highway 7 / McCumber Court item mentions a
  Meadowview Road; no source ties it to 124 Meadowview Rd, so it stays out.
