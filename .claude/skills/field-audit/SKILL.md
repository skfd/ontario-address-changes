---
name: field-audit
description: Audit which source fields (tags) a city's change detection compares vs ignores, across the full snapshot history, and propose/apply an ignore_fields + keep_fields list. Use when a city's reports show mass "Updated Addresses" events with no real address change, when a humanized category (Location Adjustments, Renumbered, Street Renames) never fires, when a source adds or drops a field, or on any request to review a city's tracked/ignored fields.
---

# Field audit

Decide what `ignore_fields` / `keep_fields` a city in `datasets/<slug>.toml` should carry,
based on what its fields actually did across every snapshot — not just the latest one.

A field that appeared for one day and vanished still poisoned two reports. Always audit
the full history.

## 1. Read the current config

`datasets/<slug>.toml` — note `[fields]` (the canonical mapping), `[classes]`, and any
existing `ignore_fields` / `keep_fields`. Reports render the ignore list verbatim, so
"Ignored — None; every source field is compared" means nothing is filtered.

## 2. Run the audit

```
python .claude/skills/field-audit/audit.py <slug>
```

Prints the full tag inventory (with `<- GONE after`, `<- appeared`, `<- intermittent`
annotations), a per-field churn tally (`touched` vs `solo`), the top co-change combos,
and per-day tallies. Seconds for a mid-size city; a few minutes for Toronto.

Two caveats on reading it:
- Keys already in `ignore_fields` when a snapshot was imported are absent from that
  snapshot's stored props, and ignored keys are filtered out of the churn tally. The
  audit shows the picture under *today's* config.
- `OBJECTID` and friends never appear: `normalize._VOLATILE_KEYS` and
  `EDIT_METADATA_FIELDS` strip them for every dataset. Don't re-list them per city.

## 3. Cross-check the live source roster

Confirms whether a vanished field is really gone upstream (vs a truncated pull):

```
python -c "import json,urllib.request;d=json.load(urllib.request.urlopen('<data_url>?f=json',timeout=60));[print(f['name'],'|',f.get('alias')) for f in d['fields']]"
```

ArcGIS **aliases are the best evidence of a field's meaning** — Guelph's `ROLL_NO`
turned out to be "Roll Vailtech" (tax system key) and `PIN` "Teranet PIN" (land
registry), which is what justified ignoring them. For `access = "static"` cities,
inspect a downloaded snapshot in `data/<slug>/` instead.

## 4. Classify each field

Ignore:
- **Fields the source dropped or briefly added.** Every roster change re-hashes every
  row and fakes a 100%-of-dataset mass event.
- **Coordinate duplicates** (`LAT`/`LONG`/`UTM_X`/`UTM_Y`/`Xcoord`/`Ycoord`). The
  geometry is already tracked as `latitude`/`longitude` at 5 dp, and these carry more
  precision, so they also fire on sub-metre jitter the rounding is meant to absorb.
- **Derived echoes of the mapped canonical fields** — a legacy/abbreviated full address,
  a map label, street-name components. `diff.field_changes` suppresses the *directly*
  mapped source names only (`[fields]`), so companions still surface as extra rows.
- **Foreign-system join keys** rekeyed in batches upstream (parcel / assessment / permit
  ids). Put these in `keep_fields` too if a consumer might need them: stored in props,
  never compared.

Keep comparing: status, place/ward, postcode, unit flags, qualifiers, landmark and
occupant names, and any date field that is real address data rather than edit metadata.

**The classification bug worth hunting.** `report._category` files a row under a
humanized category only if its *entire* changed-field set fits that category
(`{latitude, longitude}` for Location Adjustments, `[classes]` entries for the rest).
One tag-along echo demotes the row to a generic "Updated Address". Guelph's Location
Adjustments counter had never once fired in 3 months because `LAT/LONG/UTM_X/UTM_Y`
rode along with every move. If a city shows 0 in a category that should be firing,
suspect echoes before anything else.

## 5. Propose, then apply

Present the inventory + churn numbers and the proposed list, and let the user choose the
scope — the dead fields and coordinate duplicates are clear-cut, the join keys are a
judgment call. Then edit `datasets/<slug>.toml`, commenting *why* each entry is there
with the evidence (see `guelph.toml`, `toronto.toml`). `keep_fields` entries must also
be in `ignore_fields` or `registry.load` raises.

```
python -m pytest tests -q
python run.py report --city <slug>
```

`generate_all` rebuilds every historical report from the DB, and `ignore_fields` is
applied at report time — so **the fix is retroactive without re-importing**, which
matters because raw snapshots are pruned. Verify by re-reading the affected reports
(strip `<style>`/`<script>`, then tags) and confirming the mass-event days now show
0 changes and the real one-off changes survive.

Two things to tell the user afterwards:
- **One-time SCD-2 churn.** Ignored keys stop being written to props, so on the next
  import every row's `payload_hash` changes once and a new version range opens for the
  whole city. Reports stay clean. `tools/backfill_props_hash.py` deliberately does not
  re-apply `ignore_fields` to stored history.
- Fields ignored after they vanished upstream stay listed in each report's "Ignored"
  section, since the list renders `ds.ignore_fields` unconditionally.
