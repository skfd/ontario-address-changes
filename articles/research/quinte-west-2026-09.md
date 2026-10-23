# Research notes — City of Quinte West, 2026-09

Raw findings behind `articles/researched/quinte-west-2026-09.md`. Notes, not prose.
Window researched: net 2026-08-25 → 2026-09-25; four snapshots kept inside the month
(09-10, 09-16, 09-19, 09-25); 30 pull days, 0 failed. Research done 2026-10-23.

Conventions: **FACT** = the linked page says it (fetched directly). **INFERENCE** = a
reading, not the source's. **SNIPPET** = seen only in a search-engine summary; the page
itself could not be fetched — do not print. **EMPTY** = searched, nothing found.

Source caveat: the layer has no stable row id (only sequential objectid/objectid_1;
GlobalID is volatile), so `datasets/quinte-west.toml` synthesizes identity from number +
street + unit + 5 dp geometry. A point moved more than ~1 m, or a changed number field,
mints a new key and shows as retired + added.

---

## 0. Store-side findings

Net 08-25 → 09-25: rows 20,298 → 20,315 (+17); added 20, removed 3; gross = net.
One split. No renames, renumberings, status, boundary or place events. No open or held
flags. August for comparison: +9 (15 in, 6 out, 3 splits).

Days: 09-10 +4/−2; 09-16 +1; 09-19 +2; 09-25 +13/−1.

**Patrick Drive, Frankford ward (09-25, 12 rows).** Before: 6–43 on file since the
tracker's first read (2026-06-10), single numbers. New: 45; ten ranges each spanning four
same-side numbers — odd 47-53, 55-61, 63-69, 71-77, 79-85, 87-93; even 74-80, 82-88,
90-96, 98-104 (the last written without spaces, "98-104"); and one point with no number,
"PATRICK DRIVE", at 44.19434, −77.59703, 55 m from 26 Diamond St and 80 m from 81 March
St. `--near 45 PATRICK DRIVE`: March St 123 m, 20 Brittany Lane 132 m, 50 Diamond St
190 m, 36 Wolfe St 190 m, 224 South Trent St 305 m.
- INFERENCE: four numbers per range reads like one number per townhouse unit, issued for
  the block as a whole. The file does not say so.

**17294 Telephone Road, Murray ward (09-10).** Plain 17294 on file 06-10 .. 08-25,
retired; units A and B began 09-10. A sits ~47 m from the old point, B ~10 m.

**396 Deer Run Road, Sidney ward (09-19 out / 09-25 in).** Old row: label "396 DEER RUN
ROAD", number field `406`. New row: label and number field both 396, identical
coordinates (44.24383, −77.61248). The number field was corrected; the tracker re-keyed
it. Not a new address.

**205 Sagers Corners Road, Sidney ward (09-10).** Old row 06-10 .. 08-25; new row 09-10,
same number, point moved ~41 m. Re-keyed, not a new address. Same day 1648
Frankford-Stirling Road arrived 62 m away (nearest other: 15 Rosebush Rd 109 m).

**Singles:** 151 Rose Rd (Sidney, 09-16); 329 Preston Hill Rd and 44 Will Johnson Rd
(Murray, 09-19).

---

## 1. Web

- **Patrick Drive blocks — FACT.** MLS X13863234 for "79-85 Patrick Dr", Frankford: "Block
  2, A Fully Serviced Residential Development Parcel", ~0.43 acres, zoned "Residential
  Type 3 Exception 23 (R3-23), Permitting Townhouse Dwellings", preliminary concept of
  "Four Townhomes On The Block"; two adjacent blocks available too, ~1.3 acres together,
  concept for twelve townhomes; "Ready For Building Permit Applications"; $480,000,
  active, last updated 2026-10-05.
  https://www.greatertorontohomepros.com/property-search/detail/211/X13863234/79-85-patrick-dr-quinte-west-on-k0k-2c0/
  Confidence: realtor marketing copy, not a City record. 79-85 is one of the ranges the
  file issued on 09-25.
- **0 Patrick Drive — SNIPPET.** C21 listing summary: 1.3-acre site "recently rezoned" to
  R3-23, three blocks, a 4-plex on each, $1.6M. Page 404s on fetch. Do not print.
- **Rezoning / plan of subdivision — EMPTY.** No quintewest.ca by-law, notice or agenda
  for Patrick Drive or R3-23 found. Ten ranges in the file vs three blocks / twelve
  townhomes in the listings: not reconciled; do not reconcile in print.
- **17294 Telephone Road — EMPTY.** No listing, permit or notice.
- **1648 Frankford-Stirling Rd, 151 Rose Rd — EMPTY.** Frankford-Stirling Road is a
  county road, formerly part of Highway 33 (Wikipedia, numbered roads in Hastings
  County) — not needed.
- **396/406 Deer Run Road — EMPTY.**
- Not searched further: Preston Hill Rd, Will Johnson Rd, Sagers Corners Rd (single
  rural numbers; nothing to tie a search to).
