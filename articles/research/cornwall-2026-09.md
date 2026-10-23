# Research notes - City of Cornwall, 2026-09

Window 2026-08-22 -> 2026-09-25. Snapshots kept 9, 10, 11, 12, 14, 16, 25 Sep. Net +48
(50 added, 2 removed), 6 unit splits, 12 location moves, 23 postal-code edits. No open
flags for cornwall. 30 pull days, none failed. Research run 2026-10-23.

## Store facts the article leans on (verified with lookup.py / sqlite, 2026-10-23)

- **501 Tenth St E** (AddressID 24358) is itself new on 11 Sep, together with Units 1-16
  (AddressIDs 24359-24374). The brief's "parent remains" means the base row is on file
  alongside the units; it was not on file before September. FLOOR values: units 1, 2, 9,
  10 on floor -1; 3, 4, 11, 12 on 1; 5, 6, 13, 14 on 2; 7, 8, 15, 16 on 3 - four units to
  each of four levels. Postal K6H 2X6.
- **933 Marlborough St** (on file since the 11 Jun baseline) gained Units 1, 2, 3 and D on
  11 Sep. Unit 2 is FLOOR 2, the rest FLOOR 1. No unit A, B or C. 22 m from Unit 1 of 501
  Tenth St E.
- **950 Marlborough St** (on file since baseline, with a Unit A) gained Units 1-11 on
  11 Sep; base point moved 27 m and Unit A 6 m the same day. The eleven unit points run in
  an even line, about 64 m end to end (lon -74.72532 to -74.72613). Postal K6H 3Y9.
- **489 Pacific Av**, new 11 Sep, 42 m from 930 Marlborough St.
- So on 11 Sep, 33 new addresses landed within about 150 m of each other around Tenth St E
  / Marlborough St / Pacific Av (17 + 4 + 11 + 1).
- **600 Tenth St E** gained Units A-D on 11 Sep, base point moved 9 m; 25 m from 1005
  McConnell Av, so a block or two east of the cluster above.
- **215 Saunders Dr** gained Units 1-7 on 12 Sep, all FLOOR 1; base on file since baseline.
  Nearest other streets: 2215 Second St W (96 m), 24 Blackadder Dr (130 m).
- **105 Emma Av** gained Units A-C on 25 Sep (base re-keyed 16->25 Sep, 6 m move); near
  14 Eva Av and 1730 Pitt St.
- **Mauricy St**: on 16 Sep all 24 rows on the street carrying K6K 0B7 were rewritten.
  23 now read K6K 0A1, and 3190 reads **K6K 0C2**. 23 of the 24 kept their AddressID and
  are the brief's 23 postal edits; 3166 is one of them. 3181 came back under a new AddressID (24084 -> 24085), which
  is why it is both the month's one Mauricy "retirement" and one of its "additions". The
  brief splits the 23 edits as 21 POSTAL + 2 Location;POSTAL; the two with a location
  component were not pinned down, and the article does not split them.
- **A second "3166 Mauricy St"**: on 16 Sep a point appeared labelled `3166 MAURICY ST`
  whose ST_NUMBER field reads **3170**, AddressID 0, ~13 m from the existing 3166
  (AddressID 23718, still on file). On 25 Sep it was reissued with AddressID 24387, same
  label, same 3170 number field. No row labelled 3170 Mauricy exists. Still the case at
  the 23 Oct snapshot.
- **2801 Montreal Rd** new 10 Sep; 2800 on file since baseline.
- **409 Montreal Rd** retired 11 Sep; 407 next door moved 4 m and re-keyed the same day.
  File does not say whether they were merged.
- Total on file 20,647 -> 20,695.

## Web searches

| Entity | Found | URL | Confidence |
|---|---|---|---|
| 501 Tenth St E | nothing | - | searched address in quotes; only unrelated Eleventh St E hits |
| 950 Marlborough St / Tenth-Marlborough development | nothing for Cornwall ON (a "950 Marlborough Street" hit is Philadelphia) | - | silent |
| 215 Saunders Dr | nothing; a 2021 City year-in-review mentions Falcon Homes building in the "Saunders" subdivision | https://choosecornwall.ca/cornwall-year-in-review-2021 | low: a subdivision name, not this address; not used |
| Mauricy St | real-estate listings put new bungalows on Mauricy St in the "Northwoods Forest Subdivision", builder J.F. Markell Homes, postal K6K 0A1 | https://www.viewhomes.ca/idx/3149-mauricy-street-cornwall-on-k6k0a1/1800254383_spid/ (search snippet; page 403s to fetch) ; keyhomes.ca/property/ontario/cornwall/29603983 (410 Gone) | medium: listing text, seen via search snippet only |
| 3190 Mauricy St | a listing URL gives K6K0A1; the file gives K6K 0C2 | https://www.viewhomes.ca/idx/3190-mauricy-street-cornwall-on-k6k0a1/1808819836_spid/ | listing vs file disagree; noted, not resolved |
| "Cornwall HAF progress report Jan 2026" | **wrong Cornwall** (Town of Cornwall, PEI) | cornwallpe.ca | discarded |

The City of Cornwall's planning applications were not reachable by search for any of
these addresses. Every "why" in the month is silent in the public record.
