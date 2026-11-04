# Research notes - City of Hamilton, 2026-10

Window 2026-09-29 -> 2026-10-30. Snapshots kept 1, 9, 12, 19, 26, 30 Oct. Net +594
(601 added, 7 removed), gross identical, 7 unit splits, no renames, renumberings or
status changes. No open flags for hamilton. 30 pull days, none failed. The 31 Oct read
matched the 30th (same content hash). Research run 2026-11-04.

## Store facts the article leans on (verified with sqlite against data/hamilton/hamilton.db, 2026-11-04)

`lookup.py` prints blank addresses for Hamilton (the layer has no combined address
column) and `--addr`/`--near` fail, so everything here came from direct queries.

Identity is synthesized (number, street, unit), so a moved point or respelled unit leaves
under one key and arrives under another. Reconciling the net diff row by row:

- **Genuinely new: 596.** 573 units at 1190 Main St W, plus 23 elsewhere: Homestead 6,
  220 Hempstead units 1-4, Highway No. 5 W 2, Welbourn 2, Wexford 2, and one each on
  Bonhill, Erindale (182 R), Glover, Klein, Picardy, Senior, Talon.
- **Re-keyed, not new: 5 out, 5 in.** Plain 220 Hempstead (point moved about 33 m east),
  293 Highway No. 8 (about 5 m, 9 Oct), 100 Parkside -> 100 Clappison (identical
  coordinates and postal code), 4 Portside *G 1*/*G 2* -> *G1*/*G2*.
- **Labels dropped: 2.** 220 Hempstead *PT 1* and *Unit*, replaced by units 1-4.
- **Genuinely retired: 0.**
- 596 - 2 = +594 = rows 273,991 -> 274,585. Checks.

The brief marks 220 Hempstead's parent `retired`. The store shows a plain 220 still on
file, re-keyed by the move, so the article does not call it retired.

### 1190 Main St W

- All 573 units start on the 1 Oct snapshot, at one point. 30 Sep was read and unchanged,
  so they arrived between the 30 Sep and 1 Oct reads.
- Two plain 1190 records (about 4 m apart) on file since the first snapshot, 9 June. Both
  remain.
- Units run 100 to 1510. By leading digits: floor 1: 25; 2: 12; 3-5: 58 each; 6-9: 59
  each; 10-11: 45 each; 12-15: 9 each. Sum 573.
- Floors 3-9 all skip endings 04, 11, 23, 37, 46, 60; floors 3-5 also skip 41. The file
  does not say why.
- All 575 records carry postal code L8S 0A1.
- Nearest other streets: 99 Traymore Ave 24 m, 59 Forsyth Ave S 59 m, 2 Stroud Rd 67 m,
  50 Dalewood Ave 73 m.

### Other placements

- 8 Talon Rd (12 Oct): 30 Times Square Blvd 177 m, 575 Highland Rd W 182 m, 393 Pritchard
  Rd 186 m. COMMUNITY Hamilton. No near-match except Talence Dr, a different street.
- 20 Senior Dr (19 Oct): 284 Nakoma Rd 46 m, 143 Cornwallis Rd 50 m. COMMUNITY Ancaster.
  No near-match (Seneca Ave/Ct/Dr are established, separate streets).
- 100 Clappison Ave: 8 Enterprise Cres 114 m. Clappison numbers on file run 5 to 140, with
  85 and 105 either side. COMMUNITY Flamborough.
- 3334 R and 3338 R Homestead sit about 20 m west of the plain numbers. All six Homestead
  rows arrive 19 Oct. COMMUNITY Glanbrook.
- 182 R Erindale (26 Oct) sits about 12 m from plain 182.
- Numbers with an R suffix on file: 61 on 29 Sep, 64 on 30 Oct.

## Findings

- **1190 Main St W = Lincoln Alexander Hall.** McMaster's residence FAQ gives "1190 Main St
  West / Hamilton, ON / L8S 1C2". https://housing.mcmaster.ca/lincoln-alexander-hall/faq/
  High confidence. Note the postal code differs from the file (L8S 0A1) and from
  SkyriseCities (L8S 1R8).
- **Open.** "Now open!", "newest and largest on-campus student residence".
  https://housing.mcmaster.ca/lincoln-alexander-hall/ High.
- **Opened August 2026, 1,366 beds, McMaster operates.** Location given as Main St W &
  Traymore Ave. https://k-cap.com/project/lincoln-alexander-hall-mcmaster-student-residence
  High (developer's page).
- **Move-in.** CHCH: students moved in on a "Friday", "1365 beds available" (Sean Van
  Koughnett). Page metadata datePublished 2026-08-29T00:18Z; the text prints no date, so
  the article says "at the end of August".
  https://www.chch.com/chch-news/hundreds-of-students-begin-moving-into-mcmasters-new-lincoln-alexander-hall/
  High for the month, inferred for the day.
- **Pods.** Rooms are pods and pod suites of 1 to 5 beds, "more than 1300 beds". No count of
  pods or suites published. https://housing.mcmaster.ca/lincoln-alexander-hall/room-types/
  High. **Nothing found maps 573 numbers to pods, rooms or beds.**
- **Height.** "Maximum Storeys 15", "15 & 10-storey", status Complete, unit count paywalled.
  https://toronto.skyrisecities.com/database/projects/lincoln-alexander-hall.48708 Medium.
- **Namesake and groundbreaking.** 9 Nov 2023; 1,366 beds; Alexander a 1949 McMaster
  graduate, Canada's first Black MP, Ontario's first Black lieutenant-governor.
  https://news.mcmaster.ca/lincoln-alexander-hall-groundbreaking/ High.
- **Addressing policy** (PDF text extracted directly, 4 pages). Multi-floor unit numbers
  "typically include a floor indicator"; one address per multiple dwelling, "the owner
  assigns the individual Municipal Address Unit Numbers"; detached additional dwelling
  unit: "the letter 'R' will be assigned as a suffix".
  https://www.hamilton.ca/sites/default/files/2025-08/pedpolicies-municipal-addressing-policy.pdf
  High.
- **ADU FAQ.** "a separate municipal address is required for a Detached Additional Dwelling
  Unit", so emergency services, mail and utilities can find it.
  https://engage.hamilton.ca/addressingstnamingbylaw/faqs High. It does not mention R.
- **3334 Homestead.** Listing copy: "permit-ready plan for a 2 storey home with an accessory
  2 storey additional dwelling unit", "attached by garage only", detached two-car garage at
  the rear; 3334 and 3338 sold separately. Listing terminated; a linked listing shows expired
  30 Jun 2025.
  https://wahi.com/ca/en/real-estate/on/hamilton/glanbrook/3334-homestead-dr-mount-hope-l0r1w0-ontario-canada
  Medium: seller's marketing, says nothing of what was built.
- **Clappison Avenue.** By-law 21-241, passed 15 Dec 2021, Ward 15: land "established as a
  public highway, forming part of Clappison Avenue" (text extracted directly).
  https://www.hamilton.ca/sites/default/files/2022-04/21-241.pdf High. Says nothing about
  100 Parkside.

## Searched, came back empty

- **Why 100 Parkside became 100 Clappison:** no by-law, notice or story found.
- **Talon Road:** no by-law, subdivision or listing. Name not found in Hamilton searches.
- **Senior Drive:** no by-law or listing; results were seniors' services in Ancaster.
- **220 Hempstead Dr:** nothing. Results were 95 and 190 Hempstead.
- **2548 and 2574 Highway No. 5 W:** nothing.

## Not usable

- dailynews.mcmaster.ca ?p=83548 and ?p=81922: redirect to 404.
- The Silhouette, "Lincoln Alexander Hall Opens Doors to Students": HTTP 429, unread. A
  search summary attributes "legal delays" to coverage of the opening; not verified, not
  used.
- realtor-pr.realtor.ca for 100 Parkside and 3334 Homestead: 404. Meadowtown: 403.
  property.ca/listings/40688569: 404. Bay Street Group X11888320: inactive, no detail.
- 100 Parkside as a lot in the "i-Connect Industrial Park": search snippet only, never read
  on a live page. Left out.
- thepublicrecord.ca ?p=248330: a census piece, unrelated.

## Not searched

52 Bonhill, 178 Glover, 224 Klein, 121 Picardy, 15 Wexford N, 93 Welbourn, 182 R Erindale.
The article lists some of them without claiming a search.

## For November

37 Carlson Street rows open after the window, while the row count barely moves.
Not read for this month; left to November's piece.
