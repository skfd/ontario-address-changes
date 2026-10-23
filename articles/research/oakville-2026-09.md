# Research notes - Town of Oakville, 2026-09

Window 2026-08-12 -> 2026-09-25. Snapshots kept 9, 16, 22, 24, 25 Sep. Net +114 / -7
(rows 71,049 -> 71,156, +107). No splits, renames, renumberings, status or place-name
changes. No open or held flags for oakville. Research run 2026-10-23.

## Store facts the article leans on (verified with lookup.py / sqlite, 2026-10-23)

- Identity is synthesized from number + street + unit + 5 dp coordinates
  (`src/normalize.py`, `datasets/oakville.toml` has no stable key), so a moved dot re-keys.
- **The seven retirements are seven re-keyed points, not addresses leaving.** 155, 159, 163,
  167 Bowbeer Rd and 3481, 3485, 3487 Post Rd each closed on snapshot 30 (24 Sep) and
  reopened on 31 (25 Sep) with identical properties and a dot moved a few metres
  (moves: Bowbeer 155 4.6 m, 159 6.6, 163 4.6, 167 2.7; Post 3481 2.4, 3485 2.0,
  3487 2.0). So the 114 additions are 107 new points plus those 7.
- **107 new points, all in one cluster** within roughly 600 m of each other:
  - Farley St (new street): 37 numbers, 3250-3333; evens 3250-3326 + 3333 on 16 Sep (21),
    odds 3255-3329 on 22 Sep (16). Neighbours: 3224 John McKay Blvd 20 m, 1179 Maverick
    Way 54 m, 3360 Wolverine Path 88 m from 3250.
  - Bronwyn Rd (new street): 15 numbers 1140-1175, 14 on 16 Sep, 1172 on 22 Sep. 1155 is
    51 m from 3333 Farley St, 96 m from 3298 John McKay Blvd.
  - John McKay Blvd: 27 numbers 3233-3298 (22 Sep). Street on file since baseline with
    numbers 3014 upward (some of those last seen 8 Oct, gone on the 9 Oct update - October's story, not this one).
  - William Cutmore Blvd: 26 numbers - 3441, 3442 (22 Sep); 3325-3357 (9 numbers) and
    3399-3435 (15) on 24 Sep.
  - 3413 with no street (24 Sep): sits between 3411 and 3415 William Cutmore Blvd in the
    run (about 7 m from each); props carry only ADDRESS/LABEL/STREET_NUM = 3413, no SNAME.
    Still streetless at the 21 Oct snapshot.
  - 3365 Wolverine Path (9 Sep): fills a gap between 3364 and 3368; the month's first
    change.
- Busiest days: 22 Sep 46, 16 Sep 35, 24 Sep 25, 25 Sep 7 + 7 (the moved dots), 9 Sep 1.
- Bowbeer/Post Rd points are about 2.0-2.3 km from the cluster: 155 Bowbeer is 36 m from
  169 Petgor Path; 3485 Post Rd 30 m from 120 Settlers Rd E.

## Outside record

- **William Cutmore Boulevard** - "Named in 2020 after William Cutmore, a WWII veteran
  from Trafalgar Township who died in service." Town of Oakville, *Street Name Origin
  Index* (PDF, file dated 2026-02-12):
  https://www.oakville.ca/getmedia/2898f569-d8ba-4770-add5-daddc2b850a9/history-oakville-street-name-origins.pdf
  Confidence: high (verbatim from text extraction).
- **John McKay Boulevard** - "Named in 2022 after John McKay, a WWI veteran from Trafalgar
  Township who died in service." Same PDF. High.
- **Bowbeer Road** - "Named in 2016 after early settler William Bowbeer who owned a portion
  of the land on which the street is located (Concession 1 NDS Lot 15, Trafalgar Twp.)
  from 1824-1855." Same PDF. High. Not used as a lead; Bowbeer is only the moved dots.
- **Farley Street, Bronwyn Road** - not in the Street Name Origin Index (Feb 2026 file);
  the index lists only names with heritage significance, so absence means nothing either
  way. Web searches for either name + Oakville return nothing (only Fowley Dr, Bronte Rd
  and a Farley in NSW, Australia). **Silent.**
- **Who approves street names** - Oakville's *Street Names for Public Roads Procedure*:
  names are "agreed upon between the town and the applicant of new development lands";
  "The final decision on street naming shall rest with the Director, Transportation and
  Engineering Department, or designate." Council is involved only in renaming existing
  streets. Heritage Planning supplies names from the Veterans' and North Oakville
  Settlers' lists.
  https://oakville.ca/town-hall/policies-procedures/municipal-roads-policy/street-names-for-public-roads-procedure
  High. Explains why no council by-law turns up for a new street.
- **Neighbourhood** - a resale listing for 3306 Wolverine Path (one street over) carries
  the area label "1010 - JM Joshua Meadows":
  https://homli.ca/oakville-real-estate/3306-wolverine-path/W12985490
  Medium (real-estate board area code, not a Town designation). A search snippet called
  the house Mattamy-built in "Upper Joshua Creek", but the listing pages either hide that
  text behind registration or 403 - **not used.**
- **What is being built on Farley/Bronwyn/the John McKay and William Cutmore extensions** -
  UrbanToronto lists Mattamy's "Upper Joshua Creek" (7 buildings, Dundas St E and William
  Cutmore Blvd) and ClockWork condos nearby, but nothing ties either to these numbers,
  which are single street numbers rather than condo units. No plan of subdivision or
  draft-plan number found for the two new streets. **Silent.**
- **Bowbeer Rd / Post Rd dots moving** - nothing public; a positional edit by whoever
  maintains the layer. **Silent** (not expected to have a record).
- **3413 without a street** - nothing public. Silent.
