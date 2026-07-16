"""CLI entry point for the Ontario address change tracker."""

import argparse
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from src import registry


def _record_timing(slug, seconds):
    """Append one successful per-city wall-clock sample; progress.ps1 medians
    these to estimate ETA for the cities still pending in a run."""
    path = os.path.join(os.path.dirname(__file__), "logs", "timings.csv")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    header = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if header:
            f.write("slug,finished_iso,seconds\n")
        f.write(f"{slug},{datetime.now().isoformat(timespec='seconds')},{seconds:.1f}\n")


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


def _update_serial(datasets, args):
    from src import db, diff, fetch
    done = []
    failed = []
    for ds in datasets:
        print(f"\n=== {ds.slug} ===")
        try:
            filepath = fetch.fetch_path(ds, force=args.force)
            # Filename check before the (expensive) full parse: a rerun of an
            # already-imported snapshot skips json.load entirely.
            if db.already_imported(ds, filepath):
                print(f"  already imported: {os.path.basename(filepath)}")
            else:
                db.import_snapshot(ds, filepath, fetch.load_features(filepath))
            diff.report_latest(ds)
            done.append(ds)
        except Exception as e:
            print(f"  ERROR ({ds.slug}): {e}")
            failed.append(ds.slug)
    return done, failed


def _update_parallel(datasets, args):
    """Run each city as a worker subprocess (update --city X --no-report),
    printing each city's output as a block when it finishes."""
    import subprocess
    from concurrent.futures import ThreadPoolExecutor, as_completed

    # Largest DBs first so the slow cities (ottawa, brampton) start immediately.
    def db_size(ds):
        return os.path.getsize(ds.db_path) if os.path.exists(ds.db_path) else 0

    queue = sorted(datasets, key=db_size, reverse=True)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}

    def worker(ds):
        cmd = [sys.executable, os.path.abspath(__file__),
               "update", "--city", ds.slug, "--no-report"]
        if args.force:
            cmd.append("--force")
        t0 = time.perf_counter()
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", env=env)
        return ds, proc, time.perf_counter() - t0

    done = []
    failed = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for future in as_completed([pool.submit(worker, ds) for ds in queue]):
            ds, proc, secs = future.result()
            print(proc.stdout, end="")
            if proc.returncode == 0:
                _record_timing(ds.slug, secs)
                done.append(ds)
            else:
                if proc.stderr:
                    print(proc.stderr, end="")
                failed.append(ds.slug)
    done.sort(key=lambda ds: ds.slug)
    failed.sort()
    return done, failed


def cmd_update(args):
    """Fetch -> import -> diff -> report, with per-city failure isolation."""
    datasets = _resolve(args)
    if args.jobs > 1 and len(datasets) > 1:
        done, failed = _update_parallel(datasets, args)
    else:
        done, failed = _update_serial(datasets, args)
    if done and not args.no_report:
        from src import report
        report.generate_all(done)
    if failed:
        sys.exit(f"update failed for: {', '.join(failed)}")


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
    sub.choices["update"].add_argument("--jobs", type=int, default=1,
                                       help="parallel city workers (subprocesses)")
    sub.choices["update"].add_argument("--no-report", action="store_true",
                                       help="skip site generation after updating")

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
