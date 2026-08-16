# Licensing status — all tracked datasets

**The single place for each dataset's licence colour and comment.**
Hand-maintained: update this table in the same change as any edit to a
dataset's `osm_compatible` tier, any new licence finding, any government
contact sent or answered, and any LWG correspondence. The `osm_compatible`
field in `datasets/<slug>.toml` stays the machine-readable value; this file
carries the evidence and the next step. If the two disagree, this file is
newer or the toml was edited without updating it — fix whichever is stale.

Last full review: **2026-08-16** (all 19 non-green datasets probed; method:
licence page where published, else ArcGIS service JSON → `serviceItemId` →
portal item `licenseInfo`). Detail lives in the engine's
`future-work/multi-city/license-contacts-todo.md` and the draft LWG email:
<https://gist.github.com/skfd/043eded6a26b279b7cf75aa3927b14da>.

Tier legend: **green** = usable (LWG-listed licence or equivalent) ·
**yellow** = OGL-family variant awaiting the variant-review email ·
**orange** = CC BY, needs the OSMF waiver · **red** = restrictive terms,
permission ask required · **unknown** = no licence text found, must ask.

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

## Reviewed 2026-08-16 — in the drafted LWG variant-review email (6)

Clean OGL clones; diffs limited to the LWG-accepted classes (locality names,
venue, PII/records statutes). Waiting on: human read, send, reply.

**2026-08-16 user decision:** the five non-oakville clones (plus brant, now
green) are being *scaffolded* ahead of the LWG reply — onboarding is
invisible; any import stays gated on the reply. Queue state:
engine `future-work/multi-city/onboarding-queue.md`.

| dataset | tier | licence | comment (2026-08-16) |
|---|---|---|---|
| brantford | yellow-ogl | OGL – Brantford v1.0 | clone; adds PHIPA to exemptions; venue drops Federal Court |
| dufferin | yellow-ogl | OGL – County of Dufferin v2 | verbatim-verified from county PDF; PII via *provincial* FIPPA; omits the not-accessible-records exemption (more permissive) |
| huron | yellow-ogl | OGL – The County of Huron v2.0 | verbatim in ArcGIS item; self-declares diffs vs OGL-Ontario 1.0; NB: county GIS page shows a separate restrictive licence for contracted products |
| kitchener | yellow-ogl | OGL – City of Kitchener v1.0 | attribution *voluntary*; city gave explicit OSM permission (wiki: Waterloo_region/Kitchener_authorization) — effectively cleared |
| oakville | yellow-ogl | OGL — Town of Oakville | clone of OGL-Canada 2.0; ALSO brownfield-active (TronnaLegacy MapRoulette 55881) — do not touch regardless |
| sarnia | unknown-review → yellow | OGL – City of Sarnia (in item licenseInfo) | surprise find: self-declared OGL-Canada 2.0 clone; added to the email; re-tier toml when sent |

## Near-green desk work (1)

| dataset | tier | licence | comment (2026-08-16) |
|---|---|---|---|
| peel-region | unknown-review | Open Data Licence for the Regional Municipality of Peel v1.0 | based on the **UK OGL** (with National Archives permission); full text at data.peelregion.ca/pages/license is JS-rendered — browser-grab, diff, add to email. Gateway to Mississauga |

## Orange — CC BY waiver needed (1)

| dataset | tier | licence | comment (2026-08-16) |
|---|---|---|---|
| brampton | orange-ccby-waiver | CC BY 4.0 | confirmed on GeoHub; send OSMF waiver template to open@brampton.ca |

## Red — published terms are restrictive; permission ask (4)

| dataset | tier | licence | comment (2026-08-16) |
|---|---|---|---|
| burlington | red-review | City of Burlington Terms of Use | re-pull terms, then permission ask |
| london | red-review | City of London Terms of Use | same |
| sdg | unknown-review → red | copyright terms in item licenseInfo | explicit: no copying/distribution without prior written consent |
| windsor | red-review | City of Windsor Terms of Use (mappmycity.ca) | same as burlington/london |

## Unknown — no licence text published anywhere found; ask the office (13)

All probed 2026-08-16: empty item `licenseInfo`, no licence page. Ask each to
publish/state a licence or grant OSM permission (templates in the engine TODO).

| dataset | tier | comment (2026-08-16) |
|---|---|---|
| bruce | yellow-review | toml's "BGDISC Open Data Licence" is a data-sharing collaborative, not a licence; contact GIS@BruceCounty.on.ca |
| chatham-kent | unknown-review | nothing published |
| elgin | unknown-review | county-hosted server, no metadata |
| frontenac | unknown-review | nothing published |
| hastings | unknown-review (demoted from yellow-ogl 2026-08-16) | toml's licence name has no corresponding text anywhere; item says "General use. Open Data." |
| kawartha-lakes | unknown-review | item carries a *disclaimer*, not a grant — no redistribution rights as written |
| leeds-grenville | unknown-review | attribution line only |
| lennox-addington | unknown-review | "Open Data Policy" named; portal launch claims "no restrictions" but no text; ask gisservices@lennox-addington.on.ca to confirm in writing |
| milton | unknown-review | city-hosted server, no metadata |
| muskoka | unknown-review | proxied service, no metadata |
| peterborough-county | unknown-review | nothing published |
| renfrew | unknown-review | nothing published |
| wellington | unknown-review | nothing published (bbox note: Guelph sits wholly inside — clipping applies regardless) |

## Counts (2026-08-16)

green 17 · in LWG email 6 · near-green 1 · CC-BY waiver 1 · restrictive 4 ·
no licence published 13 — of 42 tracked datasets.
