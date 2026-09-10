"""Look one address, street or place name up in a city's store, with dates.

Fact-checking for the monthly article. The brief says "6 Shorncliffe Rd became 6A-6E";
this says on which snapshot each of those rows appeared, what else was on the street,
and what the source properties said at the time.

    python .claude/skills/monthly-article/lookup.py toronto --addr "6 Shorncliffe Rd"
    python .claude/skills/monthly-article/lookup.py toronto --street "Shorncliffe Rd"
    python .claude/skills/monthly-article/lookup.py toronto --street "Queen St E" --month 2026-03
    python .claude/skills/monthly-article/lookup.py toronto --place "Kennedy Station"
    python .claude/skills/monthly-article/lookup.py toronto --addr "6 Shorncliffe Rd" --props
    python .claude/skills/monthly-article/lookup.py toronto --near "18 Chloe Cooley St"
"""

import argparse
import json
import math
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


def near(ds, conn, lat0, lon0, last_id, street=None, limit=12):
    """Nearest active address on each *other* street, closest first.

    Answers "where is this, actually" without leaving the store. A new street has
    coordinates and nothing else; its neighbours are what place it. Written after
    an article located Chloe Cooley St in the West Don Lands from memory when
    33 Richardson St was sitting 28 m away in the same database.
    """
    box = conn.execute(
        "SELECT full, street, latitude, longitude FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ? "
        "AND latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?",
        (last_id, last_id, lat0 - 0.0035, lat0 + 0.0035,
         lon0 - 0.0045, lon0 + 0.0045)).fetchall()
    out = []
    for r in box:
        if r["latitude"] is None or r["longitude"] is None:
            continue
        mid = math.radians((lat0 + r["latitude"]) / 2)
        out.append((math.hypot((r["longitude"] - lon0) * 111_320 * math.cos(mid),
                               (r["latitude"] - lat0) * 111_320), r))
    out.sort(key=lambda x: x[0])
    # The anchor's own street is not a neighbour: without this the first hit
    # was always the anchor itself at 0 m.
    seen, rows = {street}, []
    for d, r in out:
        if r["street"] in seen:
            continue
        seen.add(r["street"])
        rows.append((round(d), r["full"]))
        if len(rows) >= limit:
            break
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("city")
    p.add_argument("--addr", help="full address, exact or partial (LIKE)")
    p.add_argument("--street", help="street name, exact")
    p.add_argument("--place", help="PLACE_NAME value, exact or partial")
    p.add_argument("--near", metavar="ADDR",
                   help="locate an address: nearest active address on each other street")
    p.add_argument("--month", help="only rows whose span touches this YYYY-MM")
    p.add_argument("--props", action="store_true", help="dump the source properties too")
    a = p.parse_args()

    ds = registry.load(a.city)
    dates = _dates(ds)
    # "Active" means alive in the latest NON-skipped snapshot. A skipped pull
    # (same content as the day before) records a snapshot row but no address
    # rows, so keying on max(dates) made every address look retired whenever
    # the newest pulls were duplicates (toronto, 2026-09-08).
    live = diff.nonskipped(ds)
    last_id = live[-1]["id"] if live else 0

    if a.near:
        conn = db.init_db(ds)
        anchor = conn.execute(
            "SELECT full, street, latitude, longitude FROM addresses WHERE full = ? "
            "AND min_snapshot_id <= ? AND max_snapshot_id >= ? LIMIT 1",
            (a.near, last_id, last_id)).fetchone()
        if not anchor:
            conn.close()
            raise SystemExit(f"no active address {a.near!r} in {ds.slug}")
        sys.stdout.reconfigure(encoding="utf-8")
        print(f"{anchor['full']}  ({anchor['latitude']}, {anchor['longitude']})\n")
        for d, full in near(ds, conn, anchor["latitude"], anchor["longitude"], last_id,
                            street=anchor["street"]):
            print(f"  {d:>5} m  {full}")
        conn.close()
        return

    if a.addr:
        rows = rows_for(ds, "full LIKE ?", (f"%{a.addr}%",))
    elif a.street:
        rows = rows_for(ds, "street = ?", (a.street,))
    elif a.place:
        rows = rows_for(ds, "props LIKE ?", (f'%"PLACE_NAME": "%{a.place}%',))
    else:
        p.error("one of --addr / --street / --place / --near is required")

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
