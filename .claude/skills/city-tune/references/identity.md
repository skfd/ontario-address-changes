# [identity]

The identity key is what the SCD-2 store is built on: same key + same `payload_hash` =
unchanged, same key + new hash = modified, key gone = retired. An unstable key turns
ordinary edits into retire-then-new pairs, inflates both counters, and permanently
splits an address's history.

**Settle this first, and settle it at onboarding.** Identity is resolved at *import*
time and does not reach back — changing it does not rewrite stored history, so the next
import retires every old key and adds every new one in a single report, and the city's
past is keyed one way while its future is keyed another.

## The two modes (`normalize._identity`)

- `key_field` — used when the source prop is present and non-blank on that row.
- Otherwise synthesized: `syn:` + sha1 over `synth_fields` (canonical names, uppercased)
  + `synth_props` (raw source props) + the 5 dp lon/lat when `use_geometry` (default true).

A `key_field` that is blank on some rows silently produces a mixed keyspace — those rows
fall through to the synthesized basis.

## Reading `audit.py --identity`

- **collisions** (`rows` minus `distinct` in the latest snapshot) — the key is 1:many
  with addresses. Non-zero means separate addresses are sharing a history.
- **flapped %** — keys that went absent and came back. Anything above a fraction of a
  percent means the key is not stable; the affected rows appear in reports as retired
  and re-added rather than modified.
- **keys vs rows, versions per key** — a history holding far more keys than the city has
  addresses is the signature of a key being re-minted. Muskoka's DB carries 224k keys for
  a 66k-row city with a 16.75% flap rate.

The audit reports these history-wide, so damage from *before* a config fix still shows.
Cross-check the `--tags` per-diff summary for when the add/remove spikes happened; if
they stop at a known date, it is scar tissue, not a live problem.

## Traps

- **Sequential ids are not identity.** `OBJECTID`, `FID`, `_id` are row sequence numbers
  reassigned on republish. They are in `_VOLATILE_KEYS` for props, but nothing stops a
  TOML from naming one as `key_field` — don't.
- **Geometry in the synth basis + a jittering source.** 5 dp is ~1.1 m. Muskoka's service
  jitters coordinates up to 1.36 m between republishes, which crosses that boundary: the
  2026-06-28..07-01 republish alone minted new keys for 28,250 of 65,279 addresses. The
  fix is `use_geometry = false` plus a `synth_props` disambiguator that is stable —
  Muskoka uses `PropertyNum` (an assessment roll, 1:many on its own, but the right
  tiebreak here at the cost of 279 collisions).
- **Untrusted copies.** A key is only as stable as the layer publishing it; a mirrored
  `*_exchange` copy can renumber independently of the official source.

## Verifying a candidate key

Against the latest snapshot: 100% populated, distinct count equal to row count, and a
value range that looks like a municipal id rather than a row sequence. Then check it
across snapshots — a key that is unique *within* a snapshot can still be reassigned
*between* them. Record the evidence in the TOML comment (Guelph's `ADDID` comment gives
population, uniqueness and observed range; that is the standard to match).
