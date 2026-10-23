# Research notes — County of Lennox and Addington, 2026-09

Raw findings behind `articles/researched/lennox-addington-2026-09.md`. Notes, not prose.
Window: net 2026-08-27 → 2026-09-25; six snapshots inside the month (09-01, 09-02,
09-09, 09-17, 09-23, 09-25); 30 pull days (09-01 .. 09-30), 0 failed. No open flags for
lennox-addington; nothing HELD. Research done 2026-10-23.

Conventions: **FACT** = the linked page says it. **INFERENCE** = a reading, not the
source's. **EMPTY** = searched, nothing found.

Identity: `datasets/lennox-addington.toml` has `key_field = ""`, so identity is
synthesized from the full address. A renumbering cannot show as a modification; it shows
as one retirement plus one addition. That is why the brief reports 0 renumbered.

---

## 0. Store-side findings

Net: rows 26,160 → 26,172 (+12); added 13, removed 1, 2 split events. Gross = net
(13 / 1); no address came and went inside the month.

Arrivals by snapshot (BELL_MUNIC from props):
- 09-01, Stone Mills: 1663 Centreville Road, 999 and 1001 County Road 14 (~55 m apart),
  306 Main Street.
- 09-02, Loyalist: 126A, 126B, 128A, 128B Creighton Drive; 256A Dr Richard James Crescent.
- 09-09, Stone Mills: 324 Moscow Road.
- 09-17, Loyalist: 1707 Thorpe Road (and 1725 Thorpe Road gone).
- 09-23, Stone Mills: 218 Richmond Point Lane.
- 09-25, Stone Mills: 4766 County Road 4.
Seven Stone Mills, six Loyalist. Nothing in the other municipalities.

### Creighton Drive — two splits, parents remain
- 126 and 128 Creighton Drive on file since the store began (06-11), still active.
  126A/126B and 128A/128B first on the 09-02 snapshot, each within ~3 m of its parent.
- 127A and 140A Creighton Drive have been on file since 06-11, so lettered numbers are
  not new to the street.
- Nearest other streets to 126A (`--near`): 28 Dusenbury Drive 34 m, 185 Sweetgrass Drive
  88 m, 92 Potter Drive 127 m.

### Thorpe Road — 1725 out, 1707 in, same point
- 1725 Thorpe Road: first on 08-11 snapshot, last on 09-09. Coords 44.30358, -76.76329.
- 1707 Thorpe Road: first on 09-17. Coords 44.30358, -76.76329 — identical to 5 decimals.
- Both BELL_MUNIC Loyalist. Neighbours on file: 1700, 1713 (since 06-11); 1815 next above.
  1707 sits between 1700 and 1713; 1725 sat between 1713 and 1815.
- Nearest other street: 854 Simmons Road, 58 m.
- INFERENCE: same point, new number = a renumbering in the world; the file has no record
  id to say so.

### 256A Dr Richard James Crescent
- 256 on file since 06-11 (two row versions), still there. 256A first on 09-02, ~3 m away.
- Nearest: 234 Pratt Drive 37 m, 229A Superior Drive 41 m, 249A Pratt Drive 43 m.

### 306 Main Street (Stone Mills)
- New 09-01. Not the same address as "306 Main Street-Odessa" (Loyalist, on file since
  06-11, ~17 km away).
- Nearest: 2032 County Road 1 East 101 m, 2 Elgin Street 233 m, 16 Harvey Street 270 m.
  Neighbourhood not named in the article (no source).

---

## 1. Outside record

### Creighton Drive
- FACT: listing for 75 Creighton Drive calls it a home "in the Golden Haven community" by
  Golden Falcon Homes, area "56 - Odessa".
  https://homli.ca/loyalist-real-estate/75-creighton-drive/X13653034 — marketing copy;
  medium confidence.
- FACT: Century 21 listings on Dusenbury Drive (34 m from 126A) describe Golden Falcon
  Homes models in Golden Haven, Odessa.
  https://spotlight.century21.ca/odessa-real-estate/46-dusenbury-drive/unbranded — medium.
- Not used: Frequency News, Loyalist council approved a draft plan for 584 units in west
  Odessa by Creekford Developments
  (https://www.frequencynews.ca/news/development-of-new-subdivision-moving-forward-in-odessa/).
  The article does not name Creighton Drive or Golden Haven; date not seen. Could be a
  different plan.
- EMPTY: anything on 126 or 128 Creighton Drive specifically (no listing, permit or
  consent found). Why each lot gained A and B: record silent.

### Dr Richard James Crescent
- FACT: listings place the street in the Lakeside Ponds subdivision, Amherstview
  (https://www.rew.ca/properties/184-dr-richard-james-crescent-loyalist-on).
- Snippet only: an OMA in-memoriam page for "Dr. Richard Norris James", described in
  search results as Amherstview's first doctor. Page redirects to a login wall,
  unfetchable; nothing ties it to the street name. Not used.
- EMPTY: Loyalist street-naming search for "Richard James" — only the township's general
  Commemorative Street Naming Program page
  (https://www.loyalist.ca/council-and-administration/commemorative-street-naming-program/).
- EMPTY: anything on 256 / 256A.

### Thorpe Road
- EMPTY: "Thorpe Road" + Loyalist civic address change. Only hit was the township's
  Edgewood Road / Harewood (Bath) re-addressing project
  (https://engage.loyalist.ca/edgewood) — different road; not used.

### Stone Mills single additions
- Richmond Point Lane: EMPTY (one aggregator listing at 149, nothing about 218).
- County Road 14, Centreville Road, Main Street, Moscow Road, County Road 4: not searched
  beyond the checklist; single rural numbers with no public trail expected.
