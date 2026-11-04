# Research notes - City of Greater Sudbury, 2026-10

Window: net 2026-09-30 -> 2026-10-24, 9 snapshots, 30 pull days (10-01 .. 10-31), 0 failed.
Rows 70,126 -> 70,178 (+52). No held events. No open flag for this city in the month.
The file did not change after 10-24 (snapshots 126 on are skipped pulls).

## Store facts (verified with lookup.py / direct queries on data/greater-sudbury/greater-sudbury.db)

- **Eight downtown points Active -> Retired on the 2026-10-21 snapshot**: 300, 324, 326 Elgin Street;
  214, 241, 243, 247 Shaughnessy Street; 196 Van Horne Street. All on file as Active since 2026-06-11,
  none removed. 326 Elgin still carries NAME Neighbourhood Action Project of Sudbury; 196 Van Horne
  still carries NAME Sudbury Multicultural Folk Centre.
- **Already Retired when tracking began (2026-06-11)**: 153 and 161 Brady Street, 219 and 221
  Shaughnessy Street, 170 Van Horne Street, 212 and 222 Minto Street, 212 Romanet Lane, 187
  Shaughnessy Street (NAME Wacky Wings). The first eight are on the council's 2023 resolutions list.
- **200 Minto Street** - parent 111042 on file since 06-11, no type. On 10-21 two children appeared
  (112661, 112662), UNIT_AMENITY_TYPE Government, Unit, ASSIGNEDADDRESSID 111042, at 46.48774,-80.99065
  and 46.48766,-80.99064, about 110 m from the parent. `--near 241 Shaughnessy`: 200 Minto 17 m.
- **Other Active -> Retired**: 30 Cypress Street (104235, 10-15; three other points labelled 30 Cypress
  stay Active, two named Sudbury Indoor Tennis Centre and Queens Athletic Field), 409 Spruce Street
  (10-17), 25 Savard Road (47740, 10-21). That makes the brief's 11.
- **Apartments units**: 31 of the 52 additions are UNIT_AMENITY_TYPE Apartments, all with the parent
  still Active. 26 on 10-07, 5 on 10-21 (the 7 October total of 27 additions includes plain 4053
  Larocque Avenue).
  - Three children each, 10-07: 1677 Bancroft Drive, 3368 Falconbridge Road (Garson), 213 Hillsboro
    Avenue, 50 Mikkola Road (Lively), 4307 Odile Street (Hanmer), 22 Oja Street (Naughton).
  - Two each, 10-07: 59 Teravista Way, 58 Westview Crescent (Lively).
  - One each, 10-07: 17 Colette Street, 4472 Gerard Court, 2981 and 2983 Ruby Street.
  - One each, 10-21: 1298 Cawthorpe, 1009 Chapman, 319 Moonlight, 1189 Rideau, 192 Shelley.
  - 4307 Odile parent (110180) went Pending -> Active on 10-07, the same snapshot as its three units.
  - 4472 Gerard Court child 112561 has ASSIGNEDADDRESSID 110800, not its address's 110880. Not used.
  - New Apartments points by month: July 12, August 9, September 8, October 31.
- **Rockwood Drive** - 2802, 2804, 2806, 2808, 2810, 2812, 2814, all 10-16, no unit or type, one line
  about 7 m apart. 2782-2792 (even) on file since 06-11 on the same line at about the same spacing.
  `--near 2802`: 63 Napa Valley Drive 41 m, 2772 Joseph Street 87 m.
- **Savard Road, Wahnapitae** - 17, 23, 27 added 10-21. Two points labelled 25: 47740 Active -> Retired,
  96053 Retired -> Active, both 10-21, about 11 m apart. 27 sits about 4 m from retired 47740.
  0 Savard Road (112666) added Active 10-21, Retired 10-22; it counts among the 52.
- **226 Kukagami Lake Road** - two points labelled 226 became 226 A (48297) and 226 B (101332) on 10-07,
  beside the existing 226 C (48298).
- **Names, 10-21**: 147 Lorne U Floor Me Ltd -> Top Glove Boxing; 149 Lorne Sonic Northern Electronic ->
  Johnny D; 151 Lorne Sudbury Tire -> blank; 220 Victoria GCR Tire Centre -> blank. **10-22**: 3098
  Falconbridge Road point 3808 The Beer Store -> Next Golf, one of 16 named points at that number,
  COMMUNITY Garson. **10-17**: 59 Eyre Spruce Pinto -> Spruce Pinto foods.
- **Thirteen unnumbered or mine-site points** on Strathcona Mine Road, West Morgan Lake and 117 Mine
  Road: COMMUNITY Sudbury -> blank and moved, all 10-21. Largest moves 521, 295, 286, 171, 166, 106 m.
  One (50877) is typed Mining Operations, named Falconbridge. This is the brief's COMMUNITY; Location
  set, so these are not in its location count.
- **Coordinate edits**: 253 points ended the month at different coordinates. 236 moved under the 10 m
  floor (median 2.7 m), most on Regent, Whittaker, Albinson, Elm, Pine and Oak; by snapshot 10-08 26,
  10-15 29, 10-17 22, 10-21 11, 10-22 62, 10-24 82, 10-07 4. Store-derived, not a brief line.
- **Biggest net moves** (brief): 336 Bodson Drive West 151 m (10-22), 233 Elgin Street 35 m (104194,
  one of six points so labelled), 2264 Hanmer Lake Road 18 m, 2500 Dube Road 11 m, 144 Pine 11 m,
  381 Pine 10 m.
- **Gross vs net**: 53 vs 52 additions. Blank record 112541 (alternate names Municipal Road 55 / Regional
  Road 55) appeared and left on 10-02, a single-snapshot row with no address text.

## Searches

| Entity | Found | URL | Confidence |
|---|---|---|---|
| 300 Elgin Street | The former Ledo Hotel; demolition set to begin 8 Jan 2024, four weeks expected; "one of a number" of properties acquired "to advance redevelopment in the downtown south district" (City, 2 Jan 2024) | https://www.greatersudbury.ca/city-hall/news-and-public-notices/2024/demolition-begins-on-ledo-hotel-as-part-of-downtown-redevelopment-process/ | Read. Link2Build (10 Jan 2024) says it started on the 8th: https://www.link2build.ca/news/posts/sudbury-kicks-off-downtown-redevelopment-with-ledo-hotel-demolition/ |
| 324-326 Elgin, 241-243 and 247 Shaughnessy | Listed with 300 Elgin under "Previously acquired properties and signed agreements"; "funded through the previously borrowed Event Centre capital funds". Says acquired; never says demolished | https://www.greatersudbury.ca/city-hall/news-and-public-notices/2023/city-council-meeting-wrap-up-october-24-2023/ | Read |
| 153/161 Brady, 219-221 Shaughnessy, 170 Van Horne, 212/222 Minto, 212 Romanet Lane | On the resolutions list, same page. 151 Brady and 211 Shaughnessy also listed; not checked in the store | same | Read |
| 196 Van Horne Street | Headline: "City cleared to buy/demolish 196 Van Horne St. for $500K". Snippet of a second piece says the folk arts group left, in the building since 1984 | https://www.sudbury.com/city-hall/city-cleared-to-buydemolish-196-van-horne-st-for-500k-8377115 ; https://Sudbury.com/local-news/multicultural-group-vacate-longtime-downtown-headquarters-8548501 | Search excerpts only, both 403 on fetch. Article keeps to the headline |
| 214 Shaughnessy Street | In no source found. Not on the council lists | - | Record silent |
| 187 Shaughnessy Street | Formerly Wacky Wings; work to begin 16 July 2025, "the final demolition of properties acquired by the City" | https://www.greatersudbury.ca/city-hall/news-and-public-notices/2025/downtown-redevelopment-advances-with-final-demolition-on-shaughnessy-street/ | Read. A pre-demolition notice; CTV saw crews 29 Jul 2025: https://www.ctvnews.ca/northern-ontario/article/wacky-wings-building-comes-down-in-sudbury |
| Event centre site | "the blocks bordered by Minto, Van Horne, Brady and Shaughnessy Streets" (City, 18 Feb 2025) | https://www.greatersudbury.ca/city-hall/news-and-public-notices/2025/city-selects-downtown-site-for-new-event-centre/ | Read. The Ledo's address may lie outside those blocks; the article does not place the eight on the site |
| Event centre status | "Construction is now underway"; completion "Fall of 2028" | https://www.greatersudbury.ca/city-hall/current-projects/transformation/event-centre/ | Read |
| 200 Minto Street | Nothing on the address or on any government use | - | Record silent |
| Neighbourhood Action Project, 326 Elgin | Organization exists (2001 honours record); nothing ties it to 326 Elgin or says where it went | https://gg.ca/en/honours/recipients/342-75372 | Not used |
| Four units per lot | "Greater Sudbury has adopted zoning by-law amendments to automatically allow up to four residential units per lot in many urban areas". No date or by-law number on the page | https://www.greatersudbury.ca/do-business/planning-and-development/housing-accelerator-fund1/as-of-right-zoning/ | Read. Context only, nothing links it to any address here |
| 3368 Falconbridge, 213 Hillsboro, 22 Oja, 1677 Bancroft | Nothing on any of the four | - | Record silent |
| Rockwood Drive 2802-2814 | Nothing; hits are other cities' Rockwood Drives. Earlier search with Napa Valley Drive also empty | - | Record silent |
| Savard Road, Wahnapitae | Vacant lot listings (Lot 4, 7, 9) and a Lot 9 package with 25 Savard Road; no severance found. Lot numbers are not civic numbers, so not connected | https://realtybureau.realgeeks.com/property/2129540/ | Not used |
| Garson Beer Store | "Garson — 3098 Falconbridge Hwy." among 10 stores shut on Sunday 24 Aug 2025 (insauga, 25 Aug 2025) | https://www.insauga.com/these-are-the-10-beer-store-locations-that-just-closed-in-ontario/ | Read |
| Next Golf | Only Sudbury listing found is 747 Notre Dame Ave; nothing places one in Garson | https://teebly.io/indoor-golf/next-golf-sudbury | Read. The Garson label stays unexplained |
| Top Glove Boxing, 147 Lorne | Boxing Ontario event listing for a 30 May 2026 club competition gives 147 Lorne St as venue | https://boxingontario.com/event/club-competition-north-against-the-rest | Search excerpt only; fetch failed on a TLS error. Not used, the article gives the bare name change |
| Strathcona Mine Road, West Morgan Lake | Strathcona Mine is listed as a past producer; nothing on these points or on why they changed | https://www.geologyontario.mndm.gov.on.ca/mndmfiles/mdi/data/records/MDI41I11NW00013.html | Not used |

Failed fetches: Sudbury.com, Northern Ontario Business, The Trillium and CBC AMP all 403;
greatersudbury.ca "Advancing Downtown Redevelopment" 404. A search excerpt says the rest of the Ledo's
block came down on 12 Feb 2024 (Northern Ontario Business, 403), which is unconfirmed and not used.

Not searched: Johnny D, 351 Alder and 262 Victoria name changes, 336 Bodson Drive West, 30 Cypress,
409 Spruce, 226 Kukagami Lake Road.
