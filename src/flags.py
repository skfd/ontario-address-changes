"""Event-level flags: algorithmic suspicion, a reviewable ledger, render holds.

The public site publishes on positive identification. A change event that looks
like one upstream sweep rather than city activity — a mass add, a mass removal,
or many rows changing the same field the same way — is *held* off the public
pages until a review files a verdict in flags.toml. Business verdicts publish
(retroactively, since pages are derived from the store); technical and bug
verdicts hold permanently. An open flag holds too: absence of review is not a
clean bill of health.

The discriminator is homogeneity. Real city activity is heterogeneous — a
subdivision here, a renumbering there, mixed streets and mixed fields. Upstream
sweeps are uniform: one field recoded across thousands of rows, a replayed
batch, a bulk re-geocode. Every fabricated story this project has published
(Brant's replayed batch, Renfrew's address restyle, the projected-coords days)
was homogeneous; no genuine one was.

Detection runs inside report generation, so a full re-render retroactively
flags historical days too. The ledger is append-only from this side: reviews
edit flags.toml by hand (or via the review-flags skill), the pipeline never
rewrites an existing entry.
"""

import json
import os
import tomllib
from collections import Counter
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
LEDGER_PATH = os.path.join(ROOT_DIR, "flags.toml")

# A sweep must be big in absolute terms AND big for this city (or dominate the
# day's modifications) to flag. Calibrated against the record: the largest real
# day-over-day add on file is well under 1% of a city, while Brant's replayed
# batch was +5.2%; ordinary field churn stays far below 50 same-shaped rows.
FLAG_MIN_ROWS = 50
FLAG_MIN_CITY_SHARE = 0.01     # of the previous snapshot's row count
FLAG_MIN_SECTION_SHARE = 0.25  # of the day's modified rows (mass-modified only)

VERDICTS = ("business", "technical", "bug")

_HEADER = """\
# Flag ledger: change events held off the public site pending review.
#
# The pipeline appends entries with status = "open" (see src/flags.py for the
# signatures). A review closes one by editing it in place:
#
#   status  = "reviewed"
#   verdict = "business"   the city really changed -> the event publishes
#           | "technical"  the feed changed, the city didn't -> held forever;
#                          `rule` must name the config change that prevents
#                          the same flag recurring (ignore_fields, [classes])
#           | "bug"        the data is wrong -> held forever; `rule` names the
#                          vault verdict / store repair that resolved it
#   reviewed = "YYYY-MM-DD"
#   rule     = what was changed so this never needs review again ("" for
#              business verdicts - a one-off publish needs no rule)
#   note     = one line of evidence for the verdict
#
# An OPEN flag holds its event off the public pages. Holds apply at render
# time, so re-running `python run.py report` after a review is what makes a
# verdict take effect. Never delete entries: reviewed history is the
# calibration record for the signatures.

"""


# ---- signatures ----

def _fieldset(m):
    """Canonical changed-field-set of a modified row. latitude/longitude (and
    the combined pseudo-field) collapse to 'location' so detection and holds
    agree whether they run before or after report._combine_location."""
    return tuple(sorted(
        {"location" if c["field"] in ("latitude", "longitude", "location")
         else c["field"] for c in m["changes"]}))


def _class_exempt(fs, classes):
    """Configured change classes (status, boundary, place_name) are deliberate
    per-city publish decisions; a sweep confined to one class's fields is not
    suspicious by definition."""
    fset = {f.lower() for f in fs}
    return any(fset <= {s.lower() for s in srcs} for srcs in (classes or {}).values())


def _restyle_share(pairs):
    """Share of old->new transitions that only restyle the value: same string
    up to case, whitespace and token order (renfrew's '17883 Highway 60' ->
    '17883 60 Highway'). High share = formatting, not information."""
    if not pairs:
        return 0.0
    def norm(v):
        return tuple(sorted(str(v or "").lower().split()))
    return sum(1 for old, new in pairs if norm(old) == norm(new)) / len(pairs)


def _transition_detail(rows, fs):
    """One line of evidence for a mass-modified flag: the top old->new
    transitions when the sweep is single-field, plus a restyle share."""
    if len(fs) != 1 or fs[0] == "location":
        return ""
    field = fs[0]
    pairs = [(c["old"], c["new"]) for m in rows for c in m["changes"]
             if (c["field"] if c["field"] not in ("latitude", "longitude") else "location") == field]
    top = Counter(pairs).most_common(3)
    parts = [f"{old!r} -> {new!r} ({n:,})" for (old, new), n in top]
    restyle = _restyle_share(pairs)
    tail = f"; {restyle:.0%} value-preserving restyle" if restyle >= 0.5 else ""
    return "top: " + ", ".join(parts) + tail


def detect(ds, d, city_size):
    """Signatures over one day's diff (compute_diff output, pre-render).

    `city_size` is the previous snapshot's row count — the denominator for
    "big for this city". Returns flag dicts without slug/date/detected; the
    caller stamps those. Baseline diffs must not be passed here.
    """
    out = []

    def city_mass(n):
        return n >= FLAG_MIN_ROWS and city_size and n >= city_size * FLAG_MIN_CITY_SHARE

    if city_mass(len(d["added"])):
        n = len(d["added"])
        out.append({"signature": "mass-added",
                    "scope": f"{n:,} added in one day ({n / city_size:.1%} of {city_size:,})",
                    "detail": ""})
    if city_mass(len(d["removed"])):
        n = len(d["removed"])
        out.append({"signature": "mass-removed",
                    "scope": f"{n:,} removed in one day ({n / city_size:.1%} of {city_size:,})",
                    "detail": ""})

    groups = {}
    for m in d["modified"]:
        groups.setdefault(_fieldset(m), []).append(m)
    n_mod = len(d["modified"])
    for fs, rows in sorted(groups.items()):
        n = len(rows)
        if n < FLAG_MIN_ROWS:
            continue
        if not (n >= n_mod * FLAG_MIN_SECTION_SHARE or
                (city_size and n >= city_size * FLAG_MIN_CITY_SHARE)):
            continue
        if _class_exempt(fs, ds.classes):
            continue
        out.append({"signature": "mass-modified", "fields": list(fs),
                    "scope": f"{n:,} rows changed the same field set "
                             f"[{', '.join(fs)}] ({n / n_mod:.0%} of the day's "
                             f"{n_mod:,} modifications)",
                    "detail": _transition_detail(rows, fs)})
    return out


# ---- ledger ----

def flag_key(fl):
    return (fl["slug"], fl["date"], fl["signature"],
            ",".join(fl.get("fields", [])))


def load_ledger(path=LEDGER_PATH):
    if not os.path.exists(path):
        return []
    with open(path, "rb") as f:
        return tomllib.load(f).get("flag", [])


def _toml_str(v):
    # json string escapes are a subset of TOML basic-string escapes
    return json.dumps(str(v), ensure_ascii=False)


def _entry_toml(fl):
    lines = ["[[flag]]",
             f"slug = {_toml_str(fl['slug'])}",
             f"date = {_toml_str(fl['date'])}",
             f"signature = {_toml_str(fl['signature'])}"]
    if fl.get("fields"):
        lines.append("fields = [" + ", ".join(_toml_str(f) for f in fl["fields"]) + "]")
    lines += [f"scope = {_toml_str(fl['scope'])}"]
    if fl.get("detail"):
        lines.append(f"detail = {_toml_str(fl['detail'])}")
    lines += [f"detected = {_toml_str(fl['detected'])}",
              'status = "open"', ""]
    return "\n".join(lines) + "\n"


def record(new_flags, path=LEDGER_PATH):
    """Append flags whose key is not already in the ledger. Returns the ones
    actually appended, so callers can log exactly what is new."""
    existing = {flag_key(f) for f in load_ledger(path)}
    fresh, seen = [], set()
    for fl in new_flags:
        k = flag_key(fl)
        if k not in existing and k not in seen:
            fresh.append(fl)
            seen.add(k)
    if not fresh:
        return []
    write_header = not os.path.exists(path)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        if write_header:
            f.write(_HEADER)
        for fl in fresh:
            f.write(_entry_toml(fl))
    return fresh


def stamp(flags_out, slug, date):
    """Fill in the identity fields detect() leaves to the caller."""
    today = datetime.now().strftime("%Y-%m-%d")
    for fl in flags_out:
        fl["slug"] = slug
        fl["date"] = date
        fl["detected"] = today
    return flags_out


# ---- holds ----

def is_held(fl):
    """Open flags hold (unreviewed is not innocent); technical and bug
    verdicts hold forever; business verdicts release the event."""
    if fl.get("status", "open") != "reviewed":
        return True
    return fl.get("verdict") in ("technical", "bug")


def holds_for(ledger, slug, date):
    return [f for f in ledger
            if f.get("slug") == slug and f.get("date") == date and is_held(f)]


def apply_holds(d, held):
    """Filtered copy of a diff with each held flag's rows removed, plus
    (signature, text) operator notes saying what was held (console/log only,
    never the site)."""
    if not held:
        return d, []
    d = {"added": d["added"], "removed": d["removed"], "modified": d["modified"]}
    notes = []
    for fl in held:
        sig = fl["signature"]
        why = "open" if fl.get("status", "open") != "reviewed" else fl.get("verdict", "")
        if sig == "mass-added" and d["added"]:
            notes.append((sig, f"held {len(d['added']):,} added ({why} {sig} flag)"))
            d["added"] = []
        elif sig == "mass-removed" and d["removed"]:
            notes.append((sig, f"held {len(d['removed']):,} removed ({why} {sig} flag)"))
            d["removed"] = []
        elif sig == "mass-modified":
            fs = tuple(sorted(fl.get("fields", [])))
            keep = [m for m in d["modified"] if _fieldset(m) != fs]
            n = len(d["modified"]) - len(keep)
            if n:
                notes.append((sig, f"held {n:,} modified [{', '.join(fs)}] "
                                   f"({why} {sig} flag)"))
                d["modified"] = keep
    return d, notes
