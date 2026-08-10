# Run-log triage

`health.py --runs`, read next to `addressvault report`. The job is to report only what
needs a human, which means knowing which failures are expected.

## Not failures

- **`offline`** — `daily-update.ps1` probes anchor IPs over TCP 443, no DNS involved, so
  this means the machine had no internet, not that a source was down. Exits 0 on purpose.
- **`metered`** — Windows reported a metered connection (cellular, tethering). Skipped
  deliberately; detection fails open, so an unmetered run is never blocked by a broken
  API.
- **`attempts` > 1** — the script retried itself. Task Scheduler's `RestartCount` never
  fires on a nonzero exit (it only covers launch failures), so the retry loop lives in
  `daily-update.ps1`. A run that succeeded on attempt 3 succeeded.
- **A day with no run at all** — the laptop was off. Expected on this setup; only a long
  run of them is news.
- **ottawa fetch errors** — the city sits behind an F5 that rate-limits by connection.
  Intermittent, self-clearing.

## Are failures

- A **numeric nonzero** exit in `runs.csv`.
- `publish-failed` — the site build or push broke. The update itself may have been fine;
  the public site is what is stale.
- A city appearing in `update.log` as `ERROR (<slug>)` on consecutive runs. One run is
  usually transport.

`update.log` is rewritten each run, so its ERROR lines only describe the last one. For
anything historical, `runs.csv` and the per-city logs are what survive.

## What runs.csv cannot show, and what to read instead

`runs.csv` has one row per **run**, with one exit code. It cannot express "41 cities
verified, 1 not," so a single city whose source is down looks identical to the pipeline
breaking. It also under-records: on 2026-08-06 and 2026-08-08 the vault logged checks for
every city on days `runs.csv` has no row for at all.

Worse, this repo's store cannot fill the gap, because it records only *changes*. A city
verified daily that never moves writes nothing, so counting snapshot ages here flags
cities that are perfectly healthy. A `--stale` section that did this reported 21 of 42
STALE against a true count of 1; it was deleted on 2026-08-10.

**`addressvault report` is the per-city-per-day ledger.** One row per city per day —
`new`, `unchanged` (verified, did not move), `failed`, `refused`, or no attempt — with the
cause on every failure. Two things to read off it:

- **A gap with no row** — nobody checked that day. Laptop off, `offline`, `metered`.
- **A run of `failed` on one city** — the source is down and it is theirs, not ours.
  Kingston 2026-08-08 and 08-09, seven attempts, all `arcgis error 500: Error invoking
  service`. Neither day appeared as a Kingston-shaped problem in `runs.csv`; one of them
  had no `runs.csv` row at all.

`--drift` is the quickest confirmation for a single city: a layer that answers `?f=json`
normally is publishing fine, so the break is between the source and us.
