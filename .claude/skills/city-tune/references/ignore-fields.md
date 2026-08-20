# ignore_fields / keep_fields

What change detection compares. A field left in means every wobble it makes is reported
as an address change.

## Reading `audit.py --tags`

- **inventory** — every prop key ever stored, with the date range it covers. Annotations:
  `<- GONE from the source`, `<- appeared mid-history`, `<- intermittent`.
- **churn** — `touched` (modified rows the field appeared in) vs `solo` (rows where it
  was the *only* change). Solo is what the field costs on its own; touched-minus-solo is
  how often it rides along with something else, which is the echo signal.
- **combos** — which fields move together. A field that never appears alone is derived
  from something else.

Caveats: a key already in `ignore_fields` when a snapshot was imported is absent from
that snapshot's props and filtered out of the churn tally, so the audit shows the picture
under *today's* config. And `OBJECTID`, `GLOBALID`, `SHAPE_*`, `_id` and the edit-metadata
timestamps never appear at all — `normalize._VOLATILE_KEYS` and `EDIT_METADATA_FIELDS`
strip them for every dataset. Never re-list those per city.

## What to ignore

- **Fields the source dropped or briefly added.** A roster change re-hashes every row and
  fakes a 100%-of-dataset mass event. Guelph: `STATION_RESPONSE_ORDER` existed in exactly
  one pull (2026-07-24) and cost two reports 53,796 and 53,795 fake updates; `AMAID`
  disappeared on 2026-08-04 for another 53,796.
- **Coordinate duplicates** — `LAT`/`LONG`/`UTM_X`/`UTM_Y`/`Xcoord`/`Ycoord`, including a
  pair reprojected into the layer's own CRS (kitchener's `X_COORD, Y_COORD` are the
  geometry in UTM 17N metres). The geometry is already tracked as `latitude`/`longitude`
  rounded to 5 dp; these carry more precision, so they also fire on the sub-metre jitter
  the rounding exists to absorb. What that costs the city depends on `[identity]` — see
  below.
- **Derived echoes of the mapped canonical fields** — a legacy or abbreviated full address,
  a map label, street-name components. `diff.field_changes` suppresses only the *directly*
  mapped source names from `[fields]`; companions still surface as extra rows on every
  rename or renumber. Guelph's `ADDLEG` (Legacy Address) and `LABEL` (number+unit map
  label); Toronto's `LINEAR_NAME*` and `LO_NUM`/`HI_NUM` families.
- **Foreign-system join keys** rekeyed in batches upstream — parcel, assessment, permit
  ids. Guelph's `PIN` (Teranet), `GPID` (Parcel ID) and `ROLL_NO` (Vailtech tax roll)
  produced 1,215 solo "updated address" rows carrying no address change.

Keep comparing: status, place/ward, postcode, unit flags, qualifiers, landmark and
occupant names, and any date field that is real address data rather than edit metadata.

## Which noise pattern to expect, from `[identity]`

A coordinate duplicate does one of two things, and `[identity]` says which before you
look (six for six across the 2026-08-08 audits):

- **Synthesized identity with `use_geometry`** — the 5 dp geometry is *in* the key
  (`normalize._identity`), so a real move past ~1.1 m mints a new key and reports as
  retired + added, never as a modification. `report._category` only ever labels a
  *modified* row, so Location Adjustments is structurally unreachable for these cities
  and its 0 is correct. A duplicate here can only **manufacture** updates that no real
  move underlies — the *phantom* pattern (hastings, quinte-west, burlington, renfrew;
  elgin predicted).
- **A real `key_field`** — moves arrive as modifications, so the duplicate rides along
  with them and demotes them to generic updates: the *masking* pattern (guelph,
  kitchener; peel-region `ROPADRID` and waterloo `ADDRESS_ID` predicted).

Within the phantom half, only the churn tally separates two mechanisms — and it decides
whether the field is worth pre-emptive ignoring:

- **Faithful echo** at finer precision than the 5 dp compare (hastings; burlington's
  worst deviation 1.35e-5 deg over 60,326 rows). Moves only on jitter. Low cost.
- **Stale copy** that drifts free of the geometry and fires whenever the publisher
  re-syncs it. Worth ignoring before it bites: renfrew's `Latitude, Longitude` had
  wandered 6.7e-3 deg (~530 m) on 720 rows before the county recomputed them, and the
  re-sync alone produced 1,547 updates with the geometry standing still.

`audit.py --coords` measures this: it finds the pair by name, works out whether it is
geographic or projected (fitting the CRS and reporting which one, so a wrong guess cannot
pass), and prints the deviation from the geometry across five snapshots.

Read the **p99**, not the max. A stale copy has a *bulk* of drifted rows, which is what
makes the publisher's re-sync a mass event — renfrew p99 16.7 m, quinte-west 439 m. A
faithful echo sits near the floor even when a few rows are wild: guelph shows 315 rows
over 11 m against a p99 of 6.8 m, hastings 13 against 1.6 m, and those are individually
broken rows, not drift. The floor is ~1–2 m, not zero: the geometry is stored at 5 dp and
the source pair often carries a NAD83/WGS84 datum offset on top.

Five snapshots, not just the latest, because a stale copy reads clean the day after a
re-sync — renfrew's had wandered 797 m on 2026-06-15 and was back within 2.4 m by 06-29.

Two things it surfaces that are worth a look on their own: **two CRSs in one column**
(elgin's `x`/`y` — 18,716 rows of degrees, 2,720 of UTM 17N metres) and rows that fit no
CRS at all, reported as `unmeasurable`.

A city can publish more than one pair, in which case they are paired within a family —
geographic names together, projected names together — never by position. Dufferin
publishes `LONGITUDEX`, `LATITUDEY`, `EASTINGX` and `NORTHINGY` at once, and pairing its
two x-names against its two y-names in order matches an easting against a latitude.

This narrows what to look for; it does not replace `audit.py --tags`, which is still
what shows whether the duplicate has actually moved.

## Location jitter (`location_min_move_m`)

`ignore_fields` cannot touch `latitude`/`longitude` — they come from the geometry, not
props. The lever for coordinate noise is the per-city `location_min_move_m` (top-level
TOML key, metres, 0/absent = off): `compute_diff` drops a modification whose only
changes are latitude/longitude when the move is under the floor. Moves at or above it
still publish, as does any location change riding with another field — so it is a noise
floor, not a location mute.

Calibrate it from what the sweeps actually measure, not a default: toronto 50 (the
export oscillates between two geocode sets, identical old→new transitions recurring
months apart), brampton/kingston/guelph/niagara-falls 25 (sub-parcel cartographic
maintenance, 1–15 m), muskoka 2 (republish wobble ≤1.36 m; real re-surveys travel
5–110 m and still publish). Cities whose location sweeps are genuine repositioning
programs (leeds-grenville, sdg: 30–110 m structure snapping) take no floor — those
publish as collapsed Location Adjustments. Report-time only: no re-hash, no SCD-2
churn, retroactive across the archive on the next render.

## keep_fields

For a field that should not drive change detection but must survive into `props` for a
downstream consumer. Ignored keys are otherwise dropped at import
(`normalize._clean_props`). Every `keep_fields` entry must also appear in `ignore_fields`
or `registry.load` raises. Kept fields are excluded from `payload_hash`, so their churn
cannot open a new SCD-2 range. Precedents: Guelph's three parcel/tax keys (the only link
from an address to the land registry and tax roll); Toronto's `ADDRESS_CLASS_DESC` and
`LO_NUM`/`HI_NUM` (needed by the OSM import's range safety gate).

## The classification bug worth hunting

`report._category` files a row under a humanized category only if its *entire* changed
set fits that category — `{latitude, longitude}` for Location Adjustments, the
`[classes]` entries for the rest. One tag-along echo demotes the row to a generic
"Updated Address". Guelph's Location Adjustments counter had never once fired in three
months because `LAT/LONG/UTM_X/UTM_Y` rode along with every move: 2026-06-25's 520
genuine coordinate moves were reported as 771 generic updates. **If a city shows 0 in a
category that should be firing, suspect echoes before anything else** — except for
Location Adjustments on a synth + `use_geometry` city, where 0 is structurally correct
and not a config bug (see above). Say so rather than "fixing" it.

## Applying

Comment *why* each entry is there, with the evidence — see `datasets/guelph.toml` and
`datasets/toronto.toml`. Group the entries by reason rather than listing them flat.
Then `python run.py report --city <slug>` and verify; the fix reaches the whole archive.
