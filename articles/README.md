# Monthly articles

One newsletter piece per fully-observed calendar month, written from the tracker's own
snapshot history. Markdown, ready to paste into Substack.

Each month is written **twice**, and the only difference between the two is whether the
outside world was consulted:

| | |
|---|---|
| [`offline/`](offline/) | The store alone. No external facts, no neighbourhood name that ward and coordinates don't give you, no acronym the file doesn't spell out. Where a cause is unknown it says so and stops. |
| [`researched/`](researched/) | The same month after step 5b of the `monthly-article` skill: the month's proper nouns searched, causes sourced and linked, and the record's silences stated as silences. |
| [`research/`](research/) | The raw findings behind the researched version — entity, what was found, URL, confidence. Notes, not prose. |

This is a live comparison. One variant may be dropped after review; dropping it is
`git rm -r articles/<variant>` plus the *Two variants* section of the skill.

## The months

| Month | Net | Lead, offline | Lead, researched |
|---|---|---|---|
| 2026-03 | +28 | A block of Queen East retires — cause unknown | *Nothing was demolished*: ten consecutive point ids folded back into 1238, and the development is across the street |
| 2026-04 | +29 | Eleven addresses off the even side of Secord Ave | The demolition permit was issued **25 Mar 2021** — the file is five years behind, and the surviving evens are the unpermitted next phase |
| 2026-05 | +19 | Chloe Cooley St debuts, reserved | By-law 182-2026 names it; the City's own report repeats the wrong enslaver's name from a 2007 plaque |
| 2026-06 | +15 | An address for an unbuilt station entrance | …under a name Metrolinx has since dropped; and Hamilton publishes the `R`-suffix and half-number rules Toronto doesn't |
| 2026-07 | +12 | Crosstown West gets its addresses | Those nine addresses are a **contract's parts list**; and the park "renamings" are restorations of decisions up to ten years old |

The researched versions lead on something else in four months out of five — which is
most of what this comparison was set up to find out.

February 2026 is deliberately absent: observation starts 2026-02-12, so its first
fortnight was never seen. August 2026 is still open.

## Writing the next one

Normally nothing: from the 3rd of each month the `kk-ontario-article` scheduled task
(`monthly-article.ps1`) writes the previous month unattended — both variants, the
research notes and this table's row — and commits and pushes them. It waits a day
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
