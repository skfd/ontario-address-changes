"""Field-level diff of one CSD between two NAR vintages, printed as a
proto-narrative. Usage: python sample_diff.py <csd-name> <vintage-a> <vintage-b>
e.g. python sample_diff.py Orillia 202507 202606
"""

import csv
import sys
from collections import Counter
from pathlib import Path

from coverage import norm

DATA = Path(__file__).parent / "data"

FIELDS = [
    "CIVIC_NO", "CIVIC_NO_SUFFIX", "OFFICIAL_STREET_NAME",
    "OFFICIAL_STREET_TYPE", "OFFICIAL_STREET_DIR", "APT_NO_LABEL",
    "MAIL_POSTAL_CODE", "BU_USE", "BG_X", "BG_Y",
]


def fmt(row: dict) -> str:
    parts = [row.get("CIVIC_NO", ""), row.get("CIVIC_NO_SUFFIX", ""),
             row.get("OFFICIAL_STREET_NAME", ""), row.get("OFFICIAL_STREET_TYPE", ""),
             row.get("OFFICIAL_STREET_DIR", "")]
    s = " ".join(p for p in parts if p)
    unit = row.get("APT_NO_LABEL", "")
    return f"{s} unit {unit}" if unit else s


def load_csd(vintage: str, csd: str) -> dict:
    out = {}
    target = norm(csd)
    for path in sorted((DATA / vintage).glob("Address_35_part_*.csv")):
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
            for row in csv.DictReader(fh):
                if norm(row.get("CSD_ENG_NAME", "")) == target:
                    out[row["ADDR_GUID"]] = row
    return out


def main() -> None:
    csd, va, vb = sys.argv[1], sys.argv[2], sys.argv[3]
    a, b = load_csd(va, csd), load_csd(vb, csd)
    print(f"{csd}: {len(a):,} addresses in {va}, {len(b):,} in {vb}")
    added = b.keys() - a.keys()
    removed = a.keys() - b.keys()
    common = a.keys() & b.keys()

    print(f"\n-- ADDED ({len(added)}) --")
    for g in sorted(added, key=lambda g: fmt(b[g]))[:40]:
        print("  +", fmt(b[g]), f"[use={b[g].get('BU_USE','')}]")
    print(f"\n-- REMOVED ({len(removed)}) --")
    for g in sorted(removed, key=lambda g: fmt(a[g]))[:40]:
        print("  -", fmt(a[g]), f"[use={a[g].get('BU_USE','')}]")

    changed = []
    field_counter = Counter()
    for g in common:
        diffs = [(f, a[g].get(f, ""), b[g].get(f, "")) for f in FIELDS
                 if a[g].get(f, "") != b[g].get(f, "")]
        # coordinate noise: ignore tiny XY drift (< ~1e-4 deg)
        real = [d for d in diffs if d[0] not in ("BG_X", "BG_Y")
                or _big_move(d[1], d[2])]
        if real:
            changed.append((g, real))
            field_counter.update(f for f, _, _ in real)

    print(f"\n-- MODIFIED ({len(changed)}), by field: {dict(field_counter)} --")
    for g, diffs in changed[:40]:
        print("  ~", fmt(a[g]))
        for f, x, y in diffs:
            print(f"      {f}: {x!r} -> {y!r}")


def _big_move(x: str, y: str) -> bool:
    try:
        return abs(float(x) - float(y)) > 1e-4
    except ValueError:
        return True


if __name__ == "__main__":
    sys.exit(main())
