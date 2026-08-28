"""Aggregate one calendar month of a dataset's snapshots into an article brief.

The daily reports in docs/ answer "what changed on 2026-03-17". A monthly story
needs the other shape: what the city looks like after a month of edits, which
streets grew, which buildings were subdivided, what the source itself did.

Two numbers are produced for every month and they are not the same:

  net   - one diff from the last snapshot BEFORE the month to the last snapshot
          IN it. An address added on the 4th and retired on the 20th nets to
          nothing, which is what a reader means by "how many addresses did
          Toronto gain in March".
  gross - the sum of the consecutive daily diffs: edit activity, not outcome.
          Always >= net. Quote it as "edits", never as "new addresses".

Flag holds (flags.toml) are applied per snapshot date, exactly as the public
site applies them, so the brief can never contain an event the site is holding.

Usage:
    python tools/month_digest.py --city toronto --month 2026-03
    python tools/month_digest.py --city toronto --month 2026-03 --format json
    python tools/month_digest.py --city toronto --months            # what's available
"""

import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import diff, flags, registry, report

TOP_N = 15          # rows kept in each "top" list
SAMPLE_N = 25       # example rows kept for colour


# ---- snapshot selection ----

def month_of(s):
    return diff.snap_date(s)[:7]


def months_available(ds):
    """{month: [snapshot dates]} for every month with at least one snapshot."""
    out = collections.OrderedDict()
    for s in diff.nonskipped(ds):
        out.setdefault(month_of(s), []).append(diff.snap_date(s))
    return out


def complete_months(ds):
    """Months observed end to end, i.e. worth writing a monthly article about.

    Bounded on both sides is not enough: toronto's store opens with two archive
    snapshots months apart, so 2026-02 has a "previous" snapshot from the
    September before it and its first fortnight is simply unobserved. The test
    is that the snapshot immediately BEFORE the month falls in the month right
    before it (so the month opens where the previous one closed) and that at
    least one snapshot follows the month (so its tail is closed off)."""
    snaps = diff.nonskipped(ds)
    dates = [diff.snap_date(s) for s in snaps]
    months, out = months_available(ds), []
    keys = list(months)
    for mo in keys[1:-1]:
        first = dates.index(months[mo][0])
        y, m = int(mo[:4]), int(mo[5:])
        prev_mo = f"{y - 1}-12" if m == 1 else f"{y}-{m - 1:02d}"
        if dates[first - 1][:7] == prev_mo:
            out.append(mo)
    return out


# ---- aggregation ----

def _categorize(ds, mods):
    """report._category over a list of modified rows -> {category: [rows]}."""
    cats = collections.defaultdict(list)
    for m in mods:
        m["addr"] = report._addr(m)
        report._combine_location(m)
        cats[report._category(m, ds.classes, bool(ds.fields.get("number")),
                              bool(ds.fields.get("street")))].append(m)
    return cats


def _held_diff(ds, ledger, prev, cur):
    """compute_diff for one consecutive pair, with the site's flag holds applied."""
    d = diff.compute_diff(ds, prev["id"], cur["id"])
    held = flags.holds_for(ledger, ds.slug, diff.snap_date(cur))
    d, notes = flags.apply_holds(d, held)
    return d, [t for _, t in notes]


def _props(r):
    try:
        return json.loads(r.get("props") or "{}") or {}
    except ValueError:
        return {}


def _street_counts(rows):
    c = collections.Counter(r.get("street") or "-" for r in rows)
    return [{"street": s, "count": n} for s, n in c.most_common(TOP_N)]


def _prop_counts(rows, prop, limit=TOP_N):
    c = collections.Counter()
    for r in rows:
        v = _props(r).get(prop)
        if v not in (None, ""):
            c[str(v)] += 1
    return [{"value": v, "count": n} for v, n in c.most_common(limit)]


def _place_name_summary(rows):
    """Split place renames into the three things they actually are: a name
    dropped, a name given, a name changed. Toronto's PLACE_NAME churns in bulk
    (a park layer re-joined, a transit station relabelled) and the direction is
    the story - 300 names vanishing is not 300 places being renamed."""
    kinds = collections.Counter()
    lost, gained, changed = collections.Counter(), collections.Counter(), collections.Counter()
    for m in rows:
        ch = next((c for c in m["changes"] if c["field"] == "PLACE_NAME"), None)
        if not ch:
            kinds["other place field only"] += 1
            continue
        old, new = ch["old"] or "", ch["new"] or ""
        if old and not new:
            kinds["name dropped"] += 1
            lost[old] += 1
        elif new and not old:
            kinds["name given"] += 1
            gained[new] += 1
        else:
            kinds["name changed"] += 1
            changed[f"{old} -> {new}"] += 1
    return {"kinds": [{"value": k, "count": n} for k, n in kinds.most_common()],
            "lost": [{"value": k, "count": n} for k, n in lost.most_common(TOP_N)],
            "gained": [{"value": k, "count": n} for k, n in gained.most_common(TOP_N)],
            "changed": [{"value": k, "count": n} for k, n in changed.most_common(TOP_N)]}


def _sample(rows, n=SAMPLE_N):
    return [{"addr": r.get("addr") or report._addr(r),
             "street": r.get("street"), "number": r.get("number"),
             "place": _props(r).get("PLACE_NAME") or None}
            for r in rows[:n]]


def digest(ds, month):
    snaps = diff.nonskipped(ds)
    in_month = [s for s in snaps if month_of(s) == month]
    if not in_month:
        raise SystemExit(f"no snapshots for {ds.slug} in {month}")
    first_idx = snaps.index(in_month[0])
    if first_idx == 0:
        raise SystemExit(f"{month} is {ds.slug}'s first observed month - nothing to diff "
                         "its opening against")
    opening = snaps[first_idx - 1]     # last snapshot before the month
    closing = in_month[-1]
    ledger = flags.load_ledger()

    # --- per-day (gross) ---
    timeline, held_notes = [], []
    gross = collections.Counter()
    for prev, cur in zip(snaps[first_idx - 1:], in_month):
        d, notes = _held_diff(ds, ledger, prev, cur)
        cats = _categorize(ds, d["modified"])
        day = {"date": diff.snap_date(cur), "added": len(d["added"]),
               "removed": len(d["removed"]),
               **{k: len(v) for k, v in sorted(cats.items())}}
        timeline.append(day)
        for k, v in day.items():
            if k != "date":
                gross[k] += v
        held_notes += [f"{diff.snap_date(cur)}: {t}" for t in notes]

    # --- endpoint (net) ---
    net = diff.compute_diff(ds, opening["id"], closing["id"])
    # A held mass event is held for the whole month, not just its day: strip the
    # same field sets from the endpoint diff so net can't smuggle back what the
    # site is holding.
    held_fieldsets = {tuple(sorted(f.get("fields", [])))
                      for s in in_month
                      for f in flags.holds_for(ledger, ds.slug, diff.snap_date(s))
                      if f["signature"] == "mass-modified"}
    if held_fieldsets:
        net["modified"] = [m for m in net["modified"]
                           if flags._fieldset(m) not in held_fieldsets]
    net_cats = _categorize(ds, net["modified"])

    split_groups, added_rest = report._group_splits(
        net["added"], net["removed"],
        lambda pairs: diff.bases_active(ds, pairs, closing["id"]))

    # streets debuting inside the month
    by_sid = diff.new_streets_by_snapshot(ds)
    debut = [dict(x, date=diff.snap_date(s)) for s in in_month for x in by_sid.get(s["id"], [])]
    debut.sort(key=lambda x: -x["count"])

    return {
        "meta": {
            "slug": ds.slug, "provider": ds.provider, "month": month,
            "license_name": ds.license_name, "source_url": ds.data_url,
            "opening_snapshot": diff.snap_date(opening),
            "closing_snapshot": diff.snap_date(closing),
            "snapshot_dates": [diff.snap_date(s) for s in in_month],
            "snapshot_count": len(in_month),
            "row_count_open": opening["row_count"],
            "row_count_close": closing["row_count"],
            "held_events": held_notes,
        },
        "net": {
            "added": len(net["added"]), "removed": len(net["removed"]),
            **{k: len(v) for k, v in sorted(net_cats.items())},
            "split_events": len(split_groups),
        },
        "gross": dict(sorted(gross.items())),
        "timeline": timeline,
        "top_streets_added": _street_counts(net["added"]),
        "top_streets_removed": _street_counts(net["removed"]),
        "new_streets": debut[:TOP_N],
        "splits": [{"base": g["base_addr"], "kind": g["kind"], "count": g["count"],
                    "parent": g["parent"], "children": g["children_label"]}
                   for g in split_groups[:TOP_N]],
        "renames": [{"old": g["old"], "new": g["new"], "count": g["count"]}
                    for g in report._group_renames(net_cats.get("renamed", []))],
        "renumbered": [{"addr": m["addr"],
                        "changes": [{"field": c["display_field"], "old": c["old"],
                                     "new": c["new"]} for c in m["changes"]]}
                       for m in net_cats.get("renumbered", [])[:TOP_N]],
        "status_transitions": [
            {"count": g["count"],
             "changes": [{"field": c["display_field"], "old": c["old"], "new": c["new"]}
                         for c in g["changes"]]}
            for g in report._group_transitions(net_cats.get("status", []))[:TOP_N]],
        "boundary_transitions": [
            {"count": g["count"],
             "changes": [{"field": c["display_field"], "old": c["old"], "new": c["new"]}
                         for c in g["changes"]]}
            for g in report._group_transitions(net_cats.get("boundary", []))[:TOP_N]],
        "place_name_summary": _place_name_summary(net_cats.get("place_name", [])),
        "place_name_changes": [
            {"count": g["count"],
             "changes": [{"field": c["display_field"], "old": c["old"], "new": c["new"]}
                         for c in g["changes"]]}
            for g in report._group_transitions(net_cats.get("place_name", []))[:TOP_N]],
        "significant_fieldsets": [
            {"fields": list(k), "count": n} for k, n in collections.Counter(
                tuple(sorted(c["display_field"] for c in m["changes"]))
                for m in net_cats.get("significant", [])).most_common(TOP_N)],
        "place_names_added": _prop_counts(net["added"], "PLACE_NAME"),
        "wards_added": _prop_counts(net["added"], "WARD_NAME") or _prop_counts(net["added"], "WARD"),
        "wards_removed": _prop_counts(net["removed"], "WARD_NAME") or _prop_counts(net["removed"], "WARD"),
        "sample_added": _sample(added_rest),
        "sample_removed": _sample(net["removed"]),
        "biggest_moves": sorted(
            ({"addr": m["addr"],
              "metres": round(next((c["dist_m"] for c in m["changes"]
                                    if c["field"] == "location" and c.get("dist_m")), 0))}
             for m in net_cats.get("location", [])),
            key=lambda x: -x["metres"])[:TOP_N],
    }


# ---- text rendering ----

def _cell(v):
    if isinstance(v, list):
        return "; ".join(f"{c['field']}: {c['old']} -> {c['new']}" if isinstance(c, dict)
                         else str(c) for c in v)
    return "" if v is None else str(v)


def _table(rows, cols):
    if not rows:
        return "  (none)"
    return "\n".join("  " + "  ".join(_cell(r.get(c)) for c in cols) for r in rows)


def as_text(g):
    m, net = g["meta"], g["net"]
    o = [f"# {m['provider']} - {m['month']}",
         f"{m['snapshot_count']} snapshots ({m['snapshot_dates'][0]} .. {m['snapshot_dates'][-1]}); "
         f"net measured {m['opening_snapshot']} -> {m['closing_snapshot']}",
         f"rows: {m['row_count_open']:,} -> {m['row_count_close']:,} "
         f"({m['row_count_close'] - m['row_count_open']:+,})",
         f"licence: {m['license_name']}"]
    if m["held_events"]:
        o.append("HELD (flags.toml, excluded from every number below):")
        o += ["  " + h for h in m["held_events"]]
    o.append("")
    o.append("NET (outcome over the month):")
    o += [f"  {k}: {v:,}" for k, v in net.items() if v]
    o.append("GROSS (sum of daily edits - activity, not outcome):")
    o += [f"  {k}: {v:,}" for k, v in g["gross"].items() if v]
    o.append("")
    o.append("Busiest days:")
    busy = sorted(g["timeline"],
                  key=lambda d: -sum(v for k, v in d.items() if k != "date"))[:5]
    o.append(_table(busy, ["date", "added", "removed", "significant", "location"]))
    pn = g["place_name_summary"]
    if any(pn.values()):
        o.append("\nPlace-name changes by direction:")
        o.append(_table(pn["kinds"], ["count", "value"]))
        for sub, label in (("lost", "names dropped"), ("gained", "names given"),
                           ("changed", "names changed")):
            if pn[sub]:
                o.append(f"  top {label}:")
                o.append(_table(pn[sub], ["count", "value"]))
    for title, key, cols in (
            ("Streets gaining the most addresses", "top_streets_added", ["count", "street"]),
            ("Streets losing the most addresses", "top_streets_removed", ["count", "street"]),
            ("Streets appearing for the first time", "new_streets", ["count", "street", "date"]),
            ("Address splits", "splits", ["count", "base", "kind", "parent", "children"]),
            ("Street renames", "renames", ["count", "old", "new"]),
            ("Renumbered", "renumbered", ["addr", "changes"]),
            ("Status transitions", "status_transitions", ["count", "changes"]),
            ("Boundary transitions", "boundary_transitions", ["count", "changes"]),
            ("Place renames", "place_name_changes", ["count", "changes"]),
            ("Other modifications by changed-field set", "significant_fieldsets", ["count", "fields"]),
            ("Place names on new addresses", "place_names_added", ["count", "value"]),
            ("Wards gaining addresses", "wards_added", ["count", "value"]),
            ("Wards losing addresses", "wards_removed", ["count", "value"]),
            ("Biggest location moves", "biggest_moves", ["metres", "addr"]),
            ("Sample new addresses", "sample_added", ["addr", "place"]),
            ("Sample retired addresses", "sample_removed", ["addr", "place"])):
        o.append(f"\n{title}:")
        o.append(_table(g[key], cols))
    return "\n".join(o) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--city", default="toronto")
    p.add_argument("--month", help="YYYY-MM")
    p.add_argument("--months", action="store_true",
                   help="list observed months and which are complete")
    p.add_argument("--format", choices=("text", "json"), default="text")
    p.add_argument("--out", help="write to this path instead of stdout")
    a = p.parse_args()

    ds = registry.load(a.city)
    if a.months or not a.month:
        avail, done = months_available(ds), set(complete_months(ds))
        for mo, dates in avail.items():
            print(f"{mo}  {len(dates):>3} snapshots  {dates[0]} .. {dates[-1]}"
                  f"{'  [complete]' if mo in done else ''}")
        return

    g = digest(ds, a.month)
    text = json.dumps(g, indent=2, ensure_ascii=False) if a.format == "json" else as_text(g)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {a.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)


if __name__ == "__main__":
    main()
