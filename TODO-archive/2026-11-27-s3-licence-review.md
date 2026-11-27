# TODO.md §3: closed licence review

Moved verbatim out of [TODO.md](../TODO.md) on 2026-11-27; the text is as it stood at
TODO.md's last update, 2026-10-31. History and finished work, not required reading.
Open items stay in TODO.md; where one was shortened there, its full text is here.

## 3. Licence review

- [x] Licence "Not identified" — **all 15 hunted 2026-08-20** (live item licenseInfo,
  DCAT feeds, hub terms pages; every finding + source URL recorded in each TOML).
  Outcome in four buckets:
  - **Open licences found (7):** brant CC0 (was already in the TOML from 2026-08-16),
    frontenac OGL-Frontenac v1.0, leeds-grenville OGL-UCLG v1.0, lennox-addington
    OGL-L&A v2.0, milton OGL-Milton (with a layer-vs-open-data-item caveat in the
    TOML), peel-region Open Data Licence Peel v1.0 (attribution optional), sarnia
    OGL-Canada-2.0-based (found on the renamed service's item, §4's URL fix).
  - **Confirmed none published (4):** chatham-kent, elgin (until 2026-10-16: OGL found on
    its open-data hub, see §2), wellington, kawartha-lakes —
    a real absence, verified across item/DCAT/hub in each case, not a failed search.
    Default copyright applies; asking the municipality is the only move left.
  - **RESTRICTIVE — new problem, operator decision needed (3):** **sdg** (item
    licenseInfo: "No part... may be sold, copied, distributed, or transmitted...
    without the prior written consent of the County. All rights reserved."),
    **renfrew** (hub disclaimer: "Content may not be reproduced or redistributed
    without prior written permission", explicitly binding "any associated data";
    OGDE-encumbered), **peterborough-county** (county site ToU: geospatial content
    "may not... be copied onto any other website without the written agreement...").
    These three are *worse* than "Not identified": the project publicly published
    diff reports of their data. **Decided 2026-08-20 (operator): keep tracking,
    stop publishing.** Implemented the same day as `publish_reports = false` in
    each TOML: report pages are deleted at render time, the landing row shows a
    "licence not compatible" badge with no link, and the map hull goes red and
    unclickable. Verified on all three. Reversible by flipping the flag if a
    permission ask ever succeeds.
  - **muskoka:** custom terms with no reuse grant at all (King's Printer copyright +
    disclaimer) — not open, not explicitly prohibiting; grouped with the ask-the-muni
    pile but flagged red in the TOML.
- [x] Custom Terms of Use (OSM red) — all three read in full 2026-08-20, operative
  quotes in the TOMLs:
  - **burlington + london** — near-identical terms; both **permit** automated retrieval
    (by silence; revocable, no continuity promise) and both **permit publishing derived
    diff reports** — conditioned on pass-through: distributions "in original or modified
    form" must include a copy of or URL to the terms. Operator follow-up if desired:
    add each city's terms URL to its published pages. OSM/ODbL compatibility remains
    unresolved (the pass-through clause), so both stay `red-review`.
  - **windsor** — upgraded: the "Terms of Use" PDF is actually a full OGL-Canada-style
    licence, and the city's open-data portal binds its Address datasets to it. Now
    `yellow-ogl`; both tracking and diff publishing clearly permitted. Caveat in the
    TOML: we track the mappmycity.ca server rather than the portal copy.
