# Licensing status — all tracked datasets

**The single place for each dataset's licence colour and comment.**
Hand-maintained: update this table in the same change as any edit to a
dataset's `osm_compatible` tier, any new licence finding, any government
contact sent or answered, and any LWG correspondence. The `osm_compatible`
field in `datasets/<slug>.toml` stays the machine-readable value; this file
carries the evidence and the next step. If the two disagree, this file is
newer or the toml was edited without updating it — fix whichever is stale.

Last full review: **2026-08-20** (all 18 then-unresolved datasets probed live:
item `licenseInfo`, DCAT feeds, hub terms pages, publisher websites; evidence
URLs quoted in each TOML). Previous full review 2026-08-16; its method note
stands (licence page where published, else ArcGIS service JSON →
`serviceItemId` → portal item `licenseInfo`). Detail lives in the engine's
`future-work/multi-city/license-contacts-todo.md` and the LWG email (sent,
date not recorded; no reply as of 2026-10-11), drafted at
<https://gist.github.com/skfd/043eded6a26b279b7cf75aa3927b14da>.

**Publishing gate (new 2026-08-20):** datasets whose published terms forbid
republication carry `publish_reports = false` in their TOML — tracking
continues, but the site renders no report pages for them and the landing page
marks them "licence not compatible". Currently: sdg, renfrew,
peterborough-county, cobourg (unmodified-only grant, the Peterborough shape).
From the 2026-10-16 sweep, also: blue-mountains, caledon, dryden, gorham-ware, grey, grey-assigned-addresses, haliburton, north-bay, oliver-paipoonge, oshawa, oxford, peterborough, sault-ste-marie, vaughan, vaughan-ng911.

Tier legend: **green** = usable (LWG-listed licence or equivalent; `green-self` = self-listed on wiki Contributors under the OSMF self-service procedure) ·
**yellow** = OGL-family variant awaiting the variant-review email ·
**orange** = CC BY, needs the OSMF waiver · **red** = restrictive terms,
permission ask required · **unknown** = no licence text found, must ask.

Note: OSM compatibility (this file's tiers) and *this project's own
diff-report publishing* are separate questions. The 2026-08-20 review answered
the second for every non-green city: cleared for all OGL-family cities and for
burlington/london (pass-through condition); blocked for sdg / renfrew /
peterborough-county (gated); unclear-by-silence for the unknowns.

## Green — 20 (licence on the OSMF-approved list or equivalent)

| dataset | tier | licence |
|---|---|---|
| barrie | green-self | Open Government Licence - Barrie (**self-listed on Contributors 2026-10-12**; + MFIPPA exemption (as Oakville, Niagara Region, Toronto); **re-pointed 2026-10-12** to the licensed `Open_Data/AddressVW` (item `4902c7fd…`); the old COB_ADDRESS_POINT had no licence statement. Same ADDRESSID key; AddressVW carries far fewer Pending addresses (680 vs 3,153)) |
| brant | green-cc0 | CC0 (item licenseInfo, re-tiered 2026-08-16; ODbL-compatible outright, no LWG needed; optional courtesy confirm with county) |
| cambridge | green-lwg | Open Government Licence - City of Cambridge |
| cornwall | green-lwg | Open Government Licence - City of Cornwall |
| dufferin | green-self | Open Government Licence – The County of Dufferin (**self-listed on Contributors 2026-10-12**; four OSMF categories only). The tracked Entrances layer is the **item-licensed** one; the better `Address_Points` layer is covered only by the portal-wide notice, so the 2026-10-12 licence pass did not re-point it. **Re-pointed 2026-10-16** to `Address_Points` (owner's call), fresh baseline; the self-listing reads on the county licence, which the portal-wide notice extends to this layer) |
| greater-sudbury | green-self | Open Data Licence - City of Greater Sudbury (**self-listed on Contributors 2026-10-12**; Quinte West's approved text (open-ended exemption, PHI, by-laws, "Use")) |
| guelph | green-lwg | Open Government Licence - City of Guelph |
| haldimand | green-self | Open Government Licence – Haldimand County (**self-listed on Contributors 2026-10-12**; Toronto's approved text word for word) |
| hamilton | green-lwg | Open Data Licence – Hamilton |
| huron | green-self | Open Government Licence – The County of Huron (**self-listed on Contributors 2026-10-12**; + MFIPPA/PHIPA exemption (Toronto, Hamilton)) |
| kingston | green-lwg | Open Data Licence - City of Kingston |
| niagara-falls | green-lwg | Open Government Licence - Niagara Region |
| oakville | green-lwg | Open Government Licence – Town of Oakville (**LWG-listed compatible 2026-09-14**, verified 2026-10-09 on the [OSMF variants page](https://osmfoundation.org/wiki/OGL_Canada_and_local_variants), which links the town's [licence PDF](https://www.oakville.ca/getmedia/3cb7902a-2220-433e-8aed-24f326b745b9/town-hall-oakville-open-data-licence.pdf); OSM wiki Contributors entry exists, added by TronnaLegacy 2026-08-31 via the OSMF self-service procedure — which message prompted the LWG listing is not known; Canada#Open_Data table still says "Not accepted" — stale. ALSO brownfield-active (TronnaLegacy MapRoulette 55881) — do not touch regardless) |
| ottawa | green-lwg | Open Government Licence – City of Ottawa 2.0 |
| quinte-west | green-lwg | City of Quinte West Open Data Licence |
| thunder-bay | green-lwg | City of Thunder Bay Open Data Licence |
| toronto | green-lwg | Open Government Licence – Toronto |
| waterloo | green-lwg | Open Government Licence – City of Waterloo |
| windsor | green-self | Open Government Licence – The Corporation of the City of Windsor (**self-listed on Contributors 2026-10-12**; + MFIPPA exemption, "official marks" (Niagara Region); **re-pointed 2026-10-12** to the licensed Address Polygon layer `OpenDataServices/PropertyParcels/MapServer/1` (item `6793ba07…`) — the polygons keep all synthesized keys, the Address Point layer `/0` would have re-keyed 117k) |
| york | green-lwg | York Region Open Data Licence |

## Yellow — OGL-family variants for the LWG variant-review email (9)

Five of the six from 2026-08-16 (oakville went green 2026-10-09: LWG-listed
2026-09-14) plus **five found 2026-08-20** (frontenac,
leeds-grenville, lennox-addington, milton, windsor). The email covering the
six from 2026-08-16 was sent (date not recorded; no reply as of 2026-10-11).
Next, for these and every "add to email" row in this file: the OSMF
self-service route — diff against the Ottawa Open Data Licence 2.0; if the
only differences are locality name, legal venue, PII or "records"
definitions, add a Contributors entry and email
legal-questions@osmfoundation.org; follow up with legal-questions@ for any
that are not a pure variant (diffs in progress in
`ontario-osm-data-sources/licences/`). The **2026-08-16 user decision**
stands: scaffolding ahead of licence clearance is fine; any OSM import stays
gated until the licence clears (queue state: engine
`future-work/multi-city/onboarding-queue.md`).

| dataset | tier | licence | comment |
|---|---|---|---|
| brantford | yellow-ogl | OGL – Brantford v1.0 | clone; adds PHIPA to exemptions; venue drops Federal Court. The tracked `OP_Site_Addresses2` is the item-licensed layer ("See Licence"); the parked better layer `SiteAddress_pub` has no licenseInfo, so 2026-10-12 did not re-point it. The 2026-10-11 diff found added terms, so it is not self-service compatible (`licences/brantford/verdict.md`) |
| frontenac | yellow-ogl | OGL – County of Frontenac v1.0 | **found 2026-08-20** (was unknown): PDF linked from the Frontenac GIS hub, based on OGL-Ontario 1.0; oddity: clause 5 says don't "rely on it for navigation, decision making or advising" — add to email |
| kitchener | yellow-ogl | OGL – City of Kitchener v1.0 | attribution *voluntary*; city gave explicit OSM permission (wiki: Waterloo_region/Kitchener_authorization) — effectively cleared |
| leeds-grenville | yellow-ogl | OGL – United Counties of Leeds and Grenville v1.0 | **found 2026-08-20** (was "attribution line only"): full OGL-Canada-style text at geohub-uclg hub terms page; DCAT binds the address dataset to it — add to email. **Re-pointed 2026-10-12** to the licensed `LG_CivicAddress_OpenData` (item `3587c701…`); the old CivicAddress item had an empty licenseInfo. Identical data, so no history change |
| lennox-addington | yellow-ogl | OGL – County of Lennox and Addington v2.0 | **found 2026-08-20** (was unknown): item licenseInfo links the hub terms page; commercial OK, attribution line specified — add to email; the "ask gisservices@ to confirm in writing" step is now unnecessary |
| milton | yellow-ogl | OGL – Milton | **found 2026-08-20** (was unknown): Discover Milton hub "Disclaimer and Terms of Use"; caveat — the OGL covers the open-data page whose Address Points item points at `Datasets/Address_Pts`, while we track `WebMaps/MGIS/MapServer/63` (same host/publisher); consider re-pointing — add to email. **Re-point deferred 2026-10-12**: `Address_Pts` failed every query on 2026-10-11 (HTTP 500), has no STREET_NAME/FULL_ADDRESS (street would need composing from parts normalize cannot join) and no STATUS/WARD. Reasons in the toml |
| elgin | yellow-ogl | OGL – County of Elgin | **found 2026-10-16** (was unknown): the tracked layer was re-pointed the same day to `Elgin_Civic_Numbers_2026` (item `4ec0a122…`, empty licenseInfo). Chain: the item is in group `OD_Administrative` (`0b0a5bd5…`), which is in the catalogue of the Elgin County Open Data hub site (item `5fa753ff…`), whose licenseInfo is the full OGL text (commercial use, attribution "Contains information licensed under the Open Government Licence – County of Elgin."). Caveat: the county's other site, GeoHub (`a5a386c9…`, geohub.elgin.ca), carries non-commercial web-map terms, but the item is not in its groups. Portal-wide notice only, the dufferin shape — add to email |
| lambton | yellow-ogl | OGL 2.0 – County of Lambton | **moved out of green 2026-10-12**: diff vs Ottawa 2.0 found an added "sole and exclusive rights" sentence and a dropped Versioning clause (as Sarnia) — in the 2026-10-12 LWG follow-up email |
| sarnia | yellow-ogl | OGL – City of Sarnia (item licenseInfo of the renamed service) | re-tiered in the toml 2026-08-20 with the URL fix (service renamed `Addresses_Open_Data` → `Addresses_Open_Data_AGOL`, item `2ed254db85d6442a8b040213c0c6b097`); self-declared OGL-Canada 2.0 clone; already in the email |

## Near-green desk work (2)

| dataset | tier | licence | comment |
|---|---|---|---|
| peel-region | yellow-review | Open Data Licence for the Regional Municipality of Peel v1.0 | full text confirmed 2026-08-20 at data.peelregion.ca/pages/license (hub page item `a03e28df41e5423abea4beb34d975961`): OGL-like grant incl. commercial, attribution *optional*. Based on the UK OGL. Diff it against UK OGL and add to the email |
| durham | yellow-review | Region of Durham Open Data Licence v1.0 | **moved out of green 2026-10-11.** The toml named the City of Oshawa OGL, but the Region's own item for the tracked service (`8dcfee4f…`, owner GIS_DurhamRegion) cites the Region of Durham licence. Not OGL-Canada-based (optional attribution, credit removable on request, "not harmful to others", no venue clause) — needs the LWG. Diff: ontario-osm-data-sources `licences/durham/verdict.md` |

## Orange — CC BY waiver needed (1)

| dataset | tier | licence | comment (2026-08-16) |
|---|---|---|---|
| brampton | orange-ccby-waiver | CC BY 4.0 | confirmed on GeoHub; send OSMF waiver template to open@brampton.ca |

## Red — restrictive terms (5), three of them gated off the site

| dataset | tier | licence | comment |
|---|---|---|---|
| sdg | red-review · **publish_reports = false** | Proprietary (item licenseInfo) | explicit: "No part... may be sold, copied, distributed, or transmitted... without the prior written consent of the County. All rights reserved." Gated 2026-08-20: tracked, unpublished. Next step: permission ask |
| renfrew | red-review · **publish_reports = false** | Restrictive hub disclaimer | "Content may not be reproduced or redistributed without prior written permission", binds "any associated data"; OGDE-encumbered. Gated 2026-08-20: tracked, unpublished. Next step: permission ask |
| peterborough-county | red-review · **publish_reports = false** | County website Terms of Use | geospatial content "may not... be copied onto any other website without the written agreement... of the County" (ptbocounty.ca). Gated 2026-08-20: tracked, unpublished. Next step: permission ask |
| muskoka | red-review | Custom terms, no reuse grant | King's Printer copyright + disclaimer at map.muskoka.on.ca/pages/terms-of-use; ORN road data "used under licence". Not explicitly prohibiting, so still published — but a grant should be asked for |
| burlington + london | red-review | Open-data Terms of Use (2011-style, near-identical) | **read in full 2026-08-20**: automated retrieval permitted (by silence; revocable), and publishing derived diff reports **explicitly permitted** with pass-through (include a copy of / URL to the terms, bind recipients, no further restrictions). Our publishing is cleared once the terms URL is added to their report pages. OSM/ODbL vs the pass-through clause unresolved → stays red for OSM |

## Unknown — no licence text found after a real hunt (5)

chatham-kent, wellington, kawartha-lakes re-verified as genuine
absences 2026-08-20 (elgin too, until its hub published an OGL, found 2026-10-16) (item + DCAT + hub each checked; kawartha's hub PDF is a
disclaimer, not a grant). Ask each to publish/state a licence or grant OSM
permission (templates in the engine TODO).

| dataset | tier | comment |
|---|---|---|
| bruce | yellow-review | toml's "BGDISC Open Data Licence" is a data-sharing collaborative, not a licence; contact GIS@BruceCounty.on.ca |
| chatham-kent | unknown-review | confirmed none published 2026-08-20 (29 datasets on their DCAT feed all licence-less; address layer not even listed on the portal) |
| hastings | unknown-review (demoted from yellow-ogl 2026-08-16) | toml's licence name has no corresponding text anywhere; item says "General use. Open Data." |
| kawartha-lakes | unknown-review | confirmed 2026-08-20: item/DCAT/hub all carry the same as-is disclaimer, no grant, no prohibition |
| wellington | unknown-review | confirmed none published 2026-08-20 (no hub, no org-item licence; "Free for public use." covers the Explore app, not the data — bbox note: Guelph sits wholly inside, clipping applies regardless) |

## 2026-08-20 onboarding wave — 11 added, 4 refused at the licence gate

Every licence below was hunted live during onboarding (item licenseInfo, hub
pages, county sites); evidence and quotes in each TOML.

**Onboarded (11):**

| dataset | tier | licence | note |
|---|---|---|---|
| west-parry-sound | yellow-ogl | OGL – Township of The Archipelago v2 (OGL-Canada 2.0-based) | found via re3data; caveat: one member township's name on a district-wide layer — confirm scope with info@wpsgn.ca; add to email |
| norfolk | yellow-review | Norfolk County Open Data Licence Agreement | bespoke worldwide royalty-free perpetual grant, credit optional; does not self-declare an OGL basis |
| halton-hills | yellow-review | Town of Halton Hills Open Data License (hub page) | bespoke OGL-shaped grant "for any lawful purpose" |
| simcoe | yellow-review | Open Government Licence - Simcoe County (maps.simcoe.ca/openlicense.html) | open licence exists and the site terms exempt open-data layers into it, but coverage of this exact MapServer endpoint is inferred — confirm with the county, or switch to their GeoServer WFS which is unambiguously open-data |
| prince-edward-county | yellow-review | OGL – County of Prince Edward v1.0 (hub) | full OGL-Canada 2.0 clone recovered; the address item itself lacks the stamp — confirm, then promote to yellow-ogl |
| cobourg | red-review · **publish_reports = false** | Town of Cobourg Open Data Terms of Use (2021) | grant covers copying/redistributing the UNMODIFIED datasets only (the City-of-Peterborough shape) → tracked, unpublished; ask mchatten@cobourg.ca |
| middlesex | unknown-review | as-is disclaimer only (item licenseInfo) | no grant, no prohibition. **Re-pointed 2026-10-16** to the county's `Base_Layers/MapServer/1` via its utility.arcgis.com proxy item `f4dd79bd…` (same owner, Colesberry); no licence on that item either, so the tier is unchanged |
| perth-county | unknown-review | none published (confirmed) | |
| amherstburg | unknown-review | none published (confirmed) | only Essex County muni with address points — worth an ask |
| stratford | unknown-review | none published (confirmed) | |

**Refused at the gate (4, in skipped.toml with quotes):** oxford ("must not be
used or posted on an external website" despite the folder being named
OpenData), north-bay (northbay.ca/legal forbids copying onto other websites;
data also static since 2023), haliburton (view-and-print-a-single-copy grant +
explicit anti-scraping clause — the hardest terms in the catalogue),
sault-ste-marie (SooMaps click-through: non-commercial only, expressly
covering consumed mapservices — borderline for a free tracker; operator may
overrule).

## 2026-10-16 registry sweep — 24 added, none refused

The ontario-osm-data-sources portal sweep graded every address layer on every Ontario portal;
every live, non-copy one the tracker lacked was onboarded the same evening. **New rule: licence
decides publishing, never tracking** — a live layer with no licence or restrictive terms gets a
dataset with `publish_reports = false`, and a member city's own layer is tracked even inside a
tracked region (cities usually publish fresher data than the roll-up). The four refusals of
2026-08-20 (oxford, north-bay, haliburton, sault-ste-marie) and City of Peterborough are now
tracked, gated. Licence names marked "registry" in the TOMLs were read off a portal by the
sweep, not at the service: ajax, tecumseh, waterloo-region were read at the source the same night
(below; evidence in each TOML). Left out as provable views/copies of tracked layers: four L&A township views,
SDG North Dundas, Douro-Dummer, Simcoe's NG911 export and New Tecumseth/Orillia copies,
Strathroy-Caradoc 2024. Brockville is token-secured (skipped.toml).

| dataset | tier | licence |
|---|---|---|
| ajax | yellow-review (was unknown, read 2026-10-16) | Town of Ajax - Open Data Licence v.1.0: OGL-Ontario clone, credit optional; binds the layer only via the hub's site-wide "by using this site" text (item licenseInfo null, DCAT blank) - confirm coverage, then yellow-ogl |
| blue-mountains | unknown-review · **publish_reports = false** | (none published) |
| caledon | unknown-review · **publish_reports = false** | (none published) |
| dryden | unknown-review · **publish_reports = false** | (none published) |
| gorham-ware | unknown-review · **publish_reports = false** | (none published) |
| grey | unknown-review · **publish_reports = false** | (none published) |
| grey-assigned-addresses | unknown-review · **publish_reports = false** | (none published) |
| haliburton | red-review · **publish_reports = false** | (none published) |
| mississauga | yellow-review | City of Mississauga Terms of Use |
| newmarket | unknown-review | Town of Newmarket Open Data Licence |
| niagara-falls-city | yellow-ogl | Open Government Licence - Niagara Falls |
| north-bay | red-review · **publish_reports = false** | (none published) |
| oliver-paipoonge | unknown-review · **publish_reports = false** | (none published) |
| oshawa | unknown-review · **publish_reports = false** | (none published) |
| oxford | red-review · **publish_reports = false** | (none published) |
| peterborough | red-review · **publish_reports = false** | City of Peterborough Open Data Terms of Use |
| pickering | unknown-review | City of Pickering Open Data License |
| sault-ste-marie | red-review · **publish_reports = false** | (none published) |
| tecumseh | yellow-review (read 2026-10-16) | OGL - County of Essex v1.0, hub-wide; the county hub names Tecumseh, the item says only "(c) Town of Tecumseh". The County is the licensor, so ask Tecumseh GIS to confirm the County may license its points |
| vaughan | unknown-review · **publish_reports = false** | (none published) |
| vaughan-ng911 | unknown-review · **publish_reports = false** | (none published) |
| waterloo-region | **green-lwg** (read 2026-10-16) | OGL - Region of Waterloo v2.0, LWG-approved 2025-02-10; licence page moved in the 2026-05 CMS move (old URL 404) |
| welland | yellow-ogl | Open Government Licence - City of Welland |
| whitby | yellow-ogl | The Corporation of the Town of Whitby Open Government License |

## Counts (2026-10-16, after the registry-sweep onboarding; tallied from the TOMLs)

green 21 (14 `green-lwg`, 6 `green-self`, 1 `green-cc0`) · OGL-family awaiting the LWG 13 ·
yellow-review 10 · CC-BY waiver 1 · restrictive 12 · unknown 20 — of **77 tracked datasets**.
19 are gated off the site (`publish_reports = false`): sdg, renfrew, peterborough-county,
cobourg, plus the 15 from the 2026-10-16 sweep listed above.
