# Corrupt-pull triage

Deciding whether a mass event is the source changing or the pull degrading. Get this
wrong in the permissive direction and the store carries a fake event forever
(`repair.md`); get it wrong the other way and a city stops for no reason.

## Signatures seen in production

All three are now refused before anything is written, so you will meet them as a *block*
rather than as a recorded snapshot. They are still the shapes to recognise.

- **Truncated pull** — row count an exact multiple of 2000. Address-vault's ArcGIS paging
  loop used to end on a transient blank page, so a partial layer read as a complete one:
  kitchener 102,000 of 131,912 (51 pages), huron 20,000 of 38,300 (10 pages). The tell is
  the round number, not the size of the drop.
- **Attribute-stripped pull** — every field but the identity key comes back null. Muskoka
  2026-06-28. Where identity is synthesized this also re-keys the whole city, so it reads
  as "every address retired and re-added" rather than "every address modified".
- **Row-count cliff** — no round number, just far fewer rows than yesterday.

## Reading a block

`health.py --blocks`, or `db.active_block(ds)`. The field that decides is **`attempts`**:
how many days running the guard has turned this source away.

- **1–2 attempts** — almost certainly transport. Every degraded pull in the history so
  far fixed itself on the next day's pull. Do nothing; the block clears itself.
- **Many attempts, same reason** — the source has genuinely changed and the guard is now
  refusing reality. Confirm against the live layer (`health.py --drift --city <slug>`,
  or the layer's own `?f=json`), then decide: a real shrink means relaxing the constant,
  a dropped column means a `city-tune` field-map edit. Neither is this skill's call to
  make silently.

There is deliberately no per-run override. A source that really shrinks past a threshold
is supposed to stop the city and get a human's attention.

## What still gets through

The row floor is 5% and cannot see a small truncation — replayed against real renfrew
data, a 2.6% short pull imports cleanly. The vault's count probe is what catches those,
which leaves the gap real only for **static sources**, which report no count. So for a
`access = "static"` city, a modest unexplained drop is worth checking by hand before
believing it.

## Before believing any mass event

1. **Is it one day or a run of them?** A real upstream decision persists; a degraded pull
   is a single day with normal days either side.
2. **Does the shape match a signature above?** Round row count, whole-field nulls.
3. **Is the change plausible for the field?** `city-tune`'s `audit.py --tags` per-day
   tallies show whether these fields have ever moved together before.
4. **Did the site publish it?** A report that is already out is a different decision from
   one that is not — see `repair.md`.

## The thresholds

`_MAX_ROW_DROP = 0.05`, `_MAX_COVERAGE_DROP = 0.5`, `_MIN_GUARDED_ROWS = 100` in
`src/db.py`. They were measured, not guessed: over 620 consecutive snapshot pairs the
largest genuine row-count drop is 0.63% (sdg 2026-08-01), and over 2,288 field-pairs the
largest genuine coverage loss is a relative 1.5% (milton unit 2026-06-18), against
degraded pulls that lost 23–48% of rows or all of a field at once. **Rerun that
measurement over the current history before loosening either constant** — the argument
for the number is the margin, not the number.
