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
- **Coordinate duplicates** — `LAT`/`LONG`/`UTM_X`/`UTM_Y`/`Xcoord`/`Ycoord`. The geometry
  is already tracked as `latitude`/`longitude` rounded to 5 dp; these carry more precision,
  so they also fire on the sub-metre jitter the rounding exists to absorb.
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
category that should be firing, suspect echoes before anything else.**

## Applying

Comment *why* each entry is there, with the evidence — see `datasets/guelph.toml` and
`datasets/toronto.toml`. Group the entries by reason rather than listing them flat.
Then `python run.py report --city <slug>` and verify; the fix reaches the whole archive.
