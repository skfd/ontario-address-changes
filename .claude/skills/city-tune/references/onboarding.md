# Onboarding a new source

Ends in either a `datasets/<slug>.toml` or a `skipped.toml` entry. Both are deliverables —
a documented rejection is worth as much as an addition, and the landing page renders the
skipped list so coverage gaps stay reviewable.

## 1. Find the source that is actually official

The traps, all of which have already cost time here:

- **Untrusted copies.** ArcGIS Online search surfaces `*_exchange` mirrors that look
  official and drift independently. Check the owning org.
- **The catalogue entry is stale, the city's own server is live.** Guelph's catalogued
  `services5.arcgis.com` layer is gone; the official source is the self-hosted
  `gismaps.guelph.ca` OpenData server (owner `GuelphGIS_cityofguelph`).
- **Dead municipal endpoints** with no ArcGIS Online migration (Belleville).
- **Token-secured layers** returning HTTP 499 (Norfolk County).
- **Region-wide layers** that cover many municipalities in one service (Muskoka) — fine,
  but the TOML comment should say so.

Record the resolution path in a comment at the top of the TOML. Every existing dataset
does this and it is the only record of why a URL is what it is.

## 2. Licence and OSM compatibility

`license_name` verbatim from the source, plus `osm_compatible`, using the existing
vocabulary: `green-lwg`, `green-ogl`, `yellow-ogl`, `yellow-review`, `orange-ccby-waiver`,
`red-review`, `unknown-review`. A proprietary or all-rights-reserved licence is a
`skipped.toml` entry, not a dataset (City of Peterborough).

`skipped.toml` `status` badges are a fixed set: "Dead endpoint", "Empty / secured",
"Proprietary licence", "No address layer", "Untrusted copy", "Unstable URL", "Not found".
Add a one-sentence `detail` with the concrete evidence.

## 3. Config, in this order

Required keys: `slug`, `provider`, `data_url`, `access` (`arcgis` | `static`), `format`
(`geojson` | `shapefile`). Add `source_crs` when coordinates come out projected —
`normalize._to_wgs84` only reprojects values outside lon/lat range, so a city that
switched export CRS partway through history is handled safely.

Then work the decisions in dependency order, each with its own reference:

1. `[identity]` — cannot be fixed retroactively, so get it right first.
2. `[fields]` — for synthesized-identity cities this *is* part of identity.
3. `[classes]` — needs a couple of snapshots of observed transitions; fine to defer.
4. `ignore_fields` — needs history to justify. Defer rather than guess: a first-day
   guess with no churn evidence is exactly the speculation this repo avoids.

## 4. Baseline and first look

Fetching goes through address-vault (`ADDRESSVAULT_DIR`), not direct HTTP — the tracker
never pulls city sites itself.

```
python run.py update --city <slug>
python run.py report --city <slug>
```

The first snapshot is a baseline: every row counts as added and no diff exists yet. Read
the report before declaring the city onboarded — a baseline that is 10x or 0.1x the
expected address count is a truncated or wrong layer, not a city.

Two snapshots later, run the full audit (`audit.py <slug>`) and revisit classes and the
ignore list with real churn evidence.
