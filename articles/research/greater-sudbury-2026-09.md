# Research notes - City of Greater Sudbury, 2026-09

Window: net 2026-08-31 -> 2026-09-30, 24 snapshots, 30 pull days, 0 failed.
Rows 70,097 -> 70,126 (+29). Held: 2026-09-25, 3 location-only modifications (technical flag), excluded.

## Store facts (verified with lookup.py / direct queries on data/greater-sudbury/greater-sudbury.db)

- **Vanguard Drive** - 9 points (183, 190, 232, 245, 274, 297, 322, 359, 396), all first on the
  2026-09-04 snapshot, COMMUNITY Sudbury, no unit or amenity type. 183 at 46.4942,-80.90868; 396 at
  46.49761,-80.9071, so the numbers run north for roughly 400 m. `--near 183`: 2626 Kingsway 191 m,
  264 Levesque Street 202 m, 2794 Raymond Street 286 m, 261 Donald Street 297 m.
- **68 Hemlock Street, Capreol** - one point (ADDRESSID 111960) on file since 2026-06-26. On the
  2026-09-15 snapshot it gained UNIT_AMENITY_TYPE=Townhouse, UNIT_OR_AMENITY=Unit, and three more
  points (112423, 112424, 112425) appeared beside it with the same address text and type. No unit
  numbers on any of the four; spread about 28 m east-west.
- **4589 Municipal Road 80, Val Therese** (112381) - first on 2026-09-10, status Retired from the
  2026-09-15 snapshot; the same snapshot added **4589 Fergus Avenue** (112421) at identical
  coordinates (46.65311,-81.00495). The retired row stays in the file, so it counts among the 29 net
  additions. **4670 Municipal Road 80** (112401) appeared 2026-09-11, about 45 m west.
- **2095 / 2105 Sunnyside Road** - the file carried two points labelled 2095 (39816 and 96586).
  96586 is Retired from the 2026-09-22 snapshot; the same snapshot added 2105 Sunnyside Road
  (112441) about 6 m from it. 39816 remains Active as 2095.
- **Other Active -> Retired**: 1250 South Bay Road (2026-09-30), 233 Elgin Street (2026-09-25).
  No replacement checked; the file gives no reason.
- **Retired -> Active**: 2745 Henri Street, Retired on 2026-08-29, Active again from 2026-09-01.
  Net measures from 08-31, which caught it in its retired state.
- **Business names** (NAME field on amenity points):
  - 42 Lorne Street: Salon Beejou -> Covalin Electrical Supply (2026-09-15)
  - 533 Kathleen Street: Donovan Freshmart -> Donovan Variety (2026-09-24)
  - 552 Kathleen Street: Rogers Photo Studio -> Healing Touch (2026-09-24)
  - 624 Kathleen Street: Vacant -> eCloudz (2026-09-24)
  - 4764 Regional Road 15, Chelmsford (105834, type Restaurant): no name -> Mary Brown's Chicken
    (2026-09-30). Same snapshot added another unnamed Retail point at the same civic number
    (112522). The street field reads Municipal Road 15, the full address Regional Road 15; that
    number already carries Scotiabank, Osmow's, Jiffy Lubes, Chelmsford Mall, Chartrand's Independent.

## Searches

| Entity | Found | URL | Confidence |
|---|---|---|---|
| Vanguard Drive, Sudbury | Nothing. No subdivision, by-law, naming report or listing; hits are Vanguard Drive in Whitby ON and Pontiac MI | - | Record silent |
| Vanguard (street naming, Greater Sudbury planning committee) | Nothing relevant | - | Record silent |
| Vanguard Drive Sudbury P3A (extended search) | Only generic New Sudbury listing pages, none on Vanguard | - | Record silent |
| 68 Hemlock Street, Capreol townhouses | Nothing on 68. A listing for 32-38 Hemlock Street, Capreol (four 4-plexes) is a different address | https://www.keyhomes.ca/property/ontario/capreol/30229092 | Not used - different address |
| Mary Brown's Chicken, Chelmsford | No opening notice or local news found | - | Record silent |
| Covalin, 42 Lorne Street | Search snippet said a BBB category page lists "Covalin Wiring Devices", 42 Lorne St, Unit 1, Sudbury; fetching https://www.bbb.org/ca/on/garson/category/electrical-wiring showed no such entry | - | Unconfirmed - not used in the article |
| 4589 Fergus Avenue / Municipal Road 80, Val Therese | Not searched beyond the store; small enough that the file's own sequence is the story | - | - |

Not searched: Kathleen Street business names other than as a cluster (directory churn; no
public paper trail expected), 1250 South Bay Road, 233 Elgin Street.
