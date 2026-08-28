# Researching a month

The store answers *what changed and when*. It cannot answer *why*, and the why is the
half of the story a reader actually wants: eleven addresses left Queen Street East, and
the file has no opinion about whether that was a fire, an assembly or a clerical merge.

This step goes and looks. It runs **after** the brief and **before** any writing, so
that what you find shapes which story leads rather than getting bolted onto a draft.

## Get the checklist

```
python tools/month_digest.py --city toronto --month 2026-03 --format entities
```

That prints the month's proper nouns grouped by kind, ordered by how likely each is to
have a public paper trail: new streets, streets that gained or lost three or more
addresses, splits, renames, place names given and changed.

It is a checklist, not a quota. A month has fifty additions and maybe six things worth
a search. Work down the list until the returns stop.

## Where the answers actually live

| Kind of question | Go here |
|---|---|
| Why does this street have this name? | Toronto street naming goes through community council. Search `site:toronto.ca` for the street name plus "street naming", and the council agenda item; Wikipedia for the person commemorated |
| What is being built at this address? | UrbanToronto (`urbantoronto.ca`) is the best-indexed source for Toronto development applications by address; the City's Application Information Centre (`app.toronto.ca/AIC`) is authoritative but harder to search |
| Why did a block come off the file? | Search the address range plus "demolition", "development application", "rezoning"; then local press — blogTO, Toronto Star, CBC Toronto |
| Transit structures (station entrances, exit buildings, substations) | Metrolinx project pages for the named line; the TTC for existing stations |
| Parks, community centres, arenas | `toronto.ca/parks` and the facility's own page; a renaming usually has a council decision |
| A name's history or meaning | Wikipedia, Canadian Encyclopedia, Ontario Heritage Trust — for people, treaties, Indigenous place names |

Search the **address with the street** (`"1226 Queen Street East" Toronto`), not the
number alone. For a range, search the corner or the assembly ("Queen Greenwood
Leslieville development").

### What actually works, from the first five months of doing this

- **Toronto's CKAN open data beats web search for a single address.** `datastore_search`
  against the development-applications, building-permit and Committee of Adjustment
  resources answers "what is happening at 152 Pinegrove Ave" in one call, with an
  application number and a date, where a web search returns nothing. Building permits
  carry a `structure type` field that has resolved questions the program pages could
  not — 407 Arlington Ave came back "Laneway / Rear Yard Suite".
- **`secure.toronto.ca` 403s automated fetches.** Council agenda items are reachable via
  search-engine caches and `toronto.ca` staff-report PDFs instead; a decision you can
  only see through the council portal has to be checked by hand.
- **The Application Information Centre is a JavaScript-only page.** Anything read off it
  needs a browser confirmation before it goes in an article — flag it in the notes.
- **Reverse-geocode before believing a gloss.** Read the file's coordinates against a
  map rather than trusting a neighbourhood name in the brief or in your own head; then
  cross-check with `lookup.py --near`, which names the streets next door from the store
  itself.

## Rules

1. **Every fact from a search gets a link in the article.** No link, no claim. This is
   the whole point of the step — it converts model recall into something a reader can
   check.
2. **A search that finds nothing is a result.** Write "the public record is silent on
   why", not a plausible guess. Months where the search comes back empty are honest
   months, and saying so is more interesting than filling the gap.
3. **The store wins on the file, the web wins on the world.** If a news story says a
   building was demolished in January and the address left the file in April, both are
   true and the gap is the story — the file lags the world. Never adjust a store number
   to match a source.
4. **Attribute the uncertainty, not just the fact.** "A development application for the
   site was filed in 2024" is checkable. "The block was demolished for that development"
   usually is not, unless something says so.
5. **Don't research the reader into a coma.** Two or three sourced explanations per
   article. The rest of the piece stays as it is in the offline version.
6. **Watch for the wrong city.** Ontario reuses street names, and so does the rest of
   the continent. Confirm Toronto in the source before using it.

## Recording what you find

Write the findings to `articles/research/<slug>-<YYYY-MM>.md` as a flat list — entity,
what was found, URL, and a one-line confidence note — before writing the article. Two
reasons: the article should be written from notes rather than from a browser, and the
next person to touch the month can see what was already searched and came back empty.

## The two variants

Each month currently gets written twice, and the difference is exactly this step:

- `articles/offline/<slug>-<YYYY-MM>.md` — written from the store alone. No external
  facts, no neighbourhood names that aren't derivable from ward and coordinates, no
  acronym expansions the file doesn't spell out.
- `articles/researched/<slug>-<YYYY-MM>.md` — the same month with this step applied:
  sourced causes, links, and the willingness to say what the file cannot.

They are a live comparison, not a permanent arrangement. If one is dropped, delete its
directory and this section, and fold the survivor's path back into SKILL.md step 6.
