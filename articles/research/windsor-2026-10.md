# Research notes — City of Windsor, 2026-10

Raw findings behind `articles/researched/windsor-2026-10.md`. Notes, not prose.
Window: snapshots 2026-06-11 → 2026-10-12 (1 kept inside the month: 10-12; 30 pull days,
0 failed). Research done 2026-11-10.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found. **UNREACHABLE** = the page that might answer
could not be read, so the record is unknown there, not silent. **UNVERIFIED** = seen only
in a search summary; page could not be fetched — do not print.

No open flag for windsor in 2026-10 (`python run.py flags`: 23 open, none windsor); nothing
HELD in the brief.

---

## 0. Store-side findings

Net 06-11 → 10-12: rows 118,841 → 118,843 (+2); added 2, removed 0, modified 0; gross = net.
Entities checklist (`--format entities`) is empty on every heading: no new street, no street
with 3+ additions, no split, no rename, no place name.

| Address | First snapshot | PROP_RSN / gisid | Stored point |
|---|---|---|---|
| 5050 Tecumseh Rd E | 06-11 (first read) | 191554 | 42.30898, −82.96505 |
| 5054 Tecumseh Rd E | 10-12 | 191554 | 42.30898, −82.96505 |
| 5060 Tecumseh Rd E | 10-12 | 191554 | 42.30898, −82.96505 |

All three carry the same parcel number, the same legal description (`SANDWICH EAST CON 1 PT
LOT 111 PLAN 1065 PT ALLEY AND RP 12R2700 PT PART 11 RP 12R27669 PART 3`) and the same stored
point. The point is the parcel polygon's centroid (the layer is parcels; `datasets/windsor.toml`
normalizes ring centroids), so it says nothing about where on the parcel each number is.
**Do not place 5054 or 5060 within the site.**

`--near` from that centroid: 2025 Westminster Ave 59 m, 2048 Norman Rd 92 m, 4985 Empress St
104 m, 2358 Princess Ave 173 m. Distances are from the parcel's centre.

The brief says splits: none. Keep that row at 0; describe it as one parcel now carrying three
numbers.

### The +2 is a difference between two layers, not a dated act — BLOCKING for wording

- Snapshot 28 (2026-10-12) is the tracker's **first import from the licensed layer**
  `OpenDataServices/PropertyParcels/MapServer/1`. Until 10-11 it read
  `MappMyCity/AllUniqueAddresses_Parcels/MapServer/0` (commit 53f498fca; toml comment: "First
  import 2026-10-12 (snapshot 28): +2 added, 0 removed, 0 modified", and the same 2 measured
  against the store on 10-11).
- Queried both live on 2026-11-10:
  - old layer: 133,331 rows; parcel 191554 has one row, 5050 (OBJECTID 74740).
  - licensed layer: 133,333 rows; parcel 191554 has three rows: 5050 (OBJECTID 74740), 5054
    (133332), 5060 (133333). Those two are the last two records in the layer (max OBJECTID
    133333).
  - licensed point layer `/0` returned only 5050 for `PROP_RSN=191554`.
- So: every one of the 118,841 stored records carried over; the licensed layer has the same
  file plus these two rows. Safe wording: "first on file on the 12 October snapshot, the day
  the tracker began reading the City's licensed layer". **Not** "the City added them on 12 Oct".
- When the City made the two rows: **silent**. Their `created_date` (2024-05-11) and
  `last_edited_date` (2025-05-10) are identical to 5050's, i.e. inherited from the parcel.
  Not usable to date the addresses; not printed.
- Raw content hashes of the pulls changed on 10-13 and 10-21 and went back on 10-24 while no
  snapshot was kept (rows stay 118,843). Write "no later read changed anything the tracker
  records", not "identical file".
- After 10-12 no further snapshot kept, through 2026-11-10.

Not printed: PropCode 430, Zoning CD2.1 (CD2.1 = "Commercial District 2.1" in By-law 8600 per
a search summary of the April 2026 consolidation; the PDF was not read — **UNVERIFIED**).

## 1. 5050–5060 Tecumseh Rd E — the site — LEAD

- **FACT** — [Westdell Corp., Rose City Shopping Centre](https://www.westdellcorp.com/rose-city-shopping-centre/):
  property name "Rose City Shopping Centre", address "5050-5060 Tecumseh Rd. E", total GLA
  67,969 square feet; anchors "No Frills and Shoppers Drug Mart", plus "National Bank, Pet
  Valu, Mary Brown's Chicken, and 7 am Breakfast & Lunch". Logos also: Connect Hearing, East
  Windsor Family Dental, First Choice Haircutters, Maverick's Donut Company, Mr Sub, Tahini's,
  UPS. No redevelopment text; the site plan is an image with no building numbers in text.
- **FACT** — [Loblaw release, 4 Dec 2025](https://www.loblaw.ca/en/grand-opening-of-tony-and-kathys-no-frills-in-windsor/):
  "Where: 5050 Tecumseh Rd E, Windsor, ON N8T 1C1"; "When: Thursday, December 4, 2025"; "The
  store has hired 87 local employees."
- **FACT** — [AM800 CKLW, 4 Dec 2025](https://www.am800cklw.com/news/no-frills-celebrates-grand-opening-of-new-east-end-location.html):
  "Tony and Kathy's No Frills will open their doors at Tecumseh Road East and Princess Avenue
  on December 4." / "The new 33,000-square-foot location". No plaza name, no Shoppers.
- **FACT** — [National Bank locator](https://locator.nbc.ca/banking-solutions/on/windsor/5060-tecumseh-rd-east):
  "5060 Tecumseh Rd East, Windsor, ON, N8T 1C1".
- **FACT** — [The UPS Store #26](https://www.theupsstore.ca/26/): "The Westminster Plaza, 5060
  Tecumseh Rd E", Windsor N8T 1C1. Different plaza name from Westdell's; attribute each name
  to its source.
- **INFERENCE** — the parcel is the shopping centre: the file's 5050 and the Loblaw release's
  5050 are the same number on the same street, and Westdell's range 5050–5060 is exactly the
  file's three numbers' span. Confidence high. Article states the two facts side by side.
- **INFERENCE, do not print** — 5060 was in everyday use before the tracker's file carried
  it. Only "in use now" is supported (pages read 2026-11-10, no start date on either). A dated
  earlier capture was tried once: web.archive.org is not fetchable from here (**UNREACHABLE**).
  Article says "in use", present tense, and that neither page says since when.
- AM800's "33,000-square-foot" and Princess Avenue corner: FACT above, cut from the article
  for length.
- **EMPTY** — "5054 Tecumseh Rd E" / "5054 Tecumseh Road East", standard and extended: nothing
  uses the number. Results were all 5060 or other numbers.
- **EMPTY** — City of Windsor site plan / development application / building permit for 5050
  Tecumseh Rd E (results: 6412 & 6560 Tecumseh Rd E, a different site; East Windsor NJ/CT noise).
- **UNVERIFIED** — Windsorite, [March 2025](https://windsorite.ca/2025/03/east-windsor-plaza-redevelopment-continues/)
  and [March 2026](https://windsorite.ca/2026/03/mr-sub-opens-monday/): search summaries say
  Shoppers Drug Mart relocated to the west end of the property and No Frills was built on its
  former site, with a smaller plaza for Mary Brown's, Maverick's, Noodlebox, Tahini's. Both
  pages 403. **Not printed.** So "redeveloped" and "Shoppers relocated" do not go in the
  article.
- **UNVERIFIED** — LoopNet [28440435](https://www.loopnet.com/Listing/5050-Tecumseh-Rd-E-Windsor-ON/28440435/),
  [18548675](https://www.loopnet.ca/Listing/5050-Tecumseh-Rd-E-Windsor-ON/18548675/),
  [5060 listing](https://www.loopnet.ca/Listing/5060-Tecumseh-Rd-E-Windsor-ON/28440371/):
  summaries say "6 acre Re-development site", "4.07-acre parcel built in 1988". All 403. Not used.
- **Search summary contradicted by the fetch** — [Erie St. Clair Healthline](https://www.eriestclairhealthline.ca/displayService.aspx?id=134627):
  the summary said Shoppers Drug Mart at 5050; the page itself reads "Shoppers Drug Mart -
  Windsor - 4974 Tecumseh Rd E", N8T 1C1, "last completely updated on June 19, 2026". 4974 is
  a separate parcel on the file since the first read (PROP_RSN 133825). Yelp/Yellow Pages/Doctr
  summaries still say 5050 (not fetched). Shoppers is not about 5054 or 5060: **left out**.
- **EMPTY** — a fetchable outlet on the Shoppers move (am800cklw.com, ctvnews.ca, cbc.ca):
  nothing. windsorstar.com is not searchable from here (**UNREACHABLE**).
- Not fetched, search titles only: Connect Hearing "5060-tecumseh-rd-e-6", Pet Valu store 2107,
  eXp Realty "5060 Tecumseh Rd E Unit 501", East Windsor Family Dental. Not printed beyond
  what Westdell's page lists.

## 2. What the article can and cannot say

- Can: two records, 5054 and 5060 Tecumseh Rd E, first on file 10-12 on a parcel that already
  carried 5050; all else unchanged; the day is the day the tracker changed layers; the old
  layer still has only 5050; Westdell lists a Rose City Shopping Centre at 5050–5060 (the
  page does not call Westdell the owner, and 4990 next door shares reference plan 12R27669, so
  the centre may span more than this parcel); a bank and a courier outlet give 5060 as their
  address; a grocery store opened at 5050 in Dec 2025.
- Cannot: when the City created the rows; whether 5060 was in use before the file carried it;
  which building is 5054 or 5060; anything public for 5054; that the site was redeveloped or
  that any store moved (unread pages only).
