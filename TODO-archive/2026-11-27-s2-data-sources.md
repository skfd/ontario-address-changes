# TODO.md §2: closed items, finished probes, and detail behind open ones

Moved verbatim out of [TODO.md](../TODO.md) on 2026-11-27; the text is as it stood at
TODO.md's last update, 2026-10-31. History and finished work, not required reading.
Open items stay in TODO.md; where one was shortened there, its full text is here.

## 2. Find data sources for uncovered cities

Closed rows of the places queue (consolidated 2026-10-16):

| # | place | what | why now |
|---|---|---|---|
| ~~1~~ | ~~west-parry-sound~~ | **done 2026-10-16**: re-pointed to NG911/9112, store re-baselined | — |
| ~~2~~ | ~~elgin~~ | **done 2026-10-16**: re-pointed to Elgin_Civic_Numbers_2026, store re-baselined, licence found (OGL, yellow) | — |
| ~~3~~ | ~~middlesex~~ | **done 2026-10-16**: re-pointed to Base_Layers/MapServer/1, store re-baselined | — |
| ~~4~~ | ~~Tecumseh (Essex)~~ | **done 2026-10-16**: tracked (9,860), skipped.toml fixed | — |
| ~~6~~ | ~~peel-region, waterloo, dufferin, cambridge, chatham-kent~~ | **looked 2026-10-23** (vault content hashes): waterloo and dufferin were stale layers, re-pointed 10-16 (dufferin moved again 10-21); chatham-kent is a periodic export, moved 09-30. **peel-region is a stale roll-up**: byte-identical 503,923 rows on 115 pulls since 06-27 although the item is republished (modified 10-23), while member brampton changed on 106 days - the members (brampton, mississauga, caledon) are the live record; no fresher layer in the Peel org. **cambridge**: no change since 08-07 after moving every few days in July, ArcGIS Server with no edit stamps, nothing fresher (the AGOL "Cambridge_Data Address Points" is Cambridge, Massachusetts); waterloo-region also covers it - compare once that has a few weeks | — |
| ~~7~~ | ~~stratford, prince-edward-county, haldimand~~ | **done 2026-10-23**: PEC re-keyed on NGUID (survived the 10-19 reload) and rebuilt from pulls, +182 suffix siblings the synth key had collapsed; stratford ignores G_COLL, haldimand PCL_RN/TMP_PCL_RN (pre-emptive, operator call; backfill --reapply-ignore, verify 0/0/0). Haldimand watch: ADDR_PT ("PreType") holds house suffixes on 19 of 25 filled rows while 50 stay in ADDR_HN - a cleanup moving them is ~50 retire+add pairs | — |
| ~~8~~ | ~~milton~~ | **declined 2026-10-23**: the licensed Address_Pts is a 13-of-24-field subset of the tracked MGIS/63 (same 46,437 rows); MGIS/63 failed only 10-11/10-12, clean since. Reasons in milton.toml | — |
| ~~9~~ | ~~member layers~~ | **done 2026-10-16**: ajax, whitby, pickering, oshawa, newmarket, vaughan (+ vaughan-ng911), mississauga, caledon, welland, niagara-falls-city, waterloo-region tracked; Orillia/New Tecumseth are degraded copies of simcoe, not added | cities publish fresher data than the roll-up |
| ~~11~~ | ~~Leamington (Essex)~~ | **done 2026-10-23**: tracked (11,423 baseline), key GlobalID, publish_reports = false (no licence on the item, not on the county Hub); layer last edited 2025-07-08, so watch that it moves; unit parse queued in §1 | — |
| ~~12~~ | ~~Lanark County, Timmins~~ | **done 2026-10-31**: `slims` access kind built in address-vault (geobuf export + parcel join by roll), lanark 37,215 and timmins 29,532 baselined, gated; licence ask to Lanark County / Timmins still open | — |
| ~~13~~ | ~~Kingsville (Essex)~~ | **done 2026-10-30**: tracked vault-only (10,269 rows, gated) from `MESH_WFL1/FeatureServer/0`, one Sep-2025 upload; ask drafted 2026-10-31 (requests@kingsville.ca) | — |
| ~~—~~ | ~~Owen Sound, Brockville~~ | **covered 2026-10-30**: grey holds ~6,770 Owen Sound rows, leeds-grenville 8,737 Brockville rows | — |

From "2026-10-16 sweep onboarding, follow-ups":

- [x] Licence reads (2026-10-16, evidence in each TOML + LICENSING.md): waterloo-region is
      **green-lwg** (Region OGL v2.0, LWG 2025-02-10; page moved, old link 404); ajax is
      yellow-review (OGL clone, credit optional, bound only by the hub's site-wide text);
      tecumseh stays yellow-review (County of Essex OGL, but the County licenses the Town's
      points). All three keep publishing.
- [x] Measure the daily run after the first full day: ~1.5M more rows (waterloo-region 263k,
      mississauga 220k, vaughan 140k + 94k, oshawa 64k). **Clears easily, 2026-10-20:**
      START 12:00 -> END 12:15, one attempt; ottawa is the long pole (760 s), then simcoe
      (343 s). The ~1.5 h runs before 10-19 were the render, not the extra rows.
- [x] ~~lennox-addington field-map upgrade~~ **declined 2026-10-16**: the tracked Public View
      carries a view filter, `(SUBUNITTYPE <> 'Public Redact' AND ADD_LABEL <> 'Unknown Address')
      OR (...)`; every view that exposes STREET_NAM/UNIT_IDENT (the four township views and
      "Civic Addresses (Public View)", 27,383 vs 26,613 rows) has no such filter, so it would
      import the county's redacted points (~37) plus 733 'Unknown Address' rows.
      street_from_full stays.
- [x] Landing "addresses tracked" double-counted overlaps: decided 2026-10-16 to keep the
      plain sum and relabel it "address records" (tooltip explains the overlap).

From "city-tune audit for each new city" (the first line stays in TODO.md):

  **First pass 2026-10-23:** only tecumseh, west-parry-sound and middlesex have 2+ changed
  snapshots. Proposals: tecumseh ignore `GIS_ID`/`GIS_ID_OLD` (placeholder `T_0000` gets a
  real id 1-3 days after a point appears: 5 rows so far); middlesex ignore `FULL_NAME`
  (derived echo, 1 solo change); west-parry-sound could key on `globalid` (stable on all
  21,734 across 10-19..10-21, carried the 44->30 Emily St renumber), but it needs a
  re-baseline, since stored props drop globalid. All three key on address + coords, so a
  move or renumber reads as retire + add and `location_min_move_m` can't help (middlesex's
  TOML comment saying it can is wrong). Watch grey: 129 points moved 1.4-9 m on 10-17.
  **amherstburg, cobourg, halton-hills, norfolk have been byte-identical since 08-20** -
  frozen sources, a data-integrity look, not a tuning one.
  **Looked 2026-10-23** (64-65 identical daily pulls each since 08-20; all four stores
  baseline-only, so any re-point is a fresh baseline):
  - **norfolk: stale hosted copy.** The AGOL layer was last edited 2025-11-10 (a bulk
    republish), 35,121 rows. The county's own `gis.norfolk.ca` serves the same feature
    class at 35,253, newest record created 2026-10-20 (245 created since 2025-11-10).
    Candidate: `https://gis.norfolk.ca/arcgis/rest/services/Services_Public_GISviewer/Land_Records_Public/MapServer/2`
    (same fields + COMMENTS, OID `OBJECTID`, maxRecordCount 1000; avoid CityView_GISviewer/2,
    whose LastModified is rewritten nightly). The server 403s urllib's default User-Agent.
    The licence covers the AGOL open-data item, not this viewer service.
    **Re-pointed 2026-10-23** (operator: keep publishing, the item's licence read as covering
    the county's own copy): fresh baseline, 35,251 rows; 34,933 of 35,119 old keys survive,
    318 new, 186 gone. Vault day filed `schema`. Backup `ontario-db-backup-2026-10-23-norfolk`.
  - [ ] **cobourg: stale copy of a slow town.** AGOL bulk-republished 2026-05-08 (7,837); its
    source `https://geo.cobourg.ca/server/rest/services/Operations/FireQuickLookup/MapServer/10`
    has 7,846, ~2 new points a month. Re-point there if AGOL hasn't moved by **2026-12-01**
    (ignore CREATED_DATE/LAST_EDITED_DATE; STATUS is a class candidate). Not the editable
    Operations/Property/FeatureServer/30 (anonymous edits open; 9,999 rows incl. 1,399 more units).
    **AGOL moved 2026-10-27** (found 10-30): bulk republish (all three editingInfo stamps
    equal, same signature as 05-08, so a ~5.5-month cadence), now 7,846 = the source. The
    store took it cleanly as snapshot 25: 11 added, 1 modified, 2 gone, 7,834 of 7,837 synth
    keys survived the OBJECTID re-mint; new rows are subdivision growth (61-161 Kerr St E,
    737 New Amherst Blvd). The 12-01 trigger no longer applies; what is left is an owner
    call on whether a semi-annual republish is good enough or the daily source is worth a
    re-point (gated city, so no public cost either way). Leave it unless the cadence slips.
    **Re-pointed 2026-10-31 (owner's call) as a continuation, not a baseline:** same four mapped
    columns, same native SR, 7,846 of 7,846 synth keys survive with identical coordinates, so
    the store kept its history; snapshot 29 is +0/-0/~7,846 (props roster grew by ten: STATUS,
    Roll_Num, RoutingStreetExtKey, ADD_TYPE, FDMID, ROTATION, four constants), pre-ruled technical
    in flags.toml before the import, vault day filed `schema`. CREATED_DATE/LAST_EDITED_DATE never
    reach props (EDIT_METADATA_FIELDS). STATUS {Correct 7,728, Needs Attention 116, Not Checked 2}
    is a class candidate once a transition is seen; Roll_Num/RoutingStreetExtKey are ignore
    candidates once they churn. Backup `backups/2026-10-31-cobourg/`. LAST_EDITED_DATE max 10-14.
The other six August onboards (amherstburg, cobourg, halton-hills, middlesex, norfolk,
west-parry-sound) cannot be tuned yet — none has published a second distinct snapshot.

From the ontario-osm-data-sources portal sweep, 2026-10-16:

- [x] **west-parry-sound is failing daily (urgent).** The tracked
      `wpsgnPublic/wpsgn_opendata/FeatureServer/0` answers 500 "Service ... not started"
      (both attempts, 2026-10-15). The same server's
      `https://www.wpsgn.ca/s22/rest/services/NG911/NG911/FeatureServer/9112` ("Civic Address
      Point NENA") answers with 21,734 rows against our 21,705. A re-point, but onto a
      53-field NENA schema: new field map and identity, and pre-rule the schema-switch day
      the way lambton's was (flags.toml, 2026-09-15). Same network, same OGL question (§3).
      **Cost, measured 2026-10-16:** down every day since 09-24 except 10-01 (22 days, 63
      failed pulls, same message each time; the 10-01 pull succeeded and was byte-identical
      to 08-20, so the service was briefly *started* that day, not fixed). Because it fails
      on every attempt, every daily run since 09-24 has gone the full three attempts and
      exited 1 — 21 of 22 days — which saturates the exit code (nothing new can turn it
      red) and adds ~35 min/day (median run 47 min on a clean day vs 85 on a three-attempt
      day, Sept–Oct). Two routes, decide one: the NG911 re-point above, or first an email
      to info@wpsgn.ca (the TOML already names them for the licence-scope question) — a
      "not started" service is an operator-side switch and the 10-01 blip shows it can be
      flipped. (2026-10-16: the daily cost is gone without either — WPS now fails in
      half a second with no retries and no longer fails the run, see the flaky-sources
      item in §4. `enabled = false` in its TOML now pauses it outright if wanted.)
      **DONE 2026-10-16: re-pointed to NG911/9112, store re-baselined rather than diffed.**
      Measured first: the store held a single snapshot (08-20) because the old layer was a
      frozen export, while NG911 carries edits dated 2023-03 to 2026-10. 98.1% of identity
      keys survived the new field map (`add_num`/`name_body`/`unitnumber`/`full_add`). The
      ~420 that didn't are a 2023-26 edit backlog (104 Fire Route -> named-road renames, 30
      renumbers, ~97 gone, ~130 new) plus ~120 unit re-spellings, none of it dated, so
      diffing across the switch would have published years of edits under one day. Owner
      chose a fresh baseline (no events, no flags). The landing page now reads "last snapshot
      2026-10-16", and the old 08-20 baseline report is removed. Vault day filed `schema`.
      Old store backed up at `C:\Users\kk\ontario-db-backup-2026-10-16-wps\` (it also carries
      a stray NG911 import on top; README there says how to strip it). The info@wpsgn.ca
      licence-scope question (§3) is still open: NG911 publishes no licence either.
- [x] **middlesex follows a 2023 snapshot.** `MiddlesexCountyAddressPoints` (item name
      `mc_address`) was last edited 2023-10-18 and holds 31,571. The county's live layer is
      `https://utility.arcgis.com/usrsvcs/servers/f4dd79bdd35a456c87c0c20668138c05/rest/services/MiddlesexCounty/Base_Layers/MapServer/1`,
      34,308 rows. No licence on either, so the gate is unchanged. A `utility.arcgis.com`
      proxy URL: check it is stable before trusting it.
      **DONE 2026-10-16.** The proxy is registered by public AGOL item
      `f4dd79bdd35a456c87c0c20668138c05` (same owner, Colesberry; created 2026-08-05), so it
      lives as long as that item. Same fabric (99.0% of the old address tuples reappear) but
      5,849 points re-placed by > 1.1 m, and the old store was baseline-only, so it was
      re-baselined: 34,299 rows, no events, no flags; vault day filed `schema`; old store at
      `C:\Users\kk\ontario-db-backup-2026-10-16-middlesex\`. The first pull came back
      28,637 of 34,308: the vault fetcher paged on a plain `OBJECTID` column because the
      MapServer omits `objectIdField` (fixed in address-vault `db63039`, the OID now comes
      from the field type). Liveness is still unproven - no editingInfo; the 90-day
      source-stale alert will say. Follow-ups:
  - [x] **Layer 0 of the same service, "Address (Units)", holds 2,298 unit points** (only
        `STREET_UNI` + `FULLADDRES`, 465 buildings); the tracked layer 1 has 424 unit rows,
        419 of them also in layer 0. The old export had 568 unit rows (420 here, 531 there),
        so the re-point dropped ~148 units. **Decided 2026-10-16: the tracker does not care**
        (no second dataset). An import does: noted in address-importer-friend
        `future-work/multi-city/onboarding-queue.md` (parked section) so a middlesex import
        takes its units from layer 0.
  - [x] **location_min_move_m** once a second distinct snapshot exists: the re-placement
        shape (median 0 m, p90 8.4 m) looks like toronto's jitter.
        **No floor, closed 2026-10-30.** Five distinct snapshots since the re-baseline (34,299
        -> 34,307, eight new civic addresses, zero retirements, zero modifications); over all
        34,299 persisted keys the move distribution is 0 m everywhere. The 8.4 m p90 was
        export-vs-live, one-off. The floor would be inert anyway (coords in the key).
- [x] **elgin's tracked layer has not moved since 2026-06-12** (30 identical pulls,
      21,785 rows, `Public/MapServer/1` "E911", no lastEditDate). The county now publishes
      `https://services6.arcgis.com/TCQ78XR5HqDZ1SDc/arcgis/rest/services/Elgin_Civic_Numbers_2026/FeatureServer/0`
      (item `4ec0a122eed343948c0bb705733a2861`, owner `elgingis`), 24,177 rows, edited
      2026-10-05. Its item licenseInfo is empty, but the county's Hub
      (`elgin-county-open-data-Elgin-County.hub.arcgis.com`) names "Open Government Licence -
      County of Elgin" portal-wide, which the 2026-08-20 check ("none published") predates.
      A re-point and a §3 licence recheck, the dufferin shape (portal-wide notice only).
      **DONE 2026-10-16.** Licence chain recorded in the toml and LICENSING.md (item in group
      `OD_Administrative`, which the open-data hub site catalogues; that site's licenseInfo
      is the full OGL - County of Elgin; the county's GeoHub site has non-commercial terms
      but does not list the item); tier `unknown-review` -> `yellow-ogl`, so it joins the
      LWG email list - **your verdict, not mine: I recorded evidence**. Same fabric (94.1% of
      (number, street first word) pairs) but no key survives - street types are spelled out
      now - and the old store was baseline-only, so it was re-baselined: 24,176 rows, no
      events, no flags; vault day `schema`; old store and its two raw pulls at
      `C:\Users\kk\ontario-db-backup-2026-10-16-elgin\`. StrUNIT is "N/A" on 22,756 rows,
      so normalize now drops exact "N/A" as null (`2c9de922a`). The layer was created in one
      upload on 2026-10-05 and is named for the year: it may be an annual export, and the
      90-day stale alert will tell. Issue #39 (source-stale) closes on the next hourly pass.
- [x] **Essex County is not "No address layer" any more.** (Ticked 2026-10-30: tecumseh tracked
      2026-10-16, leamington 2026-10-23, skipped.toml entry rewritten; queue rows 4 and 11.) Tecumseh publishes
      `https://gisweb.tecumseh.ca/arcgis/rest/services/OpenDataMaps/OpenDataMAP_InfraZonePropBound_Layers/MapServer/33`,
      9,860 points (number, street, suffix), catalogued under "Open Government Licence - The
      Corporation of the County of Essex". A new dataset; fix the skipped.toml entry either way.
- [x] **Grey County has an address fabric again** (ticked 2026-10-30: grey, blue-mountains and
      grey-assigned-addresses tracked 2026-10-16, gated; the licence ask is the open half, queue row 5), on `gis.grey.ca/server`:
      `Public/Service_ParcelLabels/MapServer/3` (51,458 county-wide addresses on parcel
      polygons, centroiding needed) and `.../MapServer/2` (10,509 Blue Mountains points). No
      licence published, and it answered 403 from here on 2026-10-16. Update skipped.toml
      from "No address layer" to the licence gate.
- [x] **Member layers under open licences, in regions we track** (ticked 2026-10-30: all tracked
      2026-10-16 except Orillia / New Tecumseth, degraded copies of simcoe; queue row 9)**:** Ajax (38,381, Ajax Open
      Data Licence v1.0), Whitby (49,090, Whitby OGL) and Pickering (42,743, Pickering Open
      Data License) inside durham, which is yellow-review on the Region's own licence;
      Newmarket (34,923) inside york; Welland (22,461, OGL Welland) and Niagara Falls city
      (35,700) inside niagara-falls; Orillia (11,274) and New Tecumseth (14,836) inside simcoe.
      Only durham's matter now: if its licence fails the LWG, these three cover most of it.

Checked and not new: dufferin's Entrances vs Address_Points (your decision, in its toml);
simcoe's NG911 layer (188,698, smaller than the tracked 190,432); waterloo's MapServer
endpoint (263,200, an alternative to the Hub shapefile export if that ever breaks); North
Bay, Oxford, Haliburton, Sault Ste. Marie and the City of Peterborough (the catalogue also
finds no usable licence).

**OUTCOME 2026-08-20 — the onboarding wave ran the same day the probes below landed.**
Eleven datasets imported with verified baselines: **simcoe** (190,207 — covers
Innisfil 20,540 + Collingwood 15,323 + 16 more member munis; no Barrie overlap,
verified), **norfolk** (35,119), **middlesex** (31,569 — all six dead-server munis
plus Adelaide Metcalfe and Middlesex Centre; no London overlap), **prince-edward-county**
(27,393), **haldimand** (26,597), **halton-hills** (21,900), **west-parry-sound**
(21,703), **perth-county** (18,605), **stratford** (14,873), **amherstburg** (10,924),
**cobourg** (7,837 — tracked but gated off the site: unmodified-only licence grant, see
§3). Four refused at the licence gate and returned to skipped.toml with quotes:
**oxford**, **north-bay**, **haliburton**, **sault-ste-marie** (SSM is borderline —
non-commercial-only terms; a free tracker arguably qualifies, overrule if you disagree).
Each new TOML documents identity/field-map evidence; all need a `city-tune` audit pass
once they have 2+ snapshots. The per-city probe notes below are retained as the record.

From "Dead endpoints" (re-probed 2026-08-20):

  - [x] Simcoe County (onboarded 2026-08-20) — **recovered**, different layer on the same server:
        `https://maps.simcoe.ca/arcgis/rest/services/Public/Operational_Layers_Dynamic/MapServer/1`
        ("Address Numbers"), 190,207 rows, paginated, full parsed schema (STNUM/STNAME/
        Unit/MUNI/FULL_ADDRESS + ADDRESSID). The old Search_Layers_Dynamic went
        token-secured. Licence not stated on the service. Big: would cover many member
        municipalities — check overlap policy before onboarding.
  - [x] Oxford County (refused at the licence gate 2026-08-20) — **recovered at the same server**:
        `https://public.oxfordcounty.ca/arcgis/rest/services/OpenData/OXFORD_OpenData/MapServer/0`
        ("OXFORD_CivicAddress"), 56,658 rows, maxRecordCount 100k (single-pull), rich
        schema incl. UNIT and END_DATE/END_REASON (source-side retirement tracking —
        count may include ended records; filter decision needed at onboarding).
        Licence text not exposed via REST.
  - [x] Haldimand County (onboarded 2026-08-20) — **migrated to a new server**:
        `https://gis.haldimandcounty.ca/server/rest/services/Topo/AddressPoints/FeatureServer/0`
        (NG911AddressPoints), 26,602 rows, NG911-style parsed fields + unit + Status.
        Old maps.haldimandcounty.on.ca still redirects everything to a maintenance page.
        Licence not stated.
  - [x] Middlesex County (onboarded 2026-08-20; layer is a 2023 snapshot, see the 2026-10-16 sweep above) — **migrated to ArcGIS Online**, one layer covers all six
        member municipalities (MUNCODE confirms LB/NEWB/NMID/SWM/SC/THC, plus Adelaide
        Metcalfe and some blank codes to watch):
        `https://services.arcgis.com/vhh9rYcMiBEBPGYb/arcgis/rest/services/MiddlesexCountyAddressPoints/FeatureServer/0`
        item `928ed74edad64e4aa65170fb49c46476`, 31,571 rows, parsed fields + UNIT.
        Licence: county "as is" disclaimer terms on an open public item. (A slimmer
        sibling `mc_address` without UNIT/MUNCODE also exists — prefer the full one.)
  - [x] Cobourg (onboarded 2026-08-20, gated off the site) — **migrated to ArcGIS Online**:
        `https://services5.arcgis.com/bD7yhukP2irPxz1v/arcgis/rest/services/Address_Points/FeatureServer/0`
        item `8e0339a5814b4c84b097c983c7626572`, 7,837 rows, parsed schema and a real
        source id (`ADD_ID` — good for identity). Terms of use at
        `public-hub-townofcobourg.hub.arcgis.com/pages/terms-of-use` — read before adding.
  - [x] West Parry Sound (onboarded 2026-08-20; down since 09-24, see the sweep above) — **recovered**, instance moved to `/s22`:
        `https://www.wpsgn.ca/s22/rest/services/wpsgnPublic/wpsgn_opendata/FeatureServer/0`
        ("Civic Address", official wpsgnet org), 21,705 rows, incl. unit, a `Retired`
        flag and Verified/rollnumber fields. Licence not stated.

From "No public address layer found at all" (hunted 2026-08-20):

  - [x] Perth County (onboarded 2026-08-20) — **found**: `https://services3.arcgis.com/FkQ7EeWcZFoXIXH7/arcgis/rest/services/NG911_Addresses_and_Roads_Public_View/FeatureServer/0`
        (county org, NG911 public view), 18,605 rows, parsed fields + Unit + Inc_Muni
        (North Perth / West Perth / Perth East / Perth South — Stratford and
        St. Marys, separated cities, are NOT included). Licence unstated.
  - [x] Halton Hills (onboarded 2026-08-20) — **found**: `https://services3.arcgis.com/Nn3SWZrtm4WZaUtd/arcgis/rest/services/Civic_Address_(od)/FeatureServer/152`
        ("Master Town Civic Address Dataset", note layer id 152), 21,900 rows, rich
        parsed schema + a real source id (`ADDR_ID`).
  - [x] Prince Edward County (onboarded 2026-08-20) — **found, hiding inside "Property Info"**: layer 0 of
        `https://services1.arcgis.com/4HnHVMMKSNypEIkS/arcgis/rest/services/HostedFeatures___Property_Info/FeatureServer/0`
        is "Site Structure Address Points - Unfiltered" (NENA schema), 27,580 rows;
        probably needs a `STATUS_pec = 'Current'` filter. Licence unstated.
  - [x] Innisfil + Collingwood (covered by simcoe since 2026-08-20) — **found via the recovered Simcoe County layer**
        (§ above): MUNI groupBy verified INNISFIL 20,540 and COLLINGWOOD 15,323 of
        the 190,207 county-wide rows (16 more municipalities in there too — Bradford
        West Gwillimbury, Wasaga Beach, Orillia, Midland...).
  - [x] North Bay (refused at the licence gate 2026-08-20) — **found, with a staleness caveat**:
        `https://services5.arcgis.com/ItUGraUlQOjvSGOV/arcgis/rest/services/CivicAddress_Point/FeatureServer/0`
        (city org), 21,964 rows — but editingInfo says data last edited April 2023,
        so it may be a static upload; verify it moves before onboarding.
  - [x] Stratford (onboarded 2026-08-20) — **found** on the city's ArcGIS Enterprise:
        `https://maps.stratford.ca/gisserver/rest/services/Addressing/Civic_Address/FeatureServer/0`,
        14,873 rows, parsed fields + unit.
  - [x] Amherstburg (onboarded 2026-08-20) — **found (new since last check)**, moved out of the special-cases
        list: `https://mapamherstburg.ca/arcgis/rest/services/Address_Points/FeatureServer/0`,
        10,925 rows, real address points (ARN, Add1 number, FullStName). Licence
        unstated. This is also the only Essex County municipality with points.
  - [x] Haliburton County (refused at the licence gate 2026-08-20) — **promising lead, polygon not points**:
        `https://gis.haliburtoncounty.ca/arcgis/rest/services/Public/SearchLayers_2/MapServer/4`
        ("Address", polygon, 33,980 rows, ARN/ADDNUM/STREET/TOWNSHIP). Usable only if
        centroids are acceptable (cf. windsor's parcel centroids — precedent exists).
  - [x] Lanark County (tracked 2026-10-31, gated) — was nothing machine-readable (CommunityPAL MapGuide viewer, no REST).
        **Lead 2026-10-30:** CGIS's newer SLIMS Viewer (`cgis.com/publicmaps/?c=LanarkCounty`)
        has a county-wide "Civic Addresses" dataset 83040 (created 2026-05, updated 09-30,
        tiles rebuilt daily; ~36k points, 15-digit roll keys) on public routes:
        `cgis.com/api2/public/LanarkCounty/tiles/83040/{x}/{y}/{z}?t=<tileset ts>` (MVT) and
        `.../geometry/83040.geobuf|.flatgeobuf?t=...`; `.geojson` 500s server-side. Attributes
        are roll + street_number only - the street name is on "Assessment Parcels" 85360
        (`location`, joinable by roll). Terms: the CGIS disclaimer, no open licence. See the
        CGIS item below. Perth, Mississippi Mills and Smiths Falls have their own instances.
  - [x] Timmins (tracked 2026-10-31, gated) — same stack. **Lead 2026-10-30:** SLIMS `?c=Timmins` added "Civic
        Addresses" 98640 on 2026-09-23 (updated 10-26, tiles daily), ~20-30k points with
        duplicate roll keys (one per roll+unit, likely), roll + street_number only; full
        string on Assessment Parcels 98638. Same routes, same broken geojson, same terms.
  - [x] Grey County (tracked 2026-10-16, gated) — was: still nothing, and a new fact: maps.grey.ca is their Hub
        (catalogue enumerated — no addresses); geo.grey.ca / restgeo.grey.ca remain
        down (522/timeout), a persistent outage rather than a transient one.
  - [x] Owen Sound — still nothing of its own (re-probed 2026-10-30: 48 services, Parcels
        address1-3 the only fallback), but **covered since 2026-10-16 by grey**: the tracked
        parcel-label layer holds ~6,770 Owen Sound rows (city spelt five ways in `city`).
  - [x] Brockville — PSDCitywide, the PublicOnly folder and the count all 499 Token Required
        (2026-10-16, 2026-10-30), city org roads only; but **covered by leeds-grenville**:
        8,737 rows with MUN = 'CITY OF BROCKVILLE' (edited 2026-10-06, OGL), matching the
        PSD layer's 8,796.
  - [x] **CGIS SLIMS as a source type (Lanark + Timmins, found 2026-10-30).** **Built 2026-10-31**
        (owner's call): address-vault `fetch/slims.py` downloads the civic and parcel `.geobuf`
        exports (work without `t=`; `.flatgeobuf` 500s on parcels, `.geojson` everywhere), joins
        parcel `location` to civic rows by roll, explodes each roll's MultiPoint, writes WGS84
        geojson - so the archived pull is a derived product, said in the TOMLs. `data_url` grammar
        `.../geometry/<civicId>.geobuf?join=<parcelId>`; dep `geobuf` (optional extra `slims`),
        decoder applies the spec precision default the CGIS header omits. DegradedPull below a 50%
        join rate. Join: lanark 100% of 36,153 rolls; timmins 86.3% (2,703 parcels publish no
        location). Baselines lanark 37,215 (790 rolls carry 2-20 points), timmins 29,532 (7,358
        points have no number; one roll has 123 points). Field map number = street_number, full =
        location, `street_from_full`; key synth number + roll + geometry (location kept out of the
        basis so a short parcels export shows as a held mass change, not a re-key). Only the
        2% feature-count flag guards truncation (no count endpoint). Open: the licence ask to
        Lanark County and Timmins (CGIS hosts, the data is theirs). Three decisions were
        decisions before either is trackable: (1) a new `access` kind in address-vault for
        MVT-tile sweeps or the geobuf/flatgeobuf export (the export is one file per
        dataset, simplest; the `t=` tileset stamp changes daily); (2) the street name - join
        Civic Addresses to Assessment Parcels `location` by roll number, or ask CGIS /
        the county for the records route; (3) licence - only the CGIS disclaimer exists,
        so an ask to Lanark County and Timmins (the data is theirs, CGIS hosts it) before
        anything publishes; vault-only is fine meanwhile. The probe scripts and raw
        results are in `%TEMP%\reprobe_2026-10-30\` for now (temporary, not committed).

From "Special cases":

  - [x] **Norfolk County** (onboarded 2026-08-20) — resolved itself 2026-08-20: the county published an OPEN
        sibling of the secured layer.
        `https://services1.arcgis.com/mSGV2hCLXHNsfQqK/arcgis/rest/services/Civic_Addresses/FeatureServer/0`
        item `05c74eeabb454f54b9f50ca1b0dd5326`, 35,121 rows, parsed fields + unit +
        roll number, and an explicit "Open Data Licence Agreement" (OGL-style). The
        old `CivicAddresses` is still token-secured. Ready to onboard.
  - [x] **Sault Ste. Marie** (refused at the licence gate 2026-08-20, borderline) — a stable undated layer now exists, removing the reason
        it was skipped: `https://services1.arcgis.com/nlLTq2Zj0Jwv1qft/arcgis/rest/services/SooMaps_Addresses_View/FeatureServer/0`
        (item "SooMaps_Addresses View", owner City of SSM), 33,356 rows, clean civic
        schema incl. unit + postal code, created 2026-03, data edited 2026-08-13 — a
        continuously maintained hosted view, not a dated snapshot. Licence not stated
        on the item.
  - [x] **Amherstburg** — resolved 2026-08-20: civic address points now exist (moved
        to the found-sources list above).
