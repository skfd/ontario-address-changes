# priorart — the tracker measured against the prior art

Who else holds Ontario's addresses, and how do they compare with this tracker on
**coverage** (which municipalities, how many rows), **cadence** (how often the data
actually moves), **quality** (field fill) and **licence** (what each party recorded)?

Back-office. The report is `report.html` here, not under `docs/`; it makes measured
claims about third parties' data and the method is still under review.

## Comparators

`comparators.csv`, one row each:

| id | what | measured how |
|---|---|---|
| `ours` | this repo | active rows of the latest non-skipped snapshot in `data/<slug>/<slug>.db`; snapshots in the last 30 days |
| `oa` | [OpenAddresses](https://github.com/openaddresses/openaddresses), 85 Ontario source files, 84 with an `addresses` layer (Mississauga's lists buildings and parcels only) | `batch.openaddresses.io` per-job `count`, `stats.counts`, job history; source JSON licence. Point outputs need a login, so OA is measured per source, not per municipality |
| `oda` | StatCan Open Database of Addresses v1 (2021) | `ODA_ON_v1.csv` counted once by `csdname` and `provider`; `Data_Sources.csv` for licence and download date |
| `nar` | StatCan National Address Register | each vintage under `../prototype-nar/data/<YYYYMM>/Address_35_part_*.csv`, counted by `CSD_ENG_NAME` |
| `overture` | Overture Maps addresses theme | latest release on S3, Ontario bbox, `country='CA'`, pulled with DuckDB (bbox pushdown; ~20 s) and binned by polygon |

## The key: municipality

Everything is compared per **lower- or single-tier municipality**, named as LIO's
"Municipal Bnd Lower And Single" layer names it (`MUNICIPAL_NAME_SHORTFORM`, uppercased,
accents and periods stripped: `muni.norm_name`). Points (ours, Overture) are binned by
point-in-polygon; name-keyed sources (NAR, ODA) are resolved by name, then by
`muni_aliases.csv` (hand: `alias,municipality`). Reserves and unorganized territories
have no polygon and show as "(outside any municipality)"; a *municipality* name landing
there means an alias is missing.

Where two municipalities share a short name the counts merge and the report tags the row.

## Join tables (hand-kept)

- `oa_sources.csv`: OpenAddresses source -> `our_slug`, with `match` in
  `same-url` (byte-identical endpoint), `jurisdiction` (same body, different layer or an
  OA cache zip), `covered-by` (a member municipality our county/region layer covers),
  `none`. Seeded 2026-10-16 from a URL match; the 29 non-URL matches were filled by hand.
  `measure.py oa` joins on it; a new OA source shows up with no row and must be added.
- `muni_aliases.csv`: comparator spellings that are not LIO's.

## Outputs

- `measures.csv` — append-only, `source_id,measured_on,measure,value,of,unit,method,text`.
  Idempotent per day. Source ids: `ours:<slug>`, `oa:<source>`, `oda:<provider>`, `oda`,
  `nar:<vintage>`, `nar`, `overture:<release>`, `overture`. Measures: `rows`,
  `unit_fill`/`street_fill`/`number_fill`/`postcode_fill` (value of rows), `last_success`,
  `days_stale`, `runs_365d`, `rows_vs_ours`, `snapshots_30d`, `distinct_content_30d`,
  `last_snapshot`, `tracked_since`, `unbinned_rows`, `vintages`, `releases`, `providers`.
- `coverage.csv` — regenerated per comparator (and vintage): `municipality, comparator,
  vintage, source, rows, unit_filled, street_filled, number_filled, postcode_filled`.
  For `ours` the report takes the **max** per municipality across our datasets, because a
  region layer and its member's layer both hold the member's addresses.
- `licences.csv` — per dataset: our `license_name` and `osm_compatible`, OA's licence text
  and URL for the joined sources, the ODA provider's licence title and download date. The
  ODA provider is matched by normalized provider name first, else by coverage: the provider
  whose 2021 rows fall most heavily in the municipalities our dataset covers
  (`oda_match` says which).
- `report.html` — all of the above, rendered.

## Run

```bash
python priorart/measure.py all                 # pull, measure, render
python priorart/measure.py oa --offline        # reuse cached OA pulls
python priorart/measure.py overture --release 2026-09-23.1
python priorart/measure.py render
```

Weekly is the useful cadence: OpenAddresses batches weekly, Overture releases monthly,
the NAR twice a year, the ODA never. Not wired into `daily-update.ps1`.

Needs `duckdb` and `pyarrow` on top of the repo's requirements (Overture only), and the
NAR vintages extracted under `prototype-nar/data/` (otherwise `nar` is skipped). Raw pulls
go to `cache/` (gitignored): the LIO polygons (20 MB), the ODA zip (160 MB), OA batch
JSON, NAR and ODA counts, one Overture parquet per release (19 MB).

## Known limits

- OpenAddresses point outputs are behind a login, so OA coverage per municipality is not
  measured; the per-source join stands in for it. Register an account to lift this.
- NAR and ODA bin by census-subdivision name, not by polygon; the two agree for
  municipalities but a CSD can straddle nothing we know about (e.g. a reserve) and lands
  in the unbinned bucket.
- "Unit fill" says as much about the source as the pipeline; compare within a
  jurisdiction, not across the quality table's columns.
- Overture's `address_levels[2]` for Canada is the postal municipality (NORTH YORK,
  SCARBOROUGH), which is why Overture goes through the polygons, not the names.
