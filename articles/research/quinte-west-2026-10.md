# Research notes — City of Quinte West, 2026-10

Raw findings behind `articles/researched/quinte-west-2026-10.md`. Notes, not prose.
Window researched: net 2026-09-25 → 2026-10-27; five snapshots kept inside the month
(10-05, 10-07, 10-14, 10-17, 10-27); 30 pull days (10-01 .. 10-31), 0 failed.
Research done 2026-11-08.

Conventions: **FACT** = the linked page says it (fetched directly). **INFERENCE** = a
reading, not the source's. **SNIPPET** = seen only in a search-engine summary; the page
itself could not be fetched — do not print. **EMPTY** = searched, nothing found.

Source caveat (unchanged from September): the layer has no stable row id, so
`datasets/quinte-west.toml` synthesizes identity from number + street + unit + 5 dp
geometry. A point moved more than ~1 m mints a new key and shows as retired + added.

---

## 0. Store-side findings

Net 09-25 → 10-27: rows 20,315 → 20,325 (+10); added 39, removed 29; 36 ward
(boundary) changes; one split. Gross: added 40, removed 30, boundary 36. No renames,
renumberings, status or place events. No open flags for quinte-west in `run.py flags`;
no HELD events in the brief. September for comparison: +17.

Days: 10-05 0/0 + 36 ward changes; 10-07 +8; 10-14 +3/−1; 10-17 +1/−1; 10-27 +28/−28.

**Edith Lane, Sidney ward (10-27, 28 in / 28 out).** Every one of the 28 is the same
number leaving and coming back: 2–6, 8, 10–17, 19–45 odd. Old rows 06-10 .. 10-17, new
rows 10-27 .. present, same number/street/ward, new synthetic key. Points moved
1.4–12.9 m (largest: 16 at 12.9 m, 14 at 10.5 m, 17 at 10.3 m; 33–45 odd only 1.4–1.9 m).
1, 7, 9, 47–57 odd untouched. Street on file since the tracker's first read (06-10).
`--near 2 EDITH LANE`: 38 Thomas Bata Blvd 44 m, 66 Sidney Cres 122 m, 104 Fraser Dr
178 m, 100 Plant St 198 m.
- Store conclusion: 28 points nudged, no address added or retired. Excluding them, the
  month's real additions are 11 and real retirements 1.

**Birch Street, Trenton ward (10-07).** 7, 9, 11, 13 arrive together, ~6 m apart
(lon −77.57242 .. −77.5722), between 5 Birch (on file since 06-10, ~30 m west of 7)
and 15 Birch (on file since 06-10). Street otherwise 2–25, 41–49, all since 06-10.
`--near 9 BIRCH STREET`: 13 Gilmour Ct 56 m, 195 Sidney St 69 m, 10 Robert Dr 77 m,
4 Jason Cres 86 m.

**707 Foxboro-Stirling Road, Sidney ward (10-14).** Plain 707 on file 08-25 .. 10-07;
units 1 and 2 (unit_type `House`) begin 10-14. Unit 1 on the old point exactly
(44.24523, −77.48284), unit 2 ~11 m east. Nearest other address 2485
Wallbridge-Loyalist Rd, 280 m.

**300 → 378 Eggleton Road, Sidney ward.** 300 appears 10-14 and is on file for that one
snapshot; 10-17 it leaves and 378 appears at identical coordinates (44.29599,
−77.51409). One address whose number was corrected within three days. It is the whole
gap between gross (40/30) and net (39/29). Net counts 378 as one new address.

**Singles (10-07, Murray ward):** 3 Carr Rd, 379 Stoney Point Rd S, 991 Powerline Rd,
102 McMaster Rd (373 m from 991 Powerline, 199 m from 1121 English Settlement Rd).

**Real additions (11):** 7, 9, 11, 13 Birch; 707 Foxboro-Stirling units 1, 2; 3 Carr;
379 Stoney Point S; 991 Powerline; 102 McMaster; 378 Eggleton.
**Real retirement (1):** plain 707 Foxboro-Stirling (replaced by its units).

**Ward changes (10-05, 36 points, same coordinates, same keys — only `ward` changed):**
- Rosewood Drive 23–48 (20 points: 23, 25, 27, 28, 30, 32–37, 39–43, 45–48 as listed)
  Sidney → Frankford. Before: odd 5–21 Frankford, even 4–26 Sidney, 23 upward Sidney.
  After: Frankford 29, Sidney 10 (the even 4–26). INFERENCE: the street's lower half
  reads as a ward line down the centre; the upper half is now all Frankford. The file
  does not say so. `--near 40 ROSEWOOD DRIVE`: 14 Cedarwood St 60 m, 3 Sprucewood Ct
  93 m, 11 Glenwood St 98 m.
- Hamilton Road 2323, 2327, 2335, 2343, 2353, 2369, 2383, 2393 Trenton → Sidney (8);
  2223 Hamilton Rd Sidney → Trenton (1). Hamilton Rd now Sidney 175, Trenton 5.
- 57, 61, 63 North Murray St Sidney → Trenton (3).
- 122, 124, 126 River Dr Frankford → Sidney (3).
- 432 Crowe Rd Murray → Sidney (1).
- Ward totals at close: Sidney 6,878; Trenton 6,229; Murray 5,858; Frankford 1,359;
  plus one point labelled "Prince Edward" (not investigated).

---

## 1. Web

- **Edith Lane = Batawa Landing — FACT.** Listing for 8 Edith Lane, MLS X13725182,
  PG Direct Realty: "Discover Batawa Landing by Wooler Homes!", "This brand-new left
  end-unit townhome", "Townhouse", "2-Storey", listed Aug 29, 2026, $499,900.
  https://condos.ca/addresses/8-edith-lane-quinte-west and
  https://www.wahi.com/ca/en/real-estate/on/hastings/quinte-west/8-edith-lane-quinte-west-k0k1e0-ontario
  Confidence: realtor listing, two sites agree. Place: Edith Lane sits 44 m from
  Thomas Bata Blvd in the store.
  - SNIPPET: a search summary says the listing places the project "at the base of
    Batawa Ski Hill" with ICF construction. Not seen on a fetched page — do not print.
  - EMPTY: Wooler Homes' own project page did not come up; no City record of the plan.
  - Nothing found on why 28 points were re-positioned on 27 Oct.

- **5 Birch Street rezoning — FACT.** QuinteNews, Alana Cameron, Aug 22, 2025,
  "Quinte West Planning Committee approves rezoning for Birch Street housing plan":
  "Quinte West's Planning Advisory Committee has approved a rezoning application
  allowing for two townhouse structures to be built on Birch Street." "The development
  at 5 Birch Street would see the construction of one five-unit building and another
  containing four units." https://www.quintenews.com/?p=364656
  Developer not named; meeting "Thursday" (date not stated). No mention of 7–13.
  - Staff report 25-066PD: https://quintewest.civicweb.net/document/150685/25-066PD.pdf
    is a scanned PDF with no text layer — unread. Applicant, zone, lot arrangement and
    addressing unknown.
  - SNIPPET: a RE/MAX listing for 5 Birch St as vacant land "suited to multi-unit
    residential use" (2023 tax). Not fetched — do not print.
  - INFERENCE: four new numbers right beside 5 Birch, four units in one of the two
    approved blocks. Nothing public ties the numbers to the rezoning. Five more numbers
    would match the other block; none arrived.

- **707 Foxboro-Stirling Road — EMPTY.** Search found only other numbers on the road.

- **Ward changes — mostly EMPTY.**
  - No 2026 ward boundary review for Quinte West found.
  - FACT: Quinte West's municipal election day was Oct. 26, 2026 (quintewestvotes.ca,
    posted 2026-03-26): https://quintewestvotes.ca/quinte-west-votes-what-you-need-to-know-ahead-of-the-2026-municipal-election/
    The page says nothing about ward boundaries or address assignments.
  - SNIPPET: search summary says wards are Trenton (5 councillors), Sidney (4), Murray
    (2), Frankford (1) — not fetched; do not print.
  - SNIPPET: realtor listings for 19, 34, 37, 40 Rosewood Dr label them "Frankford
    Ward" — pages 403/410 on fetch; do not print.
  - City ward map page (quintewest.ca/council-city-administration/ward-map/) 403s.

- **Carr, Stoney Point S, Powerline, McMaster, Eggleton singles — not searched beyond
  the road names**; rural single numbers, no expectation of a public record.
