# Research notes - haldimand 2026-09

Window 2026-08-26 -> 2026-09-22 (snapshots in the month: 1, 9, 12 and 22 September; 30
pull days, none failed). Haldimand's first complete month: the tracker's first read was
2026-08-20, so there is no earlier month to compare against. Net +5 (26,597 -> 26,602).
The entities checklist was empty (no new streets, no clusters of 3+, no splits, renames or
place names), so the searches were about the individual addresses.

## From the store (data/haldimand/haldimand.db, verified by query)

The layer has no stable id; the tracker keys each point on number + street + unit and its
rounded position (datasets/haldimand.toml). PCL_RN is the assessment roll number; RANK is
Primary/Secondary (26,188 Primary, 414 Secondary on 2026-09-22). ZONE_MUN is the community.
The road number of a "Haldimand Road NN" is carried in the ADDR_UN (unit) field: 225
addresses on HALDIMAND/ROAD carry "20", 6 carry "49". So "3522 HALDIMAND ROAD 20" in the
brief is the address 3522 Haldimand Road 20, not a unit 20.

- **84 Walk Road, Caledonia** - first on file 2026-09-01. Primary, Status Existing, own roll
  152005101920000 (neighbours 88/90/92/94 run 152005101430000 down to ...1400000). Fills the
  gap between 83 and 85 / 88 on Walk Road (no 86 on file). 88 Walk Rd is 22 m away. No
  FullAddress label (4,124 of 26,602 points lack one). Confidence: high (store).
- **17 Victoria Street, Hagersville** - first on file 2026-09-09. Primary, roll
  154003060020000, a separate roll that differs from 19 Victoria's (154003060000000) in two middle digits. 20 m
  from 19 Victoria St; 15 Victoria St 28 m. Confidence: high (store); what the roll suffix
  means in the world (severance) is NOT verified - no consent file found.
- **19 Victoria Street, Hagersville** - same day (2026-09-09) its point moved 9.8 m. Because
  the tracker keys on position, the brief counts this as 1 retired + 1 added. Same number,
  same roll, same label. It is the month's only "retirement". Confidence: high (store).
- **126 Concession 7 Walpole (West), Walpole** - first on file 2026-09-12. RANK Secondary,
  on the same roll (332003111000000) as 122 Concession 7 Walpole, 61 m away. Same day 122
  lost its FullAddress label ("122 CONCESSION 7 WALPOLE     WEST" -> blank) - that is the
  brief's one "Full Address" modification. Everything else on 122 unchanged.
- **151 Haldimand Road 49, Dunn** - first on file 2026-09-12. Secondary, on the roll of
  191 Haldimand Road 49 (021002216000000, Primary since the first read), 247 m away. 158
  Haldimand Road 49 is 66 m away; 189 Aikens Road 190 m.
- **3522 Haldimand Road 20, South Cayuga** - first on file 2026-09-22. Secondary, on the
  roll of 3478 Haldimand Road 20 (157001100000000, Primary since the first read). Nearest:
  3523 (94 m), 3512 (95 m).
- So: of the 6 "added", one is 19 Victoria re-keyed; of the 5 really new, 3 are Secondary
  addresses on a parcel that already had a Primary one, 2 are Primary on their own roll.
  The file does not define Primary/Secondary.

## Searches

- `"17 Victoria Street" Hagersville` - nothing for the address (8 Victoria St listings,
  other towns' 17 Victoria Sts). Silent.
- `"19 Victoria Street" Hagersville severance consent` and Committee of Adjustment
  agendas + "Victoria Street" Hagersville - nothing. A Victoria Street *Cayuga* road
  disposition notice exists; different town, not used. Silent.
- `"84 Walk Road" Caledonia`; PLB + "Walk Road" - nothing. Silent.
- `"122/126 Concession 7 Walpole"` - nothing for either number. Silent.
- `"3478/3522 Haldimand Road 20"`, `"151/191 Haldimand Road 49"` - nothing. Silent.
- 2026-09-22 Committee of Adjustment agenda
  (https://events.haldimandcounty.ca/council/detail/2026-09-22-0900-Committee-of-Adjustment)
  returns 403 to automated fetch; not checked by hand.
- Haldimand County Civic Addressing By-law 2414/23, enacted 27 March 2023
  (https://www.haldimandcounty.ca/government-administration/by-laws-and-policies/by-law-directory/civic-addressing-by-law/,
  read 2026-10-23; page says it is an unofficial digital reproduction):
  - s. 2.2.2 "No owner(s) of any lot may start construction of a building without
    obtaining the civic number or address from the County."
  - s. 2.7.1 "No building permit shall be issued without the presence of a civic address."
  - s. 2.3.1 new address assigned "when new lots or properties have been created".
  - s. 2.4.10 "Except in the case of a secondary suite, the County is not obliged to assign
    additional civic numbers" (partial quote).
  Confidence: high for the text; it says when numbers are issued in general, not why any
  of these five were.
- Haldimand County civic address page (https://www.haldimandcounty.ca/civic-addressing):
  only says owners whose property has no address can apply. Not used.
- Wikipedia "List of numbered roads in Haldimand County" names them "County Road 20/49"
  with local names (Indian Line, Aikens Road), which does not obviously square with the
  file's "Haldimand Road 20" in South Cayuga. Not used.
- Haldimand County ARU / secondary dwelling rules 2026 - only a 2024 minor variance
  agenda; nothing on the current regime. Not used.
