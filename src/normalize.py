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
import re
from functools import lru_cache

# ESRI / shapefile housekeeping keys that churn on republish and must not
# influence identity or change-detection.
_VOLATILE_KEYS = {
    "object_id", "oid",
    "globalid", "globalid_1", "global_id",
    "shape", "shape_length", "shape_area", "shape__length", "shape__area",
    "se_anno_cad_data",
    "_id",  # CKAN row-sequence id (Toronto), reassigned on every republish
}

# The numbered spellings of the same two ids. A layer that has been joined or
# re-exported carries OBJECTID_1, FID_1, and so on up -- hastings publishes
# OBJECTID_12, whose alias is literally "OBJECTID_1". Listing the spellings one
# at a time kept missing them, so match the shape instead. Anchored, so a real
# column that merely starts this way (OBJECTID_SOURCE) is untouched.
_VOLATILE_RE = re.compile(r"^(?:objectid|fid)(?:_\d+)?$")


def is_volatile(key):
    """True for a housekeeping key that must never reach props or payload_hash."""
    kl = key.lower()
    return kl in _VOLATILE_KEYS or bool(_VOLATILE_RE.match(kl))


# Edit-metadata props ignored in every dataset (case-insensitive): timestamps and
# editor names that change alongside any real edit (or on their own) and carry no
# address information. Curated from a scan of all tracked sources; meaningful date
# fields (OCCUPANCY_DATE, VERIFIED_DATE, ...) are deliberately not listed. Stripped
# from the props blob so they never influence payload_hash / change-detection.
EDIT_METADATA_FIELDS = frozenset({
    "created_date", "create_date", "createdate", "created_user",
    "edit_date", "edited_date", "editdate", "dateedit", "dateupdate",
    "update_date", "updated", "lastupdate", "lasteditdate",
    "last_edited_date", "last_edited_user", "lasteditor",
    "modified_date", "moddate", "adddate",
    # esri's newer editor-tracking spellings (west-parry-sound publishes these two;
    # nothing is stored anywhere under them, so adding them cost no backfill)
    "creationdate", "modificationdate",
})

# Literal null serializations: text a publisher's ETL emits where it means null.
# "None" is Python's str(None) leaking out of an export script -- toronto ships it
# on ~525k rows across six columns (ADDRESS_STATUS, PLACE_NAME, PLACE_NAME_ALL,
# HI_NUM_SUF, LO_NUM_SUF, LINEAR_NAME_DESC), windsor on Ward and its unaddressed
# parcels. "<Null>" is how ArcGIS renders an empty cell when a field calculator
# writes one out as text. Both are the publisher's bug, not a value, and both are
# latent mass events: the day either export is fixed to emit real nulls, every
# affected row re-hashes at once. Dropping them makes the prop absent, which is
# what it already means.
#
# Deliberately NOT here (measured across all 53 stores, 2026-08-21): "Unknown" /
# "UNKNOWN" (541,943 occurrences -- a real coded-domain value: toronto GENERAL_USE,
# kitchener UNIT_TYPE), "NA"/"na", "?", "-", "NONE". Those are things a person or a
# domain author typed meaning something; only the exact-case serializer spellings
# are machine artefacts, so the match is exact-case and not a fuzzy null-ish list.
_NULL_LITERALS = frozenset({"None", "<Null>"})

_CANONICAL = ("number", "street", "unit", "full")


def _clean(val):
    if val is None:
        return None
    s = str(val).strip()
    return s or None


@lru_cache(maxsize=None)
def _transformer(crs):
    from pyproj import Transformer
    return Transformer.from_crs(crs, "EPSG:4326", always_xy=True)


def _to_wgs84(ds, lon, lat):
    """Reproject projected coords to WGS84 via the dataset's source_crs.

    Pass-through when already in lon/lat range, or when no source_crs is set.
    The range guard means already-WGS84 snapshots are untouched even if a source_crs
    is configured (e.g. a city that switched its export CRS partway through history).
    """
    if abs(lon) <= 180 and abs(lat) <= 90:
        return lon, lat
    if not ds.source_crs:
        return lon, lat
    return _transformer(ds.source_crs).transform(lon, lat)


def _ring_centroid(ring):
    pts = [p for p in ring if isinstance(p, list) and len(p) >= 2]
    if not pts:
        return None, None
    return (sum(p[0] for p in pts) / len(pts),
            sum(p[1] for p in pts) / len(pts))


def _coords(ds, feature):
    """Representative point (lon, lat). Points pass through; polygons -> ring centroid.

    Projected coords (per ds.source_crs) are reprojected to WGS84 before rounding.
    """
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
    lon, lat = _to_wgs84(ds, float(lon), float(lat))
    return round(float(lon), 5), round(float(lat), 5)


def _clean_props(props, ignore, keep=frozenset()):
    out = {}
    for k, v in props.items():
        kl = k.lower()
        if is_volatile(kl) or kl in ignore:
            continue
        if v is None:
            continue
        if isinstance(v, str):
            # Strip, don't just drop the all-whitespace ones: a source that pads a
            # column out (" ", "\t") carries no value, and a source that re-pads a
            # real value ("2502 Calabogie Road " -> "2502 Calabogie Road", renfrew
            # on 1,060 rows) churns the prop while the canonical field sits still,
            # because _clean already strips those. A stripped value that is only a
            # serializer's word for null goes the same way (see _NULL_LITERALS).
            v = v.strip()
            if not v or v in _NULL_LITERALS:
                continue
        if kl in keep and (v == 0 or v == "0"):
            # zero-encoded "absent" (Toronto stored HI_NUM=0 for non-ranges
            # until mid-2026); a stored 0 would read downstream as a real
            # range bound. Kept fields are outside the hash, so this is safe.
            continue
        out[k] = v
    return out


def canonical(ds, feature):
    """Return the canonical record dict, or None if it lacks usable geometry."""
    props = feature.get("properties") or {}
    lon, lat = _coords(ds, feature)
    if lon is None or lat is None:
        return None

    rec = {name: _clean(props.get(src)) for name, src in ds.fields.items()
           if name in _CANONICAL}
    for name in _CANONICAL:
        rec.setdefault(name, None)

    rec["longitude"] = lon
    rec["latitude"] = lat

    ignore = {k.lower() for k in ds.ignore_fields} | EDIT_METADATA_FIELDS
    # keep_fields are ignored for change detection but still stored, for consumers
    # that need them (see datasets/toronto.toml). They are dropped from the hash
    # basis below so their churn can't open a new SCD-2 range.
    keep = {k.lower() for k in ds.keep_fields}
    clean_props = _clean_props(props, ignore - keep, keep)
    rec["props"] = json.dumps(clean_props, sort_keys=True, ensure_ascii=False, default=str)

    hash_props = {k: v for k, v in clean_props.items() if k.lower() not in keep}
    rec["identity_key"] = _identity(ds, rec, props, lon, lat)
    rec["payload_hash"] = _payload_hash(rec, hash_props)
    return rec


def _identity(ds, rec, props, lon, lat):
    if ds.key_field:
        key = props.get(ds.key_field)
        if key is not None and str(key).strip():
            return str(key).strip()
    # synthesize from configured display fields + geometry
    parts = [str(rec.get(f) or "").strip().upper() for f in ds.synth_fields]
    parts += [str(props.get(p) or "").strip().upper() for p in ds.synth_props]
    if ds.use_geometry:
        # 5 dp is ~1.1 m. A source whose coordinates jitter at that scale on
        # republish would mint a new key for every jittered row, so such a
        # dataset must disambiguate with synth_props instead (muskoka).
        parts += [f"{lon:.5f}", f"{lat:.5f}"]
    basis = "|".join(parts)
    return "syn:" + hashlib.sha1(basis.encode("utf-8")).hexdigest()


def _payload_hash(rec, hash_props):
    """Hash over the change-tracked content. ``hash_props`` is the stored props
    minus any keep_fields, so a dataset with no keep_fields hashes exactly as
    before (byte-identical to rec["props"])."""
    basis = "|".join([
        str(rec.get("number") or ""),
        str(rec.get("street") or ""),
        str(rec.get("unit") or ""),
        str(rec.get("full") or ""),
        f"{rec['longitude']:.5f}",
        f"{rec['latitude']:.5f}",
        json.dumps(hash_props, sort_keys=True, ensure_ascii=False, default=str),
    ])
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()
