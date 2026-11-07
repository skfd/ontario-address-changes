# Research notes: Muskoka, 2026-10

Window 2026-09-25 -> 2026-10-24 (snapshots 10-17, 10-19, 10-22, 10-24). Net +142 / -5,
12 location moves. No open flag for muskoka in the month (`run.py flags`, 2026-11-07).

## Store checks (data/muskoka/muskoka.db)

- **McConnell Cr, Town of Bracebridge**: 46 new numbers, all on the 10-17 snapshot, all
  on one roll number (441804001006817): 0, 38–70 even, 74–106 (both sides from 83 up).
  The street was already on file since June with 34 numbers between 1 and 39, each on
  its own roll number. Nearest other streets (`lookup --near 50 MCCONNELL CR`):
  34 Whitehorn Park Rd 112 m, 660 Manitoba St 129 m, 2 Gibbs Rd 155 m.
- **Tree Tops Ln, Town of Huntsville**: 37 new on 10-22. Units 101–304 at 11 and at 13
  (12 each), 101–302 at 9 (6), each unit with its own roll number in one run
  (…101329 to …101361); plain 5 and 7 on one roll, plain 15, 16, 17, 18 and 20 on another.
  On file since June: units at 1, 2, 3 and 4 Tree Tops Ln. Nearest other street:
  1394 Deerhurst Dr, 96 m from 9 Tree Tops Ln Unit 101.
- **4 Armstrong Point Rd, Township of Muskoka Lakes**: 16 units on 10-22, labelled L16–L18,
  M10–M15, T3–T9, all at one point on the plain address's roll number. Already on file:
  plain 4, units C1–C6 and BH1. Nearest: 110 Medora St 94 m, 108 Maple St 113 m.
- **162 Howland Dr, Town of Huntsville**: units 207–215 on 10-17, all at one point.
  Already on file: plain 162, units 101–106 and 201–206.
- **Not new, re-keyed** (the tracker keys on number + street + unit + roll number):
  20 Spencer St (Bracebridge) came back on roll …0502 instead of …0500, about 44 m from the
  old point; 1685 Lone Pine Dr (Bracebridge) came back on roll …8720 instead of …8730, same
  point; 93 Potato Island Rd Bunkie 1 and 2 (Georgian Bay) gained the street name they had
  been filed without since June. These are 4 of the 142 additions and 4 of the 5 removals.
- **The one real retirement**: 36 Ann St, Bracebridge, last on 10-17 (on file since June).
  34 Ann St (new roll …705500) and 170 Hiram St arrived on 10-19; 34 is about 21 m from
  where 36 stood. The file does not link them.
- Additions by town: Huntsville 62, Bracebridge 55, Muskoka Lakes 22, Georgian Bay 2,
  Gravenhurst 1.

## Web

| Entity | Found | URL | Confidence |
|---|---|---|---|
| McConnell Cr | 2026 listings describe brand-new freehold townhouses, Macaulay area of Bracebridge, off Clearbrook Trail, Tarion warranty | https://sothebysrealty.ca/en/property/ontario/region-muskoka/bracebridge-real-estate/3138497/3-mcconnell-cres ; https://property.ca/listings/x12950884 | Good for "listings describe"; they cover the older numbers 3–37, not the new ones |
| McConnell Cr builder/plan | Nothing names a builder or plan. Mattamy's "White Pines" is listed at Clearbrook Trail but nothing ties it to McConnell | https://newhomefinder.ca/development/White-Pines | Do not use; record silent |
| Tree Tops Ln | Condo listings put the street across the road from Deerhurst Resort, Chaffey area; condos.ca groups 1–7 as "Treetops at Hidden Valley" | https://condos.ca/buildings/treetops-at-hidden-valley-3-7-tree-tops-lane-1-tree-tops-ln/unit-102-X13424746 | Good for the older buildings |
| 13 Tree Tops Ln | Rental listing already advertises unit 202 at 13 Tree Tops Lane | https://www.keyhomes.ca/property/ontario/huntsville/29914770 | Listing exists; date not confirmed, so no claim about timing |
| 9, 11, 13 Tree Tops builder | Nothing found | — | Record silent |
| 4 Armstrong Point Rd | Hotel booking sites place "Muskoka Lakes Hotel and Resorts" at this address in Port Carling | https://www.kayak.com/Port-Carling-Hotels-Muskoka-Lakes-Hotel-and-Resorts.7844265.ksp | Aggregators only, no official site; nothing on what L/M/T unit labels mean |
| 162 Howland Dr | Baystreet lists "Huntsville Lofts" by Sandhu Developments at 162 Howland Drive: condominium, six retail units incl. a drive-thru Starbucks; unit listings for 201, 207, 211 | https://baystreetgroup.ca/en/Toronto/newdevelopment/803 ; https://www.remax.ca/on/huntsville-chaffey-real-estate/207-162-howland-drive-wp_idm73000004-28743345-lst | Good for "a listing describes" |
| 36 / 34 Ann St | Not searched beyond store; nothing to tie them | — | Record silent |
| Balsam Chutes Rd, East Elliott St | Not searched in depth; scattered single numbers | — | — |
