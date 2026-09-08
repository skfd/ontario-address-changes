# Publishing

## Where these go

**Substack is the right primary venue** for the reasons the format actually needs:
monthly cadence, an email list that reaches people who will never visit a GitHub Pages
site, comments that stay attached to the piece, and no obligation to post between
issues. The alternatives lose something specific — a personal blog has no distribution,
Medium takes the audience, a newsletter platform tied to the repo (GitHub Pages posts)
gets read by nobody who is not already reading the repo.

**The live site stays canonical.** `https://skfd.github.io/ontario-address-changes/`
holds the daily reports the article cites. The article is the narrative layer; it links
down into the reports for anything a reader wants to check. Never let a number exist
only in the newsletter.

**Cross-post highlights, not the article**, to where the specific month's story
belongs:

| Venue | What to send | Cadence |
|---|---|---|
| r/toronto | The one visual item — a split, a rename, a new street — with a link. Not the whole piece. | Only when there is a genuine local hook |
| OpenStreetMap Canada (community forum, `#canada` on the OSM Slack/Matrix) | Source-side events: bulk recodes, restyled street names, schema drift. This audience cares about exactly the parts a general reader skims. | Every month there is one |
| Toronto open-data / civic-tech circles (Code for Canada, CivicTechTO) | The methodology posts, when one comes up | Rare |
| BlueSky / Mastodon | One image + one sentence + link, as the issue goes out | Every issue |

Do not cross-post to a venue and then not read the replies. A correction arriving in a
Reddit thread that nobody watches is worse than not posting.

## Cadence

Publish in the first week of the following month, once the month has a snapshot after
it (which is what makes it `[complete]` in the digest). Skip a month rather than
publish a padded one; a missed issue costs less than a boring one.

The drafts arrive on their own: the `kk-ontario-article` task writes and commits the
previous month from the 3rd (see *The scheduled run* in the skill), so by the time
the week starts both variants and the research notes are on `main`. Posting to
Substack and the crossposts remain a person's job.

## Licence obligations travel

Every venue gets the attribution, not just the canonical copy. For Toronto:

> Contains information licensed under the Open Government Licence – Toronto.

Plus a link to the source dataset. The obligation attaches to the *content*, so it
comes along on the Substack post, the Reddit crosspost body, and any image whose data
came from the file. A screenshot of the map is derived content too.

Two things not to do:

- **Do not paste a bulk extract into a post.** Quoting a dozen addresses to tell a
  story is normal editorial use. Reproducing a street's full address list is
  redistribution, and it belongs on the site under its licence.
- **Do not write about a `publish_reports = false` city.** Four datasets are tracked
  under licences that forbid republication (`sdg`, `renfrew`, `peterborough-county`,
  and any later addition). The site gates them; an article would walk straight around
  that gate. Check the TOML before starting.

## House ads

Each issue ends with one line pointing at the site and one at the repo. No more.
The piece earns the subscription by being right, not by asking.
