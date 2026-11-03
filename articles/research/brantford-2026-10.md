# Research notes - City of Brantford, 2026-10

Window 2026-09-18 -> 2026-10-29 (snapshots 24 Oct and 29 Oct). Net 55 added, 56 removed,
rows 38,999 -> 38,998. No open flag for brantford in October.

## What the store says (verified, tools/lookup.py + direct queries on data/brantford/brantford.db)

- 53 of the 55 "added" and 53 of the 56 "removed" are the same address strings with
  identical props (FULLADDRESS, POSTALCODE, STREETNAME, STREETNUM, STREETNUMIN, STREETTYPE)
  and only the point moved. Brantford has no stable row id; the tracker's synthetic key
  includes the position, so a moved point reads as one retirement and one addition.
  - 24 Oct: 37 unit points at Northland Gardens moved: 1-332 to 10-332 North Park St
    (3-46 m), 11-20 at 56 Memorial Dr (2-7 m), 53-61 at 68 Memorial Dr (3-5 m), and 62/64-71
    at 50 Hayhurst Rd (4-8 m).
  - 29 Oct: 16 Grand River Ave points between 200 and 300 moved 2-34 m (248 the largest, 34 m).
- Genuinely new: **63-50 Hayhurst Rd** (24 Oct), filling the gap between units 62 and 64 that
  the file had carried since tracking began. **238 Grand River Ave** (29 Oct), postal N3T 4Y4,
  nearest other streets 11 Leonard St (101 m) and 10 Holme St (109 m).
- Genuinely retired (29 Oct, on file since tracking began 2026-06-11):
  **220, 256 and 260 Grand River Ave**. 238's point is 34 m from where 220's was; 256 and 260
  sat at the west end of the moved run.
- The brief's four "splits" (332 North Park, 50 Hayhurst, 56 Memorial, 68 Memorial, "parent
  remains") are artefacts of the moves: the units were all on file before; only their points
  changed. The base addresses 50 Hayhurst Rd, 332 North Park St, 56 Memorial Dr and 68 Memorial
  Dr have been on file throughout (snapshot 14 onward) and still are.
- 56 Memorial's units run 11, 12, 14-20: there is no 13-56 Memorial Dr in the store at any time.

## Outside the file

- **Northland Gardens** - City of Brantford community housing.
  The City's community housing options page lists "Northland Gardens | 56-68 Memorial Dr.,
  332 North Park St., 50 Hayhurst St" (sic, Hayhurst Rd in the file).
  https://www.brantford.ca/en/living-here/community-housing-options.aspx
  The province's designated-housing-projects regulation (O. Reg. 368/11) lists
  "332 North Park St. / 50 Hayhurst Rd. / 56, 68 Memorial Dr., Brantford".
  https://www.ontario.ca/laws/regulation/110368
  Confidence: high that the four addresses are one complex (two independent sources agree).
  A search result says the City's municipal-portfolio page gives 70 family units of 2-5
  bedrooms, but that page (brantford.ca/en/living-here/housinghomeless-buildings-internaltransferreq.aspx)
  returns 404 now, so the unit count is not used.
  Nothing found on why the points moved on 24 Oct, or why unit 63 was added then.
- **220 / 238 / 256 / 260 Grand River Ave** - searched the addresses, the street with
  "development", "demolition", "site plan", "zoning", and the 2026 official-plan notices.
  Nothing found: listings for 188, 215 and 225 Grand River Ave only; a forum mention of
  "180 Grand River Ave" in a downtown condo thread with no context. The public record is
  silent on the retirements, the new 238, and the 29 Oct re-positioning.
  Watch out: Grand River Avenue in East Lansing, MI dominates searches.

## Not used

- Nearby private rental tower at 325 North Park St (North Park Tower) - a different site.
