# Research notes — County of Lennox and Addington, 2026-10

Raw findings behind `articles/researched/lennox-addington-2026-10.md`. Notes, not prose.
Window: net 2026-09-25 → 2026-10-29; eleven snapshots inside the month (10-07, 10-09,
10-14, 10-21, 10-22, 10-23, 10-24, 10-26, 10-27, 10-28, 10-29); 30 pull days
(10-01 .. 10-31), 0 failed. No open flags for lennox-addington; nothing HELD. Research
done 2026-11-07.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found.

Identity: `key_field = ""`, so identity is synthesized from the full address (and the
point moves the key too: three same-address points nudged a few metres show as one
retirement + one addition each).

---

## 0. Store-side findings

Net: rows 26,172 → 26,249 (+77); brief says added 82, removed 5, 4 split events.
Gross 84 added / 7 removed / "34 renumbered".

Municipality (BELL_MUNIC) of the 82 net additions: 80 Greater Napanee, 2 Stone Mills.

Re-keyed moves (same address, out and back in, counted in both 82 and 5):
- 268 Newburgh Road, last on 10-24, new point 10-26, ~7 m away.
- 278 Camden Road, last on 10-26, new point 10-27, ~4 m away.
- 74 South Shore Drive (Stone Mills), last on 10-28, new point 10-29, ~43 m west.
So 79 genuinely new address strings; 2 genuine departures.

Genuine departures:
- "Unassigned Nugent Road", Stone Mills, ADD_LABEL "Unknown" — a placeholder; on file
  since June, last on 10-07, gone 10-09.
- A Stone Mills point carrying only Number 1653, no street, on file since June. On 10-09
  it gained ADDRESS "1653" (new key → in/out), and was gone by 10-14. Never had a street.

Came and went inside the month (the gross–net gap): the 1653 version above (10-09 only),
and a point with only `Number: 3` on 10-21 at the coordinates of 3 Bash Avenue, which was
3 Bash Avenue from 10-22.

Bash Avenue (39 active, numbers 1–56, both sides): 1 Bash Avenue 10-21; 34 more 10-22;
4 more 10-23. The 34 from 10-22 have no ADD_LABEL on 10-22; on 10-23 the same
identity_keys reopen with ADD_LABEL set. That is the brief's gross "renumbered 34" — a
label field filled in, no number changed. Net renumbered 0.

Bristol Crescent: 21 addresses, odd 1–41, all 10-24. 1 Bristol Crescent is 26 m from
56 Bash Avenue; 39 Bristol Crescent 85 m from 1 Bash Avenue — the two streets are one
patch.

`lookup.py --near "1 Bash Avenue"`: 63 Old Hamburg Road 80 m, 29 Champlain Street 207 m,
16 Oke Road 213 m, 8300 County Road 2 278 m. Other streets in the box: Parks Street,
Yeomans Street. No Dickson or Springside street in the store.

Splits:
- 164 and 168 Heritage Park Drive: A and B for each on 10-24; 164 and 168 on file since
  June (still there). Nearest to 272 Newburgh: 1-144 Heritage Park Drive 69 m.
- 276 Camden Road: 276, 276A, 276B, 276C all new on 10-27. No plain 276 before
  (brief's "parent remains" is misleading).
- 278 Camden Road: 278A, 278B, 278C new 10-27; 278 re-keyed ~4 m the same day (brief's
  "parent retired" is a tracker artefact; 278 is on file at month end).
- Near 276 Camden: 156A Church Street 38 m, 151 Dairy Avenue 49 m, 177 Queen Street 69 m.

Newburgh Road: 270, 272, 274 new 10-26 (with 268 re-keyed); 235 new 10-28.

Singles: 331 Stone Hedge Road 10-07; 1493 Roblin Road 10-26; 3250 County Road 9 10-29
(all Greater Napanee). 66 South Shore Drive, Stone Mills, 10-29 (with 74 re-keyed; near
5 Cherry Lane).

---

## 1. Bash Avenue / Springside Meadows

- **FACT** BASH Developments launched Springside Meadows, "a new master-planned
  residential community in the east end of Napanee", with a ribbon-cutting in January
  2026; "mostly complete, with more than 10 model homes under construction".
  https://www.napaneetoday.ca/?p=95340 (Napanee Today / 88.7 myFM, 2026-01-26).
- **FACT** Kingstonist, 2024-04-29: Springside Meadows "will begin with close to 600 homes",
  first move-ins expected 2025 and early 2026. https://www.kingstonist.com/?p=167322
- **FACT** Agent listing: developed by "BASH & Best Home Developments"; "just around the
  corner from Springside Park and riverside trail".
  https://joanne-holmes.c21.ca/springside-meadows
- **FACT** Town's approved street-name inventory (Feb 2025) lists Dickson with preferred
  location "Springside Meadows Subdivision" (Richard George Dickson once owned the land).
  Bash is not on the list.
  https://media-001-ca.cdn.govstack.com/greaternapanee-003-ca/media/inpprfyp/approved-street-names-list-as-of-february-2025.pdf
- **EMPTY** No source names Bash Avenue, ties it to Springside Meadows, or gives the
  subdivision's roads. No by-law naming Bash Avenue found.
- **INFERENCE (not printed as fact)** The street name matches the developer's name; the
  location is consistent with "east end". Article states the coincidence and the silence.

## 2. Bristol Crescent

- **FACT** "Bristol / Person / Edmund James Bristol was born in Napanee in 1861. He was
  elected as MP (Toronto riding) in 1905, and re-elected five times." On the Town's
  approved inventory (Feb 2025, PDF above), no preferred location given.
- **FACT** Kingstonist 2025-02-03, proposed-names list incl. Bristol; council to approve the
  directory on 2025-02-25. https://www.kingstonist.com/?p=188101
- **FACT** Town's street-naming page: names approved and "waiting for allocation to new
  streets". https://greaternapanee-003-ca.govstack.com/build/street-naming
- **EMPTY** No by-law or listing for a Bristol Crescent in Napanee (only North Grenville's).

## 3. Camden Road 276/278, Heritage Park Drive 164/168, Newburgh Road

- **EMPTY** "276 Camden Road" / "278 Camden Road" Napanee: nothing (listings for 170, 283,
  191-193 only).
- **EMPTY** 164 / 168 Heritage Park Drive: nothing. Listings show townhouses on the street
  (192, 198, 202 Selkirk Lifestyle Homes) — not used.
- **EMPTY** Newburgh Road 268–274, 235: not searched beyond the general pass; nothing.

## 4. Other searches

- Bridge Street Meadows (PLSUBD 2022 080, BASH, 16.4 ha) — different site
  (Bridge Street West); not used.
- Limestone Ridge, 124 Old Hamburg Road rezoning (2022) — no tie to these streets found;
  not used.
