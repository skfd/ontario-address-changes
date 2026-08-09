# Run-log triage

`health.py --runs --stale`. The job is to report only what needs a human, which means
knowing which failures are expected.

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

## The failure the logs cannot show

**`runs.csv` cannot see a frozen source.** `run.py:86` checks the snapshot filename before
`db.already_imported`, so when the vault serves the same dated file every day the run
short-circuits, writes no snapshot row — not even a skip — and exits clean. Eight cities
sat on a June file for six weeks while every day reported success.

So `--runs` alone is never a health check. Read `--stale` with it, always.

## Reading --stale

Age is judged against each city's own gap distribution (p90), not a flat threshold, plus
a 3-day floor. A flat number cannot separate a weekly publisher from a daily one that
stopped — and in this catalogue almost every city was on a 1-day cadence, so multi-day
ages are worth looking at even for cities nobody has flagged.

The list is ranked by how far past its own rhythm each city is; read from the top and
stop where it stops being interesting. The flag is deliberately sensitive — 18 of 42 on
2026-08-08 — because a missed freeze is invisible and a false positive costs one glance.

What the section does **not** establish is *why*. It proves we stopped recording, not
that the source stopped publishing. Confirming which is a vault-side question, and
`--drift` is the quickest local hint: a layer that answers `?f=json` normally is
publishing fine, so the break is between the vault and us.

Two shapes worth telling apart in the age column:

- **A cliff** — daily, daily, daily, then nothing. The eight frozen cities, and
  niagara-falls (36d after a max gap of 5).
- **A degrading cadence** — gaps stretching 1 → 6 → 7 → 8 before stopping (cornwall), or
  1 → 11 → 15 (london). These raise their own p90 as they degrade, so they rank *lower*
  than a clean cliff of the same age. Don't read rank as severity.
