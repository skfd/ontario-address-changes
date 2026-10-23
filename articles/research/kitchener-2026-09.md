# Research notes - Kitchener, 2026-09

Window 2026-08-20 -> 2026-09-23 (5 snapshots in the month: 4, 7, 21, 22, 23 Sep; 30 pull
days, 0 failed). No open flags for kitchener. Store facts checked against
`data/kitchener/kitchener.db` (net diff snapshot 22 -> 28).

## Store facts (verified)

- **Eskerwood Way 59, Taverners Cres 47, Mihai Eminescu Way 16**: all 122 arrive on the
  21 Sep snapshot, all ACTIVE, all Ward 5, all on PARCELID 50061283. Before the month the
  three streets held only unnumbered points (8, 6, 3) and 3 Mihai Eminescu Way. `--near
  201 Eskerwood Way`: 17 Taverners Cres 8 m, 835 Amand Dr 75 m, Sandymount St 89 m, Gehl
  Pl 95 m, 247 Rosenberg Way 274 m.
- **Cosens Cres**: new street name, 22 numbers 101-130 on 22 Sep, all PENDING, Ward 5,
  PARCELID 55109769. Nearest: 243 Rosenberg Way 17 m, 154 Forestwalk St 61 m, 2 Milt
  Schmidt St 146 m. About 360 m east of the Eskerwood cluster.
- **20 Cameron St S**: 265 unit records, floors 1-24 (no 13th-floor numbers), on file
  since the tracker's first read (10 Jun) as PENDING; 103 flip to ACTIVE on 4 Sep, 162 on
  7 Sep. Same PARCELID 50026170 as 475 King St E (218 unit records, ACTIVE since June)
  and 495 King St E. 44 m from 20-495 King St E.
- **481 King St E**: one of the month's two retirements, BASE, on the same parcel
  50026170, ACTIVE until 20 Aug snapshot, gone from 4 Sep.
- **Nelson Ave** (no number, UNKNOWN type): the other retirement; its neighbour point
  (id 40297969) stays. Placeholder point, nothing to write.
- **535 Manitou Dr -> 1225 Homer Watson Blvd**: new base 1225 Homer Watson Blvd on 4 Sep
  (ACTIVE, same PARCELID 50038569 and same roll 301204002201605 as 535 Manitou Dr). Units
  101-117 (PENDING, on file since 3 Aug as 101-117-535 Manitou Dr) re-streeted to
  101-117-1225 Homer Watson Blvd on 7 Sep under the same record ids; on 4 Sep
  C-535 -> A-1225 and B-535 -> B-1225, both going ACTIVE; A-535 relabelled C-535.
  535 Manitou Dr itself stays on file. 19 unit records moved in total.
- **24 Charles St W**: record 4004295 was 24 from June, became 26 on the 19 Aug snapshot
  (while a separate record 2044421 was also 26 Charles St W), and went back to 24 on
  4 Sep. The month's "renumbering" undoes August's.
- **2201 Bleams Rd**: record 1052844 was an unnumbered "BLEAMS RD" point until June, 2200
  from 3 Aug, 2201 from 4 Sep, same spot. File does not say why.
- **114 Madison Ave S**: Units 1-10 arrive 4 Sep, PENDING, Ward 9; base address remains.
  Nearest: 2-105 Cedar St S 69 m.
- Status: 282 PENDING -> ACTIVE (265 of them 20 Cameron St S), 4 ACTIVE -> PENDING
  (Chicopee Hills Dr).
- Ward 5 took 146 of the 191 additions.

## Outside record

- **Eskerwood / Taverners / Mihai Eminescu = Stamm subdivision, Rosenberg community.**
  Local Planning Appeal Tribunal decision PL171483, issued 14 Feb 2020: Stamm Investments
  Limited, ~43 ha at 186 Gehl Place "within the Rosenburg Community" (secondary plan
  2013); appeal of the City's failure to decide on zoning and draft plan 30T-14201,
  settled at the 13 Jan 2020 hearing; Tribunal granted draft approval. The attached draft
  plan labels Eskerwood Way, Taverners Cres and Mihai Eminescu Way; its revision table
  has "Sept. 20, 2016 Adjust blocks in Stages 5, 6, 7 for addition of Mihai Eminescu
  Way"; conditions require registration in stages. Conditions also reserve a School
  Block fronting Rosenberg Way and Eskerwood Way.
  https://www.omb.gov.on.ca/e-decisions/pl171483-Feb-14-2020.pdf
  Confidence: high that the streets belong to 30T-14201; the decision does not say which
  stage was registered when, so nothing on that.
- **Mihai Eminescu**: the name is that of Romania's national poet. No Kitchener record
  found for why the street carries it. Not used beyond stating the silence.
- **Cosens Cres**: no search hit at all (street, "Cosens Crescent" Kitchener). Not on the
  Stamm draft plan text. Record silent.
- **20 Cameron St S = Vertikal "Cameron Tower".** Vertikal at 475 King St E, Drewlo
  Holdings: two rental towers, 19 and 22 storeys, on a four-level podium, 488 units
  (V&B project page, completion header "2025 (projected)").
  https://www.vbands.com/copy-of-vbs-projects/vertikal-at-475-king-street-east
  SkyriseCities forum thread: posts label a "Cameron Tower" and a "Madison Tower"
  (14 Aug 2025); "Tower 1 has been completed" (22 Nov 2025); Cameron Tower "still needs
  all of its cladding" (25 Dec 2025); Tower 2 "still a work in progress" (27 Apr 2026);
  exterior "mostly complete now" (21 Sep 2026).
  https://toronto.skyrisecities.com/forum/goto/post?id=2314444
  Confidence: forum posts are observers, not Drewlo; use attributed. The file's own
  parcel link (20 Cameron St S shares parcel 50026170 with 475 King St E) is the solid
  half. Storey count of Cameron tower not stated in a source; not used.
- **481 King St E**: no search hit. Record silent on why it left; it sits on the Vertikal
  parcel, which is a fact from the file only.
- **535 Manitou Dr / 1225 Homer Watson Blvd**: lease listings describe 535 Manitou Dr as
  a newly developed retail plaza at Manitou Dr and Homer Watson Blvd in Trillium
  Industrial Park, units 101-117 and A/B for lease.
  https://www.cityfeet.com/cont/listing/535-manitou-dr-kitchener-on-n2p-1y6/cs35675602
  (403 to automated fetch; content from search index - medium confidence).
  https://www.squareyards.ca/lease/on/waterloo/kitchener/unit-112-535-manitou-drive
  Nothing public on why the units were readdressed to Homer Watson. Silent.
- **114 Madison Ave S**: listings for units 6, 8, 9, 10: 2-bed, 3-bath, 1,303 sq ft
  townhouse units, built 2026, unit 10 for rent at $2,799.
  https://condos.ca/kitchener/114-madison-avenue-s-kitchener
  Confidence: medium (aggregator listings).
- **24 Charles St W, 2201 Bleams Rd**: no searches returned anything relevant. Silent.
