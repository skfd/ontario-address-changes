---
name: monthly-article
description: Write the monthly newsletter piece about how a city's addresses changed - what was built, split, renumbered, renamed or retired in one calendar month - from the tracker's own snapshot history. Use when asked for a Substack/newsletter/blog post or monthly roundup about address changes, to write up a given month for Toronto or any tracked city, to catch up on every month observed so far, or to update an article after a re-render changed the numbers.
---

# Monthly article

One calendar month of a city's address file, written for a reader who likes their city
but has never heard of a civic-address point. The tracker already knows what changed;
this skill is about picking which of it is a story and refusing to invent the rest.

Articles live in `articles/<slug>-<YYYY-MM>.md`, one per month, Markdown that pastes
into Substack unchanged.

## The loop

1. **Find the months worth writing.**
   ```
   python tools/month_digest.py --city toronto --months
   ```
   Only `[complete]` months qualify: the month opens where the previous one closed and
   at least one snapshot follows it. A month whose first fortnight was never observed
   would silently under-report — say so and skip it rather than writing a thin piece.

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

6. **Write it** to `articles/<slug>-<YYYY-MM>.md`, following the skeleton in
   `references/house-style.md`. The attribution footer is not optional (step 8).

7. **Re-read it as the reader.** Every number in the piece must be traceable to a line
   in the brief. Cut any sentence that survives only because it was hard to research.

8. **Attribution.** Every article carries the source line for the city's licence —
   `license_name` from `datasets/<slug>.toml`. For Toronto: *"Contains information
   licensed under the Open Government Licence – Toronto."* Link the source dataset and
   link the day's report on the live site, so a reader can check any claim. Attribution
   travels with the content to every venue it is cross-posted to.

9. **Commit.** One commit per article batch.

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
| `references/verifying.md` | Queries that confirm a specific address, street, split or rename before it goes in print |
| `references/publishing.md` | Where these go, cadence, cross-posting, licence obligations per venue |

## Other cities

Nothing here is Toronto-specific except the field names in the brief (`PLACE_NAME`,
`WARD_NAME`) and the licence line. `--city <slug>` works for all 53 datasets, but
check `publish_reports` in the dataset's TOML first: four cities are tracked under
licences that forbid republication, and an article quoting their rows is exactly the
republication the gate exists to prevent. Those cities get no article.
