# Research notes — Toronto, 2026-07

Raw findings behind `articles/researched/toronto-2026-07.md`. Notes, not prose.
Window researched: snapshots 2026-06-30 → 2026-07-31. Research done 2026-08-27/28.

Conventions: **FACT** = the linked page says it. **INFERENCE** = my reading, not the
source's. Every claim carries a URL. Empty searches are recorded as results.

Access note that shaped the whole session: `secure.toronto.ca/council/agenda-item.do`,
`app.toronto.ca/tmmis/*` and `secure.toronto.ca/nm/*` all return Akamai **403** to both
WebFetch and curl, so no TMMIS agenda-item page could be opened directly. What does work:
`www.toronto.ca/legdocs/mmis/**/bgrd/backgroundfile-*.pdf`,
`www.toronto.ca/legdocs/bylaws/*.pdf`, `www.toronto.ca/wp-content/uploads/*.pdf`.
`toronto.ca` parks facility pages are JS-rendered and return an identical empty shell for
every `?id=`, so only their URL/title is usable as evidence. Archive.org was offline.

---

## 1. Eglinton Crosstown West Extension — the nine addresses added 28 July

**Searched:** `Eglinton Crosstown West Extension Metrolinx Jane Station Scarlett Station
entrances`; Metrolinx station pages for Jane-Eglinton and Scarlett; Metrolinx
"what we're building"; Wikipedia; City of Toronto ECWE page; Infrastructure Ontario
project page; `"Matheson Boulevard" Toronto Etobicoke Eglinton Crosstown West Extension
Renforth`; Canada.ca newsroom.

### The project — FACT

- 9.2 km extension of the Eglinton Crosstown LRT (Line 5) from Mount Dennis Station to
  Renforth Drive; seven stations; delivered by Metrolinx in four contracts (Stations Rail
  and Systems, Advance Tunnel 1, Advance Tunnel 2, Elevated Guideway).
  > "The Eglinton Crosstown West Extension is an approximately 9.2 kilometre extension of
  > the Eglinton Crosstown LRT, from Mount Dennis to Renforth Drive."
  <https://www.infrastructureontario.ca/en/what-we-do/projectssearch/eglinton-crosstown-west-extension/>
- City of Toronto's own page confirms the station split and the delivery entity:
  seven stations — two elevated (Jane and Scarlett) and five underground/at-grade
  (Mount Dennis, Royal York, Islington, Kipling, Martin Grove, Renforth); "Metrolinx leads
  the project through its company West End Connectors".
  <https://www.toronto.ca/services-payments/streets-parking-transportation/transit-in-toronto/transit-expansion/eglinton-crosstown-and-proposed-extensions/eglinton-west-lrt/>
- Expected opening:
  > "The extension is expected to open in 2031."
  <https://en.wikipedia.org/wiki/Eglinton_Crosstown_west_extension>
  (Wikipedia only — no Metrolinx or City page I fetched states an opening year. Treat 2031
  as **likely**, sourced to a tertiary source, not to Metrolinx.)

### Two entrances each at Jane and Scarlett — FACT, matches the file exactly

- Jane-Eglinton Station: northwest corner of Jane St and Eglinton Ave W, elevated, two
  entrances.
  > "Entrances close to the intersections on both the west and east side of Jane Street
  > will provide easy connections to bus stops"
  <https://www.metrolinx.com/en/projects-and-programs/eglinton-crosstown-west-extension/what-were-building/jane-eglinton-station>
- Scarlett Station: northwest corner of Scarlett Rd and Eglinton Ave W, elevated, two
  entrances.
  > "Station entrances on the east and west sides of the intersection will provide easy
  > connections to TTC bus routes 32, 73, 79 and 405."
  <https://www.metrolinx.com/en/projects-and-programs/eglinton-crosstown-west-extension/what-were-building/scarlett-station>
- The file's "Main Entrance" / "Secondary Entrance" pairing therefore matches Metrolinx's
  two-entrance design at both stations. The file does not say which side is which; neither
  does Metrolinx. **Do not** map main/secondary onto east/west.

### Naming discrepancy worth a sentence — FACT

The address file writes **"Jane Station"**. Metrolinx's own project pages write
**"Jane-Eglinton Station"** (and, in the same family, "Royal York-Eglinton",
"Islington-Eglinton", "Kipling-Eglinton", "Martin Grove-Eglinton"). Scarlett matches
exactly ("Scarlett Station") — Metrolinx does not hyphenate that one.
<https://www.metrolinx.com/en/projects-and-programs/eglinton-crosstown-west-extension/what-were-building>
Wikipedia lists the station as "Jane" with a working-name footnote, so the short form is
in circulation too. **INFERENCE:** the City took the short/working name.

### Timing against the 28 July file date — FACT

- **10 July 2026**, 18 days before the addresses appear: federal news release.
  > "Excavation work has officially started on four new underground stations along Eglinton
  > Avenue West at Martin Grove Road, Kipling Avenue, Islington Avenue and Royal York Road."
  > … "Toronto, Ontario, July 10, 2026"
  <https://www.canada.ca/en/housing-infrastructure-communities/news/2026/07/federal-government-highlights-progress-on-eglinton-crosstown-west-extension.html>
  Also states federal investment of ~$1.87 billion and ~4,600 jobs annually.
- **22 August 2025**, ~11 months earlier: the Stations, Rail and Systems (SRS) contract —
  the package that actually builds the entrances, the EEBs and the TPSS — was signed.
  Development & Master Construction Agreement: August 22, 2025.
  <https://www.infrastructureontario.ca/en/what-we-do/projectssearch/eglinton-crosstown-west-extension/>
- **August 2026**, after the window: tunnelling complete. The Jane-Eglinton station page
  states tunnelling was completed in August 2026 with tunnel lining next.
  <https://www.metrolinx.com/en/projects-and-programs/eglinton-crosstown-west-extension/what-were-building/jane-eglinton-station>
- **INFERENCE (high):** the nine points are the SRS contractor's permanent-works locations
  being given municipal addresses roughly a year after the contract was signed and while
  station excavation was under way. No source ties the addressing itself to any event.

**Confidence: confirmed** (project, route, stations, two entrances each, SRS scope).
Opening year 2031 is **likely** (tertiary source only).

---

## 2. "TPSS" — traction power substation

**Searched:** `Metrolinx "traction power substation" TPSS Eglinton Crosstown West
Extension`; `"3770 Eglinton Avenue West" Toronto Metrolinx traction power substation`;
Metrolinx Ontario Line "subway structures beyond the stations"; thecrosstown.ca TPSS page.

### The acronym — FACT, spelled out in a Toronto-authored transit document

> "A traction power substation (TPSS) is an electrical facility required to power the
> future electric Ontario Line trains. Excavation for the TPSS finished in the fall of
> 2025 and construction completion is scheduled for summer 2026"

— City of Toronto, *Ontario Line — Construction Update, Fourth Quarter 2025*, Report for
Action to Toronto and East York Community Council, dated **18 December 2025**, from the
Executive Director, Transit Expansion Division.
<https://www.toronto.ca/legdocs/mmis/2026/te/bgrd/backgroundfile-261289.pdf>

That is the Ontario Line, not the ECWE — but it is the City of Toronto writing the
expansion of the acronym in a Metrolinx-project context, which is the standard the task
asked for. Use it.

### What one does — FACT (Metrolinx, Line 5 Eglinton)

Metrolinx, "Crosstown LRT sees important power substations installed", **2 December 2019**:
substations "take alternating current power that's available from normal power companies
and converts it into the direct current required by the light rail vehicles."
<https://www.metrolinx.com/en/discover/crosstown-lrt-sees-important-power-substations-installed>

### The ECWE has exactly one, and the file has exactly one — FACT

> "Six emergency exit buildings." / "One standalone traction power sub-station."

— Infrastructure Ontario, ECWE Stations Rail and Systems, scope of work.
<https://www.infrastructureontario.ca/en/what-we-do/projectssearch/eglinton-crosstown-west-extension/>

Corroborated by the winning consortium's own release:
> "The scope also covers upgrades at Mount Dennis Station to connect seamlessly with the
> future Eglinton Crosstown LRT line, as well as six emergency exit buildings and a new
> traction power substation."
— Alberici (member of Trillium Rail Partners, with Amico Major Projects, Acciona
Infrastructure Canada and WSP Canada).
<https://alberici.com/alberici-secures-progressive-design-build-contract-for-eglinton-crosstown-west-extension-stations-rail-and-systems/>

**This is the strongest single finding in the month.** The contract scope says one TPSS
and six EEBs; the file adds one point labelled `TPSS1` and four labelled EEB1, EEB4, EEB5,
EEB6 — i.e. the file's numbering scheme is the contract's inventory. (EEB2 and EEB3 are
already built under the advance-tunnel contract — see item 3 — which is a plausible reason
they are not in this batch, but no source says so: **INFERENCE**.)

### What was NOT found

- **Nothing found** tying `3770 Eglinton Avenue West` specifically to the TPSS.
  Searched `"3770 Eglinton Avenue West" Toronto Metrolinx traction power substation`
  and `TPSS "traction power" Eglinton Crosstown West Extension` — no Metrolinx notice,
  council item or news story names that address. The address is the file's only evidence.
- `thecrosstown.ca` (the Line 5 project site, which has a page literally titled
  "Construction for TPSS (Traction Power Substation) 11 Begins") no longer resolves —
  `m.thecrosstown.ca` is NXDOMAIN and `thecrosstown.ca` now serves an unrelated
  train-travel site. Do not cite it.

**Confidence: confirmed** (acronym, function, one-per-project). Address-level: **nothing found**.

---

## 3. Emergency Exit Buildings (EEB)

**Searched:** `Metrolinx "emergency exit building" Eglinton Crosstown West Extension
tunnel`; `"EEB6" OR "EEB5" OR "EEB4" Eglinton Crosstown West Extension`; the ECWE
Environmental Project Report addendum set; Metrolinx ECWE community notices; the ECWE
Advance Tunnel CLC deck; Metrolinx Ontario Line "subway structures beyond the stations";
Toronto zoning by-law amendments.

### Six of them on this project — FACT

Same two sources as item 2: Infrastructure Ontario's SRS scope ("Six emergency exit
buildings") and the Alberici release. Six is the number that matters, because the file's
labels top out at EEB6.

### What they are for — FACT

Metrolinx, Ontario Line, *Subway structures beyond the stations*:
> "In case of an emergency, the EEB will allow for safe exit from the tunnels."

The same page notes an ESB at Pape/Sammon that "will serve both as an emergency exit and
access point for maintenance crews."
<https://www.metrolinx.com/en/projects-and-programs/ontario-line/subway-structures-beyond-the-stations>

**Note:** the widely-repeated line that EEBs are required "when station platforms are more
than approximately 760 metres apart" surfaced only in a search engine's synthesis. I could
**not** find it on any page I fetched. **Do not use the 760 m figure.**

### How they get built — FACT

Metrolinx, *Construction update on the Eglinton Crosstown West Extension*, **26 October 2022**:
> "Headwalls are the underground support structures made up of a series of concrete
> columns, called piles, that create a watertight wall around the area of future subway
> stations and emergency exit buildings."
> "Work for the emergency exit building at Wincott Drive also began this summer and will
> last until next spring."
<https://www.metrolinx.com/en/discover/construction-update-on-the-eglinton-crosstown-west-extension>

### The EEB numbering IS public — but only for 2 and 3 — FACT

Metrolinx ECWE Advance Tunnel Community Liaison Committee deck, meeting 8, **12 September
2024**, "Headwall overview" slide:
> "EEB #3 (Wincott Drive)  EEB #2 (Russell Road)  Additional Headwall (Russell Rd)
> Additional Headwall (Wincott Dr)"

and the dewatering slide: "EEB3: Wincott Drive", "EEB2: Russell Road".
<https://assets.metrolinx.com/image/upload/Images/Metrolinx/ECWE_ATC1_CLC_Meeting_8_FINAL.pdf>

Corroborated by the December 2021 / March 2022 virtual-open-house decks:
> "There will also be two emergency exit buildings constructed — one between Kipling Ave
> and Islington Ave, the other between Islington Ave and Royal York Rd."
<https://assets.metrolinx.com/image/upload/v1667411353/Images/Metrolinx/ECWE_march_30_voh_deck.pdf>

So the "EEB<n>" convention is Metrolinx's own, used in public community materials. **But**:

- **Nothing found** publishing EEB1, EEB4, EEB5 or EEB6 by number, or tying any of them to
  75 Richview Rd, 5070 Eglinton Ave W, 5230 Eglinton Ave W or 20 Matheson Blvd. Searched
  the EEB-number query above, `"emergency exit building" Metrolinx "Richview" OR "5070
  Eglinton" OR "5230 Eglinton" Toronto`, and the Metrolinx ECWE notices index — nothing.
  The address file appears to be the first public place these four are named.

### Land assembly for them IS in the council record — FACT (see also item 4)

City of Toronto **By-law 375-2024**, adopted by City Council 17–18 April 2024 on
Etobicoke York Community Council item **EY12.1**, amends Zoning By-law 569-2013

> "with respect to the lands municipally known in the year 2023 as portion of 3650
> Eglinton Avenue West; portion of 3700 Eglinton Avenue West; portion of 101 Emmett
> Avenue; portion of 1 Richview Road; portion of 4200 Eglinton Avenue West; … portion of
> unaddressed lands north of Eglinton Avenue West east of Richview Road cul-de-sac; …
> and portion of unaddressed lands at Eglinton Avenue West and Matheson Boulevard East to
> facilitate the Eglinton Crosstown West LRT Extension."

and grants, for a *transportation use* on those lands, no maximum height and no minimum
setbacks (Exception OR 45, RAC 209 etc.).
<https://www.toronto.ca/legdocs/bylaws/2024/law0375.pdf>

The staff report behind it (Director, Transportation Planning, 15 March 2024) is quoted in
search indexes as saying the amendments cover lands that "will accommodate transit
facilities such as emergency exit buildings, traction power substations, transit station
entrance buildings and temporary facilities required for construction" — but the report
PDF and the TMMIS item page both 403'd, so **that phrasing is search-index-level only, not
a page I fetched.** The by-law itself does not use the words "emergency exit building".
Cite the by-law; do not quote the report.

Note the by-law's address list (3650, 3700, 4200, 4300, 4400, 4530, 4600, 4760 Eglinton
Ave W; 1 Richview Rd; 101 Emmett Ave; 535/555 Martin Grove Rd) and the file's new
addresses (3770, 5070, 5230 Eglinton Ave W; 75 Richview Rd; 20 Matheson Blvd) are related
but **not identical** — the by-law addresses parcels as they existed in 2023, the file
addresses buildings on them. Treat any 1 Richview Rd → 75 Richview Rd correspondence as
**INFERENCE**, not fact.

**Confidence: confirmed** (what EEBs are, six of them, the numbering convention).
EEB1/4/5/6 locations: **nothing found**.

---

## 4. Matheson Blvd

**Searched:** Nominatim reverse geocode of the file's coordinates; `"Matheson Boulevard"
Toronto Etobicoke Eglinton Crosstown West Extension Renforth`; `"375-2024" Toronto by-law
Eglinton Crosstown West Extension zoning`.

### It is not a new street. It already exists, in Toronto. — FACT

Reverse geocode of the file's own 43.6686 / -79.5874:
> `"name": "Matheson Boulevard East"`, `"display_name": "Matheson Boulevard East,
> Eringate-Centennial-West Deane, Etobicoke Centre, Etobicoke, Toronto, Golden Horseshoe,
> Ontario, M9C 2N9, Canada"`, `"addresstype": "road"`, OSM way 1263655448
<https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=43.6686&lon=-79.5874&zoom=17>
(OSM data © OpenStreetMap contributors, ODbL 1.0.)

So the point sits on the **Toronto** end of Matheson Boulevard East — the Mississauga
arterial's short stub inside Etobicoke, by the Highway 427 / Eglinton Ave W interchange,
in the same ward (Etobicoke Centre) the file assigns. OSM's `M9C 2N9` is interpolated;
don't quote the postcode.

### The City already zoned "unaddressed lands" there for the ECWE — FACT

By-law 375-2024 (link and quote in item 3) includes
> "portion of unaddressed lands at Eglinton Avenue West and Matheson Boulevard East to
> facilitate the Eglinton Crosstown West LRT Extension."

**INFERENCE (high):** 20 Matheson Blvd is the City assigning a municipal number to the
"unaddressed lands at Eglinton Avenue West and Matheson Boulevard East" that Council
rezoned in April 2024 for a transportation use — i.e. EEB6. Gap: **~27 months** between
the by-law and the address. No source states the connection.

**Nothing found:** any Metrolinx property notice, expropriation notice or council item
naming "20 Matheson" specifically.

**Confidence: confirmed** that the street exists in Toronto and that Council rezoned
unaddressed land at that intersection for the ECWE. The link to EEB6 is **inference**.

---

## 5. Coneflower Cres — 37 reserved → regular, 22 July

**Searched:** Nominatim reverse + forward geocode; `"Coneflower Crescent" Toronto`;
`site:toronto.ca legdocs "Coneflower Crescent"`; `site:urbantoronto.ca Coneflower`
(empty); `site:app.toronto.ca "Coneflower"` (empty); `"66M-2509" Toronto plan of
subdivision` (empty); `"55 Antibes Drive" Toronto subdivision townhouse development`;
`"Bloom Park Towns" Menkes Coneflower Crescent Toronto`; `Toronto by-law assumption
"Coneflower Crescent" municipal highway 2026` (empty); `"Coneflower Crescent" Toronto 2026
construction OR occupancy OR registered` (empty).

### The location in the brief is wrong — FACT

Reverse geocode of 43.7785 / -79.4500:
> `"road": "Coneflower Crescent"`, `"neighbourhood": "Westminster-Branson"`,
> `"quarter": "York Centre"`, `"city_district": "North York"`, `"city": "Toronto"`
<https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=43.7785&lon=-79.4500&zoom=17>

This is **Westminster-Branson**, off Bathurst north of Finch — roughly 4.5 km east of
Dufferin. Not Dufferin/Finch, not Downsview. Ward York Centre is right.

### The subdivision — FACT

City of Toronto, *Parking Prohibition: Coneflower Crescent*, Report for Action to North
York Community Council, dated **10 March 2017**:
> "In 2013 the City of Toronto approved the Registered Plan of Subdivision 66M-2509 for
> 55 Antibes Drive permitting the construction of a new public road via Antibes Drive."
> "This roadway provides access to the newly constructed residential townhome subdivision
> consisting of 202 townhouse unit (41 freehold and 161 condominium)."
> "Coneflower Crescent is a newly constructed two-way local road with a regulatory speed
> limit of 50 km/h."
> "All costs associated with the implementation of the parking prohibition on Coneflower
> Crescent are to be borne by the developer."
> "prohibit parking at all times on both sides of Coneflower Crescent, from Antibes Drive
> (east intersection) and Antibes Drive (west intersection)"
<https://www.toronto.ca/legdocs/mmis/2017/ny/bgrd/backgroundfile-102081.pdf>

Coneflower Crescent is therefore a loop off Antibes Drive at both ends, built as part of
the 55 Antibes Drive subdivision (plan **66M-2509**, approved 2013).

### The project name — FACT (marketing sources)

**Bloom Park Towns**, by **Menkes**. UrbanToronto forum thread title: "Bloom Park Towns
(55 Antibes, Menkes, 3s)", with "197 - 3 storey Townhomes"; posts run Jan 2011 – Jul 2012.
<https://urbantoronto.ca/forum/threads/bloom-park-towns-55-antibes-menkes-3s.15412/>
The condominium half is addressed on Coneflower — listing-site titles: "15 Coneflower Cres
| Bloom Park Towns Condos" <https://condos.ca/toronto/bloom-park-towns-15-19-coneflower-cres>
and "17 Coneflower Cres | Bloom Park Towns"
<https://strata.ca/toronto/17-coneflower-cres-bloom-park-towns/unit-218> — both pages
returned 403/429 to direct fetch, so these are **title-level evidence only**. Use the
City's "202 townhouse unit (41 freehold and 161 condominium)" as the citable figure, not
the marketing unit counts.

**Ruled out:** 155 Antibes Drive (Tenblock, 32/34-storey towers, ZBA filed Nov 2021) is a
different project on the same arterial.
<https://www.toronto.ca/legdocs/mmis/2024/ny/bgrd/backgroundfile-247199.pdf>

### The street name — nothing found

Searched `site:app.toronto.ca "Coneflower"`, `site:toronto.ca legdocs "Coneflower
Crescent"` and a naming-specific query. **No street-naming report, agenda item or by-law
for "Coneflower" exists in the searchable record** — the only Coneflower items in the City
record are traffic matters (the 2017 parking report above; a 2021 Vision Zero speed-limit
document, <https://www.toronto.ca/legdocs/mmis/2021/ny/bgrd/backgroundfile-166468.pdf>).
**INFERENCE:** the name came through the 2013 plan-of-subdivision approval rather than a
standalone council naming item — which is why there is nothing to find.

### Nothing found for a mid-2026 event

No assumption by-law, occupancy milestone, registration or news story in 2025–26 touching
Coneflower Crescent or 55 Antibes Drive. Addresses on the street have been transacting for
years — e.g. MLS C5357955 (2021, unit 224–17 Coneflower)
<https://property.ca/toronto/17-coneflower-crescent-north-york/unit-224-C5357955>.

**INFERENCE (high):** the 22 July 2026 reserved → regular flip is City address-maintenance
records catching up with a street that was registered in 2013, described as "newly
constructed" in 2017, and occupied ever since — a **~13-year** lag, and not a real-world
2026 event. Caveat: "reserved since April 2025" is when *our file* first sees them; the
City may have set that status far earlier.

**Confidence: confirmed** (location, subdivision, plan number, developer).
Street-naming decision and any 2026 trigger: **nothing found**.

---

## 6. Park and facility renamings

### Bain Avenue Parkette → Erica Stark Parkette — confirmed, and ten years stale

**FACT.** City of Toronto staff report, *Renaming Bain Avenue Parkette to Erica Stark
Parkette*, General Manager, Parks Forestry and Recreation → Toronto and East York
Community Council, dated **26 February 2016**, Ward 30 Toronto-Danforth, reference
`P:\2016\Cluster A\PFR\TE15-040516-AFS#22334`:
> "On June 15, 2015, a request was made to rename the parkette located at 208 Bain Avenue
> to honour Erica Stark."
> "Erica Stark was passionate about her family and the importance of giving back to
> others. Her extensive volunteer work focused on children, people with disabilities,
> service dogs and improving her community park."
> "She took an active role in the development of the Friends of Withrow Park community
> group … This community group also took on a stewardship role within Bain Avenue
> Parkette, which is located adjacent to Withrow Park."
> "Erica worked closely with the local Councillor to make improvements to the parkette,
> including advocating for better lighting, new playground equipment and the replacement
> of the gate at the south park entrance"
> "As per the Delegation of Authority to Community Councils, property naming and renaming
> are a matter for which Community Council has delegated authority from City Council to
> make a final decision."
<https://www.toronto.ca/legdocs/mmis/2016/te/bgrd/backgroundfile-90933.pdf>

**FACT.** How she died, and the dedication. CBC News, *Park named after Toronto mother
struck by van in 2014*, published **12 June 2016**:
> "The parkette at Pape and Danforth was re-named in a ceremony on Saturday, and will be a
> permanent tribute to the mother of three boys."
> "In November 2014, Erica was at Midland Ave. and Gilder Rd. when a minivan jumped the
> curb and struck her."
> (David Stark) "I'm delighted but I'm also sad… And I'm sad because Erica's death was
> completely preventable."
<https://www.cbc.ca/news/canada/toronto/park-renamed-erica-stark-1.3631530>
(403 to WebFetch, 200 to curl.)

Local corroboration: danforthdad.com, 9 July 2019 — "In 2016, the Bain Avenue Parkette was
renamed in memory of Erica Stark, a neighbourhood mom who died tragically while walking
her dog." <https://www.danforthdad.com/post/stark>

**Item number unresolved.** A search index gives the agenda item as `2016.TE17.14`
(<http://app.toronto.ca/tmmis/viewAgendaItemHistory.do?item=2016.TE17.14>, 403), while the
staff report's own reference number points at the **5 April 2016** TE Community Council
meeting. Not reconciled. Say "a 2016 community council decision", not a meeting date.

**Timing:** decision Feb 2016, ceremony 11 June 2016; the file's place name changes in
July 2026 — **~10 years later**. The file is catching up, not recording an event.
**Confidence: confirmed** (person, decision, year). Exact meeting: **nothing found**.

### River Square Park → Lawren Harris Square — location confirmed, decision not found

**FACT.** "River Square" was the planning-era name for a West Don Lands Phase 1 open
space. City report *Final Report — West Don Lands, Phase 2*, **29 July 2010**, Ward 28,
lists "Don River Park" and "River Square" in its Phase 1 open-space table and refers to
"the Front Street, Mill Street, and River Square neighbourhoods".
<https://www.toronto.ca/legdocs/mmis/2010/te/bgrd/backgroundfile-33146.pdf>
(Grep for "Lawren" in that 2010 report: **zero hits**.)

**FACT.** Lawren Harris Square is a City park at Bayview Ave / Lower River St, opposite
Corktown Common. City of Toronto Parks, *Proposed Dog Off-Leash Area in Lawren Harris
Square — Survey Summary Report*, **16 May 2021**:
> "the City is considering the installation of a new dog off-leash area in your
> neighbourhood, at Lawren Harris Square (located at the intersection of Bayview Ave and
> Lawren Harris Square, across from Corktown Commons)."
<https://www.toronto.ca/wp-content/uploads/2021/06/8f00-proposed-lawren-harris-square-ola-survey-summary-may-2021.pdf>
That matches the file's ~43.654 / -79.356 West Don Lands cluster.

**FACT.** It is also a City street, in the by-laws since at least 2016 — By-law 982-2016
schedules cycling lanes on "Lawren Harris Square", citing "(north leg)" and "(west leg)"
at Lower River Street / Bayview Avenue.
<https://www.toronto.ca/legdocs/bylaws/2016/law0982.pdf>
And it was still the reference point in 2025: the Old Foundry Road renaming report (item 7)
names "a section of Eastern Avenue extending westerly from Lawren Harris Square".
<https://www.toronto.ca/legdocs/mmis/2025/te/bgrd/backgroundfile-254491.pdf>

**Nothing found:** the naming decision itself. Searched `toronto.ca legdocs "Lawren Harris
Square" naming street report`; `"River Square" West Don Lands Toronto renamed "Lawren
Harris Square" 2014`; `"River Square Park" Toronto`; `Toronto "West Don Lands" street
naming report "Lawren Harris" honour artist Group of Seven public square named`;
`"Lawren Harris" square West Don Lands street named Group of Seven Waterfront Toronto
naming`. **No council report, by-law or Waterfront Toronto release states why the square
honours Lawren Harris, or when.** Note Wikipedia distinguishes Lawren Harris (Group of
Seven) from his son Lawren P. Harris; **no source establishes which one this commemorates**
— do not assert the Group of Seven painter as fact.

**INFERENCE:** the change from the planning name "River Square" to "Lawren Harris Square"
happened between the 2010 report and the 2016 by-law — a decade-plus before the file
caught it. **Confidence: confirmed** for existence, location and the pre-2016 date range;
**nothing found** for the naming decision or the person.

### Secondary renamings — mostly label tidy-ups, no decisions found

| File change | What was found | URL | Confidence |
|---|---|---|---|
| Keelesdale North Park → North Keelesdale Park | City parks facility page uses the new form; a separate **Keelesdale Park** also exists; third-party listings still carry the old form | <https://www.toronto.ca/explore-enjoy/parks-recreation/places-spaces/parks-and-recreation-facilities/location/?id=715&title=North-Keelesdale-Park> · <https://www.toronto.ca/data/parks/prd/facilities/complex/497/index.html> | likely a word-order normalization; no naming decision found |
| Beechgrove Park → Beechgrove Ravine | **Nothing found.** Every source says "Beechgrove Park, 182 Beechgrove Dr, Scarborough". No source uses "Beechgrove Ravine". Two empty searches, stopped. | — | nothing found |
| "Stephen Leacock  C.C." → Stephen Leacock Seniors' Community Centre | The full name is in current use (2520 Birchmount Rd, Scarborough), third-party sources only; no renaming report | <https://seniortoronto.ca/content/stephen-leacock-seniors-community-centre> | likely just an abbreviation being expanded |
| Ambulance Station 13 → EMS Station 13, Richview Park | "Richview" designation confirmed third-party ("Toronto EMS Station 13 - Richview", 555 Martin Grove Rd); **the exact "Richview Park" wording is not confirmed on any City source** | <https://foursquare.com/v/toronto-ems-station-13/4e227d457d8b71715bb6b92b> | likely |
| Lawrence Park And Ravine → Lawrence Park Ravine | City parks page uses the new form; old form survives in third-party listings | <https://www.toronto.ca/explore-enjoy/parks-recreation/places-spaces/parks-and-recreation-facilities/location/?id=119&title=Lawrence-Park-Ravine> | likely a label tidy-up |
| New: "Regent Park" at 600 Dundas St E | 600 Dundas St E is Regent Park facilities; note the **Pam McConnell Aquatic Centre (formerly Regent Park Aquatic Centre) is at 640**, a different address — don't conflate | <https://torontosocietyofarchitects.ca/buildings/regent-park-aquatic-centre-now-pam-mcconnell-aquatic-centre/> | likely |
| New: "Irving Paisley Park" at 2539A Bayview Ave | Local blog (Aug 31 2011): "Formerly known as Winfields or York Mills Park" and "The park was renamed in his honour on April 23, 2009." Irving Paisley described as a North York councillor/controller and deputy mayor, founding chair of York Finch General Hospital. **Blog, not a City source** — no City/North York council document found for the 2009 renaming. City parks listing exists. | <https://ilovenorthyork.wordpress.com/2011/08/31/irving-paisley-park/> · <https://www.toronto.ca/explore-enjoy/parks-recreation/places-spaces/parks-and-recreation-facilities/location/?id=779&title=Irving-Paisley-Park> | likely — 2009 renaming, ~17 years before the file caught it |

**Pattern worth a sentence in the article:** every renaming in this month that could be
dated was decided years earlier (2009, pre-2016, 2016). None is a July 2026 event.

---

## 7. Clusters of new addresses

### Dupont St 316–338 — ANX, Freed Developments

**FACT.** City of Toronto Final Report, *316-320 Dupont Street — Zoning Amendment
Application*, **31 May 2021**, Ward 11 University-Rosedale, planning application number
**18 270843 STE 11 OZ**:
> "This application proposes a new 9-storey (48.6 metres including a mechanical penthouse)
> office building with retail uses on the ground floor at 316-320 Dupont Street. The
> proposed office building is to be integrated with the proposed mixed use building at
> 328-332 Dupont Street."
<https://www.toronto.ca/legdocs/mmis/2021/te/bgrd/backgroundfile-167759.pdf>

**FACT.** The residential half came through the OMB/OLT, not council — By-law authority
cites "Ontario Municipal Board Decision issued on December 7, 2017 and the Ontario Land
Tribunal Order issued on March 31, 2022 in File PL110543", permitting "a 13-storey
mixed-use building on the lands municipally known in the year 2021 as 328-332 Dupont
Street". <https://www.toronto.ca/legdocs/bylaws/2022/law0219.pdf>

**FACT.** UrbanToronto project page: **ANX**, 316 Dupont Street, developer **Freed
Developments**, architect **Teeple Architects**, 13 storeys, 118 units, status
**"Complete"**; described as "316-320 Dupont (commercial/office building) and 328-332
Dupont (condominium)". Forum last post 23 July 2026.
<https://urbantoronto.ca/database/projects/anx.3768>

**INFERENCE (moderate-high):** the nine new Dupont points are ANX being addressed at
occupancy. **Nothing found** for **338 Dupont Street** specifically — the assembly of
record stops at 332.

### Bloor St W 2448–2466 — Bijou on Bloor (the Humber Cinema site)

**FACT.** City report, *Construction Staging Area Time Extension — 2442-2454 Bloor Street
West and 1-9 Riverview Gardens (Phase 3)*, **29 September 2023**, Ward 4:
> "Bloor Riverview Residences Corp is constructing a 12-storey residential condominium
> building at 2442-2454 Bloor Street West and 1-9 Riverview Gardens. The site is located
> on the north-east corner of Bloor Street West at Riverview Gardens."
Staging closures authorized "from November 30, 2023 to September 30, 2026".
<https://www.toronto.ca/legdocs/mmis/2023/te/bgrd/backgroundfile-239572.pdf>

**FACT.** Councillor Gord Perks' development page: "A 12 storey mixed-use building with
193 residential (condominium) units and ground floor retail space fronting on Bloor St W";
approved 2019; "Construction is underway and is expected to last into 2026."
<https://www.gordperks.ca/2442_2454_bloor_st_w_and_1_9_riverview_gardens>

Marketing name **Bijou on Bloor**, developer Plaza (<https://bijouonbloorcondo.ca/>).
Original OPA/ZBA item indexed as `2017.EY26.6` (page 403'd — index-level evidence only).
Unit counts differ between sources (193 at 12s post-settlement vs 244 at 14s earlier); use
193/12 storeys.

**INFERENCE (moderate):** the seven new points are this building being addressed as it
completes — the staging authorization runs to 30 September 2026, and the addresses appear
in July 2026. **Nothing found** for 2456/2460/2464/2466 Bloor St W individually; the
observed range runs about 12 numbers past the assembly's east limit.

### Old Foundry Rd 153/163/165/175 + Palace St 46/48/50/52 — one block, two frontages

**This is the strongest cluster result: the two "separate" clusters are the same city block.**

**FACT.** City report, *153 and 185 Eastern Avenue — Alterations to Designated Heritage
Properties…*, **20 January 2026**, Toronto Preservation Board, Ward 13 Toronto Centre:
> "The subject site, 153, 169, 171, and 185 Eastern Avenue, is located on the south side
> of Eastern Avenue in the West Don Lands neighbourhood, between Rolling Mills Road to the
> west, Old Foundry Road to the north, and Palace Street to the south."
> "'Tower B' (31 stories) is an affordable housing tower proposed above the Machine Shop
> building along the south portion of the site, north of Palace Street."
> "The development application proposes the in-situ retention of the original heritage
> structures and the construction of three new residential buildings."
> "On November 17, 2025, a Heritage Permit application was made to allow for alterations
> to the heritage buildings on the subject site."
Plans dated 21 May 2025 by Core Architects Inc.
<https://www.toronto.ca/legdocs/mmis/2026/pb/bgrd/backgroundfile-284230.pdf>

**FACT — the street-naming decision.** City report, *Renaming a section of Eastern Avenue
extending westerly from Lawren Harris Square*, **9 April 2025**, Director, Engineering
Support Services → Toronto and East York Community Council, Ward 13:
> "This report recommends that the name 'Old Foundry Road' be approved to rename a section
> of Eastern Avenue extending westerly from Lawren Harris Square."
> "An application was received on February 28, 2025, from Councillor Moise's office,
> originally proposed by a resident…"
> "There are four sites municipally addressed from this section of Eastern Avenue. Three
> of the four sites are owned privately, with the 4th one owned by the City of Toronto,
> under Parks jurisdiction. This renaming proposal has the support of all property owners
> abutting the renamed section."
> "The proposed name, 'Old Foundry Road,' honors the Foundry Building located on the site,
> which will be integrated into the future development."
Sketch PS-2025-11 dated 20 March 2025; signage ~$600; delegated to Community Council.
<https://www.toronto.ca/legdocs/mmis/2025/te/bgrd/backgroundfile-254491.pdf>

**FACT — timing.** Councillor Chris Moise announced it 2 April 2025 ("I will be bringing a
motion to the upcoming Toronto East York Community Council meeting on May 1", aiming for
"new signage installed by the end of 2025")
<https://www.chrismoise.ca/old_foundry_road_renaming>; the sign unveiling was
**22 July 2025**, 5–6 pm, at Lawren Harris Square (year re-checked: 2025, not 2026)
<https://www.chrismoise.ca/old_foundry_road_unveiling_ceremony>.

**FACT — the developer is Aspen Ridge, not Waterfront Toronto / Dream / Kilmer / Tricon.**
> "Aspen Ridge Homes is proposing three high-rise mixed-use buildings for the Dominion
> Foundry site… The proposal, encompassing properties from 153 to 181 Eastern Avenue,
> imagines a total of 997 dwelling units across three towers of 43, 34 and 31 stories."
— The Bridge News, **7 November 2025**
<https://thebridgenews.ca/developer-pushes-new-building-plans-on-foundry-site/>
> "The remaining heritage buildings — the west Machine Shop on Palace Street and the
> Cleaning Room at the intersection of Rolling Mills Road and Eastern Avenue — will be
> integrated into residential towers."
— The Bridge News, **4 November 2023**
<https://thebridgenews.ca/cautious-optimism-about-the-foundry-development/>
UrbanToronto tracks it as "West Don Lands: Blocks 17 & 26 | 141m | 43s | Aspen Ridge |
Core Architects"
<https://urbantoronto.ca/forum/threads/toronto-west-don-lands-blocks-17-26-141m-43s-aspen-ridge-core-architects.31716/>
The Dream/Kilmer/Tricon West Don Lands rental partnership is a **different** project
around Cherry and Mill Streets
<https://www.kilmergroup.com/dream-kilmer-and-tricon-capital-group-announce-a-partnership-to-develop-1500-purpose-built-rental-units-in-torontos-west-don-lands-region-as-part-of-the-provincial-governments-fair-housing-plan/>
— do not attribute the Foundry to them.

**INFERENCE (high):** the four Old Foundry Rd points are the address file catching up with
the 2025 street rename, not new construction. The renaming report says exactly "four sites
municipally addressed from this section of Eastern Avenue", and exactly four Old Foundry Rd
points appear; 153 carries over verbatim from 153 Eastern Avenue. Lag: signs unveiled
**22 July 2025**, addresses appear **~28 July 2026** — almost exactly one year.

**INFERENCE (moderate):** 163/165/175 are *not* a straight renumbering of 169/171/185 —
the heritage report names the parcels as 153, 169, 171, 185 Eastern; the new numbers are
153, 163, 165, 175.

**INFERENCE (moderate, geography only):** Palace St 46/48/50/52 is the south frontage of
the same Aspen Ridge site, most plausibly Tower B above the Machine Shop, which the
January 2026 report places "north of Palace Street".
**Nothing found:** any source assigning 46/48/50/52 Palace Street to any project.
Searched `"50 Palace Street" Toronto`, `"Palace Street" Toronto development application
2025 2026 West Don Lands`, `"Palace Street" Toronto "Canary" condos Dream 2026` — all empty.
**Nothing found:** a City planning application file number (`2x xxxxxx STE 13 OZ/SA`) for
the Foundry rezoning/SPA. The Jan 2026 report cites only the Heritage Permit date and
prior items (2010.TE36.20, 2021.PH20.8, 2021.TE24.11, 2023.PH3.12, Designation By-law
732-2023).

### Lower-priority clusters

- **Ellesmere Rd 3064–3070** — FACT: UrbanToronto project "3070 Ellesmere", 3070 Ellesmere
  Rd M1E 4C3, developer **Podium Developments and Reichmann International Development
  Corp**, architect Arcadis, 26 storeys, 246 units, status **Under Construction**, forum
  last post 22 August 2026.
  <https://urbantoronto.ca/database/projects/3070-ellesmere.9728>
  INFERENCE (moderate): the additions are this building being addressed as it completes.
  **Nothing found** for 3064 Ellesmere specifically.
- **Queen St W 1521/1523/1525** — FACT: City *1521 Queen Street West — Zoning By-law
  Amendment Application — Preliminary Report*, **20 February 2020**, Ward 4, application
  **19 247355 STE 04 OZ**, complete application issued 6 December 2019:
  > "This application applies to the entirety of the site located at 1521 Queen Street
  > West, which is currently occupied by a two-storey mixed-used building with four
  > commercial units at grade and 40 hotel units on the second floor."
  Proposal: an eight-storey mixed-use building; applicant BSäR Group, architect Core
  Architects; appealed to LPAT November 2020.
  <https://www.toronto.ca/legdocs/mmis/2020/te/bgrd/backgroundfile-146570.pdf> ·
  <https://parkdale.to/2020/08/27/development-application-for-1521-queen-st-w-sept-9/>
  **Nothing found** for 1523 or 1525 Queen St W as separate addresses.

**Confidence: confirmed** for Dupont/ANX, Bloor/Bijou, Old Foundry Rd renaming, the
Foundry developer, Ellesmere, Queen W. **Nothing found** for Palace St, 338 Dupont, the
upper Bloor range, 3064 Ellesmere.

---

## 8. Clusters retired

### Wellesley St W 6–16 (and Yonge St 586/586A — the same site)

**FACT.** City *Refusal Report*, **6 February 2018**, Ward 27, file **17 267875 STE 27 OZ**:
> "10-16 Wellesley Street West, 5-7 St. Nicholas Street and 586 Yonge Street — Zoning
> Amendment — Refusal Report"
> "This application proposes to amend the Zoning By-law to permit a 64-storey … mixed-use
> building at 10-16 Wellesley Street West, 5-7 St. Nicholas Street and 586 Yonge Street"
> "Heritage Easement Agreements … for the properties at 10, 12, 14 and 16 Wellesley Street
> West, 5 St. Nicholas Street, and 586 Yonge Street (including 586A Yonge Street and
> 7 St. Nicholas Street)"
<https://www.toronto.ca/legdocs/mmis/2018/te/bgrd/backgroundfile-112547.pdf>

**FACT.** By-law 101-2020 (enacted 29 January 2020): "the properties at 10-16 Wellesley
Street West contain four, two-and-a-half-storey row houses, constructed by Thomas Bryce in
1876". <https://www.toronto.ca/legdocs/bylaws/2020/law0101.pdf>

**FACT.** LPAT approved the rezoning: "On January 21, 2020, the LPAT held a hearing on the
rezoning application appeal (file #PL180340). At the conclusion of the hearing the LPAT
issued an oral decision approving the application."
<https://www.toronto.ca/legdocs/mmis/2020/pb/bgrd/backgroundfile-146247.pdf>

**FACT.** Built as **8 Wellesley Residences**, 55 storeys, 600 units, CentreCourt (with
BAZIS), IBI Group; listed under "Completed Condos".
<https://centrecourt.com/projects/8-wellesley/>

**Caveat on 6 and 8:** every page actually fetched says "10-16 Wellesley". The wording
"6-16 Wellesley Street West, 5 and 7 St. Nicholas Street and 586 Yonge Street" appears only
in **search-index text** for `2019.CC10.9` and the 2020.CC16 bill index, both 403. The
project's own marketing address is 8 Wellesley St W
(<https://condonow.com/8-Wellesley-St-W-Toronto-8-Wellesley-Condos>), which is
corroboration but not proof.

Council refused March 2018 (`2018.TE30.9`), accepted a settlement October 2019
(`2019.CC10.9`), LPAT approved January 2020.
**INFERENCE:** approval Jan 2020 → address retirement July 2026 ≈ **6.5 years' lag**.
This one cluster explains **both** Wellesley 6–16 **and** Yonge 586/586A.

### Shuter St 64–70 — demolished for Core Condos

**FACT.** City heritage report, **12 May 2014**:
> "City Council endorse the conservation strategy generally described for the heritage
> properties located at 64-70 Shuter Street to allow for the construction of a twenty-four
> storey condominium with retail uses a grade."
> "Staff have determined that the property at 64-66 Shuter Street does not meet the
> Provincial criteria for designation so staff do not oppose its demolition."
> "City Council approve the request to demolish the heritage building at 68-70 Shuter
> Street in accordance with Section 34 of the Ontario Heritage Act as proposed in Site Plan
> Application No. 14 107073 SA"
> "The properties located at 64-70 Shuter Street were listed on the City of Toronto's
> Inventory of Heritage Properties in May 1990."
<https://www.toronto.ca/legdocs/mmis/2014/te/bgrd/backgroundfile-69517.pdf>
Same report: a 1995 by-law (No. 1996-0064) for a 10-storey building "was enacted, but the
building was never built"; By-law 273-2014 designated 68-70 Shuter under the OHA.

**FACT.** Built as **Core Condos**, 68 Shuter St M5B 0B4, CentreCourt, 24 storeys, status
Complete. <https://urbantoronto.ca/database/projects/core-condos.4089>

**INFERENCE:** demolition approved May 2014 → retirement July 2026 ≈ **12 years' lag**.
(The years "demolished 2015" and "occupancy 2017" surfaced only in search-result text —
unverified, don't print.)

### Howard Park Ave 24/30/30A/60/66 — the longest lag in the month

**FACT.** City *Preliminary Report*, **17 October 2011**, reference **11 252109 STE 14 OZ**:
> "24, 28, 30, 60 and 66 Howard Park Avenue - Zoning Amendment Application - Preliminary
> Report"
> "It is currently occupied by commercial and light industrial uses associated with the
> automobile industry. There is one residential unit on the site."
> "The proposed west building is 6 stepping to 8 storeys with 104 units … The proposed east
> building is 6 stepping to 10 storeys with 96 units"
<https://www.toronto.ca/legdocs/mmis/2011/te/bgrd/backgroundfile-41816.pdf>
Built as Howard Park Residences / Howard Park 2, Triumph Developments, RAW Design.
Ward 14 Parkdale-High Park, north side between Roncesvalles and Dundas W.

**INFERENCE:** application 2011 → retirement July 2026 ≈ **15 years' lag**. Note the file
retires 30 **and** 30A but the 2011 assembly lists 28, not 30A.

### Yonge St 2496/2498/2502 — the Capitol Theatre block

**FACT.** City heritage report, **18 November 2019**:
> "Council state its Intention to Designate the properties at 2490 Yonge Street (including
> entrance addresses 2492-2502 Yonge Street) and 2506 Yonge Street (including entrance
> addresses 2508-2510 Yonge Street)"
> "These elevations will be incorporated into a new, 14-storey mixed-use residential
> building encompassing 2490-2514 Yonge Street, 10-12 Castlefield Avenue and portions of
> 20 Castlefield Avenue and 567 Duplex Avenue."
> "The property at 2490-2506 Yonge Street, the Capitol Theatre Building, was added to the
> City of Toronto's Heritage Register by City Council on November 9, 2016."
<https://www.toronto.ca/legdocs/mmis/2019/pb/bgrd/backgroundfile-140649.pdf>
Facade retention; architects Turner Fleischer, heritage consultant GBCA.
("Madison" as developer appeared only in a search summary — unverified.)
**INFERENCE:** Nov 2019 → July 2026 ≈ **6.5 years' lag**.

### Sheppard Ave W 258/260/262 — the one that tracks the world in real time

**FACT.** Demolition permits, **4 June 2026** — seven weeks before the file change:
> "Demolition permits for all six houses on the site came through on June 4. The building
> permit was filed and accepted the same week. Shoring begins in mid-July."
— STOREYS, *ELM And Fiera Break Ground At 270 Sheppard West*, groundbreaking 17 June 2026,
published 25 June 2026. <https://storeys.com/270-sheppard-elm-fiera-groundbreaking/>

**FACT.** The original application: City *Preliminary Report*, **18 September 2017**,
reference **17 190573 NNY 23 OZ**:
> "258, 260, 264, 266, 268 & 270 Sheppard Avenue West and 1 & 3 Addington Avenue -
> Official Plan Amendment and Zoning By-law Amendment Applications"
> "The subject site is comprised of six lots on Sheppard Avenue West and two lots on
> Addington Avenue."
<https://www.toronto.ca/legdocs/mmis/2017/ny/bgrd/backgroundfile-107338.pdf>

**FACT.** UrbanToronto, **27 March 2026**: "The site spans 258 through 270 Sheppard Avenue
West along with 1 through 5 Add[ington]"; references "a 2019 Ontario Land Tribunal-approved
settlement permitting a 9-storey mixed-use condominium".
<https://urbantoronto.ca/news/2026/03/new-developer-reworks-sheppard-west-mid-rise-plan-rentals.60668>
Developer **ELM Developments** with **Fiera Real Estate**, architect Studio JCI, 9–10
storeys, ~205 rental suites, first residents expected late 2028; the site went through
receivership in June 2025 before the sale closed in early 2026. Ward 23 Willowdale.

**INFERENCE:** demolition permits 4 June 2026 → retirement July 2026 ≈ **one month**. The
cleanest causal story in the month, and the shortest lag by an order of magnitude.
*Discrepancy:* the 2017 application lists 258, 260, **264**, 266, 268, 270 — no 262. The
2026 article's "258 through 270" is the better fit for the retired trio.

### Cherry St 453/461 and Cooperage St 80/100 — probably NOT a demolition

**FACT.** 461 Cherry St and 80 Cooperage St are two addresses for the same complex:
> "80 Cooperage Street and 461 Cherry Street, Toronto, Ontario"
— Infrastructure Institute case study, George Brown / Cooper Koo YMCA (the former 2015 Pan
Am athletes' village: "The George", 257-unit / 507-bed student residence, plus the 82,000
sq ft Cooper Koo Family YMCA).
<https://infrastructureinstitute.ca/case-george-brown-cooper-koo-ymca/>

**FACT.** 453 Cherry St is a standing, actively leased heritage building — the 1923
Canadian National Railway Police / CNR Office Building, marketed as "Canary District — 453
Cherry Street (CNR Building)". <https://leasing.dream.ca/building/building-1114/>

**FACT.** 80 Cooperage is still operating as the Residence & Conference Centre / The George
at George Brown <https://www.georgebrown.ca/about/campuses-locations>; 100 Cooperage is a
Green P carpark.

**FACT — and a trap to avoid.** The Port Lands Cherry Street renaming is real but
geographically elsewhere, entirely south of the Gardiner:
> "Renaming Cherry Street between the Keating Channel to Commissioners Street to
> 'Ookwemin Street'." … "Renaming a remnant portion of Cherry Street between the Gardiner
> Expressway and the Keating Channel to 'Lake Shore Boulevard East'."
— City, *2025 Road Openings and Closures in the Port Lands*, **18 December 2024**.
<https://www.toronto.ca/legdocs/mmis/2025/te/bgrd/backgroundfile-251768.pdf>
453/461 Cherry are at Front & Cherry, **north** of the rail corridor and the Gardiner. The
renaming does not reach them. **Do not connect these.**

**INFERENCE (moderate):** since all four addresses correspond to buildings that are
standing and occupied, and 461 Cherry / 80 Cooperage are documented aliases for one
complex, this retirement is most likely the City collapsing duplicate/alias address points
— a data-maintenance event, not a real-world one. **Nothing found:** any demolition permit,
development application or news story for any of these four addresses. Searched
`"461 Cherry Street" Toronto building demolition West Don Lands`,
`"Cooperage Street" Toronto renamed OR "100 Cooperage" George Brown development`,
`Toronto street renaming Cherry Street north of rail "Ookwemin" council 2025 2026 addresses
renamed` — all empty.

**Confidence: confirmed** for Wellesley, Shuter, Howard Park, Yonge 2496–2502, Sheppard.
Cherry/Cooperage cause: **nothing found**; alias collapse is inference.

---

## Cross-cutting observations for the writer

1. **The lag is the story.** Sheppard Ave W is ~1 month. Wellesley and Yonge/Capitol are
   ~6.5 years. Shuter is ~12. Coneflower is ~13. Howard Park is ~15. Erica Stark Parkette
   is ~10. Irving Paisley Park is ~17. The ECWE addresses are the only ones that arrive
   *ahead* of the thing they name — the buildings do not exist yet.
2. **The ECWE nine are an inventory, not a construction event.** Infrastructure Ontario's
   SRS contract scope is "six emergency exit buildings" and "one standalone traction power
   sub-station" — the file's EEB1/4/5/6 and TPSS1 are that contract's parts list, and the
   two entrances each at Jane and Scarlett are Metrolinx's published station design. Four
   of the six EEBs and the only TPSS get municipal numbers here; EEB2 (Russell Rd) and
   EEB3 (Wincott Dr) were already built under the advance-tunnel contract.
3. **Two "separate" clusters are one block.** Old Foundry Rd and Palace St bracket the
   Dominion Foundry site (Aspen Ridge). And two "separate" retirements are one site:
   Wellesley 6–16 and Yonge 586/586A are the 8 Wellesley assembly.
4. **Nothing in this month was decided in this month**, except possibly the Sheppard
   demolitions (4 June 2026) and the ECWE station excavation start (10 July 2026).
5. **Do not print:** the 760 m EEB spacing rule; Lawren Harris as definitely the Group of
   Seven painter; a Metrolinx source for the 2031 opening; "Jane Station" as Metrolinx's
   name for it; any connection between Cherry/Cooperage and the Port Lands renaming.

## Explicitly not researched

The 9 July restoration of fields reverted on 17 March (McCaul St spelling, eight Kimbark
Blvd municipalities, seven renumberings, 480 place-name edits including the Kennedy /
Eglinton / Glencairn Station labels returning) is a known publication artefact — a data
regression and its reversal. No external research attempted, per instruction.
