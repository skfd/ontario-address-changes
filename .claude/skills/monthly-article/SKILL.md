---
name: monthly-article
description: Write the monthly newsletter piece about how a city's addresses changed - what was built, split, renumbered, renamed or retired in one calendar month - from the tracker's own snapshot history. Use when asked for a Substack/newsletter/blog post or monthly roundup about address changes, to write up a given month for Toronto or any tracked city, to catch up on every month observed so far, or to update an article after a re-render changed the numbers.
---

# Monthly article

One calendar month of a city's address file, written for a reader who likes their city
but has never heard of a civic-address point. The tracker already knows what changed;
this skill is about picking which of it is a story and refusing to invent the rest.

Articles live in `articles/researched/`, one file per month — `<slug>-<YYYY-MM>.md`,
Markdown that pastes into Substack unchanged. The findings behind each one live
alongside in `articles/research/`.

## The loop

1. **Find the months worth writing.**
   ```
   python tools/month_digest.py --city toronto --months
   ```
   Only `[complete]` months qualify, by either of two tests: the store's own (the month
   opens where the previous one closed and at least one snapshot follows it) or the
   vault's pull calendar (a pull before the month, one after, and at least two thirds
   of its days read — which is what lets a month with *no* edits count). A month that
   passes neither was not watched end to end and would silently under-report — say so
   and skip it rather than writing a thin piece. A complete month with nothing in it
   is written by `tools/article_quiet.py`, not by this loop; the brief says
   `QUIET MONTH` in its header when that applies.

2. **Check the flag queue before trusting any number.**
   ```
   python run.py flags
   ```
   An *open* flag for that city inside the target month means the digest is holding
   an unreviewed event, so the article would be written around a gap. Run the
   `review-flags` skill first. Flags already reviewed as `technical`/`bug` are held
   deliberately and need no action — the digest prints them under `HELD` and they are
   excluded from every number, which is correct: they are source noise, not news.

3. **Get the brief.**
   ```
   python tools/month_digest.py --city toronto --month 2026-03
   ```
   Add `--out <path>` to file it, `--format json` when you want to compute on it.
   Read the whole thing before writing a sentence.

4. **Pick the story.** Read `references/house-style.md`. Most months have one real
   lead and two or three supporting items; a month with none gets the quiet-month
   treatment, not padding.

5. **Verify every specific claim** you plan to make, against the store rather than
   against the brief's summary. `references/verifying.md` has the queries. Anything
   you cannot verify comes out of the article — a wrong street name is the one error
   a local reader will always catch.

5b. **Research the month's named things** — read `references/research.md`, then:
   ```
   python tools/month_digest.py --city toronto --month 2026-03 --format entities
   ```
   That prints the month's proper nouns as a search checklist. The store says eleven
   addresses left Queen Street East; only the outside record says why. Every fact that
   comes back gets a link in the article, and a search that finds nothing is written up
   as the record being silent, never as a guess. File the findings in
   `articles/research/<slug>-<YYYY-MM>.md` before drafting.

6. **Write it.** Follow the skeleton in `references/house-style.md`. Write from the
   brief and the research notes, not from a browser. The attribution footer is not
   optional (step 8).

7. **Re-read it as the reader.** Every number in the piece must be traceable to a line
   in the brief. Cut any sentence that survives only because it was hard to research.

8. **Attribution.** Every article carries the source line for the city's licence,
   and the brief's header prints it ready-made as `attribution line:` — either
   *"Contains information licensed under the <licence>."* with the source dataset
   linked, or, where `datasets/<slug>.toml` records that no licence is published, a
   plain source statement. Use it verbatim (`month_digest.attribution(ds)` is the
   one place the wording lives), then link the city's reports on the live site (the
   brief's `site:` line) so a reader can check any claim. Attribution travels with
   the content to every venue it is cross-posted to.

8b. **Index it.** Add the month's row to the table in `articles/README.md` —
   `| <month> | <slug> | <net> | <lead> |`, keeping the table ordered by month then
   city, matching the rows around it.

9. **Commit.** One commit per article batch.

## The scheduled run

Since 2026-09-08 the previous month is written unattended, and since 2026-10-22 for
every city whose licence allows it: the `kk-ontario-article` task runs
`monthly-article.ps1` daily at 15:00, which does nothing before the 3rd, asks
`tools/article_due.py --all` which city-months are complete, unflagged and unwritten,
and then works through them one city at a time. A month in which nothing changed
(`quiet` in the due list) is written by `tools/article_quiet.py` from a fixed shape;
a month with changes gets a headless run of this skill in one pass (research notes,
article, README row). After each city it renders `docs/articles/`, commits and pushes,
so a run that dies keeps what it finished. The Claude runs are capped per day
(`-MaxClaude 6`, `-BudgetMinutes 150`, inside the task's 4 h limit) and the rest is
`DEFERRED` to the next day, so a month with thirty busy cities takes about a week.
A month held by an open flag logs `WAITING` and is retried the next day.
`logs/article.log` and `logs/article-runs.csv` (one row per city-month) hold the
outcome. Months older than the previous one are still written by hand with the loop
above, or with `.\monthly-article.ps1 -Month 2026-08` for a whole batch.

## Numbers: net vs gross

The brief gives both and they are not interchangeable.

- **net** — one diff from the last snapshot before the month to the last one in it.
  This is what a reader means by "Toronto gained N addresses in March". Use it for
  every headline count.
- **gross** — the sum of the daily diffs. An address added on the 4th and retired on
  the 20th appears in gross and not in net; a row edited twice counts twice. Only ever
  describe it as *edits* or *activity*, never as addresses.

When the two differ noticeably, that gap is itself worth a sentence — it means the
month churned.

## The month is not the calendar

Snapshots are not daily and the month's last one is rarely the 30th: March 2026 closes
on the 27th, so changes between 03-27 and 04-02 land in April's article. Don't engineer
around it; the brief's header line carries the exact window and the article's
methodology footer states it.

## References

| Read | For |
|---|---|
| `references/house-style.md` | Voice, article skeleton, what counts as a lead, the quiet-month shape |
| `references/research.md` | Step 5b: the search checklist, where Toronto's answers live, citation rules |
| `references/verifying.md` | Queries that confirm a specific address, street, split or rename before it goes in print |
| `references/publishing.md` | Where these go, cadence, cross-posting, licence obligations per venue |

## Other cities

Every city gets the same piece. Nothing here is Toronto-specific except the field
names in the brief (`PLACE_NAME`, `WARD_NAME`) and the Toronto rows of the research
table; `references/research.md` says where the answers live for everyone else.
`--city <slug>` works for all 77 datasets, but only the 58 with `publish_reports =
true` get an article: the other 19 are tracked under licences that forbid
republication, and an article quoting their rows is exactly the republication the
gate exists to prevent. `article_due --all` already leaves them out. A small city's
month is a small piece — the quiet-month shape in `references/house-style.md` is the
norm outside Toronto, not the exception.
