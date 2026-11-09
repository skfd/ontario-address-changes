# Research notes — The Corporation of the County of Prince Edward, 2026-10

Window: snapshots 2026-08-20 -> 2026-10-28 (September had no change; October's five
snapshots are 10-02, 10-17, 10-19, 10-20, 10-28). 30 pull days in October, 0 failed.
No open flag for prince-edward-county (`python run.py flags`).

## What the store shows (verified against data/prince-edward-county/prince-edward-county.db)

- Points 27,575 -> 27,597 (+22). The file holds several points per address (27,597
  points for about 16,400 distinct number/street/unit/suffix combinations), typically a
  *Building* point and an *Other*/*Parcel*/*Farm 911* point a few dozen metres apart.
- 26 added points = 13 address texts x 2 points each:
  - Oct 2: 2650 County Road 13, 3098 County Road 3, 186 Walmsley Road.
  - Oct 17: 1611 County Road 15, 128 County Road 20, 2220 County Road 4, 2002 / 2026 /
    2028 / 2062 Big Island Road, 55 Mowbray Road, 91 Walmsley Extension.
  - Oct 20: 59 Lake Avenue Lane (its two points ~330 m apart).
  - 2062 Big Island Road was already on file: its two old points (Parcel, Other) were
    retired on 10-17 and two new ones (both Other) arrived within ~20 m. So 12 address
    texts are new to the file.
- 4 retired points: the two old 2062 Big Island Road points; 281 Arthur Road (Building)
  and 286 Arthur Road (Other). The same day 281 Arthur Road's *Other* point was
  renumbered 281 -> 286 at the same coordinates. Net: 281 Arthur Road left the file;
  286 Arthur Road still has two points.
- Renumbered: 80 Talbot Street -> 92 Talbot Street (Building point, same coordinates,
  10-17); 281 -> 286 Arthur Road (above).
- French Street: 50, 52, 54, 56, 58, 60 had been on file since 2026-08-20 as *Building*
  points with a number and no street name. On 10-17 each gained St_Name "French",
  St_PosTyp "Street". They sit in a line ~7 m apart on the even side, across from
  49-61 French (Parcel points). Nearest other streets: Griffin Street (78, 20 m),
  George Wright Boulevard (75, 121 m). Points with no street name: 7 -> 1.
- Walmsley: 130 Walmsley Road's two points became *Walmsley Extension* (St_PosTyp,
  10-17); 91 Walmsley Extension arrived the same day ~130 m away. First use of
  "Extension" on Walmsley in the file. 262 Walmsley Road's points became *Farm 911*
  (the month's one status change, 10-02).
- 121 Harbard Lane -> 121 Harbard Road (St_PosTyp, both points, 10-28).
- 60 and 62 Bowery Street: the "B" moved from the suffix field to the unit field and the
  plain points gained Unit A (10-28), so each now reads Units A and B. A relabel.
- 37 and 38 Lake Avenue Lane moved 159 m (10-20), to within a few metres of one of the
  new 59 Lake Avenue Lane points. Nearest other street: County Road 18 (21 m).
- 281 Taft Road gained Addtl_Loc "Driveway is off of Michael's Way" (10-28).
- Big Island Road's four new numbers are within ~300 m of each other; nearest other
  street County Road 15 at ~870 m.

## Searches

| Entity | Found | URL | Confidence |
|---|---|---|---|
| French Street, Picton (50-60) | Listings place French Street in West Meadows by Port Picton Homes; one calls it "West Meadows Trailside", the newest phase | https://www.zoocasa.com/picton-on-real-estate/49-french-st ; https://ned-burgess.c21.ca/listing/ON/Prince-Edward-County-Picton/15-French-Street-K0K-2T0/194143481 | Medium: sale listings, not the County |
| West Meadows subdivision | County file 13-T-18-501: draft plan of subdivision "south of Talbot Street in the Ward of Hallowell", 245 units in total (145 single, 6 semi, 52 apartment, 61 townhouse); status "Technical Circulation"; no street names on the page | https://www.thecounty.ca/13-t-18-501-west-meadows/ | High for the file; the page does not name French Street, so the link to these six points is via the listings |
| Why the six French Street points had no street name | Nothing found | — | Record silent |
| Big Island Road (2002, 2026, 2028, 2062) | Only sale listings; no severance, plan or notice | — | Record silent |
| Walmsley Extension | Nothing by that name; a County consent/rezoning page for 477 Walmsley Road and a heritage designation at 94 Walmsley Road, neither on the changed numbers | https://www.thecounty.ca/b38-22-z40-22-miller/ | Not used: different addresses |
| Lake Avenue Lane | No street of that name found. County site-plan file SP-06-21, Lake Avenue RV Resort & Campground: amend a 2016 site-plan agreement whose works were not finished in three years; status "Approved"; submissions Sept 2024 to 24 April 2026; drawing set filed as "1-37-Lake-Avenue-Drawing-Set-Sept10_24rev.pdf". Page gives no street address | https://www.thecounty.ca/sp-06-21-lake-avenue-rv-resort-campground/ | Medium: the filename suggests 37 Lake Avenue; nothing says why the points moved or 59 arrived |
| 92 Talbot Street / 80 Talbot Street, Picton | Nothing (results were Picton NZ / NSW) | — | Record silent |
| 281 / 286 Arthur Road | Not searched beyond the store; nothing to attach | — | Record silent |
| Harbard Lane -> Road | Not found in a search; looks like a field correction on one number | — | Record silent |
