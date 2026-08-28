# Verifying a claim before it goes in print

The brief is an aggregate. Every *specific* thing the article says — an address, a
street, a date, a before/after — gets checked against the store first. A local reader
knows their own street better than the dataset does, and a wrong detail costs the
whole piece its credibility.

## The lookup

```
python .claude/skills/monthly-article/lookup.py toronto --addr "6 Shorncliffe Rd"
python .claude/skills/monthly-article/lookup.py toronto --street "Shorncliffe Rd"
python .claude/skills/monthly-article/lookup.py toronto --place "Kennedy Station"
python .claude/skills/monthly-article/lookup.py toronto --street "Queen St E" --month 2026-03
```

Each line is one row version and the snapshot span it was valid for, so
`2026-03-26 .. present` means the row first appeared on the 2026-03-26 snapshot and is
still on file. `--props` dumps the source properties and the identity key.

## What to check, per claim type

**A split** (`6 Shorncliffe Rd` → `6A`–`6E`). Look the *street* up, not the address:
confirm the children all start on the same snapshot, and look for the parent. The
brief's `parent` column says `retired` / `remains` / `none`, and the three mean
different things in the world:

| parent | What the record shows | Safe wording |
|---|---|---|
| `retired` | base address ended on the same snapshot the children began | "the old address came off the file the same day" |
| `remains` | base address is still active alongside the children | "the original address is still there" |
| `none` | no base address was ever on file | "no plain *6* was ever on the file" — **not** "the house was demolished" |

**A street rename.** The brief groups by (old → new). Check whether the change is
physical or editorial before writing it up: `McCaul St` → `Mc Caul St` is a string
being restyled by whoever maintains the centreline file, not a street being renamed.
The tell is the shape of the change (spacing, punctuation, abbreviation, direction
suffix) and the count — an editorial restyle hits every address on the street at once.
Say "the file restyled the name", and check whether it reverts in a later month.

**A new street.** `new_streets` reports the first snapshot on which any address carried
that street name. That is a *record* debut. Confirm it looks like a real new road (a
handful of addresses appearing together, plausible suffix) rather than a spelling
variant of an existing street — search the street list for near-matches:

```
python -c "import sqlite3;c=sqlite3.connect('data/toronto/toronto.db');print([r[0] for r in c.execute(\"select distinct street from addresses where street like '%Lane%'\")][:40])"
```

**A retired address.** Check it stayed retired. Toronto's export has dropped and
restored rows before; a row with a later span starting again is churn, not a demolition.
The lookup shows every span, so a row that comes back is visible at a glance.

**A renumbering.** Confirm the old number is not simultaneously present as a separate
row (that is a range being restated, not a renumber) and note whether `ADDRESS_NUMBER`
went to a range like `282-310`, which is the file recording a whole frontage rather
than a building moving.

**A place name.** `--place` searches the props. A name going to `None` means the label
was removed from that point, which usually means a layer was re-joined upstream, not
that a park closed. Check whether the same name reappears on another point in a later
month before writing that anything was lost.

## Cross-checking outside the file

The address file records paperwork. When the article wants to say *why*, the file
cannot tell you and neither can this repo. Either attribute the cause to a source that
does know (a city notice, a development application, a council decision) with a link,
or write the sentence without a cause. There is no third option that is honest.

## Numbers

Before publishing, re-run the brief and confirm every figure in the draft still matches
it. A re-render or a config change (an `ignore_fields` edit, a new `location_min_move_m`
floor) legitimately moves the numbers, and an article is a snapshot of what the tracker
believed on the day it was written. If a published article's numbers have since moved,
add a dated note at the bottom rather than silently editing the figures.
