# House style

## Who is reading

Someone who lives in the city, walks past the buildings, and has never thought about
the address file. They do not know what a civic-address point is and will not read a
paragraph that explains it in the abstract. They *will* read "6 Shorncliffe Road became
6A through 6E" because they can picture it.

So: every abstraction arrives attached to an address. No sentence explains the dataset
before there is a reason to care about the dataset.

## Voice

- Plain, specific, unhurried. Short sentences carry the numbers; longer ones carry the
  reasoning.
- Concrete nouns over categories. Not "a split event with parent retired" but "the old
  address was retired the same day the five new ones appeared".
- The city is not a subject with intentions. A street was renamed; the city did not
  "decide to embrace" anything. Say who did what only when the record says so.
- No hype adjectives (massive, staggering, explosive) and no false drama. A month with
  50 new addresses is a quiet month and saying so is more interesting than pretending
  otherwise.
- Never guess at cause. The address file records that 33 Reidmount Ave gained A–D; it
  does not record that a house was demolished. Write "the record shows", or go and
  check a source that does know, or leave it out. **"Probably a fourplex" is the exact
  sentence that gets the piece quoted and then corrected.**
- Uncertainty is allowed and should be flagged in the text, not smoothed over: "the
  file does not say why" is a fine sentence.
- Canadian spelling (centre, neighbourhood, licence as noun).

## Skeleton

```markdown
# <Title: what happened, not what this is>

<Two or three sentences. The single most interesting thing in the month, stated
concretely, with an address or a street name in it.>

## By the numbers

| | |
|---|---|
| New addresses | 50 |
| Retired | 22 |
| Renumbered | 8 |
| Street renames | 112 addresses on 1 street |
| Address splits | 3 |
| Total on file at month end | 525,387 |

<One sentence putting the scale in perspective — a share of the whole file, or a
comparison to the previous month once there is one to compare to.>

## <Lead story, named for the thing itself>

## <Second story>

## <Third story, often "what the file itself did">

## <Quiet closer, or what to watch next month>

---
*How this is measured* — <one paragraph: snapshot window, net vs gross, the noise
floor, link to the day's report.>

*<Attribution line>* · *<link to source dataset>* · *<link to live site>*
```

Headings are the names of things, not labels: "McCaul Street lost a letter", not
"Street renames".

## Picking the lead

In rough order of how much a reader cares:

1. **A place they know changed** — a named building, park, station or landmark whose
   address or name moved.
2. **A visible split** — one address becoming five suffixed ones, or a base address
   turning into thirty units. This is a building being subdivided or a tower opening,
   and it is the most legible form of "the city got denser".
3. **A street rename or a new street** — a street debuting in the file is usually a
   new subdivision road; a rename is usually a correction, occasionally a commemoration.
4. **A cluster** — several new addresses on one street in one month is a project.
   Check whether it is one site before calling it one.
5. **A source-side event** — a bulk recode, hundreds of place names dropped, a
   restyled string. Genuinely interesting *as* a story about how the record is kept,
   as long as it is framed that way and not as physical change to the city.

If nothing clears bar 1–4, the source-side event leads and the piece is shorter.

## The quiet-month shape

Some months are 40 additions and nothing else. Do not pad. Write 400 words:
the numbers, the two or three most concrete individual items, and one honest
paragraph about what a quiet month means — the file is a record of paperwork
completing, not of construction happening, and paperwork has slow months.

A quiet month is also the right place to explain one mechanic properly (what a
retired address means, why a number goes backwards) since there is room for it.

## Length

The series runs 900-1,200 words offline and 1,300-1,700 words researched (March to
July 2026). A month that comes out at twice that is not twice as interesting; it is a
piece that kept every finding. Cut supporting items before cutting sentences from the
lead, and keep the research file as the place where everything found gets to stay.

## Traps

- **Mentioning the other variant.** The researched piece never says "the offline
  version of this piece could only..." - a reader gets one piece, and it stands alone.
  Say what the file itself does and does not say, then what the record adds.
- **Gross quoted as net.** See SKILL.md. The single most likely factual error.
- **Held events.** Anything under `HELD` in the brief is excluded from the numbers by
  design. Never write it in as news, and never quietly restore it.
- **Location noise.** Toronto's export oscillates between two geocode sets; moves under
  50 m are dropped as noise. Do not write "N addresses moved" from a location count
  without reading `location_min_move_m` in the dataset TOML and the flag notes.
- **A retired address is not a demolition.** It is a record leaving the file, which
  can mean demolition, a merge, a correction, or a reclassification.
- **A renumbering is not a mistake being fixed.** 187 Front St E becoming 185 could be
  a correction, a redevelopment, or a range being restated. The file does not say.
- **Ward counts move with boundaries.** A ward "losing" addresses may have had its
  boundary redrawn; check the boundary transitions section before attributing it to
  the neighbourhood.
- **Don't republish the table.** The article quotes a handful of addresses to tell a
  story. Wholesale reproduction of the dataset belongs on the site under its licence,
  not pasted into a newsletter.
