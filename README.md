# Ontario Address Change Tracker

Tracks changes over time to open civic-address datasets published by Ontario
municipalities. Each run fetches a fresh snapshot of a dataset, stores it as a
**Slowly-Changing-Dimension Type-2** history, and reports which addresses were
added, removed, or modified since the previous snapshot.

**Live site:** <https://skfd.github.io/ontario-address-changes/> — 53 datasets
covering every major Ontario population centre and most of the eastern, central
and southwestern counties, refreshed daily. Four of them are tracked but not
published: their licences don't permit republication, and the landing page marks
them "licence not compatible" instead of linking reports.

It generalizes the single-city
[`toronto-addresses-import`](../toronto-addresses-import) tracker to a registry
of many datasets. Adding a city is a config file, not code.

> Scope: change tracking only (download → diff → report). OSM conflation/upload
> is out of scope.

## How it works

- **Registry** — one TOML per dataset in `datasets/`. It names the source URL,
  how to fetch it (`arcgis` REST query, or `static` file), the field map, and
  how to identify a record across snapshots.
- **Fetch** (`src/fetch/`) — pulls the dataset's latest snapshot from
  `address-vault` (`Vault().pull(slug)`), which owns the `arcgis`/`static`
  acquisition and reprojection to EPSG:4326 and keeps the dated history. Requires
  `ADDRESSVAULT_DIR` set to the vault folder.
- **Normalize** (`src/normalize.py`) — applies the field map to a small canonical
  set (`number`, `street`, `unit`, `full`, lon/lat) and computes a stable
  `identity_key` plus a `payload_hash` for change detection. All source
  properties are preserved in a `props` JSON blob (volatile keys like `OBJECTID`
  stripped so they don't cause spurious "modified" churn).
- **Store** (`src/db.py`) — one SQLite DB per dataset at `data/<slug>/<slug>.db`.
  An address row is valid for `[min_snapshot_id, max_snapshot_id]`. Re-importing
  identical content is detected by content hash and recorded as a skip.
- **Diff + report** (`src/diff.py`, `src/report.py`) — diff consecutive
  snapshots into added/removed/modified (with field-level changes and
  per-address history) and render a static site into `docs/` for GitHub Pages:
  a cross-city landing (`docs/index.html`), a per-city report list
  (`docs/<slug>/index.html`), and a dated report per snapshot
  (`docs/<slug>/report-<date>.html`). The first snapshot renders as a
  "baseline" report where every address is listed as new. Modifications are
  classified into humanized sections where the changed-field set allows it —
  Location Adjustments, Renumbered, Street Renames built in; place / status /
  boundary via each dataset's `[classes]` — with per-city noise config
  (`ignore_fields`, `keep_fields`, a `location_min_move_m` floor for
  sub-parcel coordinate jitter) deciding what counts as a change at all.
- **Flags** (`src/flags.py`) — the site publishes on positive identification:
  a homogeneous mass event (mass add, mass removal, same-field sweep) is held
  off the public pages and recorded in `flags.toml` until a review files a
  verdict — `business` publishes it, `technical`/`bug` hold it forever with a
  rule that stops the recurrence. `python run.py flags` lists the open queue;
  `logs/flags.html` is its human view (back-office only, never published).

## Identity (the important part)

Diffing needs a key that is *stable across republishes*. Each dataset config
picks one:

- `key_field` — a stable source id (e.g. Ottawa `PI_MUNICIPAL_ADDRESS_ID`,
  Waterloo `ADDRESS_ID`, Toronto `ADDRESS_POINT_ID`).
- empty → **synthesized** `sha1(synth_fields + rounded lon/lat)`. ESRI
  `OBJECTID` is sequential and reassigned on republish, so it is never used as
  the key. When synthesizing, include `unit` for multi-unit buildings (Hamilton)
  or all units collapse to one point.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Set `ADDRESSVAULT_DIR` to the address-vault folder; `fetch` reads and writes there.

## Usage

```powershell
python run.py list                  # show registered datasets
python run.py update --city ottawa  # fetch -> import -> diff for one dataset
python run.py update --all          # all datasets (per-city failures isolated)
python run.py report --all          # (re)render HTML reports
python run.py flags                 # list change events held pending review
```

`download`, `import`, and `diff` are also available as individual steps.

## Datasets

53 registered, one TOML each in `datasets/` — from Toronto (525k address
points) down to Cobourg (7.8k). Region-wide layers cover their member
municipalities (Peel covers Mississauga/Brampton/Caledon; York covers
Vaughan/Markham; Durham, Niagara, and the rural counties likewise). A few
representative shapes:

| Slug | Source | Fetch path | Identity |
|---|---|---|---|
| `ottawa` | ArcGIS MapServer | `arcgis` | `PI_MUNICIPAL_ADDRESS_ID` |
| `toronto` | CKAN static geojson | `static` | `ADDRESS_POINT_ID` |
| `hamilton` | ArcGIS FeatureServer | `arcgis` | synthesized (number+street+unit) |
| `waterloo` | ArcGIS Open Data shapefile export | `static` | `ADDRESS_ID` |
| `renfrew` | County NENA address-point FeatureServer | `arcgis` | synthesized |

To add a dataset, copy a TOML in `datasets/`, set its URL/field map/identity,
and run `python run.py update --city <slug>` (the `city-tune` skill's
onboarding reference documents the full procedure).

## Scheduling (Windows)

```powershell
.\schedule-add.ps1     # daily 'update --all' at noon, logs to logs\scheduler.log
.\schedule-remove.ps1
```

After the update, `daily-update.ps1` regenerates the address-vault status page
(`addressvault report` → `<ADDRESSVAULT_DIR>\report.html`) — a local file about
the vault, not part of the published site. It runs on every outcome, including
offline/metered ones, since it reads only the catalog and disk; if it fails the
run logs `REPORT-FAILED` and the run's own exit code is unaffected.

## Data sources & attribution

Source datasets carry their own licences (see each dataset's `license_name`).
Tracking/diffing observes public data; redistribution or any downstream OSM
import must separately comply with each source's licence and the OSM
[Import Guidelines](https://wiki.openstreetmap.org/wiki/Import/Guidelines).
