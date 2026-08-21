# NAR prototype assessment — 2026-08-21

Question: can StatCan's National Address Register fill the municipalities our
53 local datasets don't cover, with narrativized (humanized) change reports?

**Verdict: yes — viable as a separate semi-annual tier.** GUID identity holds
across releases, diff volumes are small and human-meaningful, and a sample
diff surfaced real municipal events (street renames, re-addressing, new
units) in an uncovered city.

## Source facts

- Download: `https://www150.statcan.gc.ca/n1/pub/46-26-0002/2022001/<YYYYMM>.zip`
- Vintages still downloadable: **202412** (1.93 GB), **202507** (2.0 GB),
  **202606** (1.67 GB). The 2022-11 and 2024-06 releases are gone (404) —
  history effectively starts December 2024. Cadence is semi-annual;
  **each release must be archived when it appears or it is lost.**
- Licence: Statistics Canada Open Licence (attribution; republication OK).
- Ontario = province code 35: ~12 CSVs per vintage (7 address parts +
  5 location parts), ~1.6 GB per vintage extracted.
- Schema stable 202412→202507; 202606 adds `BF_REPPOINT_X/Y` (additive only).
- `BG_X/BG_Y` are **projected metres** (StatCan Lambert, EPSG:3347-style) in
  the address file itself; a NAR dataset config would need `source_crs`.

## Identity (go/no-go) — GO

| pair | common GUIDs | overlap | added | removed | modified* |
|---|---|---|---|---|---|
| 202412→202507 | 6,241,028 | 99.90% | 4,235 | 6,529 | 55,205 |
| 202507→202606 | 6,227,749 | 99.72% | 18,794 | 17,514 | 77,005 |

\* narrative fields only (civic no, street, unit, postal code, BU_USE, CSD).
`ADDR_GUID` is unique within a vintage (0 dupes in 6.25M rows) and persists
across releases. It is the identity key.

## Coverage gap NAR would fill

Of 6,246,543 Ontario addresses (202606): **5,353,648 (85.7%)** fall in CSDs
already covered by the 53 prod datasets; **892,895 (14.3%)** don't.
Blank CSD names are negligible (4,592 = 0.07%).

Top uncovered CSDs: St. Catharines 64k, Peterborough 40k, Sault Ste. Marie
37k, Belleville 27k, Welland 27k, North Bay 26k, Woodstock 22k, St. Thomas
20k, Timmins 20k, Fort Erie 17k, Orillia 17k, plus Essex County towns,
Niagara towns, Waterloo townships, and hundreds of small/northern CSDs
(523 CSDs total in NAR vs ~200 covered).

## Sample narrative diff — Orillia, 202507→202606

16,759 → 16,763 addresses; 37 added, 33 removed, 432 modified.

- **Street rename chain (real event):** "Leanne's Way" → "Lucy Lane" and the
  former "Lucy Lane" → "Huronia Rd" (~30 addresses) — exactly our Street
  Renames class.
- **Re-addressing:** `135 Atherley RD unit B102` retired, `135 B Atherley RD
  unit 102` added — the building letter moved from unit label to civic
  suffix; our split/unit-explosion humanizer already models this.
- **Use-code changes:** 184 `BU_USE` flips (residential/commercial/mixed).
- **Coordinate churn:** 338 XY changes, many `'' → value` (StatCan
  back-filling coordinates) — methodology noise, needs a metres-based
  `location_min_move_m`-style floor and an "attribute newly populated"
  suppression rule.

## Caveats for productization

1. **Semi-annual, not daily** — must be a visibly separate tier ("NAR
   half-yearly"), never mixed into daily-verified cities; keeps the
   verify-or-red rule honest.
2. **Methodology artifacts** — release-over-release record count swung
   ±0.7% nationally; the 202412→202507 pair has 4,918 CSD reassignments
   (boundary/geocoding fixes, not moves). The flag gate applies; add a
   "StatCan methodology" verdict category.
3. **Archive discipline** — old vintages disappear from StatCan; add the
   ZIP fetch to a semi-annual scheduled check.
4. **Thin attributes** — no full-address string, sparse units, postal codes
   mostly present; narratives will be leaner than municipal feeds.

## Files here

- `extract_on.py` — pulls Ontario CSVs from the vintage ZIPs in `data/`
- `assess.py` → `assessment.json` — the numbers above
- `coverage.py` — CSD-name map of what prod already covers (bilingual-name
  aware); worth reusing if this becomes a tier
- `sample_diff.py` — per-CSD field-level diff between two vintages
- `data/` — git-ignored: 3 ZIPs (~5.6 GB) + extracted Ontario CSVs
