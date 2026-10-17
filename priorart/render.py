"""Render priorart/report.html from the CSVs. Back-office: not linked from docs/."""
from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict
from datetime import date

from jinja2 import Environment, FileSystemLoader

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from muni import Municipalities  # noqa: E402

OUT = os.path.join(HERE, "report.html")


def _read(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return []
    with open(p, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _pct(a, b):
    a, b = _num(a), _num(b)
    return None if not b or a is None else 100.0 * a / b


def latest_measures(rows):
    """{source_id: {measure: row}} keeping the newest measured_on per measure."""
    out = defaultdict(dict)
    for r in sorted(rows, key=lambda r: r["measured_on"]):
        out[r["source_id"]][r["measure"]] = r
    return out


def main():
    measures = _read("measures.csv")
    coverage = _read("coverage.csv")
    licences = _read("licences.csv")
    comparators = _read("comparators.csv")
    oa_join = _read("oa_sources.csv")
    lm = latest_measures(measures)
    munis = Municipalities()

    # ---- vintages per comparator -------------------------------------------------
    vintages = defaultdict(set)
    for r in coverage:
        vintages[r["comparator"]].add(r["vintage"])
    nar_v = sorted(vintages.get("nar", []))
    ovt_v = sorted(vintages.get("overture", []))
    latest_nar = nar_v[-1] if nar_v else None
    latest_ovt = ovt_v[-1] if ovt_v else None

    # ---- coverage matrix: municipality x comparator ---------------------------------
    # ours: max over datasets (overlapping datasets must not be summed); others: sum.
    cell = defaultdict(lambda: defaultdict(lambda: {"rows": 0, "locations": 0, "unit": 0, "sources": {}}))
    for r in coverage:
        key = r["municipality"] or "(outside any municipality)"
        comp, vin = r["comparator"], r["vintage"]
        if comp == "nar" and vin != latest_nar:
            continue
        if comp == "overture" and vin != latest_ovt:
            continue
        c = cell[key][comp]
        n, u = int(r["rows"]), int(r["unit_filled"])
        loc = int(r["locations"]) if r.get("locations") else 0
        if comp == "ours":
            if n > c["rows"]:
                c["rows"], c["unit"] = n, u
        else:
            c["rows"] += n
            c["unit"] += u
            c["locations"] += loc
        c["sources"][r["source"]] = c["sources"].get(r["source"], 0) + n

    def main_sources(d):
        """Sources holding at least 2% of the largest one; border spillover stays out."""
        if not d:
            return ""
        top = max(d.values())
        return ", ".join(s for s, n in sorted(d.items(), key=lambda kv: -kv[1]) if n >= 0.02 * top)

    table = []
    for mrow in munis.table():
        name = mrow["municipality"]
        cc = cell.get(name, {})
        ours = cc.get("ours", {}).get("rows", 0)
        nar = cc.get("nar", {}).get("rows", 0)
        nar_loc = cc.get("nar", {}).get("locations", 0)
        table.append({
            "municipality": name, "official": mrow["official_name"], "upper_tier": mrow["upper_tier"],
            "type": (mrow["type"] or "").replace(" Municipality", ""),
            "ours": ours, "ours_sources": main_sources(cc.get("ours", {}).get("sources", {})),
            "nar": nar, "nar_loc": nar_loc, "oda": cc.get("oda", {}).get("rows", 0),
            "oda_sources": main_sources(cc.get("oda", {}).get("sources", {})),
            "overture": cc.get("overture", {}).get("rows", 0),
            "ratio": _pct(ours, nar_loc), "gap": ours == 0 and nar > 0,
            "collision": mrow["name_collision"],
        })
    table.sort(key=lambda r: -r["nar"])
    extra = sorted(k for k in cell if k not in munis.info)  # names only comparators produced
    extra_rows = [{"municipality": k, **{c: cell[k].get(c, {}).get("rows", 0) for c in ("ours", "nar", "oda", "overture")}}
                  for k in extra]

    tot = {c: 0 for c in ("ours", "nar", "nar_loc", "oda", "overture")}
    covered = {c: 0 for c in tot}
    for r in table:
        for c in tot:
            tot[c] += r[c]
            covered[c] += r[c] > 0
    gaps = [r for r in table if r["gap"]]
    gap_rows = sum(r["nar"] for r in gaps)
    nar_total_binned = sum(r["nar"] for r in table)

    # ---- comparator summary ----------------------------------------------------------
    def latest_sid(prefix):
        ids = [s for s in lm if s == prefix or s.startswith(prefix + ":")]
        ids = [s for s in ids if "rows" in lm[s]]
        if not ids:
            return None
        if prefix in ("nar", "overture"):
            return sorted(ids)[-1]
        return prefix
    summary = []
    for c in comparators:
        cid = c["id"]
        sid = latest_sid(cid) if cid != "ours" and cid != "oa" else None
        row = dict(c)
        if cid == "ours":
            ours_ids = [s for s in lm if s.startswith("ours:")]
            row["rows"] = sum(_num(lm[s]["rows"]["value"]) or 0 for s in ours_ids)
            row["sources"] = len(ours_ids)
            row["last"] = max((lm[s]["last_snapshot"]["value"] for s in ours_ids if "last_snapshot" in lm[s]), default="")
            s30 = [_num(lm[s]["snapshots_30d"]["value"]) for s in ours_ids if "snapshots_30d" in lm[s]]
            row["cadence_measured"] = f"median {sorted(s30)[len(s30) // 2]:.0f} snapshots / 30 d" if s30 else ""
            u = sum(_num(lm[s]["unit_fill"]["value"]) or 0 for s in ours_ids)
            row["unit_pct"] = _pct(u, row["rows"])
        elif cid == "oa":
            oa_ids = [s for s in lm if s.startswith("oa:")]
            row["rows"] = sum(_num(lm[s]["rows"]["value"]) or 0 for s in oa_ids)
            row["sources"] = len(oa_ids)
            stale = {s: _num(lm[s].get("days_stale", {}).get("value")) for s in oa_ids}
            live = [s for s, d in stale.items() if d is not None and d <= 14]
            row["last"] = max((lm[s]["last_success"]["value"] for s in oa_ids if "last_success" in lm[s]), default="")
            row["cadence_measured"] = f"{len(live)} of {len(oa_ids)} sources ran in the last 14 d"
            u = sum(_num(lm[s]["unit_fill"]["value"]) or 0 for s in oa_ids if "unit_fill" in lm[s])
            row["unit_pct"] = _pct(u, row["rows"])
        elif sid:
            row["rows"] = _num(lm[sid]["rows"]["value"])
            row["last"] = lm[sid].get("last_success", {}).get("value", "")
            row["unit_pct"] = _pct(lm[sid].get("unit_fill", {}).get("value"), lm[sid]["rows"]["value"])
            if cid == "nar":
                row["cadence_measured"] = lm.get("nar", {}).get("vintages", {}).get("text", "")
                row["sources"] = len(nar_v)
            elif cid == "overture":
                row["cadence_measured"] = "releases " + lm.get("overture", {}).get("releases", {}).get("text", "")
                row["sources"] = 1
            elif cid == "oda":
                row["cadence_measured"] = "one release"
                row["sources"] = _num(lm["oda"].get("providers", {}).get("value"))
        summary.append(row)

    # ---- quality: fill rates per comparator ----------------------------------------
    quality = []
    for cid, sid in (("ours", None), ("oa", None), ("oda", "oda"), ("nar", latest_sid("nar")), ("overture", latest_sid("overture"))):
        if cid in ("ours", "oa"):
            ids = [s for s in lm if s.startswith(cid + ":") and "rows" in lm[s]]
            n = sum(_num(lm[s]["rows"]["value"]) or 0 for s in ids)
            def tot_of(meas):
                return sum(_num(lm[s][meas]["value"]) or 0 for s in ids if meas in lm[s])
            quality.append({"comparator": cid, "rows": n, "unit": _pct(tot_of("unit_fill"), n),
                            "street": _pct(tot_of("street_fill"), n), "number": _pct(tot_of("number_fill"), n),
                            "postcode": _pct(tot_of("postcode_fill"), n) if cid == "oa" else None})
        elif sid:
            n = _num(lm[sid]["rows"]["value"])
            quality.append({"comparator": sid, "rows": n,
                            **{k: _pct(lm[sid].get(f"{k}_fill", {}).get("value"), n) for k in ("unit", "street", "number", "postcode")}})

    # ---- OpenAddresses per source vs ours --------------------------------------------
    ours_by_slug = {s.split(":", 1)[1]: lm[s] for s in lm if s.startswith("ours:")}
    oa_rows = []
    for j in oa_join:
        sid = f"oa:{j['oa_source']}"
        mm = lm.get(sid, {})
        slug = (j["our_slug"] or "").split(";")[0]
        o = ours_by_slug.get(slug, {})
        oa_n = _num(mm.get("rows", {}).get("value"))
        ours_n = _num(o.get("rows", {}).get("value"))
        oa_rows.append({
            **j, "oa_rows": oa_n, "ours_rows": ours_n,
            "ratio": _pct(oa_n, ours_n) if j["match"] in ("same-url", "jurisdiction") else None,
            "last_success": mm.get("last_success", {}).get("value", ""),
            "days_stale": _num(mm.get("days_stale", {}).get("value")),
            "runs_365d": _num(mm.get("runs_365d", {}).get("value")),
            "oa_unit": _pct(mm.get("unit_fill", {}).get("value"), oa_n),
            "ours_unit": _pct(o.get("unit_fill", {}).get("value"), ours_n),
            "oa_street": _pct(mm.get("street_fill", {}).get("value"), oa_n),
            "ours_street": _pct(o.get("street_fill", {}).get("value"), ours_n),
            "ours_last": o.get("last_snapshot", {}).get("value", ""),
        })
    oa_rows.sort(key=lambda r: (r["match"] != "none", -(r["days_stale"] or 0)))
    oa_dead = [r for r in oa_rows if (r["days_stale"] or 0) > 60]
    ours_only = sorted(s for s in ours_by_slug if not any(s in (j["our_slug"] or "").split(";") for j in oa_join))

    # ---- licences ----------------------------------------------------------------
    lic_rows = []
    for r in licences:
        flag = ""
        if r["oa_sources"] and not r["oa_licence"]:
            flag = "OA records no licence"
        elif r["oa_licence"] and r["our_licence"] and r["oa_licence"][:25].lower() not in r["our_licence"].lower() \
                and r["our_licence"][:25].lower() not in r["oa_licence"].lower():
            flag = "wording differs"
        if r["oda_licence"] and r["our_licence"] and r["oda_licence"][:20].lower() not in r["our_licence"].lower():
            flag = (flag + "; " if flag else "") + "ODA title differs"
        lic_rows.append({**r, "flag": flag})

    env = Environment(loader=FileSystemLoader(os.path.join(HERE, "templates")), autoescape=True)
    env.filters["pct"] = lambda v, d=0: "" if v is None else f"{v:.{d}f}%"
    env.filters["num"] = lambda v: "" if v in (None, "") else f"{int(round(float(v))):,}"
    html = env.get_template("report.html").render(
        today=date.today().isoformat(), summary=summary, quality=quality,
        table=table, extra_rows=extra_rows, tot=tot, covered=covered, n_munis=len(table),
        gaps=gaps, gap_rows=gap_rows, nar_total_binned=nar_total_binned,
        latest_nar=latest_nar, latest_ovt=latest_ovt, nar_v=nar_v,
        oa_rows=oa_rows, oa_dead=oa_dead, ours_only=ours_only, licences=lic_rows,
        n_measures=len(measures), first_measured=min((r["measured_on"] for r in measures), default=""),
    )
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"  wrote {OUT}")


if __name__ == "__main__":
    main()
