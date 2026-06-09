"""CLI entry point for the Ontario address change tracker."""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from src import registry


def _resolve(args):
    """Return the list of datasets a command should act on."""
    if getattr(args, "all", False):
        return registry.load_all()
    if getattr(args, "city", None):
        return [registry.load(args.city)]
    sys.exit("Specify --city SLUG or --all")


def cmd_list(args):
    datasets = registry.load_all()
    print(f"{len(datasets)} dataset(s):\n")
    print(f"  {'slug':<12} {'provider':<24} {'access':<8} {'format':<10} licence")
    print(f"  {'-'*12} {'-'*24} {'-'*8} {'-'*10} {'-'*30}")
    for ds in datasets:
        print(f"  {ds.slug:<12} {ds.provider:<24} {ds.access:<8} "
              f"{ds.format:<10} {ds.license_name}")


def cmd_download(args):
    from src import fetch
    for ds in _resolve(args):
        print(f"\n=== {ds.slug} ===")
        try:
            filepath, features = fetch.fetch(ds, force=args.force)
            print(f"  fetched {len(features):,} features -> {filepath}")
        except Exception as e:
            print(f"  ERROR: {e}")


def cmd_import(args):
    from src import db, fetch
    for ds in _resolve(args):
        print(f"\n=== {ds.slug} ===")
        filepath, features = fetch.fetch(ds, force=args.force)
        db.import_snapshot(ds, filepath, features)


def cmd_diff(args):
    from src import db, diff
    for ds in _resolve(args):
        print(f"\n=== {ds.slug} ===")
        diff.report_latest(ds)


def cmd_report(args):
    from src import report
    report.generate_all(_resolve(args))


def cmd_update(args):
    """Fetch -> import -> diff -> report, with per-city failure isolation."""
    from src import db, diff, fetch, report
    datasets = _resolve(args)
    done = []
    for ds in datasets:
        print(f"\n=== {ds.slug} ===")
        try:
            filepath, features = fetch.fetch(ds, force=args.force)
            db.import_snapshot(ds, filepath, features)
            diff.report_latest(ds)
            done.append(ds)
        except Exception as e:
            print(f"  ERROR ({ds.slug}): {e}")
    if done:
        report.generate_all(done)


def main():
    p = argparse.ArgumentParser(description="Ontario address change tracker")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_target(sp, with_force=True):
        g = sp.add_mutually_exclusive_group()
        g.add_argument("--city", help="dataset slug")
        g.add_argument("--all", action="store_true", help="all datasets")
        if with_force:
            sp.add_argument("--force", action="store_true",
                            help="re-fetch even if unchanged")

    sub.add_parser("list").set_defaults(func=cmd_list)
    add_target(sub.add_parser("download")); sub.choices["download"].set_defaults(func=cmd_download)
    add_target(sub.add_parser("import")); sub.choices["import"].set_defaults(func=cmd_import)
    add_target(sub.add_parser("diff", )); sub.choices["diff"].set_defaults(func=cmd_diff)
    add_target(sub.add_parser("report"), with_force=False); sub.choices["report"].set_defaults(func=cmd_report)
    add_target(sub.add_parser("update")); sub.choices["update"].set_defaults(func=cmd_update)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
