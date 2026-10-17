#!/usr/bin/env python
"""Measure the prior art against the tracker: coverage, cadence, quality, licence.

    python priorart/measure.py all            # every comparator, then render
    python priorart/measure.py ours oa        # a subset
    python priorart/measure.py overture --release 2026-09-23.1

Writes (all in priorart/):
  measures.csv   append-only, one row per (source, day, measure); idempotent per day
  coverage.csv   municipality x comparator x vintage x source -> rows and field fill
  licences.csv   our licence next to what OpenAddresses and the ODA record
  report.html    via render.py (back-office; not under docs/)

Comparators and the join tables are hand-maintained: comparators.csv,
oa_sources.csv (OpenAddresses source -> our slug), muni_aliases.csv (names).
Raw pulls live in priorart/cache/ (gitignored). See README.md.
"""
from __future__ import annotations

import argparse
import csv
import glob
import io
import json
import os
import re
import sys
import time
import tomllib
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from src import db, registry  # noqa: E402
from muni import CACHE, CSD_TYPES_OUTSIDE, Municipalities, norm_name  # noqa: E402

MEASURES = os.path.join(HERE, "measures.csv")
COVERAGE = os.path.join(HERE, "coverage.csv")
LICENCES = os.path.join(HERE, "licences.csv")
OA_SOURCES = os.path.join(HERE, "oa_sources.csv")
TODAY = date.today().isoformat()
UA = {"User-Agent": "ontario-address-changes/priorart (https://github.com/skfd/ontario-address-changes)"}

MEASURE_COLS = ["source_id", "measured_on", "measure", "value", "of", "unit", "method", "text"]
COVERAGE_COLS = ["municipality", "comparator", "vintage", "source", "rows", "locations",
                 "unit_filled", "street_filled", "number_filled", "postcode_filled"]


# --------------------------------------------------------------------------- io
def _read_csv(path):
    if not os.path.exists(path):
        return []
    for enc in ("utf-8-sig", "cp1252"):
        try:
            with open(path, newline="", encoding=enc) as fh:
                return list(csv.DictReader(fh))
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("csv", b"", 0, 0, f"{path}: neither UTF-8 nor cp1252")


def _write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def append_measures(rows):
    """Append, skipping rows already recorded for the same source/measure/day."""
    existing = {(r["source_id"], r["measured_on"], r["measure"]) for r in _read_csv(MEASURES)}
    new = [r for r in rows if (r["source_id"], r["measured_on"], r["measure"]) not in existing]
    fresh = not os.path.exists(MEASURES)
    with open(MEASURES, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=MEASURE_COLS, extrasaction="ignore")
        if fresh:
            w.writeheader()
        w.writerows(new)
    print(f"  measures: +{len(new)} rows ({len(rows) - len(new)} already recorded today)")


def m(source_id, measure, value, of=None, unit="", method="", text="", measured_on=None):
    return {"source_id": source_id, "measured_on": measured_on or TODAY, "measure": measure,
            "value": value if value is not None else "", "of": of if of is not None else "",
            "unit": unit, "method": method, "text": text}


def write_coverage(comparator, rows, vintage=None):
    """Replace this comparator's rows (for one vintage, or all of them)."""
    keep = [r for r in _read_csv(COVERAGE)
            if not (r["comparator"] == comparator and (vintage is None or r["vintage"] == vintage))]
    allrows = keep + rows
    allrows.sort(key=lambda r: (r["comparator"], r["vintage"], r["municipality"] or "~", r["source"]))
    _write_csv(COVERAGE, COVERAGE_COLS, allrows)
    print(f"  coverage: {len(rows)} rows for {comparator}{' ' + vintage if vintage else ''}")


def cov_row(muni, comparator, vintage, source, rows, unit=0, street=0, number=0, postcode=0, locations=""):
    return {"municipality": muni or "", "comparator": comparator, "vintage": vintage, "source": source,
            "rows": rows, "locations": locations, "unit_filled": unit, "street_filled": street,
            "number_filled": number, "postcode_filled": postcode}


def _get_json(url, timeout=60):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return json.load(r)


def _toml(slug):
    with open(os.path.join(ROOT, "datasets", f"{slug}.toml"), "rb") as fh:
        return tomllib.load(fh)


# -------------------------------------------------------------------------- ours
def cmd_ours(args):
    print("ours: reading data/<slug>/<slug>.db")
    munis = Municipalities()
    measures, cov = [], []
    since30 = (datetime.now() - timedelta(days=30)).isoformat()
    for ds in registry.load_all():
        if not os.path.exists(ds.db_path):
            continue
        conn = db.init_db(ds)
        sid = db.latest_snapshot_id(conn)
        if sid is None:
            conn.close()
            continue
        last = conn.execute("SELECT downloaded FROM snapshots WHERE id = ?", (sid,)).fetchone()[0]
        snaps30 = conn.execute(
            "SELECT COUNT(*) FROM snapshots WHERE skipped = 0 AND downloaded >= ?", (since30,)).fetchone()[0]
        hashes30 = conn.execute(
            "SELECT COUNT(DISTINCT content_hash) FROM snapshots WHERE skipped = 0 AND downloaded >= ?",
            (since30,)).fetchone()[0]
        first = conn.execute("SELECT MIN(downloaded) FROM snapshots").fetchone()[0]
        rows = conn.execute(
            "SELECT longitude, latitude, unit, street, number FROM addresses "
            "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchall()
        conn.close()
        n = len(rows)
        unit = sum(1 for r in rows if r[2] not in (None, ""))
        street = sum(1 for r in rows if r[3] not in (None, ""))
        number = sum(1 for r in rows if r[4] not in (None, ""))
        sid_str = f"ours:{ds.slug}"
        measures += [
            m(sid_str, "rows", n, method="sqlite active rows", text=f"snapshot {last[:10]}"),
            m(sid_str, "unit_fill", unit, n, method="canonical unit non-empty"),
            m(sid_str, "street_fill", street, n, method="canonical street non-empty"),
            m(sid_str, "number_fill", number, n, method="canonical number non-empty"),
            m(sid_str, "snapshots_30d", snaps30, 30, "days", "non-skipped snapshots in the last 30 days"),
            m(sid_str, "distinct_content_30d", hashes30, snaps30, "snapshots", "distinct content hashes in the last 30 days"),
            m(sid_str, "last_snapshot", last[:10], method="latest non-skipped snapshot"),
            m(sid_str, "tracked_since", (first or "")[:10], method="first snapshot"),
        ]
        pts = [(r[0], r[1]) for r in rows if r[0] is not None and r[1] is not None]
        names = munis.assign([p[0] for p in pts], [p[1] for p in pts]) if pts else []
        agg = defaultdict(lambda: [0, 0, 0, 0])
        for r, nm in zip([r for r in rows if r[0] is not None and r[1] is not None], names):
            a = agg[nm]
            a[0] += 1
            a[1] += r[2] not in (None, "")
            a[2] += r[3] not in (None, "")
            a[3] += r[4] not in (None, "")
        for nm, a in agg.items():
            cov.append(cov_row(nm, "ours", "latest", ds.slug, a[0], a[1], a[2], a[3], 0))
        outside = agg.get(None, [0])[0]
        print(f"  {ds.slug}: {n} rows, {len([k for k in agg if k])} municipalities, {outside} outside any")
    append_measures(measures)
    write_coverage("ours", cov)


# ---------------------------------------------------------------------------- oa
OA_API = "https://batch.openaddresses.io/api"
OA_RAW = "https://raw.githubusercontent.com/openaddresses/openaddresses/master/sources/ca/on/"
OA_LIST = "https://api.github.com/repos/openaddresses/openaddresses/contents/sources/ca/on"


def _oa_refresh():
    d = os.path.join(CACHE, "oa")
    os.makedirs(os.path.join(d, "sources"), exist_ok=True)
    data = _get_json(f"{OA_API}/data?source=ca/on&layer=addresses")
    with open(os.path.join(d, "data_ca_on.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    for row in data:
        try:
            h = _get_json(f"{OA_API}/data/{row['id']}/history")
            with open(os.path.join(d, f"history_{row['id']}.json"), "w", encoding="utf-8") as fh:
                json.dump(h, fh)
        except Exception as exc:  # noqa: BLE001
            print(f"  history {row['source']}: {exc}")
        time.sleep(0.2)
    try:
        names = [x["name"] for x in _get_json(OA_LIST) if x["name"].endswith(".json")]
        for name in names:
            with urllib.request.urlopen(urllib.request.Request(OA_RAW + name, headers=UA), timeout=60) as r:
                with open(os.path.join(d, "sources", name), "wb") as fh:
                    fh.write(r.read())
    except Exception as exc:  # noqa: BLE001
        print(f"  source jsons: {exc} (keeping cached copies)")
    print(f"  oa cache refreshed: {len(data)} data rows")


def _oa_licence(src_json):
    for layer in (src_json.get("layers", {}).get("addresses") or []):
        lic = layer.get("license")
        if isinstance(lic, dict):
            return (lic.get("text") or "").strip(), (lic.get("url") or "").strip()
        if isinstance(lic, str):
            return lic.strip(), ""
    return "", ""


def cmd_oa(args):
    print("oa: OpenAddresses batch API + source JSONs")
    d = os.path.join(CACHE, "oa")
    if not args.offline or not os.path.exists(os.path.join(d, "data_ca_on.json")):
        _oa_refresh()
    with open(os.path.join(d, "data_ca_on.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    join = {r["oa_source"]: r for r in _read_csv(OA_SOURCES)}
    ours_rows = {r["source_id"].split(":", 1)[1]: int(r["value"]) for r in _read_csv(MEASURES)
                 if r["measure"] == "rows" and r["source_id"].startswith("ours:") and r["measured_on"] == TODAY}
    measures = []
    year_ago = (datetime.now() - timedelta(days=365)).isoformat()
    seen = set()
    for row in data:
        name = row["source"].split("/")[-1]
        if name in seen:          # OA keeps two data rows for west_parry_sound_district
            continue
        seen.add(name)
        sid = f"oa:{name}"
        hist_path = os.path.join(d, f"history_{row['id']}.json")
        jobs = []
        if os.path.exists(hist_path):
            with open(hist_path, encoding="utf-8") as fh:
                h = json.load(fh)
            jobs = h.get("jobs", h) if isinstance(h, dict) else h
        ok = [j for j in jobs if j.get("status") == "Success"]
        latest = ok[0] if ok else None
        runs365 = sum(1 for j in ok if j.get("created", "") >= year_ago)
        last_ok = (latest or {}).get("created", row.get("updated", ""))[:10]
        if latest and latest.get("stats"):
            c = latest["stats"].get("counts", {})
            n = latest.get("count") or 0
            v = latest["stats"].get("validity", {}).get("valid")
            measures += [
                m(sid, "rows", n, method="batch job count", text=f"job {latest['id']} {last_ok}"),
                m(sid, "unit_fill", c.get("unit", 0), n, method="batch stats.counts.unit"),
                m(sid, "street_fill", c.get("street", 0), n, method="batch stats.counts.street"),
                m(sid, "number_fill", c.get("number", 0), n, method="batch stats.counts.number"),
                m(sid, "postcode_fill", c.get("postcode", 0), n, method="batch stats.counts.postcode"),
                m(sid, "valid", v, n, method="batch stats.validity.valid"),
            ]
            jr = join.get(name, {})
            slug = (jr.get("our_slug") or "").split(";")[0]
            if slug in ours_rows and ours_rows[slug]:
                measures.append(m(sid, "rows_vs_ours", n, ours_rows[slug], method=f"OA count / our active rows ({slug})",
                                  text=jr.get("match", "")))
        else:
            measures.append(m(sid, "rows", 0, method="no successful batch job", text=f"last attempt {row.get('updated', '')[:10]}"))
        measures += [
            m(sid, "last_success", last_ok, method="latest Success job created"),
            m(sid, "runs_365d", runs365, 52, "jobs", "successful batch jobs in the last 365 days"),
            m(sid, "days_stale", (date.today() - date.fromisoformat(last_ok)).days if last_ok else "",
              unit="days", method="today - last_success"),
        ]
    append_measures(measures)
    _write_licences(d)


def _write_licences(oa_dir):
    """Our licence next to OA's and the ODA's for the same jurisdiction."""
    join = _read_csv(OA_SOURCES)
    by_slug = defaultdict(list)
    for r in join:
        for s in (r["our_slug"] or "").split(";"):
            if s:
                by_slug[s].append(r)
    oa_lic = {}
    for p in glob.glob(os.path.join(oa_dir, "sources", "*.json")):
        try:
            with open(p, encoding="utf-8") as fh:
                oa_lic[os.path.basename(p)[:-5]] = _oa_licence(json.load(fh))
        except Exception:  # noqa: BLE001
            pass
    oda = {}
    for r in _read_csv(os.path.join(CACHE, "oda_data_sources.csv")):
        if r.get("Province / Territory", "").strip().upper() == "ON":
            oda[_norm_provider(r["Data Provider"])] = r
    out = []
    for ds in registry.load_all():
        t = _toml(ds.slug)
        oas = by_slug.get(ds.slug, [])
        oa_texts = sorted({oa_lic.get(r["oa_source"], ("", ""))[0] for r in oas if r["match"] != "covered-by"} - {""})
        oa_urls = sorted({oa_lic.get(r["oa_source"], ("", ""))[1] for r in oas if r["match"] != "covered-by"} - {""})
        od = oda.get(_norm_provider(t.get("provider", "")))
        out.append({
            "slug": ds.slug, "provider": t.get("provider", ""),
            "our_licence": t.get("license_name", ""), "osm_compatible": t.get("osm_compatible", ""),
            "publish_reports": "" if t.get("publish_reports", True) else "false",
            "oa_sources": ";".join(r["oa_source"] for r in oas),
            "oa_licence": " | ".join(oa_texts)[:300], "oa_licence_url": " | ".join(oa_urls)[:300],
            "oda_provider": od["Data Provider"] if od else "",
            "oda_licence": (od["Licence Title"] + (" v" + od["Licence Version"] if od["Licence Version"] else "")) if od else "",
            "oda_downloaded": od["Date Downloaded"] if od else "",
        })
    _write_csv(LICENCES, list(out[0].keys()) if out else [], out)
    print(f"  licences: {len(out)} rows")


def _norm_provider(s):
    s = norm_name(s) or ""
    s = re.sub(r"^(THE )?(CORPORATION OF THE |CORPORATION OF )?", "", s)
    s = re.sub(r"^(CITY|TOWN|TOWNSHIP|COUNTY|DISTRICT MUNICIPALITY|REGIONAL MUNICIPALITY|REGION|MUNICIPALITY|UNITED COUNTIES) OF (THE )?", "", s)
    s = re.sub(r"\s+(COUNTY|REGION|CITY)$", "", s)
    s = s.replace("&", "AND").replace(" ST ", " SAINT ")
    return s.strip()


# --------------------------------------------------------------------------- oda
ODA_ZIP_URL = "https://www150.statcan.gc.ca/n1/pub/46-26-0001/2021001/ODA_ON_v1.zip"


def _oda_prepare():
    counts = os.path.join(CACHE, "oda_on_v1_counts.csv")
    srcs = os.path.join(CACHE, "oda_data_sources.csv")
    if os.path.exists(counts) and os.path.exists(srcs):
        return counts, srcs
    zpath = os.path.join(CACHE, "ODA_ON_v1.zip")
    if not os.path.exists(zpath):
        print("  downloading ODA_ON_v1.zip (160 MB)")
        with urllib.request.urlopen(urllib.request.Request(ODA_ZIP_URL, headers=UA), timeout=900) as r, open(zpath, "wb") as fh:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                fh.write(b)
    z = zipfile.ZipFile(zpath)
    with open(srcs, "w", encoding="utf-8", newline="") as fh:   # StatCan ships it as cp1252
        fh.write(z.read("Data_Sources.csv").decode("cp1252"))
    cnt, fill = Counter(), defaultdict(lambda: [0, 0, 0, 0])
    with z.open("ODA_ON_v1.csv") as f:
        for row in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", errors="replace")):
            k = (row["csduid"], row["csdname"], row["provider"])
            cnt[k] += 1
            a = fill[k]
            a[0] += bool(row["unit"].strip())
            a[1] += bool(row["street_no"].strip())
            a[2] += bool(row["street"].strip())        # full street; str_name is the parsed part and often blank
            a[3] += bool(row["postal_code"].strip())
    with open(counts, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out)
        w.writerow(["csduid", "csdname", "provider", "rows", "unit_filled", "number_filled", "street_filled", "postcode_filled"])
        for k, n in sorted(cnt.items()):
            w.writerow([*k, n, *fill[k]])
    return counts, srcs


def cmd_oda(args):
    print("oda: StatCan Open Database of Addresses v1 (2021)")
    counts, srcs = _oda_prepare()
    munis = Municipalities()
    down = {r["Data Provider"]: r["Date Downloaded"] for r in _read_csv(srcs) if r["Province / Territory"].strip().upper() == "ON"}
    cov, per_prov, unmatched = [], defaultdict(lambda: [0, 0, 0, 0, 0]), Counter()
    for r in _read_csv(counts):
        key = munis.resolve(r["csdname"])
        if key is None and not re.search(r"\b(Unorganized|First Nation|Reserve|Territory|Island \d|\d+[A-Z]?)$", r["csdname"]):
            unmatched[r["csdname"]] += int(r["rows"])
        cov.append(cov_row(key, "oda", "2021-v1", r["provider"], int(r["rows"]), int(r["unit_filled"]),
                           int(r["street_filled"]), int(r["number_filled"]), int(r["postcode_filled"])))
        a = per_prov[r["provider"]]
        for i, c in enumerate(("rows", "unit_filled", "street_filled", "number_filled", "postcode_filled")):
            a[i] += int(r[c])
    measures = []
    tot = [0, 0, 0, 0, 0]
    for prov, a in per_prov.items():
        sid = f"oda:{prov}"
        measures += [
            m(sid, "rows", a[0], method="ODA_ON_v1.csv rows by provider", text=f"downloaded {down.get(prov, '')}"),
            m(sid, "unit_fill", a[1], a[0], method="unit non-empty"),
            m(sid, "street_fill", a[2], a[0], method="str_name non-empty"),
            m(sid, "number_fill", a[3], a[0], method="street_no non-empty"),
            m(sid, "postcode_fill", a[4], a[0], method="postal_code non-empty"),
            m(sid, "last_success", down.get(prov, ""), method="Data_Sources.csv Date Downloaded"),
        ]
        tot = [x + y for x, y in zip(tot, a)]
    measures += [
        m("oda", "rows", tot[0], method="all Ontario providers", text="v1, collected Jan-Apr 2021"),
        m("oda", "unit_fill", tot[1], tot[0]), m("oda", "street_fill", tot[2], tot[0]),
        m("oda", "number_fill", tot[3], tot[0]), m("oda", "postcode_fill", tot[4], tot[0]),
        m("oda", "providers", len(per_prov), unit="providers"),
        m("oda", "last_success", max(down.values()) if down else "", method="latest provider download date"),
    ]
    append_measures(measures)
    write_coverage("oda", cov, "2021-v1")
    if unmatched:
        print(f"  {len(unmatched)} ODA municipal csdnames resolve to no polygon ({sum(unmatched.values())} rows): "
              + ", ".join(f"{k} ({v})" for k, v in unmatched.most_common(8)))


# --------------------------------------------------------------------------- nar
NAR_DATA = os.path.join(ROOT, "prototype-nar", "data")


def _nar_counts(vintage):
    """Per-CSD rows and distinct locations. NAR rows are unit-level (one per
    apartment where known); LOC_GUID counts entrances/buildings, which is what
    a municipal address-point layer usually holds, so that is the comparable number."""
    out = os.path.join(CACHE, f"nar_{vintage}_csd.csv")
    if os.path.exists(out):
        return out
    files = sorted(glob.glob(os.path.join(NAR_DATA, vintage, "Address_35_part_*.csv")))
    if not files:
        return None
    import duckdb
    print(f"  counting NAR {vintage} ({len(files)} files)")
    pattern = os.path.join(NAR_DATA, vintage, "Address_35_part_*.csv").replace(os.sep, "/")
    con = duckdb.connect()
    con.execute(f"""
        copy (
          select trim(CSD_ENG_NAME) as csd_name, trim(CSD_TYPE_ENG_CODE) as csd_type,
                 count(*) as rows, count(distinct LOC_GUID) as locations,
                 count(nullif(trim(APT_NO_LABEL), '')) as unit_filled,
                 count(nullif(trim(CIVIC_NO), '')) as number_filled,
                 count(nullif(trim(OFFICIAL_STREET_NAME), '')) as street_filled,
                 count(nullif(trim(MAIL_POSTAL_CODE), '')) as postcode_filled
          from read_csv('{pattern}', header=true, all_varchar=true, union_by_name=true)
          group by all order by all
        ) to '{out.replace(os.sep, "/")}' (header, delimiter ',')
    """)
    return out


def cmd_nar(args):
    print("nar: StatCan National Address Register vintages")
    munis = Municipalities()
    vintages = sorted({os.path.basename(p)[4:10] for p in glob.glob(os.path.join(CACHE, "nar_*_csd.csv"))}
                      | {os.path.basename(p) for p in glob.glob(os.path.join(NAR_DATA, "2*")) if os.path.isdir(p)})
    if not vintages:
        print("  no NAR vintages under prototype-nar/data or cache; skipping")
        return
    measures = []
    for v in vintages:
        path = _nar_counts(v)
        if not path:
            continue
        cov, tot, unmatched, outside = [], [0, 0, 0, 0, 0, 0], Counter(), 0
        for r in _read_csv(path):
            key = munis.resolve(r["csd_name"], r["csd_type"])
            if key is None and r["csd_name"]:
                if r["csd_type"] in CSD_TYPES_OUTSIDE:
                    outside += int(r["rows"])
                else:
                    unmatched[f"{r['csd_name']} ({r['csd_type']})"] += int(r["rows"])
            cov.append(cov_row(key, "nar", v, f"nar {r['csd_type']}", int(r["rows"]), int(r["unit_filled"]),
                               int(r["street_filled"]), int(r["number_filled"]), int(r["postcode_filled"]),
                               locations=int(r["locations"])))
            for i, c in enumerate(("rows", "unit_filled", "street_filled", "number_filled", "postcode_filled", "locations")):
                tot[i] += int(r[c])
        rel = f"{v[:4]}-{v[4:6]}"
        sid = f"nar:{v}"
        measures += [
            m(sid, "rows", tot[0], method="Address_35 rows (unit-level)", text=f"vintage {rel}"),
            m(sid, "locations", tot[5], method="distinct LOC_GUID (building/entrance level)"),
            m(sid, "unit_fill", tot[1], tot[0], method="APT_NO_LABEL non-empty"),
            m(sid, "street_fill", tot[2], tot[0], method="OFFICIAL_STREET_NAME non-empty"),
            m(sid, "number_fill", tot[3], tot[0], method="CIVIC_NO non-empty"),
            m(sid, "postcode_fill", tot[4], tot[0], method="MAIL_POSTAL_CODE non-empty"),
            m(sid, "last_success", f"{rel}-01", method="vintage month"),
            m(sid, "outside_rows", outside, tot[0], method="rows in reserves, settlements and unorganized territory (no polygon by design)"),
            m(sid, "unbinned_rows", sum(unmatched.values()), tot[0], method="municipal CSD names that resolve to no polygon; fix in muni_aliases.csv"),
        ]
        write_coverage("nar", cov, v)
        print(f"  {v}: {tot[0]} rows / {tot[5]} locations; {outside} rows outside municipalities by design; "
              f"{sum(unmatched.values())} rows in {len(unmatched)} unresolved municipal names"
              + (": " + ", ".join(k for k, _ in unmatched.most_common(8)) if unmatched else ""))
    measures.append(m("nar", "vintages", len(vintages), unit="releases", text=", ".join(vintages)))
    append_measures(measures)


# ---------------------------------------------------------------------- overture
OVT_BUCKET = "https://overturemaps-us-west-2.s3.amazonaws.com/"
ON_BBOX = (-95.2, 41.6, -74.3, 56.9)


def _overture_releases():
    import xml.etree.ElementTree as ET
    with urllib.request.urlopen(OVT_BUCKET + "?list-type=2&prefix=release/&delimiter=/", timeout=60) as r:
        tree = ET.fromstring(r.read())
    ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    rels = [p.text.split("/")[1] for p in tree.findall(".//s3:CommonPrefixes/s3:Prefix", ns)]
    return sorted(x for x in rels if re.match(r"^\d{4}-\d{2}-\d{2}\.\d+$", x))


def _overture_points(release):
    out = os.path.join(CACHE, f"overture_{release}_on_points.parquet")
    if os.path.exists(out):
        return out
    import duckdb
    print(f"  extracting Overture {release} Ontario points (S3, bbox pushdown)")
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2'; "
                "SET s3_access_key_id=''; SET s3_secret_access_key='';")
    x0, y0, x1, y1 = ON_BBOX
    con.execute(f"""
        copy (
          select bbox.xmin as lon, bbox.ymin as lat, address_levels[2].value as muni,
                 unit is not null as has_unit, street is not null as has_street,
                 number is not null as has_number, postcode is not null as has_postcode,
                 sources[1].dataset as dataset, sources[1].update_time as src_update_time
          from read_parquet('s3://overturemaps-us-west-2/release/{release}/theme=addresses/type=address/*.parquet',
                            hive_partitioning=0)
          where country='CA' and address_levels[1].value = 'ON'
            and bbox.xmin > {x0} and bbox.xmax < {x1} and bbox.ymin > {y0} and bbox.ymax < {y1}
        ) to '{out.replace(os.sep, '/')}' (format parquet, compression zstd)
    """)
    return out


def cmd_overture(args):
    print("overture: addresses theme, Ontario bbox")
    import pyarrow.parquet as pq
    releases = _overture_releases()
    release = args.release or (releases[-1] if releases else None)
    if not release:
        print("  no release found")
        return
    path = _overture_points(release)
    t = pq.read_table(path)
    munis = Municipalities()
    names = munis.assign(t.column("lon").to_numpy(), t.column("lat").to_numpy())
    cols = {c: t.column(c).to_pylist() for c in ("has_unit", "has_street", "has_number", "has_postcode", "dataset")}
    agg = defaultdict(lambda: [0, 0, 0, 0, 0])
    for i, nm in enumerate(names):
        a = agg[(nm, cols["dataset"][i])]
        a[0] += 1
        a[1] += bool(cols["has_unit"][i])
        a[2] += bool(cols["has_street"][i])
        a[3] += bool(cols["has_number"][i])
        a[4] += bool(cols["has_postcode"][i])
    cov = [cov_row(nm, "overture", release, ds, *a) for (nm, ds), a in agg.items()]
    tot = [sum(a[i] for a in agg.values()) for i in range(5)]
    outside = sum(a[0] for (nm, _), a in agg.items() if nm is None)
    upd = max((x for x in t.column("src_update_time").to_pylist() if x), default=None)
    sid = f"overture:{release}"
    measures = [
        m(sid, "rows", tot[0], method="points with address_levels[1]=ON in the Ontario bbox (unit-level, NAR-derived)", text=f"release {release}"),
        m(sid, "unit_fill", tot[1], tot[0]), m(sid, "street_fill", tot[2], tot[0]),
        m(sid, "number_fill", tot[3], tot[0]), m(sid, "postcode_fill", tot[4], tot[0]),
        m(sid, "unbinned_rows", outside, tot[0], method="points outside every municipality polygon"),
        m(sid, "last_success", release[:10], method="release date"),
        m(sid, "source_update_time", str(upd)[:10] if upd else "", method="max sources[1].update_time"),
        m("overture", "releases", len(releases), unit="releases", text=", ".join(releases[-6:])),
    ]
    append_measures(measures)
    write_coverage("overture", cov, release)
    print(f"  {release}: {tot[0]} rows, {outside} outside any municipality; source update {str(upd)[:10]}")


# -------------------------------------------------------------------------- main
def cmd_render(args):
    import render
    render.main()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("steps", nargs="+", choices=["all", "ours", "oa", "oda", "nar", "overture", "render"])
    ap.add_argument("--offline", action="store_true", help="use cached OpenAddresses pulls")
    ap.add_argument("--release", help="Overture release id (default: latest on S3)")
    args = ap.parse_args()
    steps = ["ours", "oa", "oda", "nar", "overture", "render"] if "all" in args.steps else args.steps
    fns = {"ours": cmd_ours, "oa": cmd_oa, "oda": cmd_oda, "nar": cmd_nar, "overture": cmd_overture, "render": cmd_render}
    for s in steps:
        fns[s](args)


if __name__ == "__main__":
    main()
