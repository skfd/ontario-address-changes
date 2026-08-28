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

| Month | Net | Lead (offline) |
|---|---|---|
| 2026-03 | +28 | A block of Queen East retires; the published file reverts to its April-2025 values |
| 2026-04 | +29 | Eleven addresses off the even side of Secord Ave; rear (`R`) addresses |
| 2026-05 | +19 | Chloe Cooley St debuts, reserved; BMO Field becomes Toronto Stadium |
| 2026-06 | +15 | An address for an unbuilt SmartTrack station entrance; seven duplicate Royal York Rd points |
| 2026-07 | +12 | Eglinton Crosstown West Extension gets its addresses; the March reversion undone |

The researched versions may lead on something else — that is the point of the
comparison, and the skill says to write the second one as its own piece rather than as
an annotated diff.

February 2026 is deliberately absent: observation starts 2026-02-12, so its first
fortnight was never seen. August 2026 is still open.

## Writing the next one

```
python tools/month_digest.py --city toronto --months              # which months qualify
python run.py flags                                               # nothing open for the month?
python tools/month_digest.py --city toronto --month 2026-08       # the brief
python tools/month_digest.py --city toronto --month 2026-08 --format entities   # the research checklist
```

Then follow the `monthly-article` skill (`.claude/skills/monthly-article/`), which
carries the house style, the fact-checking queries, the research procedure and the
licence obligations.
