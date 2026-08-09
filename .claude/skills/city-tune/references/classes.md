# [classes]

Routes a modification into a humanized section instead of the generic Updated Addresses
table, so one upstream bulk decision reads as one event rather than 50,000 rows.

Valid class names (`registry._VALID_CLASSES`, anything else raises):

- `status` — lifecycle flips: Active / Retired / Proposed / Under Construction.
- `boundary` — reassignment to a different area: ward, municipality, place, service zone.
- `place_name` — the place or landmark *name* itself changing (hastings `Landmark_Name`,
  peterborough-county, toronto).

The built-in categories need no config: Location Adjustments (`{latitude, longitude}`),
Renumbered (`{number, full}`), Street Renames (`{street, full}`).

`full` changing **alone** is read against the field map (`report._category` takes
`has_number` / `has_street`): a renumber only where no `number` is mapped (waterloo), a
rename only where no `street` is (lennox-addington), and otherwise a generic update —
because with both components mapped and neither moved, the publisher is restyling the
string. Before that rule landed (2026-08-08) full-only counted as Renumbered everywhere,
which mislabelled renfrew's 1,104-row highway restyle ("17883 Highway 60" → "17883 60
Highway") plus restyles, backfills and spelling fixes in brantford, frontenac, barrie and
thunder-bay. **A category firing on a city whose source cannot produce it is the same
class of bug as one stuck at 0** — check both directions.

## The subset rule

`report._category` assigns a class only when the row's **entire** changed-field set fits
inside it. Built-ins are tested first, then each `[classes]` entry; any mix falls through
to `significant` (the generic table).

Two consequences:

1. **Ignore before you class.** A tag-along echo defeats the subset test, so a class can
   sit at 0 forever while the events happen. Clean the echoes first
   (`references/ignore-fields.md`), then class.
2. **Don't over-group.** Putting two unrelated props in one class means a row touching
   both still classes — occasionally right (`boundary = ["PLACE", "WARD"]` in Guelph,
   where a reassignment moves both), usually not.

## Reading `audit.py --classes`

Lists low-cardinality props (≤25 distinct values in the latest snapshot) with their fill
rate, their values, whether they are already classed, and — when `--tags` also ran — how
many times each changed *alone*. A good candidate is low-cardinality, well-filled, and
has solo changes. A field with high `touched` but zero `solo` is an echo, not a class.

Sample the real values before choosing; the standing TOML comment
("field values verified against the latest snapshot") is a promise that someone did.

## How it renders

- `status` and `boundary` go through `_group_transitions`: rows are grouped by their
  exact old→new signature and shown once with a count, since one upstream decision covers
  many addresses.
- Street renames group the same way via `_group_renames`.
- Sections still collapse to a summary when one event dominates — `report.MASS_MIN_SHARE`
  (0.25) of the section.

## Consequences of changing it

`[classes]` is applied at report time, so `python run.py report --city <slug>` reclassifies
the entire archive. No import, no re-hash, no SCD-2 churn. It is the cheapest and most
reversible change in this skill.
