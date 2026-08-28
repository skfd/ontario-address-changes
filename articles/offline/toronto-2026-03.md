# A block of Queen East leaves the map, and the file slips four months into the past

On 6 March 2026, eleven addresses disappeared from Toronto's address file in one go:
1226, 1228, 1230, 1232, 1234, 1236, 1240, 1244, 1246, 1248 and 1250 Queen Street East.
Every one of them had been on file since the first snapshot we hold, in April 2025.
They went together, and none has come back.

That is one continuous stretch of Queen East in Leslieville, between Greenwood and
Coxwell, now a gap in the file.

Eleven days later, something stranger happened to the file itself. We'll get to that.

## By the numbers

| | |
|---|---|
| New addresses | 50 |
| Retired addresses | 22 |
| Renumbered | 8 |
| Street renames | 112 addresses, 1 street |
| Address splits | 3 |
| Place-name edits | 386 |
| Status changes | 19 |
| Boundary changes | 8 |
| **Addresses on file, 27 March** | **525,387** (+28 over the month) |

Twenty-eight net addresses in a city of half a million is a rounding error, and that is
normal. Toronto's address file is not a construction log — it is a record of paperwork
completing. Most months it moves by a few dozen.

## What a retired address does and doesn't mean

An address leaving the file means the City stopped publishing it as a current civic
address. It can mean a building was demolished. It can also mean several addresses were
merged into one, or that a duplicate was found, or that a lot was reclassified. The file
does not say which, and neither will we.

What the file does say about 1226–1250 Queen East is that they went at once, on the same
day, and that no replacement addresses had been assigned in their place by the end of
the month. When a block is redeveloped the new addresses usually arrive later, sometimes
a year later, sometimes as a single number where eleven used to be. That is something to
watch rather than something to conclude.

## Three lots became thirteen addresses

March's other side of the ledger is the small, dense kind of growth that shows up as
letters after a number.

- **6 Shorncliffe Road** in Etobicoke gained 6A, 6B, 6C, 6D and 6E on 26 March. There
  has never been a plain "6 Shorncliffe Rd" in any snapshot we hold — the five arrived
  as a set, on a lot the file had not addressed before.
- **33 Reidmount Avenue** in Agincourt gained 33A through 33D, and **372 Glen Park
  Avenue** in North York gained 372A through 372D. In both cases the original address is
  still on file alongside its four new siblings.

All thirteen were filed as *reserved* rather than *regular* — the City's way of saying
an address has been assigned but is not yet in service. Numbers arrive before buildings
do.

Four more addresses appeared on Perth Avenue (70–76), four on King Street West
(1452–1458), and four on Dundas Street West in the Junction (2424–2432) in the same
month that 2440 Dundas West came off.

One new street appeared: **YZD Lane**, with a single address, 81 YZD Lane, on the
Downsview lands south of Sheppard Avenue West. YZD is the aviation identifier for
Downsview Airport. The lane is the first piece of that redevelopment to reach the
address file.

And on 25 March, **476 Front Street East** was added carrying the place name **Diamond
Jubilee Promenade**. New addresses rarely arrive with a name attached. This one did.

## On 17 March, the file went back to April 2025

Then there is the 17 March snapshot, which changed more rows than the rest of the month
combined and changed nothing at all about the city.

That day, 112 of the 122 addresses on **McCaul Street** were restyled as **"Mc Caul
St"** — same street, one extra space. Eight houses on **Kimbark Boulevard**, numbers 26
through 40, moved from *North York* to *former Toronto* without anyone moving. Eight
addresses were renumbered: 26 Balding Court became 24, 187 Front Street East became 185,
99 Haynes Avenue became 95, and 282 Silverstone Drive became the range 282–310. The
place name was stripped from 219 address points — Kennedy, Eglinton and Glencairn
stations, parks, Bell equipment, City car parks — and rewritten on 150 more.

Every one of those values is the value the same record carried in our **April 2025**
baseline. And on 9 July, four months later, every one of them flipped back: McCaul lost
its space, Kimbark returned to North York, 24 Balding Court became 26 again.

The plainest reading is that the published file spent four months serving an older
build. We can't prove the mechanism from the outside — only that the values went
backwards on 17 March and forwards again on 9 July, together, in lockstep. If you pulled
Toronto's address data between those dates and treated it as current, this is the sort of
thing worth knowing about.

It is also the reason a tracker like this exists. A single download tells you what the
file says today. Only the sequence tells you when it changed its mind.

---

### How this is measured

Every day a snapshot of Toronto's Address Points dataset is pulled and diffed against
the one before it. This piece covers the stretch between the snapshots of **27 February
2026** and **27 March 2026** — the file's last reading before March and its last reading
in it — so a few days at each end of the calendar month fall into the neighbouring
articles.

Counts are **net**: an address added and retired within the month nets to nothing.
Coordinate-only changes under 50 metres are treated as noise and dropped, because the
City's export oscillates between two geocode sets and the same points move back and
forth month after month. On 17 March, 52 such coordinate edits were held on exactly
those grounds and are in none of the numbers above.

The daily reports behind this article, including
[17 March 2026](https://skfd.github.io/ontario-address-changes/toronto/report-2026-03-17.html),
are public and list every changed address.

*Contains information licensed under the [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/).*
Source: [Address Points, City of Toronto Open Data](https://open.toronto.ca/dataset/address-points-municipal-toronto-one-address-repository/) ·
Daily reports: [ontario-address-changes](https://skfd.github.io/ontario-address-changes/toronto/)
