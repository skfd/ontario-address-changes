# Nothing was demolished on Queen East

On 6 March 2026, eleven addresses vanished from Toronto's address file in one go: 1226,
1228, 1230, 1232, 1234, 1236, 1240, 1244, 1246, 1248 and 1250 Queen Street East, in
Leslieville between Greenwood and Coxwell. Every one had been on file since our first
snapshot in April 2025. None has come back.

The obvious reading is a block being cleared. It is also, as far as anyone can tell,
wrong.

There is **no development application, no Committee of Adjustment file, and no building or
demolition permit** filed against any of those eleven addresses, in any of the City's four
relevant open datasets. No news coverage of a fire, a demolition or an assembly on that
stretch. The record is empty.

What the record does contain is the shape of something else entirely.

## Ten numbers that were never really eleven buildings

Look at the addresses that *stayed*. The retirement takes out an interleaved run, not a
contiguous parcel: **1238 and 1242 Queen East survived**, sitting between the retired
numbers, along with 1220, 1256, 1256A and 1260.

1238 is Chartwell Avondale Retirement Residence, a 79-suite home that has been in
Leslieville over twenty years — and, in Chartwell's own words, is "nestled above a retail
complex" with a dental clinic, banks and a bakery. That retail is leased **by unit letter
under the single number 1238**: listings read "Unit F-1238 Queen St E", not a street
number of their own. Two sign permits confirm the tenants — one for Chartwell, one for
H&R Block — both filed under 1238.

Now look at the identity keys. In the City's source data, the ten retired points 1228
through 1250 carry consecutive `ADDRESS_POINT_ID` values, 14205472 to 14205481, an
unbroken descending run. Consecutive ids mean the ten were created in a single batch. The
survivor, 1238, sits far away at 8407945, in the same old range as its neighbours.

Ten numbers issued together, retired together, along a frontage whose businesses are
addressed by unit under one number, with the one named point left standing. That reads as
a cleanup — legacy per-storefront civic numbers folded back into 1238 — and not as a
building coming down.

**No document says so.** That is an inference, and it stays labelled as one. What is
established is the absence: nothing was permitted to be demolished there.

## And the redevelopment is across the street

There *is* a live project on that block, which is exactly why this needed checking. 1233
to 1251 Queen East — a nine-storey, 149-unit mixed-use building by Core Development and
Woodbourne, zoning application `22 123730 STE 14 OZ`, conditional foundation permit issued
29 January 2026 — is on the **odd** side, about forty metres south.

Every one of those odd-side addresses is still on the file today.

An article written from the address data alone, reaching for the nearest plausible cause,
would have put a demolition and a development on the same block and been wrong twice.

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

## The lane that is a stadium

**YZD Lane** entered the file on 3 March with exactly one address: 81 YZD Lane. It is a
real street — the Toronto Centreline carries it as `LINEAR_NAME_ID 30296`, jurisdiction
**private**, address range 81 to 81, one number on the odd side and nothing else.

81 YZD Lane is **Rogers Stadium**, the 50,000-capacity temporary concert venue on the
former Downsview Airport lands. Live Nation and Ticketmaster both use that address. The
stadium opened on **29 June 2025**, eight months before its address reached the file.

YZD is the airport's old aviation code, and now Northcrest Developments' brand for the
whole 370-acre redevelopment. The stadium is temporary — five years or so, then the land
turns into a neighbourhood.

One thing left unadjudicated: Wikipedia gives Rogers Stadium's address as 105 Carl Hall
Road. The promoters say 81 YZD Lane. Both are recorded here; the file has only ever
carried the second.

## 476 Front Street East is a park

The new address of 25 March that arrived carrying the place name **Diamond Jubilee
Promenade** turns out to be exactly what it sounds like. A 2024 City Council attachment
listing every park in Toronto has it as `DIAMOND JUBILEE PROMENADE | 13 | Toronto East
York | Neighbourhood`. It has a City facility page with a splash pad and a drinking
fountain, and it sits on the north side of Front Street East in the West Don Lands, part
of Waterfront Toronto's Front Street Promenade.

## Three splits, three committee decisions

March's splits all trace to a Committee of Adjustment consent, and the dates are worth
having:

- **33 Reidmount Avenue** → 33A–33D, on file 3 March. Consent `B0033/24SC` with two
  variances, approved 12 February 2025 — about a year ahead.
- **372 Glen Park Avenue** → 372A–372D, on file 3 March. Consent `B0025/25NY`, heard 8
  January 2026, for "a fourplex and accessory garden suite on each lot" — which is why
  four suffixes appear where two lots were severed.
- **6 Shorncliffe Road** → 6A–6E, on file 26 March. **Nothing found.** No application, no
  permit, no committee file. Five addresses on a lot that never carried a plain number 6,
  and no public record of why.

Two of March's clusters also have projects behind them. The four new addresses on **Perth
Avenue** belong to Castlepoint Numa and Hazelview's 18-storey, 255-unit building — which
did not break ground until **22 May 2026**, two and a half months *after* the addresses
appeared. The four on **Dundas Street West** in the Junction are Fora Developments' towers
on the FreshCo plaza site. The four on **King Street West** have no record at all.

## And then, on 17 March, the file went back to April 2025

The month's largest event changed more rows than everything above combined and changed
nothing about the city.

That day, 112 of the 122 addresses on McCaul Street were restyled "Mc Caul St". Eight
houses on Kimbark Boulevard moved from North York to former Toronto. Eight addresses were
renumbered backwards — 187 Front Street East to 185, 99 Haynes Avenue to 95. The place
name was stripped from 219 points, Kennedy, Eglinton and Glencairn stations among them,
and rewritten on 150 more.

Every one of those values is the value the same record carried in our April 2025 baseline.
On 9 July, all of it flipped back.

This one needs no outside source, and no outside source would have caught it. It is
visible only in the sequence — and only if someone was pulling the file every day.

---

### How this is measured

Every day a snapshot of Toronto's Address Points dataset is pulled and diffed against the
one before it. This piece covers the stretch between the snapshots of **27 February 2026**
and **27 March 2026**. Counts are **net**. Coordinate-only changes under 50 metres are
dropped as noise; 52 such edits on 17 March were held on those grounds.

Causes come from the City's own published records, linked below. Where the record is
silent — the Queen East eleven, 6 Shorncliffe Road, 1452–1458 King Street West, any
council naming for YZD Lane — this piece says so. An absence of records is not proof that
nothing happened; it is proof that nothing was filed.

**Sources.** [Development Applications](https://open.toronto.ca/dataset/development-applications/) ·
[Committee of Adjustment Applications](https://open.toronto.ca/dataset/committee-of-adjustment-applications/) ·
[Building Permits](https://open.toronto.ca/dataset/building-permits-active-permits/) ·
[Toronto Centreline](https://open.toronto.ca/dataset/toronto-centreline-tcl/) ·
[Chartwell Avondale Retirement Residence](https://chartwell.com/on/toronto/avondale) ·
[1233 Queen East, UrbanToronto](https://urbantoronto.ca/forum/threads/toronto-1233-queen-east-35-7m-9s-core-development-studio-jci.33338/) ·
[Rogers Stadium, Live Nation](https://www.livenation.com/venue/KovZ917ARzt/rogers-stadium-events) ·
[Rogers Stadium opening, UrbanToronto](https://urbantoronto.ca/news/2025/06/rogers-stadium-opens-sunday-downsview-torontos-largest-outdoor-concert-venue.58877) ·
[YZD, Northcrest Developments](https://www.yzd.ca/) ·
[Citywide Parks List and Classification (2024)](https://www.toronto.ca/legdocs/mmis/2024/cc/bgrd/backgroundfile-250430.pdf) ·
[Front Street Promenade, Waterfront Toronto](https://www.waterfrontoronto.ca/our-projects/front-street-promenade)

*Contains information licensed under the [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/).*
Source dataset: [Address Points, City of Toronto Open Data](https://open.toronto.ca/dataset/address-points-municipal-toronto-one-address-repository/) ·
Daily reports: [ontario-address-changes](https://skfd.github.io/ontario-address-changes/toronto/)
