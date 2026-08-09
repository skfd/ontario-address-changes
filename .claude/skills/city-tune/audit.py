"""Audit one city's DB for every datasets/<slug>.toml decision, from its full history.

    python .claude/skills/city-tune/audit.py <slug> [--tags] [--identity] [--coords]
                                                    [--fields] [--classes]

With no flags, runs everything. Sections:

  tags      Every prop key ever stored, with the snapshot range it covers (catches a
            field the source dropped, added, or carried intermittently), plus a churn
            tally: rows each field touched vs rows where it was the ONLY change.
  identity  Whether key_field / the synthesized key is actually stable and unique.
  coords    Duplicate coordinate columns measured against the tracked geometry: a
            faithful echo that only moves on jitter, or a stale copy about to re-sync.
  fields    Coverage of the mapped canonical fields, and candidates for unmapped ones.
  classes   Low-cardinality props that could drive a [classes] entry.

Read-only. `--tags` runs one compute_diff per consecutive snapshot pair, which
dominates runtime (seconds for a mid-size city, minutes for toronto); the other
sections are single passes over the latest snapshot.
"""

import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from itertools import groupby

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

from src import db, diff, normalize, registry

VALUE_CAP = 30          # distinct values kept per prop before calling it high-cardinality
CLASS_MAX = 25          # at most this many distinct values to suggest as a class

# Deviation above which a coordinate duplicate is a stale copy rather than a faithful
# echo. 11 m is 1e-4 deg: an order above the ~0.8 m floor that comparing against a 5 dp
# geometry imposes, and an order below the drift seen on real stale copies (renfrew
# 530 m, quinte-west >10 m on 8% of rows).
STALE_M = 11.0
CRS_FIT_M = 5.0         # median residual under which a guessed CRS counts as identified
CRS_SAMPLE = 500        # rows sampled to identify a projected pair's CRS
COORD_SNAPS = 5         # snapshots sampled across history per coordinate pair

# Projected CRSs an Ontario layer publishes its own coordinate columns in. Tried in
# order against a sample; whichever fits is reported, so a wrong guess cannot pass.
CRS_GUESSES = ["EPSG:26915", "EPSG:26916", "EPSG:26917", "EPSG:26918",   # NAD83 UTM 15-18N
               "EPSG:32615", "EPSG:32616", "EPSG:32617", "EPSG:32618",   # WGS84 UTM 15-18N
               "EPSG:2951", "EPSG:2952", "EPSG:2953",                    # NAD83(CSRS) MTM 8-10
               "EPSG:3161"]                                              # Ontario MNR Lambert


# ---- helpers ----

def _ordinals(snaps):
    """{snapshot_id: position} over non-skipped snapshots.

    Skipped snapshots never appear in addresses (import_snapshot leaves the table
    alone), so a row that persists across one keeps a single unbroken range. Gaps
    must therefore be measured in this ordinal space, not in raw snapshot ids.
    """
    return {s["id"]: i for i, s in enumerate(snaps)}


def _merge(intervals, pos):
    """Merge (min_id, max_id) pairs into contiguous ordinal spans."""
    spans = []
    for lo, hi in sorted((pos[a], pos[b]) for a, b in intervals):
        if spans and lo <= spans[-1][1] + 1:
            spans[-1][1] = max(spans[-1][1], hi)
        else:
            spans.append([lo, hi])
    return spans


_VALUE_CACHE = {}


def _prop_values(ds, sid):
    """One pass over the latest snapshot: {key: (fill_count, values|None)}.

    `values` is None once a key passes VALUE_CAP distinct values (high cardinality).
    Cached: the fields and classes sections both want it.
    """
    if (ds.slug, sid) in _VALUE_CACHE:
        return _VALUE_CACHE[ds.slug, sid]
    conn = db.init_db(ds)
    rows = conn.execute(
        "SELECT je.key AS k, je.value AS v FROM addresses, json_each(addresses.props) AS je "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid))
    fill, vals = Counter(), {}
    for k, v in rows:
        fill[k] += 1
        seen = vals.get(k, set())
        if seen is not None and len(seen) <= VALUE_CAP:
            seen.add(str(v))
            vals[k] = None if len(seen) > VALUE_CAP else seen
    conn.close()
    _VALUE_CACHE[ds.slug, sid] = {k: (fill[k], vals.get(k)) for k in fill}
    return _VALUE_CACHE[ds.slug, sid]


# ---- sections ----

def tags(ds, snaps):
    pos = _ordinals(snaps)
    date = [diff.snap_date(s) for s in snaps]
    conn = db.init_db(ds)
    ivals, count = defaultdict(list), Counter()
    for mn, mx, props in conn.execute(
            "SELECT min_snapshot_id, max_snapshot_id, props FROM addresses"):
        for k in json.loads(props):
            count[k] += 1
            ivals[k].append((mn, mx))
    conn.close()

    print(f"=== tags: {len(count)} keys ever stored ===")
    print("A key already in ignore_fields is absent from every snapshot imported after")
    print("that config landed, and is filtered out of the churn tally below.\n")
    last = len(snaps) - 1
    for k, n in sorted(count.items(), key=lambda kv: -kv[1]):
        spans = _merge(ivals[k], pos)
        text = ", ".join(date[a] if a == b else f"{date[a]}..{date[b]}" for a, b in spans)
        note = ""
        if spans[-1][1] < last:
            note += "  <- GONE from the source"
        if spans[0][0] > 0:
            note += "  <- appeared mid-history"
        if len(spans) > 1:
            note += "  <- intermittent"
        print(f"  {k:26} rows={n:8}  {text}{note}")

    ids = [s["id"] for s in snaps]
    date_of = {s["id"]: diff.snap_date(s) for s in snaps}
    touched, solo, combo = Counter(), Counter(), Counter()
    per_day = defaultdict(Counter)
    print("\n=== per-diff summary ===")
    for a, b in zip(ids, ids[1:]):
        d = diff.compute_diff(ds, a, b)
        for m in d["modified"]:
            fs = tuple(sorted(c["field"] for c in m["changes"]))
            combo[fs] += 1
            for f in fs:
                touched[f] += 1
                per_day[date_of[b]][f] += 1
            if len(fs) == 1:
                solo[fs[0]] += 1
        print(f"  {date_of[a]} -> {date_of[b]}: "
              f"+{len(d['added'])} -{len(d['removed'])} ~{len(d['modified'])}", flush=True)

    print("\n=== churn (rows touched / rows where it was the only change) ===")
    for f, n in touched.most_common():
        print(f"  {f:26} touched={n:8}  solo={solo.get(f, 0)}")
    print("\n=== top change combos (co-movement reveals derived echoes) ===")
    for fs, n in combo.most_common(25):
        print(f"  {n:8}  {', '.join(fs)}")
    print("\n=== per-day field tallies ===")
    for d in sorted(per_day):
        print(f"  {d} {dict(per_day[d].most_common(12))}")
    return solo


def identity(ds, snaps):
    pos = _ordinals(snaps)
    sid = snaps[-1]["id"]
    conn = db.init_db(ds)
    total, distinct, synth = conn.execute(
        "SELECT COUNT(*), COUNT(DISTINCT identity_key), "
        "SUM(identity_key LIKE 'syn:%') FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchone()

    # Stream every key's ranges in PK order to find keys that vanished and came back:
    # a flapping key reports as retired-then-new instead of modified.
    rows = conn.execute("SELECT identity_key, min_snapshot_id, max_snapshot_id FROM addresses "
                        "ORDER BY identity_key, min_snapshot_id")
    flapped = versions = keys = 0
    for _, grp in groupby(rows, key=lambda r: r[0]):
        ivals = [(a, b) for _, a, b in grp]
        keys += 1
        versions += len(ivals)
        if len(_merge(ivals, pos)) > 1:
            flapped += 1
    conn.close()

    print("\n=== identity ===")
    print(f"  key_field    = {ds.key_field or '(synthesized)'}")
    print(f"  synth_fields = {ds.synth_fields}  synth_props = {ds.synth_props}  "
          f"use_geometry = {ds.use_geometry}")
    print(f"  latest snapshot: {total:,} rows, {distinct:,} distinct keys "
          f"({total - distinct:,} collisions), {synth or 0:,} synthesized")
    print(f"  whole history:   {keys:,} keys, {versions:,} versions "
          f"({versions / keys:.2f} per key)")
    print(f"  flapped (absent then present again): {flapped:,} "
          f"({flapped / keys:.2%} of keys)")
    print("  A high flap rate or a versions-per-key far above the number of real edits")
    print("  means the key is not stable - see references/identity.md.")


_AXIS = {"lat": "y", "latitude": "y", "y": "y", "north": "y", "northing": "y",
         "lon": "x", "long": "x", "longitude": "x", "x": "x", "east": "x", "easting": "x"}
_AXIS_NOISE = ("coordinates", "coordinate", "coord", "crd", "utm", "mtm", "wgs", "nad",
               "geo", "dd", "deg")
_AXIS_WORDS = sorted(_AXIS, key=len, reverse=True)   # longest first: 'long' before 'lon'
_GEO_WORDS = {"lat", "latitude", "lon", "long", "longitude"}
_PROJ_WORDS = {"east", "easting", "north", "northing"}


def _words(key):
    """The axis words a prop name is built from, or None if it is not one.

    The name has to be covered ENTIRELY by axis words: accepting a partial match would
    read CITY, PARITY and COUNTRY as northings.
    """
    t = re.sub(r"[^a-z]", "", key.lower())
    for noise in _AXIS_NOISE:
        t = t.replace(noise, "")
    out = []
    while t:
        for w in _AXIS_WORDS:
            if t.startswith(w):
                out.append(w)
                t = t[len(w):]
                break
        else:
            return None
    return out or None


def _axis(key):
    """'x', 'y' or None - which coordinate axis a prop name denotes.

    Handles the spellings actually published: LAT/LONG, Latitude/Longitude, UTM_X/UTM_Y,
    X_COORD/Y_COORD, Xcoord/Ycoord, and the doubled forms dufferin (LATITUDEY,
    LONGITUDEX, EASTINGX, NORTHINGY) and kawartha-lakes (Xlong, Ylat) publish.
    """
    words = _words(key)
    axes = {_AXIS[w] for w in words} if words else set()
    return axes.pop() if len(axes) == 1 else None


def _family(key):
    """'geo', 'proj' or 'bare' - which kind of coordinate the name claims to be.

    Pairing needs this: dufferin publishes EASTINGX, NORTHINGY, LONGITUDEX and LATITUDEY
    together, and pairing the two x-names against the two y-names by position matches
    metres against degrees.
    """
    words = _words(key) or []
    if any(w in _GEO_WORDS for w in words):
        return "geo"
    if any(w in _PROJ_WORDS for w in words):
        return "proj"
    return "bare"


def _fmt_m(m):
    return "unmeasurable" if math.isinf(m) else f"{m:,.2f} m"


def _metres(lon_a, lat_a, lon_b, lat_b):
    """Equirectangular distance - exact enough at the metres we are measuring."""
    dy = (lat_a - lat_b) * 111_320.0
    dx = (lon_a - lon_b) * 111_320.0 * math.cos(math.radians(lat_a))
    return math.hypot(dx, dy)


def _fit_crs(ds, sample):
    """Identify the CRS a projected pair is published in, by fitting candidates.

    Returns (crs, median_residual_m) or (None, best_median). Never guesses blind: a
    candidate has to land within CRS_FIT_M to be reported at all.
    """
    best, best_med = None, float("inf")
    for crs in ([ds.source_crs] if ds.source_crs else []) + CRS_GUESSES:
        try:
            tr = normalize._transformer(crs)
            devs = sorted(_metres(*tr.transform(x, y), lon, lat)
                          for x, y, lon, lat in sample)
        except Exception:
            continue
        med = devs[len(devs) // 2]
        if med < best_med:
            best, best_med = crs, med
    return (best, best_med) if best_med <= CRS_FIT_M else (None, best_med)


def _pair_values(conn, xk, yk, sid):
    """[(x, y, lon, lat)] for one snapshot, dropping rows missing either side."""
    rows = conn.execute(
        f"SELECT json_extract(props, '$.\"{xk}\"'), json_extract(props, '$.\"{yk}\"'), "
        "longitude, latitude FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ? AND longitude IS NOT NULL",
        (sid, sid))
    out = []
    for x, y, lon, lat in rows:
        try:
            out.append((float(x), float(y), lon, lat))
        except (TypeError, ValueError):
            continue
    return out


def coords(ds, snaps):
    """Measure any duplicate coordinate pair in props against the tracked geometry.

    A *faithful* echo of the geometry (burlington, hastings, kitchener's projected pair)
    is finer than the 5 dp everything is compared at, so it only ever moves on jitter. A
    *stale* copy (renfrew, quinte-west) drifts free and fires on every row the day the
    publisher recomputes it. Only the deviation tells them apart, and it decides whether
    the field is worth ignoring pre-emptively - see references/ignore-fields.md.

    Pairs are found in the latest snapshot, so one already in ignore_fields - or one the
    source has since dropped - does not appear here.
    """
    # Pair within a family (geographic names together, projected names together, bare
    # x/y together) and only then by position, so a city publishing both kinds does not
    # get an easting matched against a latitude.
    keyed = defaultdict(list)
    for k in _prop_values(ds, snaps[-1]["id"]):
        if _axis(k):
            keyed[_family(k), _axis(k)].append(k)

    print(f"\n=== coordinate duplicates ({COORD_SNAPS} snapshots across history) ===")
    pairs = []
    for fam in ("geo", "proj", "bare"):
        xs, ys = sorted(keyed[fam, "x"]), sorted(keyed[fam, "y"])
        if xs and ys and len(xs) != len(ys):
            print(f"  uneven {fam} candidates, pairing by position: x={xs} y={ys}")
        pairs += list(zip(xs, ys))
    if not pairs:
        print("  none: no prop names an x/y or lon/lat axis.")
        return

    # Sampled across history, not just the latest: a stale copy is only off the geometry
    # between the publisher's re-syncs, so the newest snapshot alone reads clean the day
    # after one. Renfrew's had wandered 530 m on 2026-06-15 and was back within 2 m by
    # 06-29 - measuring only 06-29 would have called it faithful.
    last = len(snaps) - 1
    picked = sorted({round(i * last / (COORD_SNAPS - 1)) for i in range(COORD_SNAPS)})

    conn = db.init_db(ds)
    for xk, yk in pairs:
        print(f"\n  {xk} / {yk}")
        crs, kind, worst_p99, worst_over = None, None, 0.0, 0
        for i in picked:
            vals = _pair_values(conn, xk, yk, snaps[i]["id"])
            if not vals:
                print(f"    {diff.snap_date(snaps[i])}  not present")
                continue
            # Per row, not per column: elgin publishes 18,716 rows of degrees and 2,720
            # of UTM metres in the same `x`/`y` pair, so deciding once for the column
            # scores 13% of the city against the wrong units.
            geo = [v for v in vals if abs(v[0]) <= 180 and abs(v[1]) <= 90]
            proj = [v for v in vals if not (abs(v[0]) <= 180 and abs(v[1]) <= 90)]
            if kind is None:
                if proj:
                    crs, med = _fit_crs(ds, proj[:CRS_SAMPLE])
                    if not crs and len(proj) > len(geo):
                        print(f"    values outside lon/lat range and no candidate CRS "
                              f"fits (best median {med:,.0f} m).\n"
                              f"    Reproject by hand, or set source_crs.")
                        break
                    if not crs:
                        # A minority that fits nothing is junk rows, not another CRS -
                        # quinte-west has exactly one, a projected northing sitting in
                        # `lat`. Score them unmeasurable rather than abandoning the pair.
                        print(f"    {len(proj):,} rows are outside lon/lat range and fit "
                              f"no CRS: junk, counted\n    below as unmeasurable.")
                kind = (f"{len(geo):,} rows geographic + {len(proj):,} projected {crs}"
                        if geo and proj and crs else
                        "geographic" if geo else f"projected, {crs}")
                print(f"    {kind}, against the 5 dp geometry - which with any "
                      f"NAD83/WGS84\n    datum offset puts a ~1-2 m floor under "
                      f"every number below")
                if geo and proj and crs:
                    print("    ^ TWO CRSs in one column. Broken on its own terms, whatever")
                    print("      the drift below says.")

            tr = normalize._transformer(crs) if crs else None
            devs = sorted([_metres(x, y, lon, lat) for x, y, lon, lat in geo]
                          + ([_metres(*tr.transform(x, y), lon, lat)
                              for x, y, lon, lat in proj] if tr
                             else [math.inf] * len(proj)))
            n = len(devs)
            p99 = devs[int(n * 0.99)]
            over = sum(d > STALE_M for d in devs)
            worst_p99, worst_over = max(worst_p99, p99), max(worst_over, over)
            print(f"    {diff.snap_date(snaps[i])}  {n:8,} rows  "
                  f"median {_fmt_m(devs[n // 2]):>14}  p99 {_fmt_m(p99):>16}  "
                  f"max {_fmt_m(devs[-1]):>18}  over {STALE_M:.0f} m: {over:,}", flush=True)
        if kind is None:
            continue
        # The verdict rides on p99, not the max: what makes a re-sync a mass event is a
        # BULK of drifted rows. A handful of wild outliers is a few corrupt rows instead
        # (hastings carries 13 of 30,856, one holding a projected northing as a latitude)
        # and would make the max useless as a discriminator.
        if worst_p99 > STALE_M:
            print("    -> STALE copy: 1%+ of the layer has drifted off the geometry, and")
            print("       every drifted row fires the day the publisher re-syncs it.")
            print("       Ignore now - this is the urgent kind.")
        else:
            print("    -> FAITHFUL echo: tracks the geometry, finer than the 5 dp compare,")
            print("       so it moves only on jitter. Ignore, but it is not urgent.")
            if worst_over:
                print(f"       ({worst_over:,} individual rows still sit over {STALE_M:.0f} m "
                      f"- broken rows, not drift.\n"
                      f"       Worth a look, but they cannot produce a mass event.)")
    conn.close()
    print("\n  Whether that noise masks real moves or manufactures fake ones follows from")
    print("  [identity] above; the churn tally under --tags is what shows it has moved.")


def field_map(ds, snaps):
    sid = snaps[-1]["id"]
    conn = db.init_db(ds)
    total = conn.execute("SELECT COUNT(*) FROM addresses WHERE min_snapshot_id <= ? "
                         "AND max_snapshot_id >= ?", (sid, sid)).fetchone()[0]
    filled = conn.execute(
        "SELECT COUNT(number), COUNT(street), COUNT(unit), COUNT(full) FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ?", (sid, sid)).fetchone()
    conn.close()

    print("\n=== field map (latest snapshot) ===")
    unmapped = []
    for name, n in zip(("number", "street", "unit", "full"), filled):
        src = ds.fields.get(name)
        if src:
            print(f"  {name:7} <- {src:22} {n:8,} / {total:,} filled ({n / total:.0%})")
        else:
            unmapped.append(name)
            print(f"  {name:7} <- (unmapped)")
    if not unmapped:
        return
    print(f"\n  candidates for {', '.join(unmapped)} - every prop with its fill rate:")
    for k, (n, vals) in sorted(_prop_values(ds, sid).items(), key=lambda kv: -kv[1][0]):
        sample = "high cardinality" if vals is None else ", ".join(sorted(vals)[:3])
        print(f"    {k:26} {n:8,} ({n / total:.0%})  {sample[:60]}")


def classes(ds, snaps, solo=None):
    sid = snaps[-1]["id"]
    conn = db.init_db(ds)
    total = conn.execute("SELECT COUNT(*) FROM addresses WHERE min_snapshot_id <= ? "
                         "AND max_snapshot_id >= ?", (sid, sid)).fetchone()[0]
    conn.close()
    classed = {f: cls for cls, srcs in ds.classes.items() for f in srcs}

    print("\n=== class candidates (low-cardinality props) ===")
    print("  A [classes] entry only fires when the row's ENTIRE changed set fits it,")
    print("  so pair this with the churn tally: a field that never changes alone is")
    print("  an echo to ignore, not a class.\n")
    for k, (n, vals) in sorted(_prop_values(ds, sid).items(), key=lambda kv: -kv[1][0]):
        if vals is None or len(vals) > CLASS_MAX:
            continue
        mark = f"  [in classes.{classed[k]}]" if k in classed else ""
        churn = f"  solo changes={solo[k]}" if solo and k in solo else ""
        print(f"  {k:26} {len(vals):3} values, {n:,} rows ({n / total:.1%}){mark}{churn}")
        print(f"    {', '.join(sorted(vals)[:12])}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a[2:] for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 1 or flags - {"tags", "identity", "coords", "fields", "classes"}:
        sys.exit(__doc__)
    if not flags:
        flags = {"tags", "identity", "coords", "fields", "classes"}

    ds = registry.load(args[0])
    snaps = diff.nonskipped(ds)
    # tags and identity need a diff; the rest read one snapshot, so a baseline-only city
    # (elgin, peel-region, waterloo behind the frozen vault) can still be audited for them.
    if len(snaps) < 2 and flags & {"tags", "identity"}:
        sys.exit(f"{ds.slug}: only {len(snaps)} non-skipped snapshot(s) - "
                 f"--coords / --fields / --classes still work")
    if not snaps:
        sys.exit(f"{ds.slug}: no non-skipped snapshots")
    print(f"{ds.slug}: {len(snaps)} non-skipped snapshots, "
          f"{diff.snap_date(snaps[0])} .. {diff.snap_date(snaps[-1])}")
    print(f"ignore_fields = {ds.ignore_fields}")
    print(f"keep_fields   = {ds.keep_fields}")
    print(f"classes       = {ds.classes}\n")

    solo = tags(ds, snaps) if "tags" in flags else None
    if "identity" in flags:
        identity(ds, snaps)
    if "coords" in flags:
        coords(ds, snaps)
    if "fields" in flags:
        field_map(ds, snaps)
    if "classes" in flags:
        classes(ds, snaps, solo)


if __name__ == "__main__":
    main()
