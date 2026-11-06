# Research notes - Kitchener, 2026-10

Window 2026-09-23 -> 2026-10-11 (1 snapshot in the month; 30 pull days, 0 failed). 16 flags
open, none for kitchener. Store facts checked against `data/kitchener/kitchener.db` (net
diff snapshot 28 -> 37).

The file changed once: content hash is unchanged from 23 Sep through the 10 Oct read, new
on 11 Oct, and unchanged from then through 6 Nov. Everything below is that one update, so
net and gross are identical. It may have been edited at any time in the window.

## Store facts (verified)

- **Blair Valley St**: 3 unnumbered points before; 67 new numbers, all PENDING, all BASE,
  Ward 4, on three parcels: 10-50 even (21, PARCELID 55105785), 31-61 odd (16, 55105784),
  825-883 odd (30, 55105789). Also re-filed in the same update: placeholder 40263288
  becomes 70; 40263287 goes from Jacob Detweiller Dr to 75 Blair Valley St; 40263284 goes
  from Blair Creek Dr to Blair Valley St and moves 8 m. 69 numbered rows now on file; the
  headline stays 67. `--near`: 10 Blair Valley: Blair Creek Dr 29 m, 77 Wild Chicory St
  130 m, 71 Pine Warbler St 150 m. 883: 63 Pine Warbler St 47 m. 825: Stauffer Woods Trail
  8 m, 3 Pine Warbler St 33 m. Not a new street (brief: none).
- **25 Wellington St S**: 13 unit records leave, 1301-1312 and 1314 (ids 40295031-43, an
  unbroken run), all ACTIVE, on file since the first read. That was the file's whole 13th
  floor; 12xx and 14xx stay, and both skip a 13 unit too. After: 455 records = base + 9
  service + 445 numbered units on floors 1-12 and 14-37 (36 floors). Before: 459 records.
  The 9 new (ids 40302100-08): PKG, LKR, seven SRV, all ACTIVE, consecutive roll numbers
  301205000109879-887, no other unit row at 25 carries a roll. Brief counts them as a
  "split"; they are not apartments. 5 Wellington St S, same parcel 50006688: 241 records,
  227 numbered units on 18 floors, no 13xx, has its own LKR/PKG/SVR rows.
- **60 Trussler Rd**: Units 1-16 new, PENDING, Ward 7, ids 40302084-99. Base stays and
  moves 60 m. `--near`: 70 Cora Dr 51 m, 1665 Highland Rd W 120 m, 68 Rauch Crt 166 m.
- **210 Heritage Dr**: 18 of the month's 20 Pending->Active (A, B, 1-16). 17-26 still
  PENDING. 28 unit records at the address. Other two: 11 Otterbein Rd, 155 Fifth Ave.
- **42 Windom Rd**: retired, ACTIVE, parcel 50041855. 32 Windom moves 25 m, B-32 28 m,
  A-32 3 m (parcel 50041854). `--near` 32: H-131 Fairway Rd N 77 m, 279 Thaler Ave 87 m.
- **Rosenberg-area placeholders**: 12 "renames" are all unnumbered UNKNOWN points (ids
  40289478-96): 7 to Pinsent Cres (from Solitude 3, George Israel 2, Burgundy 1, Sheephorn
  1), 2 to Rosebush St, 1 each to Rosenberg Way, Sidewinder St, Muirfield Cres. 8 more got
  a number and another street: 100, 105, 110, 115 Bandon Dr; 505, 535 Rosenberg Way; 250
  Gold Dust Cres; 101 Rattlesnake St. All 20 sit within about 440 x 655 m. No street was
  renamed: 133-149 Solitude St are untouched. Sheephorn St and Sawbuck St have no points
  left on file. `--near` 100 Bandon Dr: Pinsent Cres 37 m, George Israel St 101 m,
  Sidewinder St 104 m, Rosebush St 104 m, Rosenberg Way 112 m.
- **Newcastle Dr**: 23 unnumbered points (ids 40269317-39) get numbers 186-222, all PENDING,
  Ward 5, individual parcels. Modifications, not additions. One other Newcastle point
  retired. `--near` 211: 43 Castlebay St 56 m, 77 Renfrew St 139 m, 36 Newcastle Crt 144 m.
  With 35 Essex Rd and 70 Blair Valley St that is the 25 in the brief's number-only line.
- **Retirements, all 27**: 13 at 25 Wellington; 9 unnumbered points on Eskerwood (4),
  Taverners (3), Mihai Eminescu (2), the streets that took 122 numbers in September, all
  parcel 50061283 (Eskerwood still holds 4 others); 1 each Gold Dust Cres and Newcastle Dr
  placeholders; 75 and 111 Otterbein Rd; 42 Windom Rd.
- **Otterbein Rd**: record 40247513 was 75 and 40294227 was 111 until June; by 3 Aug they
  were 5 and 11, and new PENDING records 40299425 (75) and 40301714 (111) appeared. Those
  two left in October. 11 went ACTIVE.
- **Small additions**: 631 Frederick St Units 1-4 (PENDING, Ward 1, unit 2 on a different
  parcel; 51 Rosemount Dr 54 m, 92 Ethel St 59 m); A and B-69 Nathalie St (PENDING, Ward 5);
  397 King St E (ACTIVE, BASE, older-style id 4004768, never on file before); 102-305 King
  St W; 2-116 Queen St N; PKG-175 Commonwealth St.
- **Location**: no `location_min_move_m` for kitchener, so the brief's 29 includes moves of
  1-3 m. Six moved 20 m or more: 60 Trussler 60, 485 Huron Rd 40, B-32 Windom 28, 32 Windom
  25, YRD-175 Commonwealth 22, 495 Huron Rd 22.
- Wards: additions 67 W4, 16 W7, 11 W9, 4 W1, 3 W5, 1 W10. No boundary transitions.

## Outside record

- **Blair Valley St = "Harvest Park at Doon South".** KeyHomes listing, Lot H43 Blair
  Valley St, MLS 40856571, read 6 Nov 2026 ("Listed 3 days ago"): "FREEHOLD (with no POTL
  fees) Townhouses in Harvest Park at Doon South", "Harvest Park is the newest section of
  the well-established and sought-after Doon South Neighbourhood", "Road is incomplete at
  this time. Closest finished intersection is Jacob Detweiller Dr and Winter Wren Cr."
  Builder not named. https://www.keyhomes.ca/property/ontario/kitchener/30177433
  Confidence: medium (a sales listing), good enough attributed.
  Search snippet from https://precon.savemax.com/project-details/harvest-park-qjssoj says
  Activa is the developer; host refused the connection, so unread and NOT used.
  No plan of subdivision or naming record found; nothing explains the 825-883 numbers.
- **25 Wellington St S.** condos.ca building page ("5-25 Wellington St S"): "36 floors/
  445 units", builder VanMar Developments, "Built in 2025".
  https://condos.ca/kitchener/station-park-5-25-wellington-st-s
  The page does not say which tower the count is for and its overview gives 5 Wellington
  as the address. The store settles it: 36 floors and 445 numbered units is 25, exactly and
  only after October; 5 has 18 floors and 227. Confidence: medium-high.
  SkyriseCities thread: "Building C is occupied" (27 Dec 2025); "Building D is being
  marketed as Platform at Station Park", original intent was C and D together "(hence
  Duo)". https://toronto.skyrisecities.com/forum/goto/post?id=2330594
  Observers, not VanMar. Listings call 25 Wellington "DUO" and Tower C (snippets).
  No listing found for any 13xx unit; a null result, not proof. Nothing public says the
  building has no 13th floor or why the records left. SRV, LKR, PKG not defined anywhere read.
- **60 Trussler Rd.** City notice posted 20 Aug 2021: "a vacant land condominium consisting
  of 5 residential units, and common element areas", public meeting 13 Sep 2021.
  https://www.kitchener.ca/news/posts/public-meeting-proposed-vacant-land-condominium-60-trussler-road/
  Confidence: high for 2021. Demolition control DC21/028/T/ES for the house (report
  DSD-2021-163) seen only in a search snippet of a Laserfiche doc, NOT used. Nothing found
  on 16 units or on what happened after 2021. Gap left open.
- **210 Heritage Dr = Haravale Towns.** PadMapper: "a new community of 26 stacked townhomes
  at 210 Heritage Dr in east Kitchener, built in 2026 and rental-only", managed by PTH
  Management. https://www.padmapper.com/buildings/p1694274/haravale-towns-apartments-at-210-heritage-dr-kitchener-on-n2b
  Confidence: medium (rental listing). 26 matches units 1-26; A and B unexplained.
- **32-42 Windom Rd.** Up Consulting, Planning Justification and Urban Design Report, 31 Oct
  2023, for Jackman Construction: 58 stacked townhouse units in two blocks, one consolidated
  driveway off Windom, OPA and ZBA applications.
  https://app2.kitchener.ca/AppDocs/OpenData/AMANDADataSets/698857_Planning%20Justification%20Report.pdf
  Confidence: high for the proposal. Read pages 1-8 only. Record article (28 Feb 2024, council
  approved an expanded plan) seen only as a snippet, 403, NOT used. Whether anything has been
  built or demolished is not established. Precondo names Vive Development; marketing text, not used.
- **Pinsent, Bandon, Rosebush, Sidewinder, Rattlesnake, Gold Dust**: no plan or by-law found.
  Silent. Search used the names together, so a one-at-a-time search is still open.
- **Newcastle Dr 186-222**: listings for lower numbers only; no project found. Silent.
- **631 Frederick St, 69 Nathalie St, 397 King St E**: no hit for those numbers. 387 King St E
  is a different address. Silent.
- **Otterbein Rd, Essex Rd, Huron Rd moves, 102-305 King St W, 2-116 Queen St N**: not searched.

## Dead ends, so nobody re-fetches them

- sothebysrealty.ca Lot I52 Blair Valley: 404.
- pressreader.com Record articles: 403.
- lf.kitchener.ca Laserfiche: needs cookies.
- precon.savemax.com, dave.searchrealty.ca: connection refused.
- gta-homes.com: 403.
- cushmanwakefield.com Windom listing: returns a generic search page.
