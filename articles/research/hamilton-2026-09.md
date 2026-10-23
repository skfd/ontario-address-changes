# Research notes - City of Hamilton, 2026-09

Window 2026-08-31 -> 2026-09-29. Snapshots kept 7, 10, 14, 23, 24, 28, 29 Sep. Net +157
(204 added, 47 removed), gross identical, 13 unit splits, no renames, renumberings or
status changes. No open flags for hamilton. 30 pull days, none failed. Research run
2026-10-23.

## Store facts the article leans on (verified with sqlite against data/hamilton/hamilton.db, 2026-10-23)

Identity is synthesized (number, street, unit plus position), so a moved point or a
respelled unit leaves under one key and arrives under another. Reconciling the net diff
row by row:

- **Genuinely new: 158.** 108 units at 467 and 479 Charlton Ave E, 31 units at 1085
  Concession 10 W, 18 units across seven small buildings, and 35 Frid St.
- **Re-keyed, not new: 46 out, 46 in.** 16 at 85 Bonaventure Dr, 13 at 75 Berkindale Dr,
  13 at 391/393 Rymal Rd W, plus four single points moved.
- **Genuinely retired: 1.** 552 Barton Street (Stoney Creek).
- 158 - 1 = +157 = rows 273,834 -> 273,991. Checks.

Details:

- **467 Charlton Ave E** (postal L8N 0B3) and **479 Charlton Ave E** (L8N 0B4): base
  addresses on file since the 9 Jun baseline. On 10 Sep each gained 54 units, numbered
  101-108, 201-210, 301-310, 401-410, 501-510, 601-606 (six floors). The third address
  of the building, **455 Charlton Ave E** (L8N 0B2), already had its 54 units at the
  baseline. Nearest other addresses: 460 Charlton Ave E (56 m), 60 Alanson St (80 m),
  196 Grant Ave, 240 Wentworth St S (~100 m from 479).
- **1085 Concession 10 W** (Flamborough, postal N0B 2J0 in the file): base point re-keyed
  27 Aug (before the window). On 14 Sep it gained 31 units: 40-45, 80, 96, 108-131 (less
  118). Units 1-106 in other numbers were already on file at the baseline. Nearest other
  address 1091 Concession 10 W (79 m); Highway No. 6 about 1.1 km.
- Small unit additions, base addresses all on file since baseline: 567 Scenic Dr units
  101, 102, 201, 202 (14 Sep; next to 77 Upper Paradise Rd, 22 m); 27 Millen Ave 1-3,
  113 Erin Ave 1-2, 211 Cochrane Rd 1-2 (14 Sep); 31 Brenlyn Ct 1-2 (28 Sep); 1565 Rymal
  Rd E 1-3 and 1569 Rymal Rd E 1-2 (29 Sep; 1565 sits 3 m from 690 Pritchard Rd).
- **35 Frid St**, new 7 Sep, postal L8P 4M3, 28 m from 45 Frid St, 71 m from 597 Main St W.
- **85 Bonaventure Dr**: units written "B 1".."B 8" and "C 1".."C 8" (with a space) last
  seen 14 Sep; "B1".."B8", "C1".."C8" from 23 Sep. Units 1-14 untouched. A respelling.
- **75 Berkindale Dr**: units 1-13 last seen 28 Sep; units A-M from 29 Sep. Base untouched.
- **393 Rymal Rd W** (base + 11 units + 391 Rymal Rd W): all last seen 31 Aug at
  -79.90735/43.2057 (391 at -79.90689), back 7 Sep with the same numbers, units and postal
  code 220 m (393) and 239 m (391) west. The brief's "parent retired" for 393 is this move.
  Now 69 m from 2 Nolan Trail. A unit row literally named "Unit" at 393 was untouched.
- Moved single points: 2255 Barton St E 69 m (24 Sep), 279 Nash Rd N 55 m (24 Sep), 561
  Concession 5 W 71 m (14 Sep), 3 Nisbet Blvd 24 m (7 Sep).
- **552 Barton Street** (Stoney Creek, L8E 2T4): on file baseline -> 31 Aug, gone 7 Sep,
  not back by 19 Oct. **26 Hewitson Road** sits 7 m from where its point was and carries
  the same postal code L8E 2T4; 556 Barton Street is 30 m away. 552 Barton Street *East*
  in the lower city is a different address and is unaffected.

## Web searches

| Entity | Found | URL | Confidence |
|---|---|---|---|
| 467 / 479 Charlton Ave E | Vista 3 Condos on Charlton, 455-479 Charlton Ave E: "6 floors / 54 units", "Built in 2020" (developer named as Van Kleef Group, single source, not used) | https://condos.ca/hamilton-city/vista-3-condos-on-charlton-455-479-charlton-ave-e | medium: listing aggregator; the 6x54 matches the file exactly |
| 203-467 Charlton Ave E | listed for sale 15 Jul 2026 (MLS X13568248), terminated 21 Sep; "5 years old" | https://condos.ca/hamilton-city/vista-3-condos-on-charlton-455-479-charlton-ave-e/unit-203-X13568248 | medium: listing page |
| 506-479 Charlton Ave E | for-sale listing using the unit address | https://www.rew.ca/properties/506-479-charlton-avenue-e-hamilton-on | medium; date not pinned |
| 467 Charlton Ave E zoning | By-law 17-203, passed 27 Sep 2017, lifts the holding "H" from the E/S-1710 multiple-dwellings zoning on 467 Charlton Ave E (file ZAH-15-051) | https://www.hamilton.ca/sites/default/files/2022-06/17-203.pdf | high: City by-law text, read from the PDF |
| 1085 Concession 10 W | Rocky Ridge Estates, "year round land lease community" in Rural Flamborough; listings for new modular bungalows on numbered/lettered lots, leasehold, $850/month; listings give postal L0R 1K0, the file N0B 2J0 | https://www.rew.ca/properties/lot-n-1085-concession-10-road-w-hamilton-on | medium: listing text |
| 1085 Concession 10 W, unit 23 | listing for a 2024-built home | https://paulbusnello.rlpburloak.ca/listing/1085-concession-10-road-w-unit-23-flamborough-ontario-40828759/ | medium (via search snippet); not used |
| 35 Frid St | nothing; nearby 45/55/95 Frid appear in a provincial corridor-lands table, 35 does not | - | silent |
| 552 Barton St (Stoney Creek) | nothing | - | silent |
| 567 Scenic Dr | nothing | - | silent |
| 393 Rymal Rd W | By-law 18-234 rezoned the site in 2018 for low-density multiple dwellings; says nothing about the 2026 point move | https://www.hamilton.ca/sites/default/files/2022-05/18-234.pdf (search snippet only) | not used: doesn't explain the move |
| 85 Bonaventure / 75 Berkindale | not searched beyond the store: a respelling and a relettering are facts about the file | - | - |
