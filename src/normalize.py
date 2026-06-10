"""Turn a raw GeoJSON feature into a canonical address record.

Canonical record keys:
    identity_key  - stable key for SCD-2 (configured key_field, or synthesized)
    number, street, unit, full - display fields (per-dataset field map; may be None)
    longitude, latitude        - EPSG:4326, rounded to 5 dp
    props        - JSON of source properties (volatile keys stripped)
    payload_hash - sha1 over the change-tracked content; same key + same hash = unchanged
"""

import hashlib
import json

# ESRI / shapefile housekeeping keys that churn on republish and must not
# influence identity or change-detection.
_VOLATILE_KEYS = {
    "objectid", "object_id", "fid", "oid", "globalid", "global_id",
    "shape", "shape_length", "shape_area", "shape__length", "shape__area",
    "se_anno_cad_data",
    "_id",  # CKAN row-sequence id (Toronto), reassigned on every republish
}

_CANONICAL = ("number", "street", "unit", "full")


def _clean(val):
    if val is None:
        return None
    s = str(val).strip()
    return s or None


def _ring_centroid(ring):
    pts = [p for p in ring if isinstance(p, list) and len(p) >= 2]
    if not pts:
        return None, None
    return (sum(p[0] for p in pts) / len(pts),
            sum(p[1] for p in pts) / len(pts))


def _coords(feature):
    """Representative point (lon, lat). Points pass through; polygons -> ring centroid."""
    geom = feature.get("geometry") or {}
    gtype = geom.get("type")
    c = geom.get("coordinates")
    if not c:
        return None, None
    if gtype == "Point":
        lon, lat = c[0], c[1]
    elif gtype == "MultiPoint" or gtype == "LineString":
        lon, lat = c[0][0], c[0][1]
    elif gtype == "Polygon":
        lon, lat = _ring_centroid(c[0])
    elif gtype == "MultiPolygon":
        lon, lat = _ring_centroid(c[0][0])
    else:
        # unknown: descend to the first coordinate pair
        while c and isinstance(c[0], list):
            c = c[0]
        lon, lat = (c[0], c[1]) if len(c) >= 2 else (None, None)
    if lon is None or lat is None:
        return None, None
    return round(float(lon), 5), round(float(lat), 5)


def _clean_props(props):
    out = {}
    for k, v in props.items():
        if k.lower() in _VOLATILE_KEYS:
            continue
        if v is None or v == "":
            continue
        out[k] = v
    return out


def canonical(ds, feature):
    """Return the canonical record dict, or None if it lacks usable geometry."""
    props = feature.get("properties") or {}
    lon, lat = _coords(feature)
    if lon is None or lat is None:
        return None

    rec = {name: _clean(props.get(src)) for name, src in ds.fields.items()
           if name in _CANONICAL}
    for name in _CANONICAL:
        rec.setdefault(name, None)

    rec["longitude"] = lon
    rec["latitude"] = lat

    clean_props = _clean_props(props)
    rec["props"] = json.dumps(clean_props, sort_keys=True, ensure_ascii=False, default=str)

    rec["identity_key"] = _identity(ds, rec, props, lon, lat)
    rec["payload_hash"] = _payload_hash(rec)
    return rec


def _identity(ds, rec, props, lon, lat):
    if ds.key_field:
        key = props.get(ds.key_field)
        if key is not None and str(key).strip():
            return str(key).strip()
    # synthesize from configured display fields + geometry
    parts = [str(rec.get(f) or "").strip().upper() for f in ds.synth_fields]
    parts += [f"{lon:.5f}", f"{lat:.5f}"]
    basis = "|".join(parts)
    return "syn:" + hashlib.sha1(basis.encode("utf-8")).hexdigest()


def _payload_hash(rec):
    basis = "|".join([
        str(rec.get("number") or ""),
        str(rec.get("street") or ""),
        str(rec.get("unit") or ""),
        str(rec.get("full") or ""),
        f"{rec['longitude']:.5f}",
        f"{rec['latitude']:.5f}",
        rec["props"],
    ])
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()
