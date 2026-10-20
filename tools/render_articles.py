"""Render articles/ (Markdown) to docs/articles/ (HTML) for GitHub Pages.

    docs/articles/index.html              one row per month
    docs/articles/<slug>-<month>.html     the article

Only the article (articles/researched/) is rendered. The research notes are
working material with unverified SNIPPET items, so the index links to them on
GitHub instead, where the Markdown already renders.

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
    .months { display:flex; flex-direction:column; gap:12px; }
    .month { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:14px 16px; }
    .month .when { font-size:12px; font-weight:600; color:var(--text-dim); margin-bottom:8px; }
    .month .lead { margin:0 0 8px; font-size:15px; } .month .lead:last-child { margin-bottom:0; }
    .month .notes { font-size:12px; color:var(--text-dim); margin-top:8px; }
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{css}</style>
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


def render_article(path, slug, month):
    text = open(path, encoding="utf-8").read()
    title = first_h1(text) or f"{slug} {month}"
    body_html = markdown.markdown(text, extensions=["tables", "sane_lists"])
    label = html.escape(month_label(month))
    crumbs = (f'<div class="crumbs"><a href="{SITE}">Ontario Address Change Tracker</a> › '
              f'<a href="index.html">Monthly articles</a> › {label}</div>')
    footer = (f'<div class="footer">Written from the tracker&#8217;s snapshot history for {label}. '
              f'Source: <a href="{REPO_BLOB}/articles/{VARIANT}/{slug}-{month}.md">Markdown on GitHub</a> · '
              f'<a href="{REPO_BLOB}/articles/research/{slug}-{month}.md">research notes</a> · '
              f'<a href="{SITE}{slug}/">daily reports</a></div>')
    page = PAGE.format(title=html.escape(title), css=CSS, body=crumbs + body_html + footer)
    out = os.path.join(OUT, f"{slug}-{month}.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    return title


def main():
    months = {}  # (slug, month) -> title
    for path in sorted(glob.glob(os.path.join(ARTICLES, VARIANT, "*-????-??.md"))):
        name = os.path.basename(path)[:-3]
        slug, month = name[:-8], name[-7:]
        months[(slug, month)] = render_article(path, slug, month)

    rows = []
    for (slug, month) in sorted(months, key=lambda k: (k[1], k[0]), reverse=True):
        lead = (f'<p class="lead"><a href="{slug}-{month}.html">'
                f'{md_inline(months[(slug, month)])}</a></p>')
        notes = ""
        if os.path.exists(os.path.join(ARTICLES, "research", f"{slug}-{month}.md")):
            notes = (f'<div class="notes"><a href="{REPO_BLOB}/articles/research/{slug}-{month}.md">'
                     f'Research notes</a> behind this piece, on GitHub.</div>')
        rows.append(f'<div class="month"><div class="when">{html.escape(month_label(month))} · '
                    f'{html.escape(slug)}</div>{lead}{notes}</div>')

    intro = (
        f'<div class="crumbs"><a href="{SITE}">Ontario Address Change Tracker</a> › Monthly articles</div>'
        '<h1>Monthly articles</h1>'
        '<p>One piece per fully observed calendar month, written from the tracker&#8217;s own snapshot history, '
        'with the month&#8217;s named things looked up and sourced.</p>'
    )
    footer = ('<div class="footer">Toronto articles contain information licensed under the '
              '<a href="https://open.toronto.ca/open-data-license/">Open Government Licence – Toronto</a>. '
              'Repository: <a href="https://github.com/skfd/ontario-address-changes">skfd/ontario-address-changes</a></div>')
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(PAGE.format(title="Monthly articles — Ontario Address Change Tracker", css=CSS,
                            body=intro + '<div class="months">' + "".join(rows) + "</div>" + footer))
    print(f"wrote {len(months)} article page(s) to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
