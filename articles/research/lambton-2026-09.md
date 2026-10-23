# Research notes — County of Lambton, 2026-09

Raw findings behind `articles/researched/lambton-2026-09.md`. Notes, not prose.
Window: net measured 2026-06-25 → 2026-09-30 (store snapshots 16 → 22). Two snapshots
inside the month: 09-15 (downloaded 09-16, snapshot 21) and 09-30 (snapshot 22). The
store kept nothing between 06-25 and 09-15: snapshots 17–20 (06-26, 06-27, 06-28, 08-24)
were skipped as unchanged. Vault: 30 pull days in September, 0 failed. Research done
2026-10-23.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **SNIPPET** = seen only in a search-engine summary; the page itself could not
be fetched — do not print. **EMPTY** = searched, nothing found. **STORE** = this repo's
`data/lambton/lambton.db`, not the web.

---

## 0. Store-side findings

### The 15 September republish (held: six `technical` flags in flags.toml)

- The county republished the layer on a new schema. `datasets/lambton.toml` (2026-09-15
  comment) and the six flags (reviewed 2026-10-12, verdict technical) record it. Layer
  now has 26 fields (Add_Number, St_Name, St_PreDir, St_PreTyp, AddNum_Suf, Unit,
  full_add, Inc_Muni, pointtype, currentstatus, approveddate, activedate, ...) — FACT,
  layer JSON <https://www.lambtongis.ca/arcgis_adaptor/rest/services/OpenData/AddressPoints/MapServer/0?f=pjson>.
- Brief NET says added 826 / removed 739. That diff is NOT filtered by the held flags
  (GROSS is: added 2). 824 of the 826 are 09-15; 2 are 09-30.
- STORE: paired every 09-15 retired key with the nearest unclaimed 09-15 added key.
  **All 739 retired keys pair** with an added key for the same address text:
  686 at the same point (<1 m), 4 within 1–10 m, 49 moved 10–194 m (mostly Confederation
  Line, Petrolia Line, Shiloh Line, Brick Yard Line; e.g. 3772 Confederation Line ~160 m,
  8981 Brick Yard Line ~190 m). Key changes because the old file wrote the whole street
  ("West Parkway", "Port Franks Estate", "Highway 40") and the new one splits it
  (St_PreDir West + St_Name Parkway; St_PreTyp Highway + St_Name 40), and lettered numbers
  went from "347 A" to Add_Number 347 + Unit A. Rough split of pairs: 302 directional
  prefix, 217 prefix type, 116 suffix/unit, 104 other (incl. the moved points).
  → Nothing left the file on 09-15.
- Consequence: the brief's "new streets" Parkway (134), Franks Estate (83), Glen (27),
  O Pines (24), Franks (19), Abbey (16, = Glen Abbey Drive), 40 (4, = Highway 40),
  BLUE POINT BAY, Ferry Dock, Tahgahoning are parser artifacts of the re-split names —
  NOT searched. "Streets losing" list is the mirror image. Only Sante Drive and Scott
  Court are real debuts (both: zero rows on file before snapshot 21).
- The brief's 16 "address splits" (347/356/373/375/433/435 Kathleen Ave A–D, 505–511
  Louisa St A/B, 1126/1140 Chippewa, 25 Elmwood, 3300 St. Clair, 4580 Oil Springs...)
  are all re-labelling: e.g. `347 A Kathleen Avenue` .. `347 D` on file since snapshot 1,
  now `A-347 Kathleen Avenue City of Sarnia ON` with unit A. NOT searched; not news.
- `significant: 173` on 09-15: same NG911 field sets (ADDRESS/STNAME/... → Add_Number/
  St_Name/...) as the held events — the tail of the switch. Footer only.
- `approveddate`: every one of the 56,984 rows on 09-30 carries a 2026 value (old
  Turnberry rows read 2026-02-17), so it is not the date an address was first given.
  Printed only as "the date the file labels approved".

### Genuinely new rows: 85 on 09-15 + 2 on 09-30 = 87 = the brief's rows line (56,897 → 56,984)

- 19 of the 85 are not usable addresses: 9 rows whose whole address reads "ON"; 3 with a
  street and no number (Blackwell Road and Chrisvale Boulevard, City of Sarnia;
  Tahgahoning Road, Walpole Island @ Bkejwanong); 7 numbered 0 (four "0 St. Clair
  Parkway Aamjiwnaang", "0 Vidal Street South" Sarnia, two blank "0").
- 66 numbered addresses on 09-15:
  - **Scott Court, Village of Point Edward — 25**: 300, 301, 303, 305–316, 318–325, 327,
    329. approveddate 2026-09-09 on all 25; pointtype Driveway Entrance. `--near` 300:
    1600 Venetian Boulevard 235 m, 92 Alexandra Avenue 280 m, 99 Michigan Avenue 368 m.
  - **Turnberry Lane, Town of Plympton-Wyoming — 13**: 3808, 3810, 3814, 3816, 3820,
    3822, 3826, 3828, 3832, 3834, 3838, 3840, 3844. Even side between 3806 and 3848,
    which were already on file (as were odd 3821–3843 and 3792–3806 even, 3848–3854).
    approveddate 2026-06-10 on all 13; 3808 is pointtype Parcel Centroid. `--near` 3808:
    6732 St. Andrew's Circle 38 m, 3810 Sybil Court 66 m, 6703 Saleem Court 127 m,
    6743 Egremont Road 129 m.
  - **Sante Drive, Town of Plympton-Wyoming — 5**: 3603, 3607, 3611, 3615, 3619. New
    street to the file. approveddate 2026-06-22. `--near` 3603: 6871 Shoreside Drive
    58 m, 6884 Elizabeth Way 60 m, 3576 Rear Street 138 m.
  - 23 scattered singles/pairs across the county: Sarnia (1400 Wellington St, 610 Devine
    St, 187 Front St N, 100 Lochiel St, 1988 Lakeshore Rd), Lambton Shores (104 Coastal
    Cres, 29 Tattersall Lane, 6468 Lakeshore Rd, 5497 Huron View Ave), Warwick (6418 &
    6436 Quaker Rd, 8704 Confederation Line, 8944 Birnam Line), Enniskillen (3097 & 3197
    Oil Springs Line), Brooke-Alvinston (8017 & 8033 Shiloh Line), St. Clair (135
    Sutherland Dr, 3215 Mill St), Plympton-Wyoming (6722 Cooper St, 402 Broadway St),
    Dawn-Euphemia (7145 Aughrim Line), Aamjiwnaang (701 Scott Road). approveddates
    Feb–Sep 2026. Not researched individually.
- 2 on 09-30: **5674 Lakeshore Road, Plympton-Wyoming** (nearest 8174 Elmsley Road
  244 m) and **4544 McMillan Street, Township of Enniskillen** (4549 Shamrock St 57 m,
  4548 Keating St 86 m, 3076 Main St 100 m). Both approveddate 2026-09-29, pointtype
  Driveway Entrance, status 4 (Active).
- Nothing retired, renumbered or renamed. No status or boundary transitions.

---

## 1. Scott Court, Point Edward

- FACT: Sarnia News Today, 11 May 2026, "Work to begin on new Point Edward subdivision":
  developer Alan Merrington has signed a subdivision agreement with the Village of Point
  Edward for 21 new homes at 1600 Venetian Blvd; one-level villas, $600,000–$700,000;
  site servicing expected to begin the week of 11 May. Does not name Scott Court.
  <https://sarnianewstoday.ca/sarnia/news/2026/05/11/work-to-begin-on-new-point-edward-subdivision>
- INFERENCE: Scott Court is that project — nearest address on file is 1600 Venetian
  Boulevard (235 m). But 25 numbers ≠ 21 homes and no source names the street with the
  project. Print as a possibility with the gap stated.
- SNIPPET: ViewHomes listing "303 Scott Court Point Edward, ON N7T0A4" summarised by
  search as "an exclusive 21 home enclave", 2026 build, 2027 move-in. Page 403s to
  automated fetch. Do not print.
  <https://www.viewhomes.ca/idx/303-scott-court-point-edward-on-n7t0a4/1810014492_spid/>
- EMPTY: Point Edward council street-naming by-law for Scott Court.
- Not the Holmes Foundry redevelopment (~1,900 units, Southcoast Developments) — a
  different site; left out.

## 2. Sante Drive, Plympton-Wyoming

- FACT: Plympton-Wyoming Planning Council, 23 March 2026: public meeting on Zoning
  By-law Amendment 22 of 2026, removal of the holding symbol "for 5 lots on Sante Drive",
  and passed By-law 22 of 2026 amending By-law 97 of 2003.
  <https://www.plympton-wyoming.com/news/posts/2026-03-23-2026-03-25-planning-council-regular-council-meeting-highlights/>
- Store: exactly 5 Sante Drive addresses appeared 09-15. Confidence high that they are
  the five lots (same street, same count, same municipality).
- EMPTY: street-naming item for Sante Drive; developer.

## 3. Turnberry Lane, Plympton-Wyoming

- EMPTY: no council, planning or press item for new lots on Turnberry Lane. Town news
  for 2026 does not mention Turnberry. Other "Turnberry" hits are Barrie, Burlington,
  Morris-Turnberry and the US — wrong places.
- SNIPPET: condos.ca lists "14 - 3823 Turnberry Lane" as a condo townhouse (an address
  already on file). Not printed.
  <https://condos.ca/addresses/3823-turnberry-lane-plympton-wyoming>
- Record is silent on what the 13 even numbers are.

## 4. The schema switch

- FACT: layer field list (26 fields) from the layer JSON above. No description,
  copyright text or edit date published on the layer.
- EMPTY: any county notice, changelog or press about the republish (lambtongis.ca,
  lambtononline.ca, general search for Lambton NG911 address data).
- The county's 911 address-sign page exists (sign rules only) — not relevant.
  <https://www.lambtononline.ca/en/resident-services/911-address-signs.aspx>

## 5. The two 09-30 additions

- Not searched beyond the store: single rural/village numbers; nothing to search on.
