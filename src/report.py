"""Render the static HTML site: per-city dated reports, per-city index, and a
cross-city landing page (docs/index.html) for GitHub Pages.

Layout:
    docs/index.html              cross-city landing
    docs/<slug>/index.html       per-city report list
    docs/<slug>/report-<date>.html
"""

import glob
import json
import math
import os
import tomllib
from collections import Counter
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from src import diff

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
SKIPPED_PATH = os.path.join(ROOT_DIR, "skipped.toml")

MAX_RENDER = 1000          # cap rows rendered per table (true counts still shown)
SPARK_KEYS = ("added", "removed", "modified", "modified_location",
              "renumbered", "renamed")

_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)


def _friendly_date(d):
    try:
        return datetime.strptime(d[:10], "%Y-%m-%d").strftime("%A, %b %d, %Y")
    except (ValueError, TypeError):
        return d


def _addr(r):
    if r.get("full"):
        return r["full"]
    parts = " ".join(p for p in (r.get("number"), r.get("street")) if p).strip()
    return parts or r.get("identity_key", "")


def _bearing_arrow(dx, dy):
    if dx == 0 and dy == 0:
        return ""
    angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
    return ["→", "↗", "↑", "↖", "←", "↙", "↓", "↘"][int((angle + 22.5) // 45) % 8]


def _combine_location(m):
    """Fold latitude/longitude changes into one 'location' change with arrow+distance."""
    changes = m["changes"]
    lat_c = next((c for c in changes if c["field"] == "latitude"), None)
    lon_c = next((c for c in changes if c["field"] == "longitude"), None)
    if not (lat_c or lon_c):
        return
    new_lat, new_lon = m.get("latitude"), m.get("longitude")
    old_lat = lat_c["old"] if lat_c else new_lat
    old_lon = lon_c["old"] if lon_c else new_lon

    arrow = ""
    if None not in (old_lat, old_lon, new_lat, new_lon):
        mid = math.radians((old_lat + new_lat) / 2)
        dy = new_lat - old_lat
        dx = (new_lon - old_lon) * math.cos(mid)
        if abs(dy) > 1e-6 or abs(dx) > 1e-6:
            dy_m = dy * 111_320
            dx_m = (new_lon - old_lon) * 111_320 * math.cos(mid)
            arrow = f"{_bearing_arrow(dx, dy)} {math.hypot(dx_m, dy_m):.1f}m"

    def fmt(lat, lon):
        return "—" if lat is None or lon is None else f"{lat:.5f}, {lon:.5f}"

    changes = [c for c in changes if c["field"] not in ("latitude", "longitude")]
    changes.append({"field": "location", "display_field": "Location",
                    "old": fmt(old_lat, old_lon), "new": fmt(new_lat, new_lon), "arrow": arrow,
                    "old_pt": None if None in (old_lat, old_lon) else (old_lat, old_lon),
                    "new_pt": None if None in (new_lat, new_lon) else (new_lat, new_lon)})
    m["changes"] = changes


def _stats(d):
    street_added, street_removed, field_changes = Counter(), Counter(), Counter()
    for r in d["added"]:
        if r.get("street"):
            street_added[r["street"]] += 1
    for r in d["removed"]:
        if r.get("street"):
            street_removed[r["street"]] += 1
    for m in d["modified"]:
        for ch in m["changes"]:
            field_changes[ch.get("display_field") or ch["field"]] += 1
    MIN = 3

    def top(counter, min_count=1):
        # count desc, then name A-Z so ties are deterministic across runs
        items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
        return {k: v for k, v in items if v >= min_count}

    return {
        "top_streets_added": top(street_added, MIN),
        "top_streets_removed": top(street_removed, MIN),
        "field_changes": top(field_changes),
    }


def _sparkline_svg(values, color, width=110, height=20, pad=2):
    if not values:
        return ""
    n = len(values)
    vmax = max(values) or 1
    iw, ih = width - 2 * pad, height - 2 * pad
    xs = [pad + iw] if n == 1 else [pad + i * iw / (n - 1) for i in range(n)]
    ys = [pad + ih - (v / vmax) * ih for v in values]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return (f'<svg class="sparkline" viewBox="0 0 {width} {height}" width="{width}" '
            f'height="{height}" preserveAspectRatio="none" aria-hidden="true">'
            f'<polyline fill="none" stroke="{color}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" points="{pts}"/>'
            f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="2" fill="{color}"/></svg>')


_env.globals["sparkline_svg"] = _sparkline_svg


def _category(m):
    """Classify a modified row by its changed-field set.

    Works both before and after _combine_location (raw latitude/longitude or the
    combined 'location' pseudo-field). 'full' is derived from number+street, so it
    rides along with either; number takes precedence (matches the sibling Toronto
    tracker's renumbered category).
    """
    fields = {c["field"] for c in m["changes"]}
    if fields <= {"latitude", "longitude", "location"}:
        return "location"
    if fields <= {"number", "full"}:
        return "renumbered"
    if fields <= {"street", "full"}:
        return "renamed"
    return "significant"


def _group_renames(renamed):
    """Group street renames by (old, new) street: one upstream rename event covers
    every address on the street, so present it once with a count."""
    groups = {}
    for m in renamed:
        ch = next(c for c in m["changes"] if c["field"] == "street")
        groups.setdefault((ch["old"] or "—", ch["new"] or "—"), []).append(m)
    out = [{"old": o, "new": n, "count": len(rows), "rows": rows[:MAX_RENDER]}
           for (o, n), rows in groups.items()]
    out.sort(key=lambda g: (-g["count"], g["old"]))
    return out


def _prepare(ds, d, new_id):
    """Cap rows, attach addr + history, split modifications into categories."""
    for r in d["added"] + d["removed"]:
        r["addr"] = _addr(r)
    for m in d["modified"]:
        m["addr"] = _addr(m)
        _combine_location(m)

    cats = {"significant": [], "location": [], "renumbered": [], "renamed": []}
    for m in d["modified"]:
        cats[_category(m)].append(m)

    counts = {"added": len(d["added"]), "removed": len(d["removed"]),
              "modified": len(cats["significant"]),
              "modified_location": len(cats["location"]),
              "renumbered": len(cats["renumbered"]),
              "renamed": len(cats["renamed"])}

    added = d["added"][:MAX_RENDER]
    removed = d["removed"][:MAX_RENDER]
    modified = cats["significant"][:MAX_RENDER]
    location_only = cats["location"][:MAX_RENDER]
    renumbered = cats["renumbered"][:MAX_RENDER]
    renamed_groups = _group_renames(cats["renamed"])

    # history only for the rows we actually render
    keys = [r["identity_key"] for r in added + removed]
    hist = diff.compute_histories(ds, keys, new_id)
    for r in added + removed:
        r["history"] = hist.get(r["identity_key"], [])

    return added, removed, modified, location_only, renumbered, renamed_groups, counts


_CANON_LABEL = {"number": "Street number", "street": "Street name",
                "unit": "Unit", "full": "Full address"}


def _compared_fields(ds, prop_keys):
    """Exact list of the fields change detection compares, for the info popup.

    Canonical mapped fields first (labelled, with source name), then every
    remaining source prop key seen in the latest snapshot, minus ignored.
    """
    out = [f"{_CANON_LABEL[k]} ({src})"
           for k in ("number", "street", "unit", "full") if (src := ds.fields.get(k))]
    out.append("Coordinates (latitude, longitude)")
    seen = {src.lower() for src in ds.fields.values() if src}
    seen |= {f.lower() for f in ds.ignore_fields}
    seen |= diff.EDIT_METADATA_FIELDS
    out += [k for k in prop_keys if k.lower() not in seen]
    return out


def _render_report(ds, snap, d, is_baseline, spark, source_url, compared, ignored):
    new_id = snap["id"]
    added, removed, modified, location_only, renumbered, renamed_groups, counts = \
        _prepare(ds, d, new_id)
    date = diff.snap_date(snap)
    ctx = {
        "compared_fields": compared, "ignored_fields": ignored,
        "provider": ds.provider, "license_name": ds.license_name,
        "generated": datetime.now().strftime("%b %d, %Y at %I:%M %p"),
        "new_snapshot": snap, "new_date_friendly": _friendly_date(date),
        "old_date_friendly": "", "is_baseline": is_baseline,
        "added": added, "removed": removed, "modified": modified,
        "modified_location": location_only,
        "renumbered": renumbered, "renamed_groups": renamed_groups,
        "added_count": counts["added"], "removed_count": counts["removed"],
        "modified_count": counts["modified"], "modified_location_count": counts["modified_location"],
        "renumbered_count": counts["renumbered"], "renamed_count": counts["renamed"],
        "stats": _stats(d), "sparklines": spark, "source_url": source_url,
    }
    html = _env.get_template("report.html").render(**ctx)
    out = os.path.join(DOCS_DIR, ds.slug, f"report-{date}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return counts


def _spark_series(history, idx):
    """Trailing 7 values for each key ending at report index idx."""
    lo = max(0, idx - 6)
    return {k: [history[k][j] for j in range(lo, idx + 1)] for k in SPARK_KEYS}


def generate_all(datasets):
    os.makedirs(DOCS_DIR, exist_ok=True)
    open(os.path.join(DOCS_DIR, ".nojekyll"), "w").close()
    cities = []

    for ds in datasets:
        snaps = diff.nonskipped(ds)
        if not snaps:
            continue
        os.makedirs(os.path.join(DOCS_DIR, ds.slug), exist_ok=True)
        source_url = _source_url(ds)

        # chronological diffs: baseline first, then each consecutive pair
        diffs = [(snaps[0], diff.compute_baseline(ds, snaps[0]["id"]), True)]
        for i in range(len(snaps) - 1):
            diffs.append((snaps[i + 1],
                          diff.compute_diff(ds, snaps[i]["id"], snaps[i + 1]["id"]), False))

        new_by_snap = diff.new_streets_by_snapshot(ds)
        pkeys = diff.prop_keys(ds, snaps[-1]["id"])
        compared = _compared_fields(ds, pkeys)
        ignored = sorted(set(ds.ignore_fields) |
                         {k for k in pkeys if k.lower() in diff.EDIT_METADATA_FIELDS})

        series = {k: [] for k in SPARK_KEYS}  # filled as we render, for sparklines
        meta = []
        for idx, (snap, d, is_base) in enumerate(diffs):
            cat = Counter(_category(m) for m in d["modified"])
            series["added"].append(len(d["added"]))
            series["removed"].append(len(d["removed"]))
            series["modified"].append(cat["significant"])
            series["modified_location"].append(cat["location"])
            series["renumbered"].append(cat["renumbered"])
            series["renamed"].append(cat["renamed"])

        for idx, (snap, d, is_base) in enumerate(diffs):
            counts = _render_report(ds, snap, d, is_base, _spark_series(series, idx), source_url,
                                    compared, ignored)
            date = diff.snap_date(snap)
            meta.append({
                "date": date, "friendly_date": _friendly_date(date),
                "filename": f"report-{date}.html", "is_baseline": is_base,
                "added": counts["added"], "removed": counts["removed"],
                "modified": counts["modified"] + counts["modified_location"]
                            + counts["renumbered"] + counts["renamed"],
                "new_streets": new_by_snap.get(snap["id"], []),
            })

        meta.reverse()                       # newest first
        if meta:
            meta[0]["is_latest"] = not meta[0]["is_baseline"]

        # flatten new-street debuts across reports, newest first, cap at 15
        recent_new_streets = [
            {"street": s["street"], "count": s["count"],
             "filename": m["filename"], "friendly_date": m["friendly_date"]}
            for m in meta for s in m["new_streets"]
        ][:15]

        with open(os.path.join(DOCS_DIR, ds.slug, "index.html"), "w", encoding="utf-8") as f:
            f.write(_env.get_template("city_index.html").render(
                provider=ds.provider, license_name=ds.license_name,
                source_url=source_url, reports=meta,
                recent_new_streets=recent_new_streets,
                compared_fields=compared, ignored_fields=ignored))

        latest = meta[0]
        card = {
            "slug": ds.slug, "provider": ds.provider, "license_name": ds.license_name,
            "row_count": snaps[-1]["row_count"], "last_date": diff.snap_date(snaps[-1]),
            "added": latest["added"], "removed": latest["removed"], "modified": latest["modified"],
            "has_changes": not latest["is_baseline"], "report_count": len(meta),
            "compared_fields": compared, "ignored_fields": ignored,
        }
        cities.append(card)
        # Persist the landing card so a single-city update still leaves the
        # cross-city landing complete (it's rebuilt from every city's card below).
        with open(os.path.join(DOCS_DIR, ds.slug, "_card.json"), "w", encoding="utf-8") as f:
            json.dump(card, f)

    # Landing lists every city that has a persisted card, not just the ones
    # rendered this run, so `update --city X` doesn't clobber it to one city.
    rendered = {c["slug"] for c in cities}
    for path in glob.glob(os.path.join(DOCS_DIR, "*", "_card.json")):
        if os.path.basename(os.path.dirname(path)) not in rendered:
            with open(path, encoding="utf-8") as f:
                cities.append(json.load(f))

    cities.sort(key=lambda c: c["provider"])
    with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(_env.get_template("cities.html").render(
            cities=cities, skipped=_load_skipped(),
            generated=datetime.now().strftime("%b %d, %Y at %I:%M %p")))
    print(f"\nwrote site for {len(cities)} dataset(s) to {DOCS_DIR}")


def _load_skipped():
    """Sources probed but not added, for the landing page. Empty if no file."""
    if not os.path.exists(SKIPPED_PATH):
        return []
    with open(SKIPPED_PATH, "rb") as f:
        return tomllib.load(f).get("skipped", [])


def _source_url(ds):
    # ArcGIS layers have a browsable HTML page at their REST URL.
    return ds.data_url if ds.access == "arcgis" else ""
