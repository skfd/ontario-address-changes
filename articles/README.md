# Monthly articles

One newsletter piece per fully-observed calendar month, written from the tracker's own
snapshot history. Markdown, ready to paste into Substack.

Each month's piece sits in [`researched/`](researched/), with the raw findings behind it
(entity, what was found, URL, confidence; notes, not prose) in [`research/`](research/).

The same pieces are rendered to HTML on the live site at
[`/articles/`](https://skfd.github.io/ontario-address-changes/articles/) by
`tools/render_articles.py`, which the scheduled run calls before committing. The
research notes are not rendered; the site links to them here on GitHub.

From March to September 2026 each month was also written a second time from the store
alone, with no outside facts (`offline/`). The researched version led on something else
in six of the seven months, and the offline pieces were wordier and said less, so that
variant was dropped on 2026-10-20. `git log -- articles/offline` has them.

## The months

| Month | Net | Lead |
|---|---|---|
| 2026-03 | +28 | *Nothing was demolished*: ten consecutive point ids folded back into 1238, and the development is across the street |
| 2026-04 | +29 | The demolition permit was issued **25 Mar 2021** — the file is five years behind, and the surviving evens are the unpermitted next phase |
| 2026-05 | +19 | Chloe Cooley St debuts, reserved; By-law 182-2026 names it, and the City's own report repeats the wrong enslaver's name from a 2007 plaque |
| 2026-06 | +15 | An address for an unbuilt station entrance, under a name Metrolinx has since dropped; and Hamilton publishes the `R`-suffix and half-number rules Toronto doesn't |
| 2026-07 | +12 | Those nine addresses are a **contract's parts list**; and the park "renamings" are restorations of decisions up to ten years old |
| 2026-08 | +7 | The swapped addresses are buildings the City dated years ago (Yonge/Glebe rezoned **2010**, Hullmark Centre, Alter); a park council renamed on 30 July reached the file in **20 days**; a 2023 permit named 530 Duplex Ave before the file did |
| 2026-09 | −105 | The 13 Carlaw Ave doors were the **Riverdale Shopping Centre**, demolished for the Ontario Line's Gerrard portal (permit completed **15 Dec 2025**); the station rename trails Metrolinx by 17½ months; three new lanes, each over a finished laneway suite |

February 2026 is deliberately absent: observation starts 2026-02-12, so its first
fortnight was never seen. October 2026 is still open.

## Writing the next one

Normally nothing: from the 3rd of each month the `kk-ontario-article` scheduled task
(`monthly-article.ps1`) writes the previous month unattended — the research notes, the
article and this table's row — renders the site copy, and commits and pushes them. It waits a day
whenever Toronto has an open flag inside the month. `logs/article-runs.csv` says what
each day's run did. By hand, for an older month or another city:

```
python tools/month_digest.py --city toronto --months              # which months qualify
python run.py flags                                               # nothing open for the month?
python tools/month_digest.py --city toronto --month 2026-08       # the brief
python tools/month_digest.py --city toronto --month 2026-08 --format entities   # the research checklist
```

Then follow the `monthly-article` skill (`.claude/skills/monthly-article/`), which
carries the house style, the fact-checking queries, the research procedure and the
licence obligations.
