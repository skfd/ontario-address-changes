# Research notes - Thunder Bay, 2026-09

Window 2026-07-24 -> 2026-09-09 (one snapshot, 9 Sep; the file did not change in August).
Brief: 9 added, 5 removed, 8 significant, 1 boundary, net +4, 45,102 on file.

## From the store

- Four of the five "retirements" are the same addresses re-keyed after their points moved
  (identity is synthesized from number + street + coordinates; the layer has no stable id):
  4100 25th Side Rd (54.0 m), 140 Churchill Dr W (15.4 m), 681 Mercier St (7.3 m),
  683 Mercier St (6.7 m). Same PCL_PIN, RSN and props before and after. Real: 5 new, 1 retired.
- 1075 Central Ave: new, REFNAME ADDRESS-ONLY, no TYPE, PCL_PIN 621170041 - the parcel of
  1091 Central Ave, ~28 m away. 1091's TYPE went City Owned -> None in the same update.
- 1077 Central Ave: new, ADDRESS-ONLY, PCL_PIN 621170091, shared with 1175 Central Ave (~83 m),
  whose TYPE also went City Owned -> None the same day.
- 1112 Premier Way: new, Regular Property, PCL_PIN 621170117, shared with 1245 Central Ave
  (~140 m), which itself first appeared on the 2026-07-24 snapshot. Nearest other-street
  address 1306 Capital Way, 102 m.
- 2288 Government Rd: new, own parcel 622400314; nearest 145 Boyko Rd, 160 m.
- 639 Hilldale Rd: new, own parcel 622330365, between 635 and 640; it is published with no
  ADDRESS / ADDRESS_NUMBER field (number only in COMPLETE).
- 2131 R.S. Piper Ave: the one real retirement; only address on parcel 622660114; nearest
  live addresses 3112 Sparrow Dr (40 m) and 2111 R.S. Piper Ave (48 m).
- Field-only changes: 1171, 1175, 1181, 1191 Oliver Rd Regular Property/ADDRESS-REGULAR ->
  Address Only/ADDRESS-ONLY, and 1165 Oliver Rd the other way; 700 Red River Rd Regular
  Property -> City Owned; 1091 and 1175 Central Ave City Owned -> (none);
  5405 Mapleward Rd CITY "THUNDER BAY" -> (none).

## From outside

- **1091 Central Ave rezoning** - council approved by-law changes for a 15,049.5 m² retail
  warehouse with a gas station; site described as the south side of Central Avenue, west of
  Golf Links Road, north of Innovation Drive. Your ThunderBay, 14 Apr 2025.
  https://yourthunderbay.ca/114107-2/ - fetched and read. High confidence.
- **Costco and the land** - NetNewsLedger, 7 Apr 2026: the 7.7-hectare property at Golf Links
  and Central; "per recent local reporting" Costco bought the land in December 2025; 2027 a
  best-guess opening, not official.
  https://www.netnewsledger.com/2026/04/07/costco-in-thunder-bay-could-reshape-jobs-prices-traffic-and-retail-across-northwestern-ontario/
  - fetched and read. Medium confidence on the sale (secondhand within the article).
- **Building permit application, 30 Jul 2026** - City notice "Growth Continues as Costco Permit
  Application Submitted" (thunderbay.ca) and CBC "It's official: Costco applies for building
  permit". Search snippet only; the City URL 404'd and CBC/TBNewsWatch 403'd to fetch. Not used
  in the article.
- TBNewsWatch, "Zoning amendment request fuels Costco speculation" / "Cannot confirm or deny
  it's a Costco, says developer" - 403 to fetch; content only via search summaries
  (185 -> 20,000 m² floor area request; Forum Properties). Not used.
- The layer's service description calls REFNAME the address type; no published list of REFNAME
  or TYPE values found.
  https://services5.arcgis.com/h9xShea49ZANgOtx/ArcGIS/rest/services/Municipal_Address_Feature_Layer/FeatureServer

## Searched, nothing found

- "1075 Central Avenue" / "1077 Central Avenue" Thunder Bay - nothing for either number.
- "1112 Premier Way", "1245 Central Avenue" - nothing (1269 Premier Way is an office address
  of engineering firms, unrelated).
- "2288 Government Road" - nothing.
- "639 Hilldale Road" - nothing.
- "2131 R.S. Piper Avenue" - nothing on demolition, fire or severance.
- Oliver Rd 1165-1191 - nothing on the numbers.
- "700 Red River Road" - nothing.
