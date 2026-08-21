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
`future-work/multi-city/license-contacts-todo.md` and the draft LWG email:
<https://gist.github.com/skfd/043eded6a26b279b7cf75aa3927b14da>.

**Publishing gate (new 2026-08-20):** datasets whose published terms forbid
republication carry `publish_reports = false` in their TOML — tracking
continues, but the site renders no report pages for them and the landing page
marks them "licence not compatible". Currently: sdg, renfrew,
peterborough-county, cobourg (unmodified-only grant, the Peterborough shape).

Tier legend: **green** = usable (LWG-listed licence or equivalent) ·
**yellow** = OGL-family variant awaiting the variant-review email ·
**orange** = CC BY, needs the OSMF waiver · **red** = restrictive terms,
permission ask required · **unknown** = no licence text found, must ask.

Note: OSM compatibility (this file's tiers) and *this project's own
diff-report publishing* are separate questions. The 2026-08-20 review answered
the second for every non-green city: cleared for all OGL-family cities and for
burlington/london (pass-through condition); blocked for sdg / renfrew /
peterborough-county (gated); unclear-by-silence for the unknowns.

## Green — 17 (licence on the OSMF-approved list or equivalent)

| dataset | tier | licence |
|---|---|---|
| barrie | green-lwg | Open Government Licence - Barrie |
| brant | green-cc0 | CC0 (item licenseInfo, re-tiered 2026-08-16; ODbL-compatible outright, no LWG needed; optional courtesy confirm with county) |
| cambridge | green-lwg | Open Government Licence - City of Cambridge |
| cornwall | green-lwg | Open Government Licence - City of Cornwall |
| durham | green-lwg | Open Government Licence – City of Oshawa |
| greater-sudbury | green-lwg | Open Data Licence - City of Greater Sudbury |
| guelph | green-lwg | Open Government Licence - City of Guelph |
| hamilton | green-lwg | Open Data Licence – Hamilton |
| kingston | green-lwg | Open Data Licence - City of Kingston |
| lambton | green-ogl | Open Government Licence - County of Lambton |
| niagara-falls | green-lwg | Open Government Licence - Niagara Region |
| ottawa | green-lwg | Open Government Licence – City of Ottawa 2.0 |
| quinte-west | green-lwg | City of Quinte West Open Data Licence |
| thunder-bay | green-lwg | City of Thunder Bay Open Data Licence |
| toronto | green-lwg | Open Government Licence – Toronto |
| waterloo | green-lwg | Open Government Licence – City of Waterloo |
| york | green-lwg | York Region Open Data Licence |

## Yellow — OGL-family variants for the LWG variant-review email (11)

The six from 2026-08-16 plus **five found 2026-08-20** (frontenac,
leeds-grenville, lennox-addington, milton, windsor). Waiting on: adding the
new five to the drafted email, human read, send, reply. The
**2026-08-16 user decision** stands: scaffolding ahead of the LWG reply is
fine; any OSM import stays gated on the reply (queue state: engine
`future-work/multi-city/onboarding-queue.md`).

| dataset | tier | licence | comment |
|---|---|---|---|
| brantford | yellow-ogl | OGL – Brantford v1.0 | clone; adds PHIPA to exemptions; venue drops Federal Court |
| dufferin | yellow-ogl | OGL – County of Dufferin v2 | verbatim-verified from county PDF; PII via *provincial* FIPPA; omits the not-accessible-records exemption (more permissive) |
| frontenac | yellow-ogl | OGL – County of Frontenac v1.0 | **found 2026-08-20** (was unknown): PDF linked from the Frontenac GIS hub, based on OGL-Ontario 1.0; oddity: clause 5 says don't "rely on it for navigation, decision making or advising" — add to email |
| huron | yellow-ogl | OGL – The County of Huron v2.0 | verbatim in ArcGIS item; self-declares diffs vs OGL-Ontario 1.0; NB: county GIS page shows a separate restrictive licence for contracted products |
| kitchener | yellow-ogl | OGL – City of Kitchener v1.0 | attribution *voluntary*; city gave explicit OSM permission (wiki: Waterloo_region/Kitchener_authorization) — effectively cleared |
| leeds-grenville | yellow-ogl | OGL – United Counties of Leeds and Grenville v1.0 | **found 2026-08-20** (was "attribution line only"): full OGL-Canada-style text at geohub-uclg hub terms page; DCAT binds the address dataset to it — add to email |
| lennox-addington | yellow-ogl | OGL – County of Lennox and Addington v2.0 | **found 2026-08-20** (was unknown): item licenseInfo links the hub terms page; commercial OK, attribution line specified — add to email; the "ask gisservices@ to confirm in writing" step is now unnecessary |
| milton | yellow-ogl | OGL – Milton | **found 2026-08-20** (was unknown): Discover Milton hub "Disclaimer and Terms of Use"; caveat — the OGL covers the open-data page whose Address Points item points at `Datasets/Address_Pts`, while we track `WebMaps/MGIS/MapServer/63` (same host/publisher); consider re-pointing — add to email |
| oakville | yellow-ogl | OGL — Town of Oakville | clone of OGL-Canada 2.0; ALSO brownfield-active (TronnaLegacy MapRoulette 55881) — do not touch regardless |
| sarnia | yellow-ogl | OGL – City of Sarnia (item licenseInfo of the renamed service) | re-tiered in the toml 2026-08-20 with the URL fix (service renamed `Addresses_Open_Data` → `Addresses_Open_Data_AGOL`, item `2ed254db85d6442a8b040213c0c6b097`); self-declared OGL-Canada 2.0 clone; already in the email |
| windsor | yellow-ogl | OGL – The Corporation of the City of Windsor v1.0 | **upgraded from red 2026-08-20**: the "Terms of Use" PDF at opendata.citywindsor.ca is a full OGL; the city's portal binds its Address datasets to it. Caveat: we track mappmycity.ca rather than the portal copy — consider re-pointing. Add to email |

## Near-green desk work (1)

| dataset | tier | licence | comment |
|---|---|---|---|
| peel-region | yellow-review | Open Data Licence for the Regional Municipality of Peel v1.0 | full text confirmed 2026-08-20 at data.peelregion.ca/pages/license (hub page item `a03e28df41e5423abea4beb34d975961`): OGL-like grant incl. commercial, attribution *optional*. Based on the UK OGL. Diff it against UK OGL and add to the email |

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

## Unknown — no licence text found after a real hunt (6)

chatham-kent, elgin, wellington, kawartha-lakes re-verified as genuine
absences 2026-08-20 (item + DCAT + hub each checked; kawartha's hub PDF is a
disclaimer, not a grant). Ask each to publish/state a licence or grant OSM
permission (templates in the engine TODO).

| dataset | tier | comment |
|---|---|---|
| bruce | yellow-review | toml's "BGDISC Open Data Licence" is a data-sharing collaborative, not a licence; contact GIS@BruceCounty.on.ca |
| chatham-kent | unknown-review | confirmed none published 2026-08-20 (29 datasets on their DCAT feed all licence-less; address layer not even listed on the portal) |
| elgin | unknown-review | confirmed none published 2026-08-20 (self-hosted server + 23 hub datasets, all licence-less) |
| hastings | unknown-review (demoted from yellow-ogl 2026-08-16) | toml's licence name has no corresponding text anywhere; item says "General use. Open Data." |
| kawartha-lakes | unknown-review | confirmed 2026-08-20: item/DCAT/hub all carry the same as-is disclaimer, no grant, no prohibition |
| wellington | unknown-review | confirmed none published 2026-08-20 (no hub, no org-item licence; "Free for public use." covers the Explore app, not the data — bbox note: Guelph sits wholly inside, clipping applies regardless) |

## 2026-08-20 onboarding wave — 11 added, 4 refused at the licence gate

Every licence below was hunted live during onboarding (item licenseInfo, hub
pages, county sites); evidence and quotes in each TOML.

**Onboarded (11):**

| dataset | tier | licence | note |
|---|---|---|---|
| haldimand | yellow-ogl | OGL – Haldimand County v1.0 | full OGL text recovered from the hub site config item; add to the LWG email |
| west-parry-sound | yellow-ogl | OGL – Township of The Archipelago v2 (OGL-Canada 2.0-based) | found via re3data; caveat: one member township's name on a district-wide layer — confirm scope with info@wpsgn.ca; add to email |
| norfolk | yellow-review | Norfolk County Open Data Licence Agreement | bespoke worldwide royalty-free perpetual grant, credit optional; does not self-declare an OGL basis |
| halton-hills | yellow-review | Town of Halton Hills Open Data License (hub page) | bespoke OGL-shaped grant "for any lawful purpose" |
| simcoe | yellow-review | Open Government Licence - Simcoe County (maps.simcoe.ca/openlicense.html) | open licence exists and the site terms exempt open-data layers into it, but coverage of this exact MapServer endpoint is inferred — confirm with the county, or switch to their GeoServer WFS which is unambiguously open-data |
| prince-edward-county | yellow-review | OGL – County of Prince Edward v1.0 (hub) | full OGL-Canada 2.0 clone recovered; the address item itself lacks the stamp — confirm, then promote to yellow-ogl |
| cobourg | red-review · **publish_reports = false** | Town of Cobourg Open Data Terms of Use (2021) | grant covers copying/redistributing the UNMODIFIED datasets only (the City-of-Peterborough shape) → tracked, unpublished; ask mchatten@cobourg.ca |
| middlesex | unknown-review | as-is disclaimer only (item licenseInfo) | no grant, no prohibition |
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

## Counts (2026-08-20, post-onboarding-wave)

green 17 · OGL-family in/joining the LWG email 13 · yellow-review 6
(peel-region, bruce, norfolk, halton-hills, simcoe, prince-edward-county) ·
CC-BY waiver 1 · restrictive 6 (4 gated off the site: sdg, renfrew,
peterborough-county, cobourg) · unknown 9 — of **53 tracked datasets**.
