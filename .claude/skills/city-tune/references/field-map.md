# [fields]

Maps source props to the four canonical display fields: `number`, `street`, `unit`,
`full`. Unmapped props are not lost — they stay in the props blob and are still compared
for changes.

## What the mapping actually controls

- **Report display and ordering.** `diff.addr_sort_key` sorts by street, then number
  numerically. A city with no `street` mapped sorts as one undifferentiated block.
- **The `full` fallback.** With no `full` selected, reports render "number street", which
  omits units. Prefer a real full-address column when the source has one.
- **Two built-in categories.** `report._category` keys Renumbered on `{number, full}` and
  Street Renames on `{street, full}`. Neither can fire for a slot that is not mapped.
- **Echo suppression.** `diff.field_changes` drops a source prop's change when it is the
  *directly mapped* source of a canonical field that also changed. Mapping the right
  column therefore silences its duplicate for free; near-duplicate companions (a legacy
  address string, a label) still need `ignore_fields`.
- **Synthesized identity.** `synth_fields` names canonical fields, so for a city with no
  `key_field`, changing `[fields]` changes every identity key. Treat it as an identity
  change — see `references/identity.md`.

## Reading `audit.py --fields`

Prints fill rate per mapped slot against the latest snapshot, and for any unmapped slot,
every prop with its fill rate and sample values so a candidate can be picked on evidence.

Rules of thumb:

- **Never map a column that is blank.** Frontenac's `UnitNumber` is 100% empty across
  22k rows — mapping it just puts an empty column in every report. Either leave it
  unmapped or note in the TOML that the source publishes none.
- **A low fill rate is not a disqualifier for `unit`** — 10-30% is normal, since most
  addresses have no unit. It *is* a red flag for `number`, `street` or `full`.
- **Prefer parsed columns over parsing.** If the source only publishes a combined string
  (Waterloo's `CIVIC_ADDR`), that is a human decision: accept full-address-only display,
  or add parsing. Don't invent a parser unasked.

## Open decisions

`TODO.md` §1 tracks the cities whose field map is still unresolved, with a per-city
coverage table (row counts and fill percentages for all 42). Update that table when a
mapping lands.

## Consequences of changing it

`[fields]` is resolved at import time. Existing rows keep the display values captured
when they were imported; the next import re-hashes every row once (one-time SCD-2
churn), and for synthesized-identity cities re-keys the entire store. Reports for past
snapshots keep showing the old display values, because they are rebuilt from stored rows.
