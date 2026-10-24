"""Streaming the GeoJSON (ijson) must give exactly what json.load gave.

Feature values feed payload_hash and content_hash, so any drift -- Decimal for
float, int for float, a mangled string -- is a phantom mass event on every
city. Equality is also checked type-strictly, since ``1 == 1.0`` would let
exactly that drift through a plain ``==``.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db
from src.fetch import load_features
from src.registry import Dataset


def _old(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("features", [])


def _strict_eq(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(_strict_eq(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(_strict_eq(x, y) for x, y in zip(a, b))
    if isinstance(a, float):
        return repr(a) == repr(b)  # tells -0.0 from 0.0, and NaN equals NaN
    return a == b


# Not a raw string: \\u00c9 and \\ud83c\\udfe0 reach the file as JSON escapes,
# É / \U0001F3E0 as literal UTF-8.
_RAW = """{
  "type": "FeatureCollection",
  "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
  "name": "addresses",
  "features": [
    {"type": "Feature",
     "properties": {"ID": 1, "NUM": "12", "ST": "Rue Saint-\\u00c9tienne",
                    "FULL": "12 Rue Saint-Étienne", "AREA": 0.1, "TINY": 1e-7,
                    "BIG": 1E5, "NEG0": -0.0, "WHOLE": 3.0, "N": -42, "ZERO": 0,
                    "HUGE": 4611686018427387904, "NIL": null, "T": true, "F": false,
                    "EMPTY": "", "CJK": "多伦多",
                    "EMOJI": "\\ud83c\\udfe0 \U0001F3E0",
                    "NESTED": {"a": [1, 2.5, {"b": null}], "c": {}},
                    "LIST": [], "PI": 3.141592653589793238462643},
     "geometry": {"type": "Point", "coordinates": [-79.38318430, 43.65322300]}},
    {"type": "Feature",
     "properties": {"ID": 2, "NUM": "14", "ST": "Main St", "FULL": "14 Main St"},
     "geometry": {"type": "Point", "coordinates": [-79.1, 43.7, 0]}},
    {"type": "Feature", "properties": {"ID": 3}, "geometry": null}
  ]
}"""


def _write(tmp_path, text, name="pull.geojson"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_stream_matches_json_load(tmp_path):
    path = _write(tmp_path, _RAW)
    old = _old(path)
    new = load_features(path)
    assert not isinstance(new, list)  # a stream, not a parsed list
    new = list(new)
    assert new == old
    assert _strict_eq(new, old)
    props = new[0]["properties"]
    assert type(props["AREA"]) is float and type(props["ID"]) is int
    assert type(props["WHOLE"]) is float and type(props["HUGE"]) is int


def test_hashes_unchanged(tmp_path):
    ds = Dataset(slug="_test_stream", provider="Test", data_url="x", access="static",
                 format="geojson", key_field="ID",
                 fields={"number": "NUM", "street": "ST", "full": "FULL"})
    path = _write(tmp_path, _RAW)
    old, new = db._records(ds, _old(path)), db._records(ds, load_features(path))
    assert old and old == new
    assert db._content_hash(old) == db._content_hash(new)


def test_no_features_key_is_empty(tmp_path):
    path = _write(tmp_path, '{"type": "FeatureCollection", "crs": {}}')
    assert list(load_features(path)) == _old(path) == []


def test_falls_back_where_yajl_refuses(tmp_path):
    """NaN, integers past int64 and float overflow: json.load takes them, yajl
    raises. The stream re-reads with json.load and still matches, without
    repeating the features it had already yielded."""
    text = ('{"features": [{"properties": {"a": 1.5}}, {"properties": {"b": NaN}},'
            ' {"properties": {"c": 123456789012345678901234567890}},'
            ' {"properties": {"d": 1e400}}, {"properties": {"e": 2}}]}')
    path = _write(tmp_path, text)
    assert _strict_eq(list(load_features(path)), _old(path))


def test_untouched_until_iterated(tmp_path):
    """Nothing is opened until the first feature is asked for, so an
    already-imported snapshot costs no parse at all."""
    stream = load_features(str(tmp_path / "missing.geojson"))  # no error yet
    try:
        next(stream)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("expected FileNotFoundError on first read")
