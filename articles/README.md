# Monthly articles

One newsletter piece per fully-observed calendar month, written from the tracker's own
snapshot history. Markdown, ready to paste into Substack.

| Month | Piece | Net | Lead |
|---|---|---|---|
| 2026-03 | [toronto-2026-03.md](toronto-2026-03.md) | +28 | A block of Queen East retires; the published file reverts to its April-2025 values |
| 2026-04 | [toronto-2026-04.md](toronto-2026-04.md) | +29 | Eleven addresses off the even side of Secord Ave; rear (`R`) addresses |
| 2026-05 | [toronto-2026-05.md](toronto-2026-05.md) | +19 | Chloe Cooley St debuts, reserved; BMO Field becomes Toronto Stadium |
| 2026-06 | [toronto-2026-06.md](toronto-2026-06.md) | +15 | An address for an unbuilt SmartTrack station entrance; seven duplicate Royal York Rd points |
| 2026-07 | [toronto-2026-07.md](toronto-2026-07.md) | +12 | Eglinton Crosstown West Extension gets its addresses; the March reversion undone |

February 2026 is deliberately absent: observation starts 2026-02-12, so its first
fortnight was never seen. August 2026 is still open.

## Writing the next one

```
python tools/month_digest.py --city toronto --months     # which months qualify
python run.py flags                                      # nothing open for the month?
python tools/month_digest.py --city toronto --month 2026-08
```

Then follow the `monthly-article` skill (`.claude/skills/monthly-article/`), which
carries the house style, the fact-checking queries and the licence obligations.
