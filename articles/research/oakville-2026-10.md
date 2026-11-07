# Research notes - Town of Oakville, 2026-10

Window 2026-09-25 -> 2026-10-30. Snapshots kept 7, 8, 9, 21, 24, 28, 30 Oct (3-6 Oct and
the other days were identical reads). Net +113 / -53 (rows 71,156 -> 71,216, +60); gross
equals net. Brief: 2 splits, 0 renames, 0 renumberings, 1 full-address modification. No
open or held flags for oakville. 30 pull days, none failed. Research run 2026-11-07.

## Store facts the article leans on (verified with lookup.py / sqlite, 2026-11-07)

- Identity is synthesized from number + street + unit + 5 dp coordinates
  (`src/normalize.py` `_identity`; `datasets/oakville.toml` has no stable key), so a moved
  dot re-keys and reads as one retirement plus one addition. Second month running.
- **44 of the 53 retirements are re-keyed points, not addresses leaving.** Each has an
  addition with the same number, street and unit, its dot moved 0.8-6.4 m. 43 of them on
  the 9 Oct update, one (133 East St, 0.8 m) on 7 Oct:
  - John McKay Blvd: 3014, 3016, 3018, 3020, 3022, 3029, 3038, 3040, 3045, 3067, 3069,
    3073, 3075, 3077, 3079 (6.4 m, the largest), plus 3070 Units 2, 3, 4, 8, 9, 10, 16, 17
  - Dartmouth Cres: 1162-1174 evens (7), plus 1220 Units 12, 13, 15, 16
  - Wheat Boom Dr 1082, 1084, 1154; Milland Dr 1195, 1197; Robert Lamb Blvd 3079, 3081;
    Meadowridge Dr 3201, 3203; East St 133
  - On the unit rows the label also changed "UNIT 12" -> "Unit 12"; 1082 Wheat Boom Dr was
    "1082WHEAT BOOM DR" (no space) before and is spelled correctly after. The brief's
    "Other modifications: 1 Full Address" is 1220 Dartmouth Cres Unit 14, restyled the same
    way without a move.
  - **The brief's two "splits"** (3070 John McKay -> 8 units, 1220 Dartmouth -> 4 units) are
    exactly these unit rows; all have been on file since the 2026-06-10 baseline. No
    building was subdivided.
- **69 genuine additions, 9 genuine retirements.**
- **Eclipse Ave + Post Rd, 28 Oct, one block.** All 52 of the day's additions:
  Eclipse Ave (new street) 29 even numbers 52-114 (no 68, 84, 102); Post Rd 23 odd numbers
  3529-3579 (no 3539, 3553, 3567), continuing a run that stopped at 3525 (3497-3525 on
  file since baseline, 3500 since snapshot 23). 114 Eclipse is 50 m from 3529 Post Rd;
  3454 Vernon Powell Dr 51 m from 3529 Post; 52 Eclipse is 109 m from 40 Burnhamthorpe
  Rd E and 191 m from 3500 Post Rd.
- **2365-2377 Lakeshore Rd W -> 2375.** 2365, 2367, 2369, 2371, 2373, 2377 last on the
  25 Sep snapshot, gone on 7 Oct; 2375 (never on file before) appears 7 Oct, 18.5 m from
  where 2377 sat and 28 m from 2365. Neighbours 2361 and 2381 unchanged. Near 96 Nelson St
  (60 m), 103 Jones St (89 m).
- **Three number changes at the same point** (brief misses them: the number is in the key):
  - 234 Cardinal Dr -> 236 (last 8 Oct, first 9 Oct, 0 m). Street has 230, 231, 235,
    238, 239; no 236 before.
  - 2485 Plymouth Dr -> 2845 (2485 on file from 6 Aug, gone 21 Oct; 2845 from 21 Oct,
    identical coordinates). Neighbours 2830, 2860, 2871, 2880 - 2845 fits the block, 2485
    did not. The file does not say it was a correction. (2485 Badger Cres also arrived
    21 Oct - unrelated, another street.)
  - 208 Tilford Rd -> 210 (208 last 28 Oct, 210 from 30 Oct, 0 m). Street has 205, 216.
- Singles: 350 Randall St (8 Oct); 3430 William Cutmore Blvd, 1179, 1187, 1195 Maverick
  Way, 3347 Wolverine Path, 3325 Dove Dr, 3358 Wrybill Path (9 Oct); 2523 Littlefield
  Cres, 2485 Badger Cres (21 Oct); 500 Burnhamthorpe Rd E (24 Oct, no neighbours returned
  by `--near`; 43.50632, -79.73284); 1166 Bronwyn Rd, 3240 John McKay Blvd (30 Oct).
- **Correction to September's piece:** it placed 3250 Farley St "about 50 [m] from 1179
  Maverick Way", but 1179 Maverick Way first reached the file on 9 Oct 2026. The distance
  is real, the neighbour was not yet on file on 16 Sep. Not restated in October's article.
- 3413 (William Cutmore run, no street name) still streetless on the 30 Oct snapshot.

## Outside record

- **Graywood Bronte Village, 2365 to 2377 Lakeshore Road West** - Town of Oakville site
  plan application, file 1729.075/01: "Seven storey mid-rise building containing 618 m2
  of retail space and 157 residential condominium units." Submissions July 2022 through
  December 2024; no status or decision on the page.
  https://www.oakville.ca/business-development/planning-development/active-development-applications/ward-1-development-and-site-plan-applications/graywood-bronte-village-2365-to-2377-lakeshore-road-west-1729-075-01/
  High (Town page, read via fetch).
- **Claystone at 2375 Lakeshore Rd W** - the same project marketed by Graywood as
  "Claystone"; listing aggregators put it at 2375 Lakeshore Rd W, 7 storeys, 141 units:
  https://condos.ca/oakville/claystone-condos-2375-lakeshore-rd-w ,
  https://strata.ca/oakville/2375-lakeshore-road-west-claystone-condos
  Medium (aggregators; unit counts disagree: 138 in Graywood's 2021 release, 141 here,
  157 on the Town page - article uses only the Town description). UrbanToronto thread
  (https://urbantoronto.ca/forum/threads/33055) quotes a Graywood release on the Sept
  2021 purchase and a RENX piece (Oct 2025) saying the developer wanted to be "in the
  ground" in the back half of 2026 - a plan, not a confirmed start. Construction status
  unconfirmed (strata.ca says completed 2025, precondo.ca says occupancy 2028). **No
  source for demolition.** Not used beyond the address link.
- **Eclipse Ave** - no web result for an Eclipse Avenue in Oakville (only Mississauga's
  Churchill Meadows and US streets). Street Name Origin Index not re-checked this month.
  Oakville names new streets by staff decision under its Street Names for Public Roads
  Procedure, so no council by-law is expected:
  https://oakville.ca/town-hall/policies-procedures/municipal-roads-policy/street-names-for-public-roads-procedure
  **Silent** on the name's origin and the plan of subdivision.
- **Post Rd 3529-3579** - listing sites already carry pages for 3561 and 3573 Post Road
  as three-storey row townhouses ("Att/Row/Twnhouse", "Rural Oakville"), no dates, no
  builder: https://condos.ca/oakville/3561-post-road-oakville ,
  https://condos.ca/oakville/3573-post-road-oakville . Medium; no dates, so nothing
  about the file lagging the world can be said. Builder: **silent.**
- **500 Burnhamthorpe Rd E** - nothing public for the address. The new HDSB secondary
  school near Sixth Line is at 4020 Sixth Line (formerly 103 Burnhamthorpe Rd W), not
  this point: https://www.hdsb.ca/schools/landing-pages/new-oakville-secondary-school/
  **Silent**; not used.
- **Renumberings (Cardinal, Plymouth, Tilford)** - not searched beyond the store; no
  public record expected for a number change. Silent.
- **44 moved dots** - positional edit by whoever maintains the layer; no public record.
  Silent.
