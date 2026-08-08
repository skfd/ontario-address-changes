# Skill backlog — ontario-address-changes

Last updated: 2026-08-08. Claude Code skills for `.claude/skills/`, drawn from work that
has already recurred across the 42 tracked cities. Unlike `TODO.md` (per-city decisions
for the human operator), these are tooling tasks: each turns a procedure we have run by
hand into something repeatable.

Two tracks, split by what the work *ends in* — a config edit, or a trust decision about
an observation. An earlier draft of this file split the same work eight ways; that was
wrong, because four of those skills would have loaded the same city DB, walked the same
history, and ended in the same file. Keep the tracks broad and use `references/` for the
per-decision detail, so only what is needed gets read.

## 1. city-tune — ends in a `datasets/<slug>.toml` edit

Shipped 2026-08-08 (`.claude/skills/city-tune/`). Covers identity key, field map,
change classes, ignore/keep fields, and onboarding, over one `audit.py` pass.

- [x] `ignore_fields` / `keep_fields` — built out of the Guelph review.
- [x] identity health — collisions, flap rate, keys-vs-rows.
- [x] field map — coverage of mapped slots, candidates for unmapped ones.
- [x] class candidates — low-cardinality props cross-referenced with solo churn.
- [x] onboarding path — source resolution, licence/OSM compat, `skipped.toml`.

Remaining work on it:

- [ ] Work `TODO.md` §1 with it: waterloo's unparsed `CIVIC_ADDR`, lennox-addington's
  `ADD_LABEL`, the five cities with no full-address field, the unit-field verification
  pass starting with toronto. The skill exists; the decisions are still open.
- [ ] Sweep all 42 cities for the echo bug the Guelph audit exposed — a humanized
  category stuck at 0 because duplicate coordinate or derived fields ride along with
  every change. Guelph's Location Adjustments had never fired in three months.
- [ ] `audit.py --identity` reports flap history-wide, so damage predating a config fix
  still shows (muskoka: 16.75%). Add a per-snapshot breakdown, or teach the reference to
  always cross-check the per-diff summary for when the spikes stopped.

## 2. data-integrity — ends in a trust decision about a snapshot or a run

Not built yet. Triggered by "the daily run did something weird", takes logs and HTTP
rather than the field config, and never edits a dataset.

- [ ] **Corrupt-pull triage.** Decide whether a mass event is a real upstream change or
  a degraded pull. Signatures already seen: a row count that is an exact multiple of 2000
  (address-vault's ArcGIS paging loop ending on a transient blank page — kitchener
  102,000 of 131,912, huron 20,000 of 38,300), an attribute-stripped pull where every
  field but the identity key is null (muskoka 2026-06-28), and plain row-count cliffs.
- [ ] **Repair.** Generalize `tools/repair_bad_snapshots.py` from a one-shot script into
  an on-demand tool: drop the bad snapshot, rebuild the store's SCD-2 history, regenerate.
- [ ] **Run-log triage.** Read `logs/runs.csv` and the daily log; separate genuine
  failures from expected skips (`offline`, `metered`, F5 connection rate-limits on
  ottawa) and report only what needs a human.
- [ ] **Source drift.** Periodic health check across all 42 `data_url`s: URL rot, schema
  drift (fields added or dropped since the last audit), licence text changes. Feeds
  city-tune rather than duplicating it.
