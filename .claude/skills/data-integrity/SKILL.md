---
name: data-integrity
description: Decide whether to trust a snapshot or a run - triage a mass event as a real upstream change or a degraded pull, repair a store that recorded a bad snapshot, separate genuine daily-run failures from expected skips, and check the 42 sources for URL rot, schema drift or licence changes. Use when the daily run did something weird, when a city shows a refusal badge or has stopped updating, when a report shows an implausible mass event, when logs/runs.csv or logs/update.log needs reading, or on any request to check the health of the pipeline rather than the config of a city.
---

# Data integrity

The other half of `city-tune`. That skill ends in a `datasets/<slug>.toml` edit and asks
"what should we compare?". This one ends in a **trust decision about an observation** and
asks "did we see what we think we saw?". It reads logs, DBs and HTTP; it never edits a
dataset config. When the answer turns out to be a config question, hand it to `city-tune`
and stop.

## Start here

```
python .claude/skills/data-integrity/health.py
```

Sections: `stale`, `blocks`, `runs` (all local). `--drift` adds the one network pass and
is deliberately not in the default set. Narrow with `--city <slug>`.

That one command covers three of the four questions below. Read the reference for
whichever it turns up, then decide.

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
  so the refusal is visible on the site as a red "needs a look" badge rather than only
  in a log.
- **Recovery** — a pull that passes clears the block by itself, including the unchanged
  republish that takes the content-hash skip path. Nobody has to clear it by hand.

So the leftovers are what this skill is for: a degraded pull small enough to pass the
thresholds, a city failing the guard every day because the source genuinely changed, and
the failure modes the guards were never in a position to see.

## The failure that is invisible everywhere else

`run.py:86` checks the snapshot filename before `db.already_imported`, so when the vault
hands back the same dated file every day, **no snapshot row is written at all — not even
a skip** — and `logs/runs.csv` records the day as a clean success. Eight cities sat
frozen on a June file for six weeks without a single log line saying so.

`health.py --stale` is the only place this surfaces. It reads max snapshot age per city
and judges it against that city's own gap history, because a flat threshold cannot tell
a weekly publisher from a daily one that stopped. Note what it does *not* prove: that the
source stopped publishing. It proves only that we stopped recording. Confirming which is
a vault-side question.
