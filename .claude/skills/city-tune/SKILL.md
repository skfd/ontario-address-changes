---
name: city-tune
description: Tune a city's datasets/<slug>.toml against what its snapshot history actually shows - identity key, field map, change classes, and ignore/keep fields - or onboard a new source. Use when reports show mass "Updated Addresses" events with no real address change, when a humanized category (Location Adjustments, Renumbered, Street Renames, Status, Boundary) never fires, when a source adds or drops a field, when addresses churn as retired-then-new, when a field map or unit/full-address column is unselected, or on any request to review, audit, or configure a city's tracked fields.
---

# City tune

Every decision in `datasets/<slug>.toml` is the same job: look at what the source has
actually done across the whole history, change the config, regenerate, verify. This
skill is that loop. The per-decision detail lives in `references/`; read only the one
you need.

Never decide from the latest snapshot alone. A field that appeared for a single day and
vanished still faked a 53k-row mass event in two Guelph reports.

## The loop

1. **Read `datasets/<slug>.toml`.** `[identity]`, `[fields]`, `[classes]`,
   `ignore_fields` / `keep_fields`, and the comments — they carry why the last person
   chose what they chose.
2. **Audit the history:**
   ```
   python .claude/skills/city-tune/audit.py <slug>
   ```
   Sections: `tags` (inventory + churn), `identity`, `coords`, `fields`, `classes`.
   Narrow with `--tags` / `--identity` / `--coords` / `--fields` / `--classes`. `--tags`
   runs one diff per snapshot pair and dominates runtime — seconds for a mid-size city,
   minutes for toronto; the rest are single passes. A baseline-only city can still be
   audited with `--coords` / `--fields` / `--classes`, which need no diff.
3. **Cross-check the live source** when a field's meaning or existence is in question:
   ```
   python -c "import json,urllib.request;d=json.load(urllib.request.urlopen('<data_url>?f=json',timeout=60));[print(f['name'],'|',f.get('alias')) for f in d['fields']]"
   ```
   ArcGIS **aliases are the best evidence of meaning** — Guelph's `ROLL_NO` turned out
   to be "Roll Vailtech" (tax system) and `PIN` "Teranet PIN" (land registry), which is
   what justified ignoring them. For `access = "static"`, inspect a file in `data/<slug>/`.
4. **Read the reference for the decision at hand** (table below), then propose with the
   numbers attached and let the user pick the scope. Clear-cut cases (a field the source
   deleted, coordinate duplicates) and judgment calls (foreign-system join keys) should
   be offered separately.
5. **Apply and verify:**
   ```
   python -m pytest tests -q
   python run.py report --city <slug>
   ```
   Then re-read the affected reports (strip `<style>`/`<script>`, then tags) and confirm
   the noise days went quiet *and the real one-off changes survived*.
6. **If you edited `ignore_fields` or `keep_fields`, finish the job in the store** —
   before that city's next import, or it is only half-applied:
   ```
   python tools/backfill_props_hash.py --reapply-ignore --city <slug>
   ```
   The reports go quiet immediately (both are report-time filters) while the stored
   props and `payload_hash` still carry the old basis, so the next import re-hashes
   every row at once and opens a fresh SCD-2 range for the whole city. Skipping this
   step on 2026-08-08 left five cities in exactly that state — 282,583 rows, found
   only by measuring. Back the city's DB up first: the flag rewrites history and the
   values leave the store.

## Which reference

| Symptom | Read |
|---|---|
| Mass "Updated" events, echo rows, a category stuck at 0 | `references/ignore-fields.md` |
| Addresses churning as retired-then-new; duplicate or unstable keys | `references/identity.md` |
| A canonical slot unmapped, or mapped to a blank/wrong column | `references/field-map.md` |
| Bulk upstream decisions buried in the generic Updated table | `references/classes.md` |
| A brand-new source, or one that moved/died | `references/onboarding.md` |

Order matters when several apply: **identity first** (it is the only one that cannot be
fixed retroactively), then the field map, then classes, then the ignore list — each
later decision is evaluated against the earlier ones.

## Two things that hold for every change here

- **Report fixes are retroactive; stored history is not.** `ignore_fields` and
  `[classes]` are applied at *report* time (`diff.field_changes`, `report._category`),
  and `report.generate_all` rebuilds every historical report from the DB — so those two
  fix the whole archive without re-importing, which matters because raw snapshots are
  pruned. `[identity]` and `[fields]` are resolved at *import* time and do not reach
  back.
- **One-time SCD-2 churn on the next import.** Anything that changes what lands in
  `props` or in `payload_hash` re-hashes every row once, opening a fresh version range
  for the whole city. Reports stay clean, which is what makes this easy to miss.
  `tools/backfill_props_hash.py` does not re-apply today's per-city config by default —
  `--reapply-ignore` does, which is step 6 above and the only way to avoid the churn
  rather than merely hide it.

Always tell the user which of these applies to the change they just approved.
