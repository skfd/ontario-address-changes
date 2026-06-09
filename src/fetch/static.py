"""Fetch a static file (geojson or shapefile, optionally zipped) -> GeoJSON (4326)."""

import glob
import json
import os
import zipfile
from datetime import date

import requests

TIMEOUT = 300


def _download(url, dest):
    with requests.get(url, stream=True, timeout=TIMEOUT) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 18):
                f.write(chunk)


def _unzip(path, dest_dir):
    with zipfile.ZipFile(path) as z:
        z.extractall(dest_dir)


def _read_geojson(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("features", [])


def _read_shapefile(shp_path):
    """Read a point shapefile, reprojecting to EPSG:4326 using its .prj."""
    import shapefile  # pyshp
    from pyproj import CRS, Transformer

    prj_path = shp_path[:-4] + ".prj"
    transformer = None
    if os.path.exists(prj_path):
        with open(prj_path, encoding="utf-8", errors="replace") as f:
            crs = CRS.from_wkt(f.read())
        if crs.to_epsg() != 4326:
            transformer = Transformer.from_crs(crs, CRS.from_epsg(4326), always_xy=True)

    reader = shapefile.Reader(shp_path)
    field_names = [f[0] for f in reader.fields[1:]]  # drop DeletionFlag
    feats = []
    for sr in reader.iterShapeRecords():
        pts = sr.shape.points
        if not pts:
            continue
        x, y = pts[0]
        if transformer:
            x, y = transformer.transform(x, y)
        props = dict(zip(field_names, sr.record))
        feats.append({
            "type": "Feature",
            "properties": props,
            "geometry": {"type": "Point", "coordinates": [x, y]},
        })
    return feats


def _locate(work_dir, pattern):
    hits = glob.glob(os.path.join(work_dir, "**", pattern), recursive=True)
    if not hits:
        raise FileNotFoundError(f"no {pattern} found in {work_dir}")
    return hits[0]


def fetch(ds, force=False):
    filename = f"{ds.slug}-{date.today().isoformat()}.geojson"
    filepath = os.path.join(ds.data_dir, filename)
    if os.path.exists(filepath) and not force:
        print(f"  using cached {filename}")
        return filepath, _read_geojson(filepath)

    os.makedirs(ds.data_dir, exist_ok=True)
    work = os.path.join(ds.data_dir, "_download")
    os.makedirs(work, exist_ok=True)

    # Download to a fixed name; query-string URLs make basename unusable on Windows.
    raw = os.path.join(work, "download.bin")
    print(f"  downloading {ds.data_url}")
    _download(ds.data_url, raw)

    is_zip = zipfile.is_zipfile(raw)
    if is_zip:
        _unzip(raw, work)

    if ds.format == "shapefile":
        shp = _locate(work, "*.shp")
        print(f"  reading shapefile {os.path.basename(shp)}")
        features = _read_shapefile(shp)
    else:  # geojson
        if is_zip:
            try:
                src = _locate(work, "*.geojson")
            except FileNotFoundError:
                src = _locate(work, "*.json")
        else:
            src = raw
        features = _read_geojson(src)

    print(f"  parsed {len(features):,} features")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)
    return filepath, features
