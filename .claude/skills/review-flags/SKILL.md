---
name: review-flags
description: Review the flagged change events holding content off the public site - triage each open flag in flags.toml as a business change (publish), a technical feed change (suppress + config rule), or a data bug (suppress + vault verdict/repair), file the verdict with a date, and re-render. Use when the user asks to review flags, work through the flag queue, or asks why a day's changes are missing from a city's public report; also when the daily run prints FLAGGED lines or logs/flags.html shows open entries.
---

# Review flags

The editorial half of the flag pipeline. `src/flags.py` holds any homogeneous
mass event (mass add, mass removal, same-field sweep) off the public site until
a verdict lands in `flags.toml`. This skill is how verdicts land. The goal of
the site is to show **business changes only** — what actually happened in the
city — never feed mechanics and never data bugs.

Every review must end in one of exactly three verdicts, and the queue must
shrink permanently: a `technical` or `bug` verdict without a rule that stops
the same flag recurring is an unfinished review.

## Workflow

1. **List the queue** (oldest first — age is content held off the site):

   ```
   python .claude/skills/review-flags/brief.py
   ```

2. **Brief one flag**: `brief.py <slug> <date>`. It prints sample rows with
   old->new values, the full value-transition distribution, street spread for
   adds/removals, this city's past flags with the same signature, and the
   vault's day verdict. If the brief is not enough to decide, escalate the
   diagnosis — `data-integrity` for "is this pull trustworthy", `city-tune`
   for "is this config right" — then come back here to file.

3. **Decide.** The discriminator is homogeneity and reader-relevance:

   | Verdict | It means | Tell-tales |
   |---|---|---|
   | `business` | The city really changed; a reader should see it. | Heterogeneous rows; adds clustered on few streets (subdivision); a rename/renumber a municipality would announce; vault verdict `real`. |
   | `technical` | The feed changed, the city didn't. | One field recoded 1:1 across the sweep; value-preserving restyles (case/whitespace/token order); uniform coordinate shifts; field appearing/vanishing everywhere; vault verdict `schema`. |
   | `bug` | The data is not true of the world. | Replayed/duplicated batches (adds spread evenly citywide, often removed again next day); truncation just under the guards; stripped values; vault verdict `artifact`. |

   Unsure? Leave it open with a `note` saying what is missing. Open holds; an
   unreviewed flag is never a clean bill of health.

4. **File the verdict** by editing the entry in `flags.toml` in place (never
   delete entries; never touch other entries):

   ```toml
   status = "reviewed"
   verdict = "technical"
   reviewed = "<today YYYY-MM-DD>"
   rule = "datasets/<slug>.toml: ignore_fields += STREET_TYPE"
   note = "1:1 recode AVE->Avenue on all 83 rows; full echoes it; no address moved."
   ```

5. **Make the rule real** — the verdict alone only hides one day:
   - `technical` → the config change that prevents the recurrence, via
     `city-tune` conventions (`ignore_fields` for noise, a `[classes]` entry
     if it should publish humanized instead of suppressed). `rule` names the
     edit. If a `[classes]` entry is the fix, the event will publish under
     that class — that is a business reclassification, not a suppression.
   - `bug` → the vault verdict (`addressvault review`) and, if the bad
     snapshot is in this repo's store, the repair path in
     `data-integrity/references/repair.md`. `rule` names both.
   - `business` → no rule (`rule = ""`); a one-off publish needs none. If the
     vault flagged the same day, file its verdict as `real` so the two
     ledgers agree.

6. **Re-render and verify**: `python run.py report --city <slug>`, then check
   the console — a `business` verdict must stop printing `held ...` for that
   day, a `technical`/`bug` one must keep holding without the FLAGGED line
   reappearing. `logs/flags.html` is the human view of the queue.

7. **Commit** the ledger edit, any config edits, and the re-rendered docs
   together, one commit per review session, message like
   `Review flags: brant 2026-06-17 technical (STREET_TYPE restyle)`.

## Hard rules

- Never delete or rewrite a ledger entry's identity fields; reviewed history
  is the calibration record for the signatures.
- Never weaken thresholds in `src/flags.py` to make a queue go away; a city
  that flags weekly has a config problem — fix it with `city-tune`.
- A verdict changes what the public site shows. When genuinely torn between
  `business` and anything else, hold (leave open) — a real story delayed
  beats a fabricated story published; every mass event reviewed before this
  system existed (51 of them) turned out to be a non-story.
