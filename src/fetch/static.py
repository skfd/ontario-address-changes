"""Fetch a static file (geojson or shapefile, optionally zipped) -> GeoJSON (4326)."""

import glob
import json
import os
import zipfile
from datetime import date

import requests

TIMEOUT = 300


def _int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def _download(url, dest):
    """Stream ``url`` to ``dest``; return its response headers of interest."""
    with requests.get(url, stream=True, timeout=TIMEOUT) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 18):
                f.write(chunk)
        return {"last_modified": r.headers.get("Last-Modified"),
                "content_length": _int(r.headers.get("Content-Length"))}


def _head(url):
    try:
        r = requests.head(url, timeout=30, allow_redirects=True)
        r.raise_for_status()
        return {"last_modified": r.headers.get("Last-Modified"),
                "content_length": _int(r.headers.get("Content-Length"))}
    except requests.RequestException as e:
        print(f"  (HEAD check failed, will download: {e})")
        return {}


def _sidecar_path(ds):
    # Per-dataset, per-repo: tracks the last download's headers so an unchanged
    # remote can reuse the existing dated file without re-pulling (matters for
    # Toronto's ~590 MB snapshot). The dated file itself lives in download_dir.
    return os.path.join(ds.data_dir, ".last-download.json")


def _load_sidecar(ds):
    path = _sidecar_path(ds)
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def _save_sidecar(ds, headers, filename):
    os.makedirs(ds.data_dir, exist_ok=True)
    with open(_sidecar_path(ds), "w", encoding="utf-8") as f:
        json.dump({**headers, "filename": filename}, f, indent=2)


def _cached_if_unchanged(ds):
    sc = _load_sidecar(ds)
    if not sc:
        return None
    remote = _head(ds.data_url)
    if not remote:
        return None
    same = (remote.get("last_modified") == sc.get("last_modified")
            and remote.get("content_length") == sc.get("content_length"))
    path = os.path.join(ds.download_dir, sc.get("filename", ""))
    return path if same and os.path.isfile(path) else None


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
    os.makedirs(ds.download_dir, exist_ok=True)
    filename = f"{ds.slug}-{date.today().isoformat()}.geojson"
    filepath = os.path.join(ds.download_dir, filename)

    # Today's file already in the (possibly shared) cache: reuse without a HEAD,
    # so a sibling repo that already pulled this source today costs nothing.
    if os.path.exists(filepath) and not force:
        print(f"  using cached {filename}")
        return filepath, _read_geojson(filepath)

    # First pull of the day: skip the download if the remote is byte-for-byte
    # what we last saw (Last-Modified / Content-Length), reusing the prior file.
    if not force:
        cached = _cached_if_unchanged(ds)
        if cached:
            print(f"  using cached {os.path.basename(cached)} (remote unchanged)")
            return cached, _read_geojson(cached)

    work = os.path.join(ds.download_dir, "_download")
    os.makedirs(work, exist_ok=True)

    # Download to a fixed name; query-string URLs make basename unusable on Windows.
    raw = os.path.join(work, "download.bin")
    print(f"  downloading {ds.data_url}")
    headers = _download(ds.data_url, raw)

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
    tmp = filepath + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)
    os.replace(tmp, filepath)  # atomic: a shared-cache reader never sees a partial file
    _save_sidecar(ds, headers, filename)
    return filepath, features
