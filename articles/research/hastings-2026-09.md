# Research notes — County of Hastings, 2026-09

Raw findings behind `articles/researched/hastings-2026-09.md`. Notes, not prose.
Window: snapshots 2026-08-29 → 2026-09-29 (17 snapshots inside the month, 09-02 .. 09-29;
30 pull days, 0 failed). No open flags for hastings. Research done 2026-10-23.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found. **DROPPED** = found but failed a check.

Source caveat: hastings publishes no stable row id (`UNIQUE_ID` is a reassigned
`HC911_<n>` sequence), so `datasets/hastings.toml` synthesizes the identity key from
number + street + unit + rounded lon/lat. A point the County moves by more than about a
metre reads as one retirement and one addition. That is most of this month.

---

## 0. Store-side findings (this repo, not the web)

Brief: rows 31,316 → 31,336 (+20); net added 251, removed 231, boundary 1, significant 1,
13 "split events". Gross = net.

Pairing the 251 added and 231 removed rows by identical label (full address + unit):
- **199 pairs** have the same label on both sides: the same address, point moved.
  Median move 20 m, min 1 m, max 722 m (497B/C King Rd, WOLL).
  By street: St. Lawrence St East (MADV) 56 on 09-12/09-18, max 56 m; Chemaushgon Rd
  (BANC) 21 on 09-18; Thrasher Rd (TYEN) 11 on 09-15; Mink Lake Rd (MCCL) 9 on 09-11;
  Baker St (STIR) 9 on 09-16; Jarvis Rd (MADO) 6, 66–472 m; then a long tail of 1–6 per
  street through to 09-29. The work runs street by street across the month.
- So the remaining 52 additions / 32 removals are the different labels. 16 of them pair
  at **0 m** (same point readdressed); roll number (RnoTXT2) confirmed identical on the
  ones named below. 5 more pair at 37–186 m (5→10 Charles Ct, 2→4 Crawford Dr,
  744→764 Hogs Back Rd, 498→478 Marysville Rd, 215→175 West Rd): not printed as
  readdresses. The rest
  includes some matched only by nearness (≤300 m), so no clean "genuinely new" count is
  printed in the article.
- **All 13 brief "splits" are artifacts** of the moves: the units/suffixes were already on
  file (e.g. 297/299/301 St. Lawrence St East APT 1–6 all span 2026-06-11..09-11 then
  09-12..present; 671A–E Jarvis Rd moved 317–472 m; 497A–C King Rd 411–722 m).
  4 Chescher Ct → 4A/4B is two houses renumbered, not a split: 4A took old **6**'s point
  and roll number (…523702), 4B took old **4**'s (…523701), 09-14.

Same-point readdresses (point identical, roll number identical, verified in store):
- **380 Dundas St → 140 Prince St** (DESE), 09-15. Roll 120203004001900. `--near`: 383
  Dundas St 57 m, 139 Fourth St 58 m.
- **101 Egan Ln → 9 Old Bessemer Trail** (DUNG), 09-15. New street in the file. Roll
  126206401020041. `--near`: 89 Egan Ln 46 m, 21 Bessemer Ln 163 m, 265 Bradshaw Rd 173 m.
- **262 Mephisto Lake Landing → 1 Water-Mephisto Lake-Island B** (CASH), 09-15. Same roll
  124800002525100, point moved ~518 m. Nearest other address 54 Renata Ln, 193 m.
- **4, 6 Chescher Ct → 4B, 4A** (WOLL), 09-14 (see above).
- **450 → 678 Boundary Rd** (WOLL), 09-12; same roll 125400002527500, moved ~930 m.
- Suffix consolidations, same point & roll: **68A/68B Maple St → 68** (BANC, 09-04; 68B's
  point gone); **71A/71B/71C York Rd → 71** (TYEN, 09-15, all three shared one point);
  **396A/396B Spry Rd → 396 and 412** (RAWD, 09-15, each kept its point and roll).
- Near-renumbers, small: 10→8 Tom Ln, 12→8 Old Diamond Lake Rd, 1451→1467 East Road
  Loop, 52→60 Finnegan Lake Rd, 571→573 Courneya Rd, 923→943 Limerick Lake Rd (all 0 m).

New labels with no partner on the same point (sample): **231, 233, 235 Baker St** (STIR,
09-16, consecutive rolls …2012030/31/32, 6–8 m apart; 229 Baker St on roll …2012019 moved
the same day; `--near` 38 Tanner Dr 44 m); **15138 Highway 62** (MADO, 09-19);
**6404 Highway 620** (WOLL, 09-19); 1805 Bay Lake Rd; 1889 and 1900 Melrose Rd; 53 and 95
Palmateer Rd.

Retired with no partner (sample): 214 Church St (STIR, last 09-16), 2112 Spring Brook Rd
(RAWD), 88 Norwood Rd (MARV, one of two rows with that label).

Single-row edits:
- **39 Prince Albert St West → East** (MADV), 09-19. The file held *two* 39 Prince Albert
  St West rows with different rolls (…1509300 and …1009700), ~300 m apart; the …1509300
  one became EAST. The other is still West.
- **560 Bronson Rapids Rd**: MUNICIPALI RAWD → HUNT, 09-16; roll number also changed
  (1220119030001 00 → 1230224030001 00). Point unchanged.

MUNICIPALI codes: the layer has **no coded-value domain** on the field (alias
"Municipality"); FACT from the service JSON
https://services1.arcgis.com/1xcPmb5WGexkkJ9w/arcgis/rest/services/CivicAddresses/FeatureServer/0?f=json
— so codes are not expanded in print except where a source places the street.

## 1. Web

- **St. Lawrence Street East is in Madoc / Centre Hastings.** FACT: listing
  https://www.c21.ca/listing/ON/Centre-Hastings/210-St-Lawrence-Street-E-K0K-2K0/220397553
  ("210 St Lawrence Street E, Centre Hastings"). Centre Hastings = Huntingdon Township +
  Village of Madoc, 1998: https://en.wikipedia.org/wiki/Centre_Hastings . Why the points
  moved: EMPTY (no county GIS notice found).
- **Baker St is in Stirling-Rawdon; 229 Baker St is a townhouse.** FACT: listing
  https://www.houseful.ca/stirling-rawdon-on/229-baker-st-stirling-rawdon-on-k0k-3e0/pid_bn6heffsxx
  (end-unit townhouse, cul-de-sac). INFERENCE only that 231–235 continue the row; not
  printed as fact. Builder / plan for 231–235: EMPTY.
- **Deseronto** is a town in Hastings County: https://en.wikipedia.org/wiki/Deseronto .
  Why 380 Dundas became 140 Prince: EMPTY.
  DROPPED: Tufts photo "140-144 Prince Street, ca. 1870"
  (https://dl.tufts.edu/concern/images/2n49tb23j) puts 140 Prince at Lafayette Ave; the
  store has no Lafayette anywhere in the county and the point sits by Dundas/Fourth, so
  not shown to be this Prince Street.
- **Old Bessemer Trail**: EMPTY (only Bessemer, Michigan hits and the Hastings Heritage
  Trail). Dungannon township merged into the Town of Bancroft in 1999:
  https://en.wikipedia.org/wiki/Bancroft,_Ontario .
- **Mephisto Lake** is in the geographic township of Cashel, municipality of Tudor and
  Cashel: https://en.wikipedia.org/wiki/Mephisto_Lake . Island address / water-access
  numbering policy: EMPTY.
- County GIS civic-address programme or notice of a 2026 re-survey: EMPTY.
