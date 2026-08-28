"""Look one address, street or place name up in a city's store, with dates.

Fact-checking for the monthly article. The brief says "6 Shorncliffe Rd became 6A-6E";
this says on which snapshot each of those rows appeared, what else was on the street,
and what the source properties said at the time.

    python .claude/skills/monthly-article/lookup.py toronto --addr "6 Shorncliffe Rd"
    python .claude/skills/monthly-article/lookup.py toronto --street "Shorncliffe Rd"
    python .claude/skills/monthly-article/lookup.py toronto --street "Queen St E" --month 2026-03
    python .claude/skills/monthly-article/lookup.py toronto --place "Kennedy Station"
    python .claude/skills/monthly-article/lookup.py toronto --addr "6 Shorncliffe Rd" --props
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

from src import db, diff, registry


def _dates(ds):
    return {s["id"]: diff.snap_date(s) for s in db.get_snapshots(ds)}


def _span(dates, r, last_id):
    """'2026-03-17 .. 2026-04-02' or '2026-03-17 .. present'."""
    lo = dates.get(r["min_snapshot_id"], "?")
    hi = "present" if r["max_snapshot_id"] == last_id else dates.get(r["max_snapshot_id"], "?")
    return f"{lo} .. {hi}"


def rows_for(ds, where, params):
    conn = db.init_db(ds)
    rows = [dict(r) for r in conn.execute(
        "SELECT min_snapshot_id, max_snapshot_id, identity_key, number, street, unit, "
        "full, longitude, latitude, props FROM addresses WHERE " + where +
        " ORDER BY street, CAST(number AS INTEGER), number, unit, min_snapshot_id",
        params).fetchall()]
    conn.close()
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("city")
    p.add_argument("--addr", help="full address, exact or partial (LIKE)")
    p.add_argument("--street", help="street name, exact")
    p.add_argument("--place", help="PLACE_NAME value, exact or partial")
    p.add_argument("--month", help="only rows whose span touches this YYYY-MM")
    p.add_argument("--props", action="store_true", help="dump the source properties too")
    a = p.parse_args()

    ds = registry.load(a.city)
    dates = _dates(ds)
    last_id = max(dates) if dates else 0

    if a.addr:
        rows = rows_for(ds, "full LIKE ?", (f"%{a.addr}%",))
    elif a.street:
        rows = rows_for(ds, "street = ?", (a.street,))
    elif a.place:
        rows = rows_for(ds, "props LIKE ?", (f'%"PLACE_NAME": "%{a.place}%',))
    else:
        p.error("one of --addr / --street / --place is required")

    if a.month:
        rows = [r for r in rows
                if dates.get(r["min_snapshot_id"], "") <= f"{a.month}-31"
                and (r["max_snapshot_id"] == last_id
                     or dates.get(r["max_snapshot_id"], "") >= f"{a.month}-01")]

    sys.stdout.reconfigure(encoding="utf-8")
    if not rows:
        print("no rows")
        return
    print(f"{len(rows)} row version(s) in {ds.slug}\n")
    for r in rows:
        pr = json.loads(r["props"] or "{}")
        place = pr.get("PLACE_NAME") or ""
        print(f"{_span(dates, r, last_id):<26} {r['full'] or '-':<40} "
              f"{('unit ' + r['unit']) if r['unit'] else '':<10} {place}")
        if a.props:
            for k in sorted(pr):
                print(f"    {k}: {pr[k]}")
            print(f"    coords: {r['latitude']}, {r['longitude']}")
            print(f"    identity_key: {r['identity_key']}")


if __name__ == "__main__":
    main()
