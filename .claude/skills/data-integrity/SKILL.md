---
name: data-integrity
description: Decide whether to trust a snapshot or a run - triage a mass event as a real upstream change or a degraded pull, repair a store that recorded a bad snapshot, separate genuine daily-run failures from expected skips, and check the 42 sources for URL rot, schema drift or licence changes. Use when the daily run did something weird, when a city was refused by the guards or has stopped updating, when a report shows an implausible mass event, when logs/runs.csv or logs/update.log needs reading, or on any request to check the health of the pipeline rather than the config of a city.
---

# Data integrity

The other half of `city-tune`. That skill ends in a `datasets/<slug>.toml` edit and asks
"what should we compare?". This one ends in a **trust decision about an observation** and
asks "did we see what we think we saw?". It reads logs, DBs and HTTP; it never edits a
dataset config. When the answer turns out to be a config question, hand it to `city-tune`
and stop.

## Start here

**"Was every city checked?" is a vault question.** Open the operator report — one row per
city per day, `new` / `unchanged` / `failed` / `refused` / `no attempt`, each failure
carrying its cause:

```
python -m addressvault.cli report      # writes <vault>/report.html; daily-update.ps1 runs it
```

Then, for the project-side questions:

```
python .claude/skills/data-integrity/health.py
```

Sections: `blocks`, `runs` (both local). `--drift` adds the one network pass and is
deliberately not in the default set. Narrow with `--city <slug>`.

Read the reference for whatever the two turn up, then decide.

| What you are looking at | Read |
|---|---|
| A mass event you don't believe; a city refused by the guards | `references/corrupt-pulls.md` |
| A bad snapshot already recorded, which has to come back out | `references/repair.md` |
| A failed run, a missing day, a city that stopped updating | `references/runs.md` |
| URL rot, a source that added or dropped a column, licence text | `references/drift.md` |

## The one thing to know before reading any of it

**A recorded snapshot is expensive to take back.** Reports are rebuilt from the store on
every run, so a bad snapshot keeps producing a fake event until the store itself is
rebuilt (`references/repair.md`), and a report that was already published cannot be
un-published. That asymmetry is why the guards refuse a suspect pull outright instead of
recording it and flagging it, and it is the tiebreak whenever you are unsure: refusing a
good pull costs one day of staleness, recording a bad one costs a manual rebuild.

## What is already automatic

Do not re-derive these; they landed 2026-08-08 and change what is worth looking at.

- **Truncated pulls** — address-vault's arcgis fetcher probes `returnCountOnly` and
  refuses a pull more than 1% short of the layer's own count.
- **Row-count cliffs and stripped fields** — `db._check_sanity` refuses a snapshot more
  than 5% below the previous row count, or with a mapped field losing more than half its
  populated share. It writes the reason to the city's `blocks` table *before* raising,
  so `health.py --blocks` can see it. It is deliberately **not** on the public site — see
  below.
- **Recovery** — a pull that passes clears the block by itself, including the unchanged
  republish that takes the content-hash skip path. Nobody has to clear it by hand.

So the leftovers are what this skill is for: a degraded pull small enough to pass the
thresholds, a city failing the guard every day because the source genuinely changed, and
the failure modes the guards were never in a position to see.

## Never ask this repo's store whether a city was checked

It does not know, and it will answer anyway. This store records only **changes**:
`run.py:86` checks the snapshot filename before `db.already_imported`, so a city whose
source is verified every day and simply never moves writes no row at all — not even a
skip. Waterloo was pulled at noon every day through August 2026 and had not written a row
since June 27. Measured here, it reads as 44 days stale. It was never stale.

A `health.py --stale` section used to do exactly that and reported **21 of 42 cities
STALE when the true number was 1**. It was deleted on 2026-08-10 rather than fixed; two
staleness implementations disagreeing is what let Kingston fail two days running without
anyone noticing.

The vault holds the real ledger — one row per city per day:

```
Snapshot(slug='waterloo', date='2026-08-09', unchanged_since='2026-06-27',
         sha256='a1e0bb…', features=55543, fetched_at='2026-08-09T16:02:31Z')
```

`fetched_at` = we checked. `unchanged_since` = and it had not moved. A day with **no row**
is a day nobody checked; a day with a `jobs` row in state `failed` / `refused` / `deferred`
is a day somebody tried and it did not work, with the cause in `detail`. Read it through
`addressvault report`.

## Failures are back-office only

The public reports never say a city failed. A city that fails is simply not re-rendered
(`run.py`), so its pages keep the last good data and say nothing about why they stopped
moving. Refusal badges and "updates paused" panels were removed from `cities.html` and
`city_index.html` on 2026-08-10.

So a reader cannot tell you a city is stuck — only `addressvault report` and
`health.py --blocks` can. That is the intended trade: the operator's problem stays the
operator's.
