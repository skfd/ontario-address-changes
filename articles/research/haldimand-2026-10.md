# Research notes - haldimand 2026-10

Window 2026-09-22 -> 2026-10-22 (snapshots in the month: 7, 17 and 22 October; 30 pull days,
none failed). Net -1 (26,602 -> 26,601); brief says 3 added, 4 removed, gross = net. No open
flag for haldimand in `run.py flags`. The entities checklist was empty, so the searches were
about the individual addresses.

## From the store and raw pulls (data/haldimand/haldimand.db; vault pulls of 07 and 22 Oct)

Identity is synthesized from number + street + unit and rounded position (datasets/haldimand.toml),
so a changed number field reads as one retired + one added. All three "added" rows sit on the
exact coordinates of a "retired" row. Only the fourth retirement has no partner.

PCL_RN has been ignored since 2026-10-23 and is not in the store props; rolls below were read
from the raw pulls (the 07 Oct pull is cold, dumped to a temp folder, not thawed).

- **1544 Concession 12 Townsend, Townsend** - two records on file since the first read, 315 m
  apart, both Primary/Existing, same label, same roll 339080172000000 (07 Oct pull). The one at
  42.90483, -80.15964 last appears on 07 Oct and is gone on 17 Oct; the one at 42.90659, -80.15661
  (about 315 m north-east) stays. So a record left, not an address. Confidence: high (store, pull).
- **212 Cross Street East, Dunnville** - 7 Oct. A point with street and no number (42.90628,
  -79.6111, on file since the first read) got number 212 at the same coordinates. Roll
  024005059020000 on the 07 Oct pull. Nearest: 625 Tamarac St 48 m, 201 Forest St E 70 m. Next
  numbers on Cross St E above 180: 181, 205. A separate 212 Cross St West is on file, about 660 m
  away. Confidence: high (store). Whether the unnumbered point had the roll before 7 Oct: not read.
- **1A Nairne Street, Caledonia** - 22 Oct. ADDR_HN "1A" became ADDR_HN "1" + ADDR_PT "A", same
  coordinates, same roll 151002291100000. Plain 1 Nairne is 24 m away on roll 151002291000000.
  No FullAddress label before or after. The tracker's number field is ADDR_HN, so its reports
  show "1 NAIRNE". Confidence: high.
- **172C King Street East, Hagersville** - 22 Oct. Same change: ADDR_HN "172C" became "172" +
  ADDR_PT "C", same coordinates. No roll on either side. Two plain 172 King St E records sit 23
  and 26 m away, about 11 m apart, on rolls 159007198620000 and 159007198630000, both unchanged.
  No 172A or 172B has ever been on file (store, all spans). Confidence: high.
- **File-wide, 22 Oct:** ADDR_PT holds a letter on 19 records (A 7, B 11, C 1) and THE on 6 (The
  Esplanade, Dunn). 50 records keep a digit+letter in ADDR_HN: 46 at 68A Main St N, Hagersville,
  plus 37A Talbot St E, 1A Helen, 38A Buchanan, 66A Oswego Park. 2,425 records have no number. 451
  numbered addresses, matched on number, letter, street, direction, unit and community, are on
  more than one record (969 records), including 172 King St E.
- After the window: the 4 Nov snapshot drops a street-only North Shore Drive point in Moulton.
  November's, not used.

## Searches

- `"1544 Concession 12 Townsend" Haldimand` - nothing for the number. Hits are 954 Concession 12
  Townsend, listed in Norfolk County: wrong place, not used. Silent.
- `"212 Cross Street East" Dunnville` (twice) - listings for 108-152 Cross St E only. Silent.
- `"1A Nairne Street" Caledonia` - nothing; 125 Nairne St only. Silent.
- `"172C King Street East" / "172 King Street East" Hagersville` - nothing for 172C.
  **172B King St E**: sold listing, MLS 40622219, "all brick semi on the edge of Hagersville",
  built 1998 (https://richardrutkowski.evrealestate.com/sold-listing/detail/1174942877/address).
  Sold date blank on the page; page also says "New Construction Yes", a data error. Neither 172A
  nor 172C mentioned. Coldwell Banker copy of the listing 404s. A detached "172 King St E" was
  listed in 2026 at $569,900 (Busnello, Wahi); unclear how it relates, not used. Confidence:
  medium, a listing, used only to say the name exists outside the file.
- Civic Addressing By-law 2414/23, enacted 27 March 2023
  (https://www.haldimandcounty.ca/government-administration/by-laws-and-policies/by-law-directory/civic-addressing-by-law/,
  unofficial digital reproduction, read 2026-11-04):
  - s. 2.4.4 "Civic number may have a letter suffix if there is insufficient supply of numbers."
  - s. 2.5.1 "The County may change or reassign civic numbers to keep consistency..."; "Affected
    landowners shall be notified in advance of any changes."
  - No provision on duplicate civic numbers (s. 3.1.6 covers duplicate road names only).
  Confidence: high for the text; it says nothing about any of these four.
- `Haldimand County NG911 civic address data readiness` - the layer's name is NG911AddressPoints
  and the County became an NG911 community on 2026-03-04
  (https://www.haldimandcounty.ca/news/posts/haldimand-county-is-now-a-next-generation-911-community/),
  but the page does not mention address data. Nothing ties October's edits to NG911. Not used.
- Haldimand Press, 2025-05-08, "County address issue in emergency call system resolved"
  (https://haldimandpress.com/county-address-issue-in-emergency-call-system-resolved/): a phone
  system registration fix at the County Administration Building per the visible teaser. Not
  address data, not used.
