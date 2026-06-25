"""Fetch an ArcGIS REST feature/map layer via paginated /query, as GeoJSON (4326)."""

import json
import os
from datetime import date

import requests

TIMEOUT = 120
DEFAULT_PAGE = 2000


def _layer_meta(url):
    r = requests.get(url, params={"f": "json"}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def _query(url, params):
    r = requests.get(url + "/query", params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def _esri_to_geojson(esri):
    """Convert an esri-json query response (point layers) to GeoJSON features."""
    feats = []
    for f in esri.get("features", []):
        g = f.get("geometry") or {}
        x, y = g.get("x"), g.get("y")
        coords = [x, y] if x is not None and y is not None else None
        feats.append({
            "type": "Feature",
            "properties": f.get("attributes", {}),
            "geometry": {"type": "Point", "coordinates": coords} if coords else None,
        })
    return feats


def _max_oid(batch, oid_field, fmt):
    # OID lives in properties for geojson and in attributes for esri-json;
    # _esri_to_geojson already moved attributes into properties.
    return max(f["properties"][oid_field] for f in batch)


def fetch(ds, force=False):
    filename = f"{ds.slug}-{date.today().isoformat()}.geojson"
    filepath = os.path.join(ds.download_dir, filename)
    if os.path.exists(filepath) and not force:
        print(f"  using cached {filename}")
        with open(filepath, encoding="utf-8") as f:
            return filepath, json.load(f)["features"]

    meta = _layer_meta(ds.data_url)
    page = min(meta.get("maxRecordCount") or DEFAULT_PAGE, DEFAULT_PAGE)
    can_geojson = "geoJSON" in (meta.get("supportedQueryFormats") or "")
    fmt = "geojson" if can_geojson else "json"
    oid_field = meta.get("objectIdField") or "OBJECTID"
    print(f"  querying {ds.slug} (page={page}, f={fmt}, oid={oid_field})")

    # OBJECTID-window pagination: each page is an indexed range scan
    # (`oid > last`), which stays fast — unlike resultOffset, which re-scans
    # from the start on every page and degrades badly on large layers.
    features = []
    last_oid = -1
    while True:
        params = {
            "where": f"{oid_field} > {last_oid}", "outFields": "*",
            "outSR": 4326, "f": fmt,
            "orderByFields": oid_field, "resultRecordCount": page,
        }
        data = _query(ds.data_url, params)
        batch = data.get("features", []) if fmt == "geojson" else _esri_to_geojson(data)
        if not batch:
            break
        features.extend(batch)
        last_oid = _max_oid(batch, oid_field, fmt)
        print(f"\r  fetched {len(features):,} features ...", end="", flush=True)
        if len(batch) < page:
            break
    print()

    os.makedirs(ds.download_dir, exist_ok=True)
    tmp = filepath + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)
    os.replace(tmp, filepath)  # atomic: a shared-cache reader never sees a partial file
    return filepath, features
