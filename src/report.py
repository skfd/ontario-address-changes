"""Render per-city HTML change reports and a cross-city index for GitHub Pages."""

import html
import os
from datetime import datetime

from src import db, diff

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

_PAGE = """<!doctype html><meta charset="utf-8">
<title>{title}</title>
<style>
 body{{font:15px/1.5 system-ui,sans-serif;margin:2rem auto;max-width:60rem;padding:0 1rem;color:#222}}
 h1{{margin-bottom:.2rem}} .sub{{color:#666;margin-top:0}}
 table{{border-collapse:collapse;width:100%;margin:1rem 0}}
 th,td{{border:1px solid #ddd;padding:.4rem .6rem;text-align:left}}
 th{{background:#f5f5f5}} td.n{{text-align:right;font-variant-numeric:tabular-nums}}
 .add{{color:#137333}} .rem{{color:#a50e0e}} .mod{{color:#a56b00}}
 a{{color:#1a56db;text-decoration:none}} a:hover{{text-decoration:underline}}
</style>
{body}
<p class="sub">Generated {now}</p>
"""


def _esc(v):
    return html.escape("" if v is None else str(v))


def _sample_rows(rows, fields):
    out = []
    for r in rows[:50]:
        cells = "".join(f"<td>{_esc(r.get(f))}</td>" for f in fields)
        out.append(f"<tr>{cells}</tr>")
    return "".join(out)


def _city_body(ds, snaps, d):
    n_snaps = len(snaps)
    rows = "".join(
        f"<tr><td>{s['id']}</td><td>{_esc(s['downloaded'][:10])}</td>"
        f"<td class=n>{s['row_count']:,}</td>"
        f"<td>{'skipped' if s['skipped'] else ''}</td></tr>"
        for s in snaps[-10:])
    parts = [
        f"<p><a href='index.html'>&larr; all datasets</a></p>",
        f"<h1>{_esc(ds.provider)}</h1>",
        f"<p class=sub>{_esc(ds.license_name)} &middot; {n_snaps} snapshot(s)</p>",
        "<h2>Snapshots</h2>",
        "<table><tr><th>id</th><th>date</th><th>rows</th><th></th></tr>"
        + rows + "</table>",
    ]
    if d:
        parts.append("<h2>Latest changes</h2>")
        parts.append(
            f"<p><span class=add>+{len(d['added']):,} added</span> &middot; "
            f"<span class=rem>-{len(d['removed']):,} removed</span> &middot; "
            f"<span class=mod>~{len(d['modified']):,} modified</span></p>")
        if d["added"]:
            parts.append("<h3 class=add>Added (sample)</h3>")
            parts.append("<table><tr><th>full</th><th>street</th><th>lon</th><th>lat</th></tr>"
                         + _sample_rows(d["added"], ["full", "street", "longitude", "latitude"])
                         + "</table>")
        if d["removed"]:
            parts.append("<h3 class=rem>Removed (sample)</h3>")
            parts.append("<table><tr><th>full</th><th>street</th><th>lon</th><th>lat</th></tr>"
                         + _sample_rows(d["removed"], ["full", "street", "longitude", "latitude"])
                         + "</table>")
    else:
        parts.append("<p class=sub>Need a second snapshot to show changes.</p>")
    return "\n".join(parts)


def _write(path, title, body):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_PAGE.format(title=_esc(title), body=body,
                             now=datetime.now().strftime("%Y-%m-%d %H:%M")))


def generate_all(datasets):
    index_rows = []
    for ds in datasets:
        snaps = db.get_snapshots(ds)
        if not snaps:
            continue
        d = diff.report_latest_silent(ds)
        _write(os.path.join(REPORTS_DIR, f"{ds.slug}.html"),
               f"{ds.provider} — address changes", _city_body(ds, snaps, d))

        active = [s for s in snaps if not s["skipped"]]
        last = active[-1] if active else snaps[-1]
        delta = ("" if not d else
                 f"<span class=add>+{len(d['added']):,}</span> / "
                 f"<span class=rem>-{len(d['removed']):,}</span> / "
                 f"<span class=mod>~{len(d['modified']):,}</span>")
        index_rows.append(
            f"<tr><td><a href='{ds.slug}.html'>{_esc(ds.provider)}</a></td>"
            f"<td>{_esc(ds.license_name)}</td>"
            f"<td>{_esc(last['downloaded'][:10])}</td>"
            f"<td class=n>{last['row_count']:,}</td>"
            f"<td>{delta}</td></tr>")

    body = ("<h1>Ontario address change tracker</h1>"
            "<p class=sub>Open civic-address datasets tracked for additions, "
            "removals, and modifications over time.</p>"
            "<table><tr><th>dataset</th><th>licence</th><th>last snapshot</th>"
            "<th>rows</th><th>latest change (+/-/~)</th></tr>"
            + "".join(index_rows) + "</table>")
    _write(os.path.join(REPORTS_DIR, "index.html"),
           "Ontario address change tracker", body)
    print(f"\nwrote {len(index_rows) + 1} report file(s) to {REPORTS_DIR}")
