# Research notes - City of Burlington, 2026-10

Window 2026-09-28 -> 2026-10-28. Snapshots kept 5, 9, 15, 16, 19, 20, 21, 28 Oct. Net -1
(6 added, 7 removed), 5 status changes (Pending -> Active), no splits, renames or
renumbers; gross equals net. 29 pull days, 1 failed. No open flags for burlington in the
month (`run.py flags`, 2026-11-03). Research run 2026-11-03, fanned out to three agents
(James St; Burlington Ave/Caroline + Wickens; Drury, Queensway, Fisher, Plains Rd).
Burlington's Committee of Adjustment publishes agendas on events.burlington.ca but not
decisions, so "nothing found" means nothing *indexed*.

## Store facts the article leans on (sqlite + lookup.py --near, 2026-11-03)

- **James St.** 2082, 2086, 2090 James St (Property, Active, RSNs 41323/41325/41327, on
  file since the 11 Jun baseline) last seen 15 Oct, gone 16 Oct. 2088 James St (RSN
  103494, Property, Pending since the baseline) went Active 16 Oct. 20 Oct: a second 2088
  point, PROPCODE 140 "Address", RSN 104212, Active, ~9 m from the first. 2088 is now the
  only number on James between 2060 and 2110. Neighbours: 0000 Martha St 41 m, 443 Pearl
  St 54 m.
- **Burlington Ave / Caroline St.** 548 and 550 Burlington Ave (Property, Active, RSNs
  99613/102073) last seen 15 Oct, gone 16 Oct. 1389 Caroline St (RSN 106741, Pending,
  first seen 9 Jul) went Active 19 Oct; its point is ~5 m from where 548's was, ~19 m
  from 550's. Neighbours: 534 Burlington Ave 33 m; Caroline numbers 1375, 1379, 1385,
  1389 on file.
- **Plains Rd E (Northshore).** 498 Pending -> Active 5 Oct; 496 Pending -> Active 15 Oct
  (both PROPCODE 140 "Address", Pending since baseline). The extra 500 Plains Rd E
  "Property" point (RSN 106746, added 20 Aug) gone 5 Oct; the 500 "Address" point that
  turned Active 28 Sep remains. 496 is 41 m from 945 Nora Dr, 50 m from 494 Atkins Pl.
- **Wickens Ave.** 677 Wickens (RSN 106745, Pending since 18 Aug) went Active 21 Oct. Same
  day 675 Wickens's point moved ~4 m and its RSN changed 9196 -> 106794 (one retired + one
  added in the counts). 677 is ~19 m from 675; 687 Penny Lane 33 m, 681 Enfield Rd 59 m.
- **2298 Queensway Dr** (RSN 106787, Pending) new 9 Oct, between 2294 and 2300, both still
  on file. 84 m from 998 Cleta St, 90 m from 2295 Glenwood School Dr.
- **541 Drury Lane** (RSN 106788, PROPCODE 180 "Secondary Building", NAME "Central Park",
  Active) new 15 Oct. Neighbours on file: 500 Drury (Burlington YMCA), 501 (Central Park
  and Burlington Tennis Club), 519 (Central Park and Arena).
- **1321 and 1323 Fisher Ave** (RSNs 106796/106795, Pending, ward 3) new 28 Oct, between 1320
  and 1325. 55 m from 1335 Augustine Dr, 59 m from 2315 Mount Forest Dr.
- RSN run: 106787 Queensway, 106788 Drury, **106789-106793 never on file**, 106794 Wickens,
  106795-96 Fisher. 106783 (missing in September) still never seen. Max RSN 106796.
- Pending on file at 28 Oct: 185 (187 at 28 Sep: -5 flipped, +3 new Pending).

## Findings

### 2082-2090 James St / 2088 James St - Martha James Condominiums
- Mattamy (Monarch) Ltd. applied to build an 18-storey condo at 2082, 2086 and 2090 James St
  (corner of Martha), 0.23 ha; 153 units per one post, 164 per another.
  https://www.mariannemeedward.ca/posts-to-be-added/six-new-development-applications-ward-2-public-meetings-march-7-27
  (fetched). Confidence: high on site identity; unit count conflicts.
- Files 505-07/17 and 520-16/17 (snippet only, mariannemeedward.ca/.../development-burlington-ward-2). Not used.
- LPAT settlement early 2021 to 13 storeys / 150 units: forum hearsay quoting a City memo
  (skyrisecities.com/forum/threads/31661). Not used.
- 13 storeys, 150 units, Graziani + Corazza: UrbanToronto 2022-03-01
  https://urbantoronto.ca/news/2022/03/martha-james-condominiums-rise-burlington.47329 (fetched).
- Groundbreaking late January 2023: RENX 2023-02-13
  https://renx.ca/mattamy-breaks-ground-on-three-gta-condos (fetched).
- Listings at 2088 James St in 2026; condos.ca unit 413 listing (23 Jul 2026) gives building
  age "0-1 years": https://condos.ca/burlington/martha-james-condominiums-2088-james-st/unit-413-W13598160
  (fetched). Registration date / corporation number: **not found**. That the Oct flip
  tracks registration is inference only.

### 548/550 Burlington Ave -> 1389 Caroline St
- Committee of Adjustment 23 Sep 2026, item 8.1, A-041/26 (agenda PDF text extracted):
  new one-storey house with attached garage on 548/550 Burlington Ave; variances treat
  **Caroline St as the front yard** and Burlington Ave as the street side yard; staff report
  says 548 and 550 have been "formally consolidated with the Land Registry Office"; lot
  725.5 m2, vacant. Heritage staff note it faces the designated Skelton-Giddings House at
  534 Burlington Ave and "would have expected the front façade to front Burlington Avenue
  (not Caroline Street)". Earlier files on the lots: B-015/2015 (severance of 546), A156/2016,
  A033/2020 and A035/2020 (OLT refused), A087/2024. Decision not online. The agenda never
  says "1389"; the link is inference from the Caroline frontage + consolidation + the point
  sitting on 548's spot.
  https://events.burlington.ca/meetings/Detail/2026-09-23-1300-Committee-of-Adjustment/8dadfc82-38f7-46aa-b6d2-b4bf00f27c54
  Confidence: high on the application. Owners named in the agenda are private; left out
  of the article.
- A-061/25 for 550 Burlington Ave, 5 Nov 2025 (snippet only, page wouldn't load). Not used.

### Plains Rd E - Northshore
- condos.ca: HCC-811 registered 24 Nov 2025, 8 storeys, 188 units, addressed "498 and 500
  Plains Rd E"; townhouse units listed as "TH06/TH08 - 498 Plains Rd E", apartments at 500.
  https://condos.ca/burlington/498-plains-road-e-townhouses-498-plains-rd-e-500-plains-rd-e (fetched).
- Nothing found on 496 or on a Sep-Oct 2026 event (phase 2 registration/occupancy).

### 2298 Queensway Dr
- Council unanimously approved Waggy Inc. townhouses at 2294-2300 Queensway Dr: 24 units
  (16 standard + 8 back-to-back), 24-lot plan of subdivision with a common element road,
  OPA 127, rezoning to H-RM3-513. Page gives 17 May but no year.
  https://www.mariannemeedward.ca/posts-to-be-added/burlington-council-unanimously-approves-townhouse-complex-at-2294-2300-queensway-drive (fetched)
- REW lists "2294 & 2300 Queensway Drive Townhomes", coming soon, move-in TBD:
  https://www.rew.ca/developments/12081/2294-2300-queensway-drive-townhomes-burlington-on (fetched)
- Nothing names 2298. That 2298 belongs to this project is inference.

### 541 Drury Lane, "Central Park", Secondary Building
- Nothing found for 541 Drury. Only lead: a ConstructConnect RFP for design of a "New
  Central Park Maintenance Facility" at 2299 New St (published 23 Jun 2026, "remains in
  design phases"); different street, inconsistent dates. Not used.

### 1321 / 1323 Fisher Ave
- Nothing found. 1317 Fisher had a porch variance (A-027/24, 2024), not a severance.
  1244 Fisher listing mentions semis under by-law 09-2026 (unverified marketing copy). Not used.

### 675 / 677 Wickens Ave
- Nothing found (consent, variance, listing). Only Wickens agenda item is 649 Wickens,
  A-058-2025, a large floor-area variance, unrelated.

## Empty queries (abridged)
"541 Drury" Burlington; Central Park Burlington washroom/pavilion/fieldhouse 2025-26;
"2298 Queensway" Burlington; "1321/1323/1325 Fisher" Burlington; site:events.burlington.ca
Fisher consent; "675 Wickens"/"677 Wickens" Burlington; Wickens severance/consent;
"1389 Caroline Street" Burlington; "548 Burlington Avenue" Burlington; Martha James
registration/occupancy 2026; Northshore occupancy Sep-Oct 2026.
