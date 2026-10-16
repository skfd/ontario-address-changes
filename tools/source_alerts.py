"""Tell the operator when a source has stopped working, as GitHub issues.

    python tools/source_alerts.py status              # every city on a streak or frozen
    python tools/source_alerts.py down                # one line per known outage (commit message)
    python tools/source_alerts.py sync [--dry-run]    # open / close the alert issues

Two conditions, each one issue per city, opened once and closed by itself:

* ``source-down`` -- the city's pulls have failed ``run.KNOWN_OUTAGE_DAYS``
  pull days running (the same threshold at which the daily run stops failing
  on it, so the issue is what replaces the red run). Closed, with a comment, on
  the first day a pull succeeds.
* ``source-stale`` -- every pull for ``STALE_DAYS`` has been byte-identical.
  Not an error: the pull works, the publisher just stopped publishing, or the
  layer is a one-off export. That is how elgin's and middlesex's layers turned
  out to be replaced without anyone noticing. Closed when the content moves.

Before this, a source down for three weeks (west-parry-sound, 2026-09-24..
10-15) produced nothing but a red run on a run that was red every day anyway.

Writes go out under the flag bot's token when FLAG_BOT_GH_TOKEN is set, so
GitHub notifies the owner (see tools/flag_issues.py). Nothing is opened or
closed between midnight and 07:00 local, when nothing should ping anybody;
the next hourly pass picks it up.
"""

import argparse
import os
import sys
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import flag_issues as fi  # noqa: E402  (gh plumbing, REPO, BOT_MARK)
import run  # noqa: E402  (KNOWN_OUTAGE_DAYS)
from src import registry  # noqa: E402

STALE_DAYS = 90
QUIET_HOURS = range(0, 7)

LABELS = {
    "source-down": ("d73a4a", "A source has failed every pull for days"),
    "source-stale": ("fbca04", "A source has served identical data for months"),
}
MARK = "<!-- source-alert: {kind} {slug} -->"


def _vault_cat():
    from addressvault import Vault
    return Vault(link_wait=False).cat


def collect(today=None):
    """``(down, stale)`` -- ``slug -> info`` for every enabled dataset that
    meets each condition."""
    today = today or date.today()
    cat = _vault_cat()
    streaks = cat.failure_streaks()
    down, stale = {}, {}
    for ds in registry.load_all():
        st = streaks.get(ds.slug)
        if st and st["days"] >= run.KNOWN_OUTAGE_DAYS:
            down[ds.slug] = st
        snap = cat.latest_snapshot(ds.slug)
        if not snap:
            continue
        since = snap["unchanged_since"] or snap["date"]
        age = (today - date.fromisoformat(since)).days
        if age >= STALE_DAYS:
            stale[ds.slug] = {"since": since, "days": age, "pulls": _pulls_since(cat, ds.slug, since)}
    return down, stale


def _pulls_since(cat, slug, since):
    return cat.conn.execute(
        "SELECT COUNT(*) FROM snapshots WHERE slug=? AND date>?", (slug, since)).fetchone()[0]


# ---- issue text ----

def _toml_link(slug):
    return f"https://github.com/{fi.REPO}/blob/main/datasets/{slug}.toml"


def _down_issue(slug, st):
    title = f"{slug}: source down since {st['since']}"
    body = "\n".join([
        MARK.format(kind="down", slug=slug), fi.BOT_MARK,
        f"Every pull of **{slug}** has failed for **{st['days']} pull days**, "
        f"since {st['since']}. Last good pull: {st['last_good'] or 'none recorded'}.",
        "",
        "Latest error:",
        "```",
        (st["detail"] or "")[:1000],
        "```",
        "",
        "The daily run still tries it every day, but no longer counts it as a failure, "
        "so this issue is the alert. The site keeps showing the last good pull.",
        "",
        f"Options: re-point `data_url` in [datasets/{slug}.toml]({_toml_link(slug)}), "
        "ask the publisher, or pause it with `enabled = false` until one of those lands.",
        "",
        "Closes by itself on the first day a pull succeeds.",
    ])
    return title, body


def _stale_issue(slug, info):
    title = f"{slug}: source unchanged since {info['since']}"
    body = "\n".join([
        MARK.format(kind="stale", slug=slug), fi.BOT_MARK,
        f"**{slug}** has served byte-identical data on every pull since "
        f"**{info['since']}** ({info['days']} days, {info['pulls']} pulls).",
        "",
        "The pulls themselves succeed, so nothing else reports this. Usually it means "
        "the layer is a one-off export, or the publisher moved to a new layer and left "
        "this one behind; sometimes it is just a quiet place.",
        "",
        f"Worth a look: the publisher's portal for a newer layer, and the notes in "
        f"[datasets/{slug}.toml]({_toml_link(slug)}).",
        "",
        "Closes by itself the day the content changes.",
    ])
    return title, body


# ---- GitHub ----

def ensure_labels():
    have = {l["name"] for l in fi.gh_json("label", "list", "--repo", fi.REPO,
                                          "--limit", "500", "--json", "name")}
    for name, (color, desc) in LABELS.items():
        if name not in have:
            fi.gh("label", "create", name, "--repo", fi.REPO, "--color", color,
                  "--description", desc, "--force", write=True)


def open_alerts(kind):
    """``slug -> issue number`` of the open alerts of one kind."""
    out = {}
    for r in fi.gh_json("issue", "list", "--repo", fi.REPO, "--label", f"source-{kind}",
                        "--state", "open", "--limit", "500", "--json", "number,body"):
        body = r.get("body") or ""
        for slug in _marked_slugs(body, kind):
            out[slug] = r["number"]
    return out


def _marked_slugs(body, kind):
    prefix = f"<!-- source-alert: {kind} "
    for line in body.splitlines():
        if line.startswith(prefix) and line.endswith(" -->"):
            yield line[len(prefix):-len(" -->")]


def plan(down, stale, open_down, open_stale):
    """The actions a sync would take: ``[(verb, kind, slug, payload)]``."""
    acts = []
    for kind, now, have, make in (("down", down, open_down, _down_issue),
                                  ("stale", stale, open_stale, _stale_issue)):
        for slug in sorted(now):
            if slug not in have:
                acts.append(("open", kind, slug, make(slug, now[slug])))
        for slug in sorted(have):
            if slug not in now:
                acts.append(("close", kind, slug, have[slug]))
    return acts


def _close_text(kind, slug):
    if kind == "down":
        return f"{fi.BOT_MARK}\n{slug} pulled successfully again. Closing."
    return f"{fi.BOT_MARK}\n{slug} published new content. Closing."


def sync(dry_run=False, force=False):
    if not force and not dry_run and datetime.now().hour in QUIET_HOURS:
        print("quiet hours: no alert issues opened or closed before 07:00")
        return
    down, stale = collect()
    acts = plan(down, stale, open_alerts("down"), open_alerts("stale"))
    if not acts:
        print(f"source alerts: nothing to change ({len(down)} down, {len(stale)} stale)")
        return
    if not dry_run:
        ensure_labels()
    for verb, kind, slug, payload in acts:
        if verb == "open":
            title, body = payload
            print(f"open  source-{kind:5s} {slug}: {title}")
            if not dry_run:
                fi.gh("issue", "create", "--repo", fi.REPO, "--title", title,
                      "--label", f"source-{kind}", "--body", body, write=True)
        else:
            print(f"close source-{kind:5s} {slug}: #{payload}")
            if not dry_run:
                fi.gh("issue", "close", str(payload), "--repo", fi.REPO,
                      "--comment", _close_text(kind, slug), write=True)


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("down")
    s = sub.add_parser("sync")
    s.add_argument("--dry-run", action="store_true", help="print what would change")
    s.add_argument("--force", action="store_true", help="ignore quiet hours")
    args = p.parse_args()

    if args.cmd == "sync":
        sync(dry_run=args.dry_run, force=args.force)
        return
    down, stale = collect()
    if args.cmd == "down":
        for slug, st in sorted(down.items()):
            print(f"{slug} ({st['days']} days, last good {st['last_good'] or 'never'})")
        return
    for slug, st in sorted(down.items(), key=lambda kv: -kv[1]["days"]):
        print(f"down   {slug:22s} {st['days']:3d} pull days since {st['since']}  "
              f"last good {st['last_good'] or '-'}  {(st['detail'] or '')[:80]}")
    for slug, info in sorted(stale.items(), key=lambda kv: -kv[1]["days"]):
        print(f"stale  {slug:22s} {info['days']:3d} days unchanged since {info['since']}  "
              f"({info['pulls']} pulls)")


if __name__ == "__main__":
    main()
