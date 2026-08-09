# Source drift

`health.py --drift`. One `?f=json` per arcgis layer, comparing the live field roster and
copyright text against what the store actually holds. This is the only section that goes
to the network; it is a periodic chore, not part of triage.

It **feeds `city-tune` rather than deciding anything**. A field that appeared or vanished
is a config question. Report it, hand it over, stop.

## What each result means

- **UNREACHABLE** — URL rot. The layer moved or the service is gone. `TODO.md` §2 is the
  standing list of these; the recovery path is the municipality's own open-data page,
  provincial portals, or an email to the GIS department. Five of five originally-dead
  cities were eventually recovered, so re-probe rather than assume.
- **no field list in the layer json** — the service answered but errored. Kingston was in
  this state on 2026-08-08, matching three `ERROR (kingston)` lines in `update.log` — the
  two sections corroborating each other is the useful signal.
- **DROPPED** — a field we store is gone from the layer. This is the urgent one: a
  disappearing field re-hashes every row and fakes a mass event covering the whole city
  (guelph's `AMAID` cost one report 53,796 fake updates). `ignore_fields` it in
  `city-tune` before the next import, not after.
- **new (n)** — fields the layer publishes that we do not store. Mostly uninteresting,
  with three exceptions worth scanning for:
  - a **coordinate pair** (`X`/`Y`, `LATITUDE`/`LONGITUDE`) — a fresh duplicate that will
    start churning; run `audit.py --coords` and ignore it.
  - a **unit or full-address column** — several cities are recorded as "source publishes
    no unit field" and would be wrong if the source added one (`TODO.md` §1).
  - a **status, place or ward column** — a `[classes]` candidate.

Volatile ESRI ids, edit-metadata timestamps and anything already in `ignore_fields` are
subtracted, so what is listed is genuinely unstored.

## Two things that will mislead you

- **A frozen city accumulates drift that is not new.** Its store stopped in June, so
  everything the source added since reads as new. Check `--stale` first and read the
  drift of a frozen city as "what changed while we weren't looking", not "what changed
  today".
- **Static sources are not probed at all** (toronto, waterloo). `access = "static"` means
  a file download with no layer metadata to ask, so drift there has to be found by
  inspecting a file in `data/<slug>/`.

## Licence text

`copyrightText` is printed whenever it is not already contained in the TOML's
`license_name`. It is a hint, not an authority — plenty of layers carry a department name
there ("Planning Department", "Development & Emergency Services") rather than a licence.
The real licence lives on the publisher's portal page, which is what `TODO.md` §3 tracks
for the 15 cities currently recorded as "Not identified".

A licence that has genuinely changed matters for republication and OSM compatibility, not
for tracking, so it never blocks a run.
