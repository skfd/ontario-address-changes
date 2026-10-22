# Monthly articles

One newsletter piece per fully-observed calendar month, written from the tracker's own
snapshot history. Markdown, ready to paste into Substack.

Each month's piece sits in [`researched/`](researched/), with the raw findings behind it
(entity, what was found, URL, confidence; notes, not prose) in [`research/`](research/).

The same pieces are rendered to HTML on the live site at
[`/articles/`](https://skfd.github.io/ontario-address-changes/articles/) by
`tools/render_articles.py`, which the scheduled run calls before committing. The
research notes are not rendered; the site links to them here on GitHub.

## The months

| Month | City | Net | Lead |
|---|---|---|---|
| 2026-03 | toronto | +28 | A block of Queen East retires, and *nothing was demolished*: ten consecutive point ids folded back into 1238, and the development is across the street |
| 2026-04 | toronto | +29 | Eleven addresses off the even side of Secord Ave; the demolition permit was issued **25 Mar 2021** — the file is five years behind, and the surviving evens are the unpermitted next phase |
| 2026-05 | toronto | +19 | Chloe Cooley St debuts, reserved; By-law 182-2026 names it, and the City's own report repeats the wrong enslaver's name from a 2007 plaque |
| 2026-06 | toronto | +15 | An address for an unbuilt station entrance, under a name Metrolinx has since dropped; and Hamilton publishes the `R`-suffix and half-number rules Toronto doesn't |
| 2026-07 | toronto | +12 | Crosstown West gets its addresses, and the nine of them are a **contract's parts list**; the park "renamings" are restorations of decisions up to ten years old |
| 2026-08 | toronto | +7 | Twelve retirements that are still on file, the file swapping which record it keeps for an address; the swapped addresses are buildings the City dated years ago (Yonge/Glebe rezoned **2010**, Hullmark Centre, Alter); a park council renamed on 30 July reached the file in **20 days**; a 2023 permit named 530 Duplex Ave before the file did |
| 2026-09 | amherstburg | 0 | Nothing changed: 29 reads, the file unchanged since 20 August 2026 |
| 2026-09 | barrie | +23 | The five townhomes the City approved at 159 Huronia Rd (**13 Aug 2025**) get Units 1 and 2 on 151–159; the five St Paul's Cres lots at the rebuilt Yonge corner gain Yonge numbers 905–919 alongside their old ones, and the City has moved that intersection 90 m north; 174 addresses on Strawberry, Sunflower and Blue Forest flip *Current→Pending* in one day, words the City never defines |
| 2026-09 | brampton | +429 | Gillcrest, the 1870s mansion at 7 English St (apartments since **1945** per its heritage by-law), gets units 1–10; 100 lots on five new streets off Mayfield Rd were in the file **nearly two weeks before** the date on the City's addressing list; 246 houses gained a Unit 2, and the City's August two-unit register (237) matches the file's August additions 227 for 237; Temple Manor reissued as Temple Manor Road, 25 out and 25 in |
| 2026-09 | brant | +22 | Six new numbers on Highway 54 in Onondaga (760–792, **17 Sep**) with no permit or consent on record, which the County's addressing by-law says is the normal order; four houses gained a *Unit 2*, and every ARU permit the County issued in Aug–Sep was for an address the file already had, by **4 to 14 weeks**; seven "retirements" are points nudged 1–289 m and re-keyed by the tracker |
| 2026-09 | brantford | +13 | Eleven numbers fill gaps on Turnbull, Gillespie and Wilmot in West Brant (**5 Sep**), streets council dedicated from Plan 2M-1928 in Aug 2021; one row reads 26 in its number fields and 36 on its label, so the file has two 36 Turnbulls; a four-acre Core Natural parcel at 486 King George Rd gets a number, 891 m from any other street's address in the City's file |
| 2026-09 | bruce | +58 | 15 Cassidy St in Teeswater becomes Units 1–12 on twelve consecutive roll numbers (**25 Sep**), twelve weeks after a listing offered Unit 6 for 1 July; six unnumbered Farm Road points in Neyaashiinigmiing get 54–74, 66 m from a federally registered lot-servicing project "for community housing"; six Huron-Kinloss addresses become Unit 1 + Unit 2; 44 of 124 additions are moved points re-keyed by the tracker, hiding three renumberings and three suffix respellings |
| 2026-09 | cambridge | 0 | Nothing changed: 28 reads, the file unchanged since 7 August 2026 |
| 2026-09 | chatham-kent | 0 | Nothing changed: 30 reads, the file unchanged since 24 July 2026 |
| 2026-09 | halton-hills | 0 | Nothing changed: 30 reads, the file unchanged since 20 August 2026 |
| 2026-09 | kawartha-lakes | 0 | Nothing changed: 30 reads, the file unchanged since 1 August 2026 |
| 2026-09 | norfolk | 0 | Nothing changed: 30 reads, the file unchanged since 20 August 2026 |
| 2026-09 | peel-region | 0 | Nothing changed: 30 reads, the file unchanged since 11 June 2026 |
| 2026-09 | prince-edward-county | 0 | Nothing changed: 30 reads, the file unchanged since 20 August 2026 |
| 2026-09 | sarnia | 0 | Nothing changed: 30 reads, the file unchanged since 20 August 2026 |
| 2026-09 | stratford | 0 | Nothing changed: 30 reads, the file unchanged since 20 August 2026 |
| 2026-09 | toronto | −105 | The 13 Carlaw Ave doors were the **Riverdale Shopping Centre**, demolished for the Ontario Line's Gerrard portal (permit completed **15 Dec 2025**); the station rename trails Metrolinx by 17½ months; three new lanes, each over a finished laneway suite |
| 2026-09 | windsor | 0 | Nothing changed: 30 reads, the file unchanged since 11 June 2026 |

Toronto's February 2026 is deliberately absent: observation starts 2026-02-12, so its
first fortnight was never seen. Every city is written from September 2026 on (the
first month the whole registry was watched end to end), including the months in
which nothing changed — those say so, in a fixed shape from `tools/article_quiet.py`,
on the evidence of the vault's pull calendar. The 19 datasets whose licence forbids
republication (`publish_reports = false`) get no article. October 2026 is still open.

## Writing the next one

Normally nothing: from the 3rd of each month the `kk-ontario-article` scheduled task
(`monthly-article.ps1`) writes the previous month for every city unattended — the
research notes, the article and this table's row — renders the site copy, and commits
and pushes after each city. Quiet months cost no Claude run; months with changes are
capped at a few headless runs a day, so the whole registry takes about a week. It
waits a day on any city with an open flag inside the month. `logs/article-runs.csv`
says what each day's run did, one row per city-month. By hand, for an older month or
one city:

```
python tools/month_digest.py --city toronto --months              # which months qualify
python run.py flags                                               # nothing open for the month?
python tools/month_digest.py --city toronto --month 2026-08       # the brief
python tools/month_digest.py --city toronto --month 2026-08 --format entities   # the research checklist
```

Then follow the `monthly-article` skill (`.claude/skills/monthly-article/`), which
carries the house style, the fact-checking queries, the research procedure and the
licence obligations.
