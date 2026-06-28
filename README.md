# Ontario Address Change Tracker

Tracks changes over time to open civic-address datasets published by Ontario
municipalities. Each run fetches a fresh snapshot of a dataset, stores it as a
**Slowly-Changing-Dimension Type-2** history, and reports which addresses were
added, removed, or modified since the previous snapshot.

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
  "baseline" report where every address is listed as new.

## Identity (the important part)

Diffing needs a key that is *stable across republishes*. Each dataset config
picks one:

- `key_field` — a stable source id (e.g. Ottawa `PI_MUNICIPAL_ADDRESS_ID`,
  Waterloo `ADDRESS_ID`, Renfrew `PROPNUM`).
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
```

`download`, `import`, and `diff` are also available as individual steps.

## Pilot datasets

| Slug | Source | Fetch path | Identity |
|---|---|---|---|
| `ottawa` | ArcGIS MapServer | `arcgis` | `PI_MUNICIPAL_ADDRESS_ID` |
| `hamilton` | ArcGIS FeatureServer | `arcgis` | synthesized (number+street+unit) |
| `waterloo` | ArcGIS Open Data shapefile export | `static` | `ADDRESS_ID` |
| `renfrew` | OpenAddresses geojson cache (parcel polygons) | `static` | `PROPNUM` |

To add a dataset, copy a TOML in `datasets/`, set its URL/field map/identity,
and run `python run.py update --city <slug>`.

## Scheduling (Windows)

```powershell
.\schedule-add.ps1     # daily 'update --all' at noon, logs to logs\scheduler.log
.\schedule-remove.ps1
```

## Data sources & attribution

Source datasets carry their own licences (see each dataset's `license_name`).
Tracking/diffing observes public data; redistribution or any downstream OSM
import must separately comply with each source's licence and the OSM
[Import Guidelines](https://wiki.openstreetmap.org/wiki/Import/Guidelines).
