"""Render articles/ (Markdown) to docs/articles/ (HTML) for GitHub Pages.

    docs/articles/index.html              every city, newest month first
    docs/articles/<slug>-<month>.html     the article

Only the article (articles/researched/) is rendered. The research notes are
working material with unverified SNIPPET items, so the index links to them on
GitHub instead, where the Markdown already renders.

Attribution travels inside each article (its own licence line, step 8 of the
skill), so the pages add no licence text of their own.

Nothing else touches docs/articles: src/report.py clears only per-city report
pages, and daily-update.ps1's `git add docs` sweeps changes here in.

Usage:  python tools/render_articles.py
"""

import glob
import html
import os
import re
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src import registry  # noqa: E402

ARTICLES = os.path.join(ROOT, "articles")
OUT = os.path.join(ROOT, "docs", "articles")
VARIANT = "researched"
REPO_BLOB = "https://github.com/skfd/ontario-address-changes/blob/main"
SITE = "https://skfd.github.io/ontario-address-changes/"

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

CSS = """
    :root { --bg:#fafafa; --surface:#ffffff; --surface2:#f5f5f5; --border:#e0e0e0;
      --text:#242424; --text-secondary:#424242; --text-dim:#616161; --accent:#0078d4;
      --accent-hover:#106ebe; --accent-bg:#eff6fc; color-scheme:light; }
    @media (prefers-color-scheme: dark) { :root { --bg:#1f1f1f; --surface:#292929; --surface2:#333333;
      --border:#525252; --text:#ffffff; --text-secondary:#d6d6d6; --text-dim:#adadad; --accent:#2899f5;
      --accent-hover:#3aa0f3; --accent-bg:#002848; color-scheme:dark; } }
    * { box-sizing:border-box; }
    body { margin:0; padding:24px 20px 64px; background:var(--bg); color:var(--text);
      font-family:'Segoe UI Variable','Segoe UI',system-ui,-apple-system,sans-serif;
      font-size:16px; line-height:1.6; -webkit-font-smoothing:antialiased; }
    main { max-width:720px; margin:0 auto; }
    a { color:var(--accent); text-decoration:none; } a:hover { text-decoration:underline; color:var(--accent-hover); }
    .crumbs { font-size:13px; color:var(--text-dim); margin-bottom:24px; }
    .crumbs a { color:var(--text-dim); } .crumbs a:hover { color:var(--accent); }
    h1 { font-size:26px; line-height:1.25; font-weight:600; margin:0 0 20px; }
    h2 { font-size:19px; font-weight:600; margin:36px 0 10px; }
    h3 { font-size:16px; font-weight:600; margin:28px 0 8px; }
    p { margin:0 0 14px; } li { margin:0 0 6px; }
    blockquote { margin:0 0 14px; padding:4px 16px; border-left:3px solid var(--border); color:var(--text-secondary); }
    table { border-collapse:collapse; width:100%; margin:0 0 18px; font-size:14px; }
    th, td { text-align:left; vertical-align:top; padding:7px 10px; border-bottom:1px solid var(--border); }
    th { color:var(--text-dim); font-weight:600; } tr:last-child td { border-bottom:none; }
    th:empty { padding:0; border:none; }
    code { font-family:Consolas,'Cascadia Mono',monospace; font-size:0.9em; background:var(--surface2); padding:1px 4px; border-radius:4px; }
    pre { background:var(--surface2); border:1px solid var(--border); border-radius:8px; padding:12px; overflow:auto; font-size:13px; }
    pre code { background:none; padding:0; }
    hr { border:none; border-top:1px solid var(--border); margin:32px 0; }
    .footer { margin-top:40px; padding-top:16px; border-top:1px solid var(--border); font-size:13px; color:var(--text-dim); }
    .city { margin-top:28px; }
    .city h2 { margin:0 0 10px; font-size:17px; }
    .city h2 a { color:var(--text); } .city h2 a:hover { color:var(--accent); }
    .city h2 small { font-weight:400; color:var(--text-dim); font-size:13px; margin-left:8px; }
    .months { display:flex; flex-direction:column; gap:8px; }
    .month { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:12px 16px; }
    .month .when { font-size:12px; font-weight:600; color:var(--text-dim); margin-bottom:4px; }
    .month .lead { margin:0; font-size:15px; }
    .month .notes { font-size:12px; color:var(--text-dim); margin-top:6px; }
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{css}</style>
  <script data-goatcounter="https://osm-ontario.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""


def month_label(month):
    y, m = month.split("-")
    return f"{MONTHS[int(m) - 1]} {y}"


def first_h1(text):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def md_inline(text):
    """Render one line of Markdown (for the index) without the wrapping <p>."""
    out = markdown.markdown(text).strip()
    return re.sub(r"^<p>|</p>$", "", out)


def city_name(slug):
    try:
        return registry.load(slug).provider
    except Exception:
        return slug


def render_article(path, slug, month, city):
    text = open(path, encoding="utf-8").read()
    title = first_h1(text) or f"{city}, {month_label(month)}"
    body_html = markdown.markdown(text, extensions=["tables", "sane_lists"])
    label = html.escape(month_label(month))
    crumbs = (f'<div class="crumbs"><a href="{SITE}">Ontario Address Change Tracker</a> › '
              f'<a href="index.html">Monthly articles</a> › {html.escape(city)} › {label}</div>')
    footer = (f'<div class="footer">Written from the tracker&#8217;s snapshot history of {html.escape(city)} '
              f'for {label}. '
              f'Source: <a href="{REPO_BLOB}/articles/{VARIANT}/{slug}-{month}.md">Markdown on GitHub</a> · '
              f'<a href="{REPO_BLOB}/articles/research/{slug}-{month}.md">research notes</a> · '
              f'<a href="{SITE}{slug}/">daily reports</a></div>')
    page = PAGE.format(title=html.escape(f"{title} — {city}"), css=CSS,
                       body=crumbs + body_html + footer)
    out = os.path.join(OUT, f"{slug}-{month}.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    return title


def main():
    names = {}
    titles = {}  # slug -> {month: title}
    for path in sorted(glob.glob(os.path.join(ARTICLES, VARIANT, "*-????-??.md"))):
        name = os.path.basename(path)[:-3]
        slug, month = name[:-8], name[-7:]
        if slug not in names:
            names[slug] = city_name(slug)
        titles.setdefault(slug, {})[month] = render_article(path, slug, month, names[slug])

    # Stale pages (an article renamed or withdrawn) come off the site.
    wanted = {f"{slug}-{month}.html" for slug, ms in titles.items() for month in ms}
    for path in glob.glob(os.path.join(OUT, "*-????-??.html")):
        if os.path.basename(path) not in wanted:
            os.remove(path)

    # Cities ordered by their newest month, then name, so the index leads with
    # whatever was written most recently.
    def city_key(slug):
        return (max(titles[slug]), names[slug])

    sections = []
    for slug in sorted(titles, key=city_key, reverse=True):
        rows = []
        for month in sorted(titles[slug], reverse=True):
            notes = ""
            if os.path.exists(os.path.join(ARTICLES, "research", f"{slug}-{month}.md")):
                notes = (f'<div class="notes"><a href="{REPO_BLOB}/articles/research/{slug}-{month}.md">'
                         f'Research notes</a> behind this piece, on GitHub.</div>')
            rows.append(f'<div class="month"><div class="when">{html.escape(month_label(month))}</div>'
                        f'<p class="lead"><a href="{slug}-{month}.html">{md_inline(titles[slug][month])}</a></p>'
                        f'{notes}</div>')
        n = len(rows)
        sections.append(f'<section class="city"><h2><a href="{SITE}{slug}/">{html.escape(names[slug])}</a>'
                        f'<small>{n} month{"s" if n != 1 else ""}</small></h2>'
                        f'<div class="months">{"".join(rows)}</div></section>')

    intro = (
        f'<div class="crumbs"><a href="{SITE}">Ontario Address Change Tracker</a> › Monthly articles</div>'
        '<h1>Monthly articles</h1>'
        '<p>One piece per city per fully observed calendar month, written from the tracker&#8217;s own '
        'snapshot history, with the month&#8217;s named things looked up and sourced. A month in which '
        'the file did not change says so.</p>'
    )
    footer = ('<div class="footer">Each piece carries the attribution its source licence requires. '
              'Repository: <a href="https://github.com/skfd/ontario-address-changes">skfd/ontario-address-changes</a></div>')
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(PAGE.format(title="Monthly articles — Ontario Address Change Tracker", css=CSS,
                            body=intro + "".join(sections) + footer))
    total = sum(len(ms) for ms in titles.values())
    print(f"wrote {total} article page(s) for {len(titles)} cit{'y' if len(titles) == 1 else 'ies'} to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
