# Research notes — Stratford, 2026-10

Window: net 2026-08-20 -> 2026-10-29 (snapshots 10-09, 10-14, 10-28, 10-29; September had
none). 30 pull days, 0 failed. Rows 14,873 -> 14,887 (+14): 21 added, 7 removed, 5 splits.

## From the store (lookup.py)

- **16 Kastner St** — old point (43.39571, -80.98965) last seen 2026-10-09. On 2026-10-14 a
  new 16 Kastner St appears at (43.39594, -80.99015), roughly 45-50 m west, plus five points
  numbered `0 KASTNER ST` in a line from (43.39593, -80.98939) to (43.39541, -80.98983).
  All six new rows are still on file at 2026-10-29. On the 2026-11-05 snapshot (outside this
  window) the five `0` points are replaced by 6, 12, 18, 24 and 30 Kastner St at exactly the
  same coordinates. `--near 18 Kastner`: 0 Perth Line 36 at 50 m, 34-2 Orchard Dr at 86 m.
- **74 and 76 Church St, 227 St. Patrick St** — all three last seen 2026-08-20, gone on
  2026-10-09; 74-1..74-3 and 76-1..76-4 Church St appear 2026-10-09. The three old points and
  the new units sit within about 5 m of each other: one corner, Church at St. Patrick.
  `--near 74-1 Church`: 235 St. Patrick St at 37 m, 47 Birmingham St at 54 m.
- **64 Norfolk St** — parent gone 2026-10-09, Units 1-3 the same day. Next door: 90 Taylor St
  (15 m), 77 Perth St (38 m).
- **19 McKenzie St** — parent last seen 2026-10-14, Units 1-3 from 2026-10-28. Next door:
  67 St. David St (42 m), 18 Victoria St (51 m).
- **148 Rebecca St** — parent last seen 2026-10-28, Units 1 and 2 from 2026-10-29. Next door:
  192 Front St (18 m), 215 Brunswick St (40 m).

## From outside the file

- **16 Kastner Street — OPA2-25 / Z06-25.** Engage Stratford project page:
  https://engagestratford.ca/official-plan-amendment-opa2-25-and-zoning-by-law-amendment-z06-25-16-kastner-street
  Owner Countryside Developments (2014) Inc.; re-designate "the eastern portion of the
  subject lands, fronting Kastner Street" to allow "single detached dwellings", and "a four
  (4)-storey apartment building on the west half of the subject lands accessible from Perth
  Line 36". Submitted and deemed complete 22 Oct 2025; public meeting 8 Dec 2025; "Application
  Considered by Council" 26 Jan 2026 shown as the current stage. No lot count, no unit count,
  no decision or by-law number on the page. Confidence: high for what the page says.
- The December 8, 2025 planning report (pub-stratford.escribemeetings.com DocumentId=10316)
  and a 23 Feb 2026 council calendar item both refuse automated fetches (403); a search
  summary claims the report says staff wanted access from Kastner rather than Line 36 and
  that the zoning amendment was on the 23 Feb agenda. **Not verified — not used.**
  The notice PDF on stratford.ca now 404s.
- No source found saying whether council adopted the amendment, or that the five new
  Kastner points are the single-detached lots. The file's shape matches the layout the
  application describes; that is as far as the article goes.
- **74 Church Street** — sale listing (RE/MAX):
  https://www.remax.ca/luxury/on/stratford-real-estate/74-church-street-wp_idm73000004-26313616-lst
  describes a three-level multi-residential building at the corner of Church and
  St. Patrick. Several listings for "#1 - 74 Church Street" exist (e.g.
  https://realtris.ca/listings/X10780957/74-unit-1--church-street-stratford-stratford-on-n5a-2r2),
  but listing dates are unreliable, so no claim about the file lagging the market.
  Nothing found on 76 Church St or 227 St. Patrick St, or why the corner was re-addressed.
  Confidence: medium (a listing, not a City record).
- **64 Norfolk, 19 McKenzie, 148 Rebecca** — searched by address; nothing public found.
  The record is silent.
