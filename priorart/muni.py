"""Ontario lower- and single-tier municipalities as polygons, and point binning.

The comparison key for everything in priorart/ is the municipality name as LIO
publishes it (MUNICIPAL_NAME_SHORTFORM, normalized by norm_name). StatCan's
census subdivisions carry the same names for municipalities; reserves and
unorganized territories have no polygon here and bin to None.

Source: LIO Open Data, "Municipal Bnd Lower And Single" (LIO_Open03 layer 14),
pulled once into cache/ and generalized to ~10 m, which is far below the
precision any address point needs for a municipality assignment.
"""
from __future__ import annotations

import json
import os
import re
import time
import unicodedata
import urllib.parse
import urllib.request

import numpy as np
import shapely
from shapely.geometry import shape
from shapely.strtree import STRtree

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
POLY_PATH = os.path.join(CACHE, "lio_municipal_lower_single.geojson")
LIO_QUERY = ("https://ws.lioservices.lrc.gov.on.ca/arcgis1071a/rest/services/"
             "LIO_OPEN_DATA/LIO_Open03/MapServer/14/query")
ALIASES_PATH = os.path.join(HERE, "muni_aliases.csv")


def norm_name(s: str | None) -> str | None:
    """Uppercase, accent-stripped, no periods, single spaces. 'Sault Ste. Marie' -> 'SAULT STE MARIE'."""
    if s is None:
        return None
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.upper().replace(".", "").replace("’", "'")
    s = re.sub(r"\s*/\s*", "/", s)          # 'GORDON / BARRIE ISLAND' == 'Gordon/Barrie Island'
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


CSD_TYPE_WORD = {"CY": "CITY", "C": "CITY", "T": "TOWN", "TP": "TOWNSHIP", "TV": "TOWN", "VL": "VILLAGE",
                 "M": "MUNICIPALITY", "MU": "MUNICIPALITY", "CV": "CITY"}
# StatCan CSD types with no municipal polygon by design: reserves, Indian settlements,
# unorganized territories, Indian government districts. Rows there are "unbinned" and expected.
CSD_TYPES_OUTSIDE = {"R", "NO", "S-É", "S-E", "IGD", "IRI", "SG"}


def type_word(official_name: str | None) -> str:
    """'CITY OF HAMILTON' -> 'CITY'; 'TOWNSHIP OF HAMILTON' -> 'TOWNSHIP'."""
    n = norm_name(official_name) or ""
    mm = re.match(r"^(CITY|TOWN|TOWNSHIP|MUNICIPALITY|VILLAGE|COUNTY|REGION|DISTRICT|UNITED TOWNSHIPS|SEPARATED TOWN)\b", n)
    return mm.group(1) if mm else "MUNICIPALITY"


def load_aliases() -> dict[str, str]:
    """Hand aliases: a comparator's name -> LIO shortform, both normalized."""
    out = {}
    if os.path.exists(ALIASES_PATH):
        import csv
        with open(ALIASES_PATH, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row.get("alias") and row.get("municipality"):
                    out[norm_name(row["alias"])] = norm_name(row["municipality"])
    return out


def ensure_polygons(force: bool = False) -> str:
    """Download the LIO layer into cache/ if it is not there. Pages of 25: the
    server answers larger GeoJSON pages with an HTML error."""
    if os.path.exists(POLY_PATH) and not force:
        return POLY_PATH
    os.makedirs(CACHE, exist_ok=True)
    feats, off, page = [], 0, 25
    while True:
        q = urllib.parse.urlencode({
            "where": "1=1",
            "outFields": "MUNID,MAH_CODE,MUNICIPAL_NAME,MUNICIPAL_NAME_SHORTFORM,"
                         "MUNICIPAL_TYPE,UPPER_TIER_MUNICIPALITY,MUNICIPAL_AREA_EXTENT_TYPE",
            "outSR": "4326", "f": "geojson", "resultOffset": off,
            "resultRecordCount": page, "orderByFields": "OBJECTID",
            "geometryPrecision": 6, "maxAllowableOffset": 0.0001,
        })
        data = None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(LIO_QUERY + "?" + q, timeout=600) as r:
                    data = json.loads(r.read())
                break
            except Exception as exc:  # noqa: BLE001 - retry whatever it was
                print(f"  lio page {off}: retry {attempt + 1} ({str(exc)[:60]})")
                time.sleep(3 * (attempt + 1))
        if data is None:
            raise RuntimeError(f"LIO municipal layer: gave up at offset {off}")
        fs = data.get("features", [])
        feats += fs
        if len(fs) < page:
            break
        off += page
    with open(POLY_PATH, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": feats}, fh)
    return POLY_PATH


class Municipalities:
    """Polygons + STRtree. assign() maps lon/lat arrays to normalized names."""

    def __init__(self, path: str | None = None):
        path = path or ensure_polygons()
        with open(path, encoding="utf-8") as fh:
            fc = json.load(fh)
        self.geoms, self.names, self.info = [], [], {}
        # Two municipalities can share a short name (HAMILTON: the city and the
        # township in Northumberland). Key those as "NAME (TYPE WORD)" instead.
        by_short = {}
        for f in fc["features"]:
            p = f["properties"]
            short = norm_name(p.get("MUNICIPAL_NAME_SHORTFORM")) or norm_name(p.get("MUNICIPAL_NAME"))
            by_short.setdefault(short, set()).add(str(p.get("MUNID")))
        for f in fc["features"]:
            p = f["properties"]
            short = norm_name(p.get("MUNICIPAL_NAME_SHORTFORM")) or norm_name(p.get("MUNICIPAL_NAME"))
            name = short
            if len(by_short[short]) > 1:
                name = f"{short} ({type_word(p.get('MUNICIPAL_NAME'))})"
            g = shape(f["geometry"])
            if g.is_empty:
                continue
            self.geoms.append(g)
            self.names.append(name)
            rec = self.info.setdefault(name, {
                "municipality": name, "short": short,
                "official_name": p.get("MUNICIPAL_NAME"),
                "munid": set(), "type": p.get("MUNICIPAL_TYPE"),
                "type_word": type_word(p.get("MUNICIPAL_NAME")),
                "upper_tier": norm_name(p.get("UPPER_TIER_MUNICIPALITY")) or "",
            })
            rec["munid"].add(str(p.get("MUNID")))
        self.tree = STRtree(self.geoms)
        self.aliases = load_aliases()
        self.by_short = {}
        for name, rec in self.info.items():
            self.by_short.setdefault(rec["short"], []).append(name)

    # -- lookups ---------------------------------------------------------
    def table(self) -> list[dict]:
        rows = []
        for name, rec in sorted(self.info.items()):
            r = dict(rec)
            r["munid"] = ";".join(sorted(rec["munid"]))
            r["name_collision"] = len(self.by_short[rec["short"]]) > 1
            rows.append(r)
        return rows

    def resolve(self, name: str | None, csd_type: str | None = None) -> str | None:
        """A comparator's municipality name -> our key, or None if unknown.

        Tries, in order: the name as given, a hand alias, each half of a
        bilingual "X / Y" name, with and without a trailing COUNTY, and without
        a "CITY OF" style prefix. csd_type (StatCan CY/TP/T/M/VL...) breaks a
        short-name collision; without it the city wins."""
        n = norm_name(name)
        if n is None:
            return None
        n = re.sub(r"\s*/\s*", "/", n)
        cands = [n]
        if n in self.aliases:
            cands.append(self.aliases[n])
        if "/" in n:
            cands += n.split("/")
        more = []
        for c in cands:
            if c.endswith(" COUNTY"):
                more.append(c[:-7])
            else:
                more.append(c + " COUNTY")
            mm = re.match(r"^(?:CITY|TOWN|TOWNSHIP|MUNICIPALITY|VILLAGE|COUNTY|REGION|DISTRICT) OF (?:THE )?(.+)$", c)
            if mm:
                more.append(mm.group(1))
        for c in cands + more:
            c = c.strip()
            if c in self.info:
                return c
            if c in self.by_short:
                names = self.by_short[c]
                want = CSD_TYPE_WORD.get((csd_type or "").upper())
                for nm in names:
                    if want and self.info[nm]["type_word"] == want:
                        return nm
                for nm in names:
                    if self.info[nm]["type_word"] == "CITY":
                        return nm
                return names[0]
        return None

    def assign(self, lons, lats) -> list[str | None]:
        """Point-in-polygon for arrays of coordinates. Points outside every
        municipality (reserves, unorganized, water, bad coords) get None."""
        lons = np.asarray(lons, dtype=float)
        lats = np.asarray(lats, dtype=float)
        out: list[str | None] = [None] * len(lons)
        if len(lons) == 0:
            return out
        pts = shapely.points(lons, lats)
        pi, gi = self.tree.query(pts, predicate="within")
        for p, g in zip(pi.tolist(), gi.tolist()):
            if out[p] is None:
                out[p] = self.names[g]
        return out
