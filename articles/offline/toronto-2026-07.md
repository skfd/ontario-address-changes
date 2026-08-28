# The Crosstown West gets its addresses, and the file comes back from the past

On 28 July 2026, nine addresses appeared in Toronto's file that together describe a
subway line that isn't open yet.

| Address | What the file calls it |
|---|---|
| 1010 Jane St | Jane Station Main Entrance (Eglinton Crosstown West Extension) |
| 1015 Jane St | Jane Station Secondary Entrance (Eglinton Crosstown West Extension) |
| 400 Scarlett Rd | Scarlett Station Main Entrance (Eglinton Crosstown West Extension) |
| 401 Scarlett Rd | Scarlett Station Secondary Entrance (Eglinton Crosstown West Extension) |
| 3770 Eglinton Ave W | TPSS1 (Eglinton Crosstown West Extension) |
| 75 Richview Rd | Proposed Emergency Exit Building (EEB1) |
| 5070 Eglinton Ave W | Proposed Emergency Exit Building (EEB4) |
| 5230 Eglinton Ave W | Proposed Emergency Exit Building (EEB5) |
| 20 Matheson Blvd | Proposed Emergency Exit Building (EEB6) |

Each of the two stations gets two civic addresses — a main entrance and a secondary one
across the street. A traction power substation gets one. So do four emergency exit
buildings, the small windowless structures that surface every few hundred metres along a
tunnel and that nobody notices until they need one.

**20 Matheson Boulevard** is the best of them. Matheson Boulevard did not exist in the
address file before 28 July. It was created, as far as the file is concerned, to hold an
emergency exit.

A second new street, **Caspian Lane**, arrived two days later in Etobicoke Centre with
one address, 8 Caspian Lane.

## By the numbers

| | |
|---|---|
| New addresses | 84 |
| Retired addresses | 72 |
| Address splits | 1 |
| Renumbered | 9 |
| Street renames | 112 addresses, 1 street |
| Place-name edits | 486 |
| Status changes | 168 |
| Boundary changes | 8 |
| **Addresses on file, 31 July** | **525,462** (+12 over the month) |

Nine of the 84 additions are reissues — the same address coming back under a new record
identifier, most of them 90 through 98 Cherrywood Avenue, which came off and went back on
within the month.

## The file returns from 2025

Regular readers have been waiting for this one.

On 17 March, Toronto's published address file quietly reverted a set of fields to values
it had last carried in our April 2025 baseline. McCaul Street acquired a space and became
"Mc Caul St" on 112 of its 122 addresses. Eight houses on Kimbark Boulevard moved from
North York to former Toronto. Eight addresses were renumbered backwards — 187 Front Street
East to 185, 99 Haynes Avenue to 95, 282 Silverstone Drive to the range 282–310. And 219
address points lost their place name entirely, Kennedy, Eglinton and Glencairn stations
among them.

On **9 July**, all of it came back at once. In a single snapshot:

- 112 addresses on Mc Caul Street became McCaul Street again.
- The eight Kimbark Boulevard houses returned to North York.
- Seven of the day's nine renumberings exactly reverse March's. (An eighth, 151 Hudson
  Drive, had already flipped back on its own in May. The two left over are genuine: 133
  Wilton Street became 107, and 26½ Glasgow Street became 28 — another half-address
  converted to a letter, after June's 121½ Fern Avenue.)
- 480 place-name edits landed in that single snapshot. Across July as a whole, 247 points
  were given a name they did not have: Kennedy Station, Eglinton Station, Glencairn
  Station, Grand Avenue Park, Bell Structure, Carpark 507.
- Eighty-three coordinate changes landed too. They were held as noise, on the grounds
  that these are the same points that have been oscillating between two geocode sets all
  year.

One hundred and fourteen days, start to finish. If you took a copy of Toronto's address
data between 17 March and 9 July and treated it as current, some of what you got was a
year old. Nothing in the file itself said so. The only way to know is to have been
watching every day.

That is the entire argument for a tracker like this one, made better by the file than we
could have made it ourselves.

## Coneflower Crescent went live

Thirty-seven addresses on **Coneflower Crescent**, in York Centre, flipped from *reserved*
to *regular* on 22 July. Every one of them had been sitting on the file, assigned but not
in service, since our first snapshot in April 2025 — at least fifteen months of being a
number without being an address.

They were part of a batch of 89 promotions that day, alongside fourteen on Antibes Drive
and nine on Sir William Hearst Avenue. Another 31 followed on 28 July, seven of them on
Green Gates Court. All told, 168 addresses changed status in July, and once the 21 that
belong to the 9 July reversion are set aside, the rest are the file's quiet good news:
numbers that had been waiting are now real places.

## Where the city moved

The additions cluster in a way the previous four months didn't:

- **Dupont Street**, nine addresses added between 316 and 338 (one of them a reissue of
  316) — the corridor's steady redevelopment showing up as numbers.
- **Bloor Street West** in Bloor West Village, seven new: 2448 through 2466.
- **Old Foundry Road** (four) and **Palace Street** (four) in the Canary District.
- **Ellesmere Road** (3064–3070) and **Bellamy Road North** in Scarborough.
- Pairs on Beta Street, Galbraith Avenue, Holmstead Avenue, Elder Avenue, Logan Avenue,
  Spadina Road, Glencairn Avenue, Orchard Park Drive, Centennial Park Boulevard and
  Yonge Street.

The retirements cluster too, and mostly downtown. Four addresses came off **Wellesley
Street West** (6, 8, 10, 16) and four off **Shuter Street** (64–70). Five went from
**Howard Park Avenue**, five from **Yonge Street**, three from **Sheppard Avenue West**,
two each from Cherry Street, Cooperage Street, Anndale Drive, Lakeridge Drive, Marlee
Avenue, Oxford Street and Dufferin Street.

Three rear addresses arrived — 9R Bedford Road, 9R Spruce Street and 266R Indian Grove —
and two came off, 1245R Wilson Avenue and 744R Woodbine Avenue. The month's single split
was **245 Torrens Avenue** into 245A and 245B, original still standing.

And **2539A Bayview Avenue**, which was retired in June carrying the place name *Irving
Paisley Park*, came back in July, still carrying it.

---

### How this is measured

Every day a snapshot of Toronto's Address Points dataset is pulled and diffed against the
one before it. This piece covers the stretch between the snapshots of **30 June 2026** and
**31 July 2026**.

Counts are **net**: an address added and retired within the month nets to nothing, and
where that happened we have said so. Coordinate-only changes under 50 metres are treated
as noise and dropped, because the City's export oscillates between two geocode sets. On 9
July, 83 such coordinate edits were held on those grounds, and 3 more on 24 July; none of
them are in the numbers above.

The daily reports behind this article, including
[9 July 2026](https://skfd.github.io/ontario-address-changes/toronto/report-2026-07-09.html),
are public and list every changed address.

*Contains information licensed under the [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/).*
Source: [Address Points, City of Toronto Open Data](https://open.toronto.ca/dataset/address-points-municipal-toronto-one-address-repository/) ·
Daily reports: [ontario-address-changes](https://skfd.github.io/ontario-address-changes/toronto/)
