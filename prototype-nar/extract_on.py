"""Extract only the Ontario CSVs from each NAR vintage zip.

Standalone prototype tooling: reads prototype-nar/data/*.zip, writes
prototype-nar/data/<vintage>/. Never touches the prod store or vault.
"""

import re
import sys
import zipfile
from pathlib import Path

DATA = Path(__file__).parent / "data"

ON_PAT = re.compile(r"(^|[_/])(ON|ONT|Ontario|35)([_.]|$)", re.IGNORECASE)


def main() -> None:
    for zpath in sorted(DATA.glob("*.zip")):
        vintage = zpath.stem
        outdir = DATA / vintage
        outdir.mkdir(exist_ok=True)
        with zipfile.ZipFile(zpath) as zf:
            names = zf.namelist()
            print(f"\n== {zpath.name}: {len(names)} entries ==")
            for n in names:
                print("  ", n, zf.getinfo(n).file_size)
            picks = [n for n in names if ON_PAT.search(Path(n).name)]
            print(f"-- Ontario picks: {picks}")
            for n in picks:
                target = outdir / Path(n).name
                if target.exists() and target.stat().st_size == zf.getinfo(n).file_size:
                    print(f"   already extracted: {target.name}")
                    continue
                with zf.open(n) as src, open(target, "wb") as dst:
                    while chunk := src.read(1 << 20):
                        dst.write(chunk)
                print(f"   extracted -> {target}")


if __name__ == "__main__":
    sys.exit(main())
