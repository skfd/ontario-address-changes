# Research notes — County of Perth, 2026-09

Raw findings behind `articles/researched/perth-county-2026-09.md`. Notes, not prose.
Window: snapshots 2026-08-20 → 2026-09-08 (one snapshot inside the month). 30 pull days
in September, 0 failed. Research done 2026-10-23. First article for this city (the
layer was first read 2026-08-20).

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found.

No open flag for perth-county (`python run.py flags`); nothing HELD in the brief.

---

## 0. Store-side findings

Vault catalog (`~/Code/.address-cache/catalog.db`): sha 83f4681875 (18,605 features) every
day 08-20 → 09-07; sha e547e63f42 (18,701) from 09-08 through 10-01. So the County
published exactly one change in the window, first read 8 September; the file then stood
still for the rest of the month.

Net 08-20 → 09-08: rows 18,605 → 18,701 (+96); added 112, removed 16, modified 18;
gross = net.

Identity is synthesized from Full_Add + rounded lon/lat (`datasets/perth-county.toml`),
so a point that moves reads as a removal plus an addition.

Of the 16 "retirements":
- 12 are the same address re-keyed after its point moved: 34 Clayton St (23 m), 101 and
  103 Clayton St (6 m each; they shared roll …506620 at one point, now separate points,
  103 on a new roll …506632), 91 and 93 Kenton St (14 m; were one point on roll …506604,
  now two points, 91 on new roll …506634), 6077 Frank St (21 m), 230 Ontario Rd
  (105 m), 7003 Raymond Dr (43 m, roll changed), 693 and 695 Conners Dr Units A/B (7–9 m).
- 1 is a street change on the same point and roll: 6604 LINE 66 → 6604 ROAD 154
  (North Perth, roll 314036000513400, 0 m). Brief does not count it as a rename or
  renumber because identity changed.
- 3 are suffix splits, parent retired on the same snapshot: 135 Pugh St → 135A/135B
  (Perth East, same point, same roll); 6675 Perth Line 86 → 6675A/B (North Perth, same
  point, same roll); 7568 Road 154 → 7568A/B (North Perth, same point, same roll).

So **99 addresses new to the file**, 3 genuinely gone (the split parents): 99 − 3 = 96 ✓.

New addresses by township (`Inc_Muni`):
- West Perth 86: Arend St 28, Rose Lane 28, Napier St 24 (Units A/B on 7–29 odd),
  Clayton St 36/38/40, Nelson St 28/30, 6962 Line 19.
- North Perth 10: 8358C/D Fairlane Rd, 6675A/B Perth Line 86, 7568A/B Road 154,
  6267 Line 89, 5054 Line 92, 6750 Perth Road 147, 8849 Road 146.
- Perth East 3: 135A/B Pugh St, 4195 Line 52.
- Perth South 0.
Net by township: West Perth +86, North Perth +8, Perth East +2, Perth South 0.

The 18 "modifications" are all `Property_Number` (assessment roll) changes on unchanged
points: 12 on William Shakespeare St 2234–2247 (Perth East; rolls 311001000114803–810
replaced by 311001000114812–819, pairs of numbers still sharing a roll), 137A/B Pugh St, 4699 and
6856 Line 26, 5211 Line 71, 3276 Perth Road 130. Paperwork on the roll, not addresses
changing. Not worth more than a line.

Stratford and St. Marys are not in this layer (separated cities).

## 1. The Frank–Napier–Clayton–Nelson block, Mitchell (West Perth) — LEAD

Store: all first on 09-08. Arend St 6–32 plus 34 (28 numbers; no 1–5, no 33); Napier St
7–29 odd, each with Unit A and Unit B (24 units); no plain 7…29 Napier ever on file
(parent "none"). Clayton St 36, 38, 40 new; Nelson St 28, 30 new. 34 Clayton moved 23 m.
Napier units on rolls 313026000505381–392 (12 consecutive, one roll per number, A and B
share). Arend rolls 3130260005053xx, also consecutive; 29 and 31 Arend, 34–40 Clayton
and 28/30 Nelson carry roll 313026000505300 (INFERENCE: the parent parcel's roll, not yet
split). Arend runs ~220 m. `--near 20 AREND STREET`: 17 Napier St Unit B 37 m, 20 Nelson
St 92 m, 40 Clayton St 111 m, 6077 Frank St 141 m.

- **FACT** — StratfordToday Staff, "61 new homes coming to Mitchell", 1 June 2023:
  Perth County council received a recommended plan of subdivision; "a currently-empty
  lot between the streets of Frank, Napier, Clayton and Nelson"; "37 lots for single
  detached dwellings, 12 lots for 24 semi-detached dwellings and a new municipal street";
  Phase 1 the 37 singles, Phase 2 the 12 semi lots; staff report estimated $650,000
  detached / $550,000 semi, "these units will not be attainable for either a moderate- or
  low-income household"; 9.4 acres, cash crops; no sidewalks on surrounding streets.
  https://www.stratfordtoday.ca/local-news/61-new-homes-coming-to-mitchell-7085455
  (direct fetch 403s; read via r.jina.ai proxy, archived 2023-06-09 on the Wayback
  Machine). Confidence: high on the text.
- **INFERENCE** — 12 Napier numbers × Units A/B = 24 exactly matches "12 lots for 24
  semi-detached dwellings". Arend + Clayton 36–40 + Nelson 28/30 = 33 new numbers vs the
  plan's 37 detached lots; can't reconcile (34 Clayton pre-existed; plan may have
  changed). Print the counts side by side, don't claim a match for the singles.
- **INFERENCE** — The plan's "new municipal street": Arend is the only street name new
  to the file on this block. Don't claim it IS that street.
- Plan named the phases singles-first; the file issued both at once. Nothing says what
  is built.
- **EMPTY** — "Arend Street" Mitchell: no naming by-law, no origin of the name found.
- **EMPTY** — 2023 draft plan file number / registration date: not found. Perth County's
  current-applications PDFs for other Mitchell plans (WP 25-01 Clarke at 34 Nelson St,
  19 singles + 15 townhouses; WP 25-02 Parkwood "Mitchell Ridge") are separate,
  later applications; the Clarke PDF URL now 404s. Not this block. Not used.

## 2. Rose Lane and 230 Ontario Road, Mitchell (West Perth)

Store: Rose Lane 10–33 plus 35, 37, 39, 41 (28), all 09-08, spread ~140 m. Rolls
313026000307501–528, i.e. children of 230 Ontario Road's roll 313026000307500.
230 Ontario Road itself moved 105 m to sit 16 m from 10 Rose Lane. `--near 20 ROSE LANE`:
238 Ontario Rd 37 m, 5878A Line 34 143 m, 129A Mitchell Court 148 m.

- **EMPTY** — "Rose Lane" Mitchell / "230 Ontario Road" Mitchell / condominium plan on
  Ontario Road: nothing public found. Geocoder.ca and listings silent.
- Not used: a REW listing for "Mitchell Lands" (8 acres, R4 for 216 stacked townhouses,
  R4 approved 20 Apr 2026 per a search summary) names no street; can't tie to Rose Lane.

## 3. Smaller items (record silent on all)

- 135 Pugh St (Perth East) → 135A/135B same point same roll; 137A/B next door already
  existed. EMPTY.
- 6675 Perth Line 86 and 7568 Road 154 (North Perth) → A/B on the same point. EMPTY.
- 8358C/D Fairlane Rd new (North Perth). EMPTY.
- 6604 Line 66 → 6604 Road 154, same point. EMPTY.
- Not searched further: single rural numbers (Line 19, 52, 89, 92, Perth Road 147,
  Road 146).
