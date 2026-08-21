"""Assess NAR vintages for change-tracking viability. Read-only over
prototype-nar/data/<vintage>/, writes assessment.json next to this file.

Questions answered:
  1. schema per vintage (column drift between releases)
  2. ADDR_GUID uniqueness + stability across consecutive vintages (go/no-go)
  3. per-CSD counts, split covered / not-covered by the 53 prod datasets
  4. size of the field-level modification set between vintages
"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

from coverage import COVERED_NORM, norm

DATA = Path(__file__).parent / "data"

# fields that would drive a humanized change narrative
NARRATIVE_FIELDS = [
    "CIVIC_NO", "CIVIC_NO_SUFFIX", "OFFICIAL_STREET_NAME",
    "OFFICIAL_STREET_TYPE", "OFFICIAL_STREET_DIR", "APT_NO_LABEL",
    "MAIL_POSTAL_CODE", "BU_USE", "CSD_ENG_NAME",
]


def find_addr_csv(vintage_dir: Path) -> list[Path]:
    picks = [p for p in vintage_dir.glob("*.csv") if "ADDR" in p.name.upper()]
    return picks or sorted(vintage_dir.glob("*.csv"))


def load_vintage(vintage_dir: Path):
    """Return (columns, {addr_guid: (csd, narrative_hash)})."""
    records = {}
    columns = None
    dupes = 0
    for path in find_addr_csv(vintage_dir):
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
            reader = csv.DictReader(fh)
            if columns is None:
                columns = reader.fieldnames
            fields = [f for f in NARRATIVE_FIELDS if f in reader.fieldnames]
            csd_col = next((c for c in reader.fieldnames if "CSD" in c and "ENG" in c and "NAME" in c), None)
            guid_col = next((c for c in reader.fieldnames if "ADDR" in c.upper() and "GUID" in c.upper()), None)
            if guid_col is None:
                print(f"!! no ADDR_GUID-like column in {path.name}: {reader.fieldnames}")
                continue
            for row in reader:
                guid = row[guid_col]
                key = guid.encode()
                if key in records:
                    dupes += 1
                csd = row.get(csd_col, "") if csd_col else ""
                sig = hash(tuple(row.get(f, "") for f in fields))
                records[key] = (csd, sig)
    return columns, records, dupes


def main() -> None:
    vintages = sorted(d for d in DATA.iterdir() if d.is_dir())
    report = {"vintages": {}, "pairs": {}}
    loaded = {}
    for vd in vintages:
        cols, recs, dupes = load_vintage(vd)
        loaded[vd.name] = recs
        csd_counts = Counter(csd for csd, _ in recs.values())
        covered = sum(n for csd, n in csd_counts.items() if norm(csd) in COVERED_NORM)
        report["vintages"][vd.name] = {
            "columns": cols,
            "rows": len(recs),
            "duplicate_guids": dupes,
            "distinct_csds": len(csd_counts),
            "covered_addr": covered,
            "uncovered_addr": len(recs) - covered,
            "top_uncovered_csds": [
                [csd, n] for csd, n in csd_counts.most_common()
                if norm(csd) not in COVERED_NORM
            ][:40],
        }
        print(f"{vd.name}: {len(recs):,} rows, {dupes} dupe GUIDs, "
              f"{len(csd_counts)} CSDs, covered {covered:,} / uncovered {len(recs)-covered:,}")

    names = sorted(loaded)
    for a, b in zip(names, names[1:]):
        ra, rb = loaded[a], loaded[b]
        common = ra.keys() & rb.keys()
        modified = sum(1 for k in common if ra[k][1] != rb[k][1])
        moved_csd = sum(1 for k in common if ra[k][0] != rb[k][0])
        pair = {
            "a_rows": len(ra), "b_rows": len(rb),
            "common": len(common),
            "overlap_pct_of_a": round(100 * len(common) / len(ra), 2),
            "overlap_pct_of_b": round(100 * len(common) / len(rb), 2),
            "added": len(rb.keys() - ra.keys()),
            "removed": len(ra.keys() - rb.keys()),
            "modified_narrative_fields": modified,
            "csd_changed": moved_csd,
        }
        report["pairs"][f"{a}->{b}"] = pair
        print(f"{a}->{b}: {pair}")

    out = Path(__file__).parent / "assessment.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    sys.exit(main())
