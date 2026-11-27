# Operator TODO — ontario-address-changes

## 1. Complete field selection for tracked cities

These cities are imported and tracking, but their field maps need a human decision:

- [ ] **waterloo — the key_field only covers 29% of the city.** Found 2026-08-10 while
  ignoring its coordinate duplicate. `ADDRESS_ID` is populated on 15,861 of 55,541 rows;
  the other 39,680 fall through to `synth_fields = ["full"]`, so the city runs on two
  identity regimes at once (`95099.0` vs `syn:d19669…`). Nothing is wrong today — 55,541
  distinct keys, zero collisions — but the day the city backfills `ADDRESS_ID` on the
  rest, all 39,680 switch key form and report as retired + re-added on one day. Two
  choices, both re-keying and neither retroactive: leave it and accept the risk, or set
  `key_field = ""` so the whole city synthesizes (uniform and immune, but it re-keys the
  15,861 today and gives up a stable id where the source does provide one). Note also the
  ids are stored float-formatted (`95099.0`, out of the shapefile), so a source switch to
  integer formatting re-keys those 15,861 by itself.
- [ ] **dufferin — `FULLADDY` disagrees with its own components on 857 rows (3.2%).**
  Found 2026-08-10. It is the mapped `full`, so it is what the reports display, and it is
  hand-maintained rather than derived: 359 rows carry a *different house number* than
  `STREETNUM` (many in runs where `FULLADDY` holds the neighbour's number — 713051 shown
  as 713053, 713053 as 713055, 713055 as 713057, the signature of a spreadsheet fill off
  by one row), 466 disagree on the street text (mostly styling — "30 SIDEROAD" vs "30TH
  SIDE ROAD" — but some name a different road outright: "10 SIDEROAD" vs "10TH LINE"),
  and 4 lost the separating space ("58744810 SIDEROAD"). The remaining 26,214 match.
  Re-measured 2026-08-20: grown slightly to 873 disagreeing / 363 number mismatches —
  the county is still hand-maintaining it, and the drift direction is worse, not better.
  Decide whether to keep publishing the county's string as-is, or unmap `full` and let
  reports compose "number street" from the cleaner components. Not urgent and not an
  identity risk (`key_field = "ID"`, and `full` is not in `synth_fields`), but it means
  ~1.3% of displayed dufferin addresses show a number that belongs to a neighbour.
- [ ] Spot-check low coverage — open a handful of the blank rows and judge: wrong
  column selected, or genuinely unaddressed points (towers, outbuildings)? Note the
  verdict in each TOML:

## 1b. Fields the sources have added since we last looked

## 2. Find data sources for uncovered cities

**Places queue, consolidated 2026-10-16** (detail for each in the items below; this is
the order to work them):

| # | place | what | why now |
|---|---|---|---|
| 5 | Grey County | **tracked 2026-10-16** (grey 51k parcels, blue-mountains 10.5k pts, grey-assigned-addresses 1.7k), gated; licence ask still open | publish if the county grants one |
| 10 | Oxford, North Bay, Haliburton, Sault Ste. Marie, City of Peterborough | **tracked 2026-10-16, publish_reports = false**; licence asks still open | the gate holds publishing only now |
| — | Belleville, Northumberland, Kenora | still no machine-readable layer (re-probed 2026-10-30, unchanged) | quarterly re-probe, next ~2027-01-30 |

**2026-10-16 sweep onboarding, follow-ups** (24 datasets added, dufferin re-pointed to its address layer, LICENSING.md has the table):
- [ ] Confirmation asks, publishing already: ajax (does the site-wide OGL cover Civic
      Addresses item e48315e9?), tecumseh (may the County of Essex OGL license the Town's points?).
- [ ] Gated for no licence text, worth an ask: caledon, dryden, oshawa ("reference use only"
      claim unverified), vaughan, vaughan-ng911, grey x3, gorham-ware, oliver-paipoonge.
      **Asks drafted 2026-10-23** for all of these plus the gated five from August and
      leamington, with contacts off official pages: address-importer-friend
      `future-work/multi-city/license-contacts-todo.md` section E. New there: ajax's hub
      settings say "CC-BY-SA", not the OGL clone read on 10-16 - ask which applies.
- [ ] city-tune audit for each new city after two changed snapshots (classes, ignore_fields).
  - [ ] **halton-hills: one-shot export** (all 21,900 rows created 2025-10-17). The town's
    `https://map.haltonhills.ca/awse/rest/services/eP/MapServer/0` has 21,902 and ~20
    differences, but no date fields to prove it is live itself. Re-probe its count and max
    OBJECTID (888,739 on 10-23) around **2026-11-06**; if it moved, re-point (street becomes
    `STR_FULL`, no unit column - parse from `ADDR_FULL`, `unit_from_full` precedent;
    GlobalID shared with the current layer, a key candidate). Ask gis@haltonhills.ca to
    refresh the (od) item meanwhile.
    **Re-probed 2026-10-30 (a week early): neither layer moved.** Candidate still 21,902 /
    max OBJECTID 888,739; AGOL item still 21,900, its editingInfo stamp 2025-11-28 (an
    overwrite, before tracking began). Draft map if it ever moves: number=STR_NUM,
    street=STR_FULL, unit parsed from ADDR_FULL, full=ADDR_FULL, classes status=ADDR_STAT /
    boundary=ADDR_COMM, ignore Latitude/Longitude. Next look: **2026-12-01** with cobourg.
  - [ ] **amherstburg: unknown, likely batch-fed.** Its own edit layer; `Type` tags show
    monthly loads Sep 2024-Feb 2025, nothing tagged 2026; no alternative anywhere (Essex has
    no points). Watch to **2026-12-31**, then ask building@amherstburg.ca whether it still
    gets batches. Re-probed 2026-10-30: still 10,925, Type tags unchanged (newest Feb 2025),
    no editingInfo and no date-typed field, so liveness cannot be shown; date stands.
    north-bay re-read the same day: data stamp still 2023-04-24, frozen, 1 distinct pull.

**From the ontario-osm-data-sources portal sweep, 2026-10-16.** That repo graded every
address layer on every Ontario portal (`catalogue/layers/*.csv`, theme `addresses`); these
are the ones that change something here. Counts and dates probed live 2026-10-16.

  - [ ] **Elgin's OGL: take it to the wiki** (licence verdict agreed 2026-10-16). The OSMF
        self-service route, as for the six self-listed 2026-10-12: diff the hub's "Open
        Government Licence - County of Elgin" against the Ottawa Open Data Licence 2.0 into
        `ontario-osm-data-sources/licences/elgin/verdict.md`; if the only differences are
        locality, venue, PII or records definitions, add an OSM wiki Contributors entry,
        email legal-questions@osmfoundation.org, and move the toml to `green-self`
        (LICENSING.md and the import queue's parked list follow). If not a pure variant, it
        goes in the LWG follow-up instead. Cite the hub site item (`5fa753ff…`) as the
        licence source - the layer's own item carries no licenseInfo.
  - [ ] **Watch for an `Elgin_Civic_Numbers_2027`.** The service is named for the year; if
        the county publishes next year's as a new service and freezes this one, the 90-day
        source-stale issue is the signal, and the fix is another re-point (this time with
        history, so a flagged switch day as for lambton 2026-09-15, not a fresh baseline).
Cities/counties with no working source (full reasons in `skipped.toml`, shown on the
landing page). ArcGIS Online search is exhausted for all of these — next steps are
human ones: browse each municipality's own open-data/GIS page, check provincial
portals (geohub.lio.gov.on.ca), or email the GIS department.

- [ ] Dead endpoints — re-probed 2026-08-20, and the picture flipped: **6 of 8 have a
  live, verified address layer again** (every URL below probed with a field-list read
  and a returnCountOnly count). Each recovered one is now an onboarding decision
  (licence + city-tune pass), not a search problem:
  - [ ] Belleville — **still nothing** (re-probed 2026-10-30: 71 services, no address layer,
        Parcels carry ROLL/ParcelID only). Old server's services root is empty (and its
        TLS cert is broken); the city now has an AGOL org (`BellevilleGIS`, hub
        `opendata-bellevillegis.hub.arcgis.com`, ~60 public services) but no address
        layer in it. Hastings County's `CivicAddresses` does NOT cover Belleville
        (separated city; its MUNICIPALI codes are all rural townships).
  - [ ] Northumberland County — server back (`/arcgis` moved to `/server`) but the full
        service sweep shows roads/parks/wards only — **no address layer.** (Cobourg
        below now partially covers the county.) Re-probed 2026-10-30: unchanged; the AGOL
        org's `Parcel_Fabric_2025` (6,437 polygons, one lower tier, STREET_NUM/STREET_NAM)
        is the only fallback and not worth it.
- [ ] No public address layer found at all — hunted again 2026-08-20 (muni portals,
  hubs, org sweeps, Ontario GeoHub), and **8 of the 14 now have a verified source**
  (each probed live: field list read + returnCountOnly). One provincial fact settled
  on the way: LIO's Address Point data class is NOT on the open GeoHub (only ORN
  road ranges); it sits behind OGDE licensing, so no provincial layer can cover
  these municipalities.
  - [ ] Essex County — still nothing county-wide (re-probed 2026-10-30: hub 120 datasets,
        cwserver OpenData 5 services). Amherstburg, tecumseh and leamington are tracked.
        **Kingsville tracked 2026-10-30, gated (10,269 rows); ask drafted 10-31.** Was: the county org's `MESH_WFL1/FeatureServer/0`
        "KingAddress_Sep25" (item 72dcf35a…, owner rpalmini_kingsville, public): 10,270
        points, CIVIC/HOUSE_NO/STREET, last edited 2025-10-28, no licence - a dated
        snapshot inside a staff working map, so a vault-only onboarding (it would sit
        frozen until the next drop) or an ask to Kingsville for the live layer. LaSalle,
        Lakeshore, Essex and Pelee: nothing.
  - [ ] Kenora — still nothing: city org live (13 public services), no address or
        parcel-address layer. Re-probed 2026-10-30: unchanged.
- [ ] Special cases — need a decision, not a search:
  - [ ] **City of Peterborough** — licence CHANGED (checked 2026-08-20): the Address
        item now carries custom "Open Data Terms of Use" instead of the old blanket
        proprietary label — but the grant is to "copy and use the **unmodified** Open
        Datasets"; no modification right, so publishing *derived* diff reports is
        still not clearly licensed. Keeping it skipped is defensible; skipped.toml
        detail updated. Ask the city if it ever matters — the County layer's own terms
        turned out restrictive too (§3), so "leave it to the County layer" is no
        longer the easy answer it was.

## 3. Licence review

- [ ] NEW follow-ups out of the review: ~~decide the sdg / renfrew /
  peterborough-county publishing question~~ (decided + implemented 2026-08-20 —
  gated, see above); optionally send permission asks to those three counties so the
  gates can lift; ~~add the five newly-found OGL variants (frontenac, leeds-grenville,
  lennox-addington, milton, windsor) to the drafted LWG variant-review email
  (gist in LICENSING.md) and send it~~ (2026-10-11: the email went out covering
  the original six — date not recorded, no reply yet; these five and the rest
  are being evaluated for the OSMF self-service route, see LICENSING.md Yellow);
  optionally add the burlington/london terms-URL
  pass-through to their report pages; ~~optionally re-point milton and windsor at
  the URLs their open licences literally cover~~ (2026-10-12: windsor re-pointed,
  with barrie and leeds-grenville; milton deferred, reasons in milton.toml).

## 3b. Monthly articles

September 2026 is written for all 44 publishable city-months (11 quiet, 33 researched)
and live, unlisted, at <https://skfd.github.io/ontario-address-changes/articles/>. The
two items after the review wait on it: a style change found there should land before
70 more pieces are written in the old style, and before the pieces get a public link.

- [ ] **Review the style of the September pieces.** Compare the two batches, which
  were written by different models. Barrie, Brampton, Brant, Brantford, Bruce and
  Burlington (and Toronto) came from the default model, which fanned out parallel
  research agents: longer, 10-28 sources in each research note. Cornwall through York came from Opus 5.5
  after the default model ran out of usage credits on 2026-10-23: one research pass,
  shorter, mostly 1-10 sources (York 14). Quiet months (e.g. Amherstburg, Windsor) use a fixed
  shape from `tools/article_quiet.py`. House style lives in
  `.claude/skills/monthly-article/references/house-style.md`; changes go there so
  every later run picks them up.
- [ ] **After the review: decide on backfilling July and August 2026** for the cities
  other than Toronto — about 36 city-months each, 5 quiet each, so roughly 70
  researched pieces at 2-25 min apiece. Each plan session window allowed 1-6 before
  the limit stopped the batch, so this is several days of plan usage competing with
  every other session. Run one month at a time:
  `.\monthly-article.ps1 -Month 2026-08 -MaxClaude 40 -BudgetMinutes 420` (add
  `-Model claude-opus-5-5` if the default model is out of credits). The batch stops
  cleanly at a limit and resumes where it left off on the next run.
- [ ] **Re-check three September pieces after the 2026-10-24 render.** The dedupe tie-break
  and muskoka's key change moved their numbers: greater-sudbury "54 location edits" -> 7
  (gross significant 47 -> 18, net 17 -> 16), muskoka "95 location edits against 87 net" ->
  87/87, brampton net significant 29 -> 33, gross 59 -> 63 (agent's estimates; take the
  numbers from the re-rendered pages). The monthly-article skill covers "update an article
  after a re-render changed the numbers".
- [ ] **After the review: link the articles from the landing page.** The link belongs
  in `templates/cities.html` (`docs/index.html` is regenerated every render), the way
  the prior-art comparison is linked; it shows on the next daily render. Until then the
  pages are reachable only by URL.

## 4. Periodic / ops chores

- [ ] **Re-probe `skipped.toml` quarterly** — endpoints come back or migrate
  (5 of 5 originally-dead cities were eventually recovered via ArcGIS Online).
- [ ] **Revisit Orangeville and Hanover as their own datasets, around 2027-10.** Both
  publish live layers that OpenAddresses reads (Orangeville `gis.orangeville.ca/arcgis/
  rest/services/Location/SiteAddress/MapServer/0`, OGL-Orangeville; Hanover
  `gis.grey.ca/server/rest/services/Public/Service_HanoverAssets/FeatureServer/16`).
  Declined 2026-10-22 because our county layers already hold them in full (dufferin 106%,
  grey 109% of the NAR's locations; `priorart/report.html`). Re-check two things: whether
  the municipal layer moves on a different **cadence** than the county's (it may be the
  upstream the county copies from, so changes would show here first), and whether its
  **data differs** (rows, units, suffixes, fields) from the county's rows inside the town.
  A one-off pull of each into a scratch store and a diff against the county rows covers both.
- [ ] **Import refusals never escalate (found 2026-10-23).** Peterborough's pull was
  refused all three attempts on 10-23 (29,062 of 34,096: a publisher-side partial reload,
  whole again by 20:00 the same day; vault verdict `artifact`, signature added to the
  data-integrity skill's `corrupt-pulls.md`). It fixes itself on the next pull. The gap it
  showed does not: `failure_streaks()` counts only vault jobs `failed`/`refused`, and the
  vault logged this pull `done`; the refusal lives only in this repo's `blocks` table, and
  `run.py` `_split_known_outages` treats an import refusal as having no streak. So a layer
  that stayed short would fail the run every day forever and never open a `source-down`
  issue: the west-parry-sound blind spot again, through a different door. Fix: count
  consecutive pull days with an active block toward the same N = 3. Also, `active_block`'s
  docstring and `corrupt-pulls.md` call the block's "3 attempt(s)" days; it is three tries
  inside one run. Check 10-24: `health.py --blocks --city peterborough` should be empty.
- [ ] **Watch the daily scheduled task** — check `logs/` and that the site commit/push
  ran. `addressvault report` is the first command (per-city-per-day: checked, unchanged,
  failed, or no attempt); `health.py --blocks --runs` is the project-side second.
- [ ] **A Windows Update restart skips the day silently — diagnosed 2026-08-12, left
  unfixed by choice.** Found while checking why 08-12 had no run at all: no `runs.csv`
  row, zero lines in `update.log`, no vault snapshots pulled, and the task itself
  reporting `LastRunTime = 08-11 12:00` with `NextRunTime = 08-13 12:00`.
- [ ] **Watch for more `index.lock` publish failures — observing, deliberately not fixed.**
  The manually-triggered 08-12 run updated all 42 cities cleanly and then lost the publish
  to a 0-byte `.git/index.lock`: `git add docs` failed, so nothing was staged, committed or
  pushed, and the run ended `publish-failed` with the site a day stale. Recovered by hand
  the same evening (`e22515ad`) — the lock was removed and the run's own `docs/` output
  committed unmodified.

## 5. Hand to coding agent when convenient

Code fixes found during the audits. Every one of them changes payload hashes → a
one-time "modified" spike, so batch them:
