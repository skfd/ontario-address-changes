"""The flag queue as GitHub issues, so a review can happen from a phone.

    python tools/flag_issues.py open       # one issue per open flag-day that has none
    python tools/flag_issues.py inbox      # what is waiting: operator verdicts, unreviewed days
    python tools/flag_issues.py apply      # file the operator's business/hold answers (no model)
    python tools/flag_issues.py file N --verdict V --note N [--rule R] [--vault V] [--from-comment ID]
    python tools/flag_issues.py propose N --verdict V --note N
    python tools/flag_issues.py publish    # render filed cities, commit, push, close their issues

flags.toml (and the vault's own ledger) stay the record; the issues mirror it.
An issue is opened for every (slug, date) holding content off the site -- or
flagged by the vault alone -- with the review brief inside it and the links a
reviewer needs, and it closes only once every question on it has a verdict
filed where verdicts live. The operator answers by commenting; the hourly task
(review-flags.ps1) reads the comment, files it, re-renders, pushes, and
replies with the commit.

Two things are never done from a comment by anyone but the repository owner:
a ``business`` verdict (it publishes to the site) and a vault ``real`` (it says
the world changed). Both repos are public, so every other comment is ignored,
and headless Claude is refused those two verdicts outright -- ``file`` demands
the owner's comment id for them. The bot posts as the owner too (gh runs under
the operator's login), so its own comments are told apart by a marker, not by
author.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date as date_t, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src import flags, registry  # noqa: E402

REPO = "skfd/ontario-address-changes"
SITE = "https://skfd.github.io/ontario-address-changes"
BRIEF = os.path.join(ROOT, ".claude", "skills", "review-flags", "brief.py")

DAY_MARK = "<!-- flag-day: {slug} {date} -->"
DAY_RE = re.compile(r"<!-- flag-day: (\S+) (\d{4}-\d{2}-\d{2}) -->")
BOT_MARK = "<!-- flag-bot -->"

LEDGER_VERDICTS = ("business", "technical", "bug")
VAULT_VERDICTS = ("real", "schema", "artifact")
# What only the owner may say: the two verdicts that make a public claim.
OWNER_ONLY = {"business", "real"}

LABELS = {
    "flag": ("5319e7", "a mass change held pending review"),
    "needs-triage": ("fbca04", "nobody has looked yet"),
    "needs-operator": ("d93f0b", "Claude proposed; the operator decides"),
    "on-hold": ("c5def5", "operator asked to keep it open"),
    "vault": ("0e8a16", "the vault flagged the same day"),
    "vault-only": ("0e8a16", "flagged by the vault alone; no site event"),
    "licence-blocked": ("e4e669", "city publishes no pages; a verdict releases nothing"),
    "verdict:business": ("0075ca", "the city really changed"),
    "verdict:technical": ("bfdadc", "the feed changed, the city did not"),
    "verdict:bug": ("d73a4a", "the data was not true of the world"),
}
VAULT_LABELS = {v: (LABELS[f"verdict:{k}"][0], f"vault: {v}")
                for k, v in (("business", "real"), ("technical", "schema"), ("bug", "artifact"))}

BRIEF_MAX = 30_000  # issue bodies cap at 65,536 chars


# ---- gh ----

def gh(*args, input=None, check=True):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True,
                          encoding="utf-8", input=input, cwd=ROOT)
    if check and proc.returncode:
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {proc.stderr.strip()}")
    return proc.stdout


def gh_json(*args):
    return json.loads(gh(*args) or "null")


def ensure_labels(extra=()):
    have = {l["name"] for l in gh_json("label", "list", "--repo", REPO, "--limit", "500",
                                       "--json", "name")}
    want = dict(LABELS)
    for v, spec in VAULT_LABELS.items():
        want[f"vault:{v}"] = spec
    for name in extra:
        want.setdefault(name, ("ededed", ""))
    for name, (color, desc) in want.items():
        if name not in have:
            gh("label", "create", name, "--repo", REPO, "--color", color,
               "--description", desc, "--force")


def list_issues(state="all"):
    rows = gh_json("issue", "list", "--repo", REPO, "--label", "flag", "--state", state,
                   "--limit", "500", "--json", "number,title,body,labels,state,url")
    out = []
    for r in rows:
        m = DAY_RE.search(r.get("body") or "")
        if not m:
            continue
        r["slug"], r["date"] = m.group(1), m.group(2)
        r["labels"] = {l["name"] for l in r.get("labels", [])}
        out.append(r)
    return out


def comments(number):
    return gh_json("issue", "view", str(number), "--repo", REPO, "--json", "comments")["comments"]


def comment(number, body):
    gh("issue", "comment", str(number), "--repo", REPO, "--body", BOT_MARK + "\n" + body)


def relabel(number, add=(), remove=()):
    args = ["issue", "edit", str(number), "--repo", REPO]
    for l in add:
        args += ["--add-label", l]
    for l in remove:
        args += ["--remove-label", l]
    if add or remove:
        gh(*args)


# ---- what is open, on both sides ----

def open_ledger_days():
    """(slug, date) -> open ledger entries, oldest detection first."""
    days = {}
    for f in flags.load_ledger():
        if f.get("status", "open") != "reviewed":
            days.setdefault((f["slug"], f["date"]), []).append(f)
    return dict(sorted(days.items(), key=lambda kv: (kv[1][0].get("detected", ""), kv[0])))


def vault_changes(days=400):
    """The vault's large-change list, (slug, date) -> row. ``None`` when the
    vault cannot be asked -- which is not the same as no rows: an issue can be
    opened without its vault section, but nothing may be closed on it."""
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "addressvault.cli", "report", "--json", "--days", str(days)],
            capture_output=True, text=True, encoding="utf-8", timeout=180, cwd=ROOT)
        data = json.loads(proc.stdout)
    except Exception as e:  # noqa: BLE001
        print(f"  (vault unreachable: {e})", file=sys.stderr)
        return None
    return {(c["slug"], c["date"]): c for c in data.get("changes", [])}


def vault_review(slug, date, verdict, note):
    proc = subprocess.run(
        [sys.executable, "-m", "addressvault.cli", "review", slug, date, verdict, "-m", note],
        capture_output=True, text=True, encoding="utf-8", timeout=300, cwd=ROOT)
    if proc.returncode:
        raise RuntimeError((proc.stderr or proc.stdout).strip())
    return (proc.stdout or "").strip()


# ---- the operator's comment ----

_VERDICT_WORDS = "|".join(LEDGER_VERDICTS + VAULT_VERDICTS + ("hold",))
_SEP = r"\s*(?:[:=]|-+|–|—)?\s*"  # "business: x", "business -- x", "business x"
_FIRST = re.compile(r"^\s*(?:verdict\s*[:=]\s*)?(" + _VERDICT_WORDS + r")\b" + _SEP + r"(.*)$",
                    re.IGNORECASE)
_VAULT = re.compile(r"^\s*vault\s*[:=]\s*(real|schema|artifact)\b" + _SEP + r"(.*)$",
                    re.IGNORECASE)
_RULE = re.compile(r"^\s*rule\s*[:=]\s*(.+)$", re.IGNORECASE)


def parse_verdict(body, vault_only=False):
    """A verdict comment: first non-blank line names the verdict, the rest is
    the note. Optional lines ``vault: real|schema|artifact`` and ``rule: ...``.
    Returns None when the comment is not a verdict at all (a question, a
    remark), so ordinary conversation on an issue files nothing."""
    lines = [l.rstrip() for l in (body or "").splitlines()]
    lines = [l for l in lines if l.strip()]
    if not lines:
        return None
    m = _FIRST.match(lines[0])
    if not m:
        return None
    word = m.group(1).lower()
    out = {"verdict": None, "vault": None, "rule": "", "note": ""}
    note = [m.group(2).strip()] if m.group(2).strip() else []
    if word in VAULT_VERDICTS:
        out["vault"] = word
    elif word == "hold":
        out["verdict"] = "hold"
    else:
        out["verdict"] = word
    vault_note = []
    for l in lines[1:]:
        mv = _VAULT.match(l)
        if mv:
            out["vault"] = mv.group(1).lower()
            if mv.group(2).strip():
                vault_note.append(mv.group(2).strip())
            continue
        mr = _RULE.match(l)
        if mr:
            out["rule"] = mr.group(1).strip()
            continue
        note.append(l.strip())
    out["note"] = " ".join(note).strip()
    out["vault_note"] = " ".join(vault_note).strip() or out["note"]
    if vault_only and out["verdict"] not in (None, "hold"):
        # The day has no site event; a ledger word here is a slip of the thumb.
        return {"error": f"this day is flagged by the vault alone; answer with "
                         f"one of {', '.join(VAULT_VERDICTS)} (or hold), not {out['verdict']!r}"}
    return out


def is_bot(c):
    return BOT_MARK in (c.get("body") or "")


def pending_operator_comment(cmts):
    """The owner's newest verdict comment since the bot last spoke, or None.
    Non-owner comments never count: the repo is public."""
    last_bot = max((c["createdAt"] for c in cmts if is_bot(c)), default="")
    for c in sorted(cmts, key=lambda c: c["createdAt"], reverse=True):
        if is_bot(c) or c["createdAt"] <= last_bot:
            continue
        if c.get("authorAssociation") != "OWNER":
            continue
        if parse_verdict(c.get("body")) is not None:
            return c
    return None


# ---- issue bodies ----

def _brief_text(slug, date):
    try:
        proc = subprocess.run([sys.executable, BRIEF, slug, date], capture_output=True,
                              text=True, encoding="utf-8", timeout=600, cwd=ROOT)
        text = (proc.stdout or "") + (("\n" + proc.stderr) if proc.returncode else "")
    except Exception as e:  # noqa: BLE001
        text = f"(brief failed: {e})"
    text = text.strip() or "(brief produced nothing)"
    if len(text) > BRIEF_MAX:
        text = text[:BRIEF_MAX] + "\n... (truncated; run brief.py on the laptop for the rest)"
    return text


def _vault_section(row):
    if not row:
        return ""
    a = row.get("addresses")
    if a is None:
        moved = "no baseline that day to measure against"
    else:
        share = ("rewrite share unmeasured" if a.get("rewritten") is None
                 else f"{a['rewritten']:.3%} rewritten")
        moved = f"{a['net']:+,} {a['unit']} net, {share}"
    v = row.get("verdict")
    state = f"answered `{v}`" if v else "**unanswered**"
    lines = [f"**Vault:** {row.get('why', '')}",
             f"Addresses: {moved}. Vault verdict: {state}."]
    if row.get("note"):
        lines.append(f"Vault note: {row['note']}")
    if not v:
        lines.append("The vault asks its own question about this day; answer it with a "
                     "`vault: real|schema|artifact` line (see below).")
    return "\n".join(lines) + "\n\n"


def _how_to_answer(vault_flagged, vault_only):
    if vault_only:
        return (
            "## How to answer\n"
            "Comment with one of these words on the first line, then your reasoning "
            "(the note is required and is the record):\n\n"
            "- `artifact` -- what arrived is not true of the world; no address changed\n"
            "- `schema` -- the source changed what it publishes, not the addresses\n"
            "- `real` -- the addresses really moved (owner only)\n"
            "- `hold` -- keep it open; say what is missing\n\n"
            "Only the repository owner's comments are read. The hourly task files the "
            "verdict in the vault and closes this issue.\n")
    text = (
        "## How to answer\n"
        "Comment with one of these words on the first line, then your reasoning "
        "(the note is required and is the record):\n\n"
        "- `business` -- the city really changed; publish it (owner only)\n"
        "- `technical` -- the feed changed, the city did not; Claude makes the config "
        "rule that stops the recurrence (a `rule: ...` line tells it what you have in mind)\n"
        "- `bug` -- the data is not true of the world; held, and the vault is told\n"
        "- `hold` -- keep it open; say what is missing\n\n")
    if vault_flagged:
        text += ("Add a second line `vault: real|schema|artifact` to answer the vault's "
                 "question on the same comment; until both are answered the issue "
                 "stays open.\n\n")
    text += ("Only the repository owner's comments are read. The hourly task (18:00 to "
             "22:00) files the verdict, re-renders the city, pushes, and replies here "
             "with the commit.\n")
    return text


def build_body(slug, date, entries, vault_row, ds):
    vault_only = not entries
    licence_blocked = ds is not None and not ds.publish_reports
    parts = [DAY_MARK.format(slug=slug, date=date), ""]
    if entries:
        for e in entries:
            fields = f" [{', '.join(e['fields'])}]" if e.get("fields") else ""
            parts.append(f"**{e['signature']}{fields}** -- {e['scope']}")
            if e.get("detail"):
                parts.append(f"<sub>{e['detail']}</sub>")
            parts.append("")
        if len(entries) > 1:
            parts.append(f"This day carries {len(entries)} held events; one verdict "
                         "applies to all of them. If they differ, answer `hold` and "
                         "file them apart on the laptop.")
            parts.append("")
    else:
        parts.append("Flagged by the vault alone: the pull moved, but the site recorded "
                     "no mass event that day.")
        parts.append("")
    if licence_blocked:
        parts.append("**Licence-blocked city:** it publishes no report pages, so a verdict "
                     "here releases nothing to the site. It still settles the record.")
        parts.append("")
    links = []
    if ds is not None and ds.publish_reports:
        links.append(f"[day page]({SITE}/{slug}/report-{date}.html)")
    links.append(f"[dataset config](https://github.com/{REPO}/blob/main/datasets/{slug}.toml)")
    if ds is not None:
        links.append(f"[source layer]({ds.data_url})")
    links.append(f"[this city's flags](https://github.com/{REPO}/issues?q=label%3Acity%3A{slug})")
    if entries:
        sig = entries[0]["signature"]
        links.append(f"[same signature](https://github.com/{REPO}/issues?q=label%3Asig%3A{sig})")
    parts.append("Links: " + " · ".join(links))
    parts.append("")
    parts.append(_vault_section(vault_row))
    parts.append(_how_to_answer(bool(vault_row), vault_only))
    if entries:
        parts.append("<details><summary>Review brief (rows, transitions, this city's "
                     "past flags)</summary>\n\n```\n" + _brief_text(slug, date) + "\n```\n</details>")
    return "\n".join(parts)


def title_for(slug, date, entries, vault_row):
    if entries:
        e = entries[0]
        fields = f": {', '.join(e['fields'])}" if e.get("fields") else ""
        more = f" (+{len(entries) - 1} more)" if len(entries) > 1 else ""
        return f"{slug} {date} — {e['signature']}{fields}{more}"
    return f"{slug} {date} — vault: {vault_row.get('test') or 'large change'}"


# ---- commands ----

def _dataset(slug):
    try:
        return registry.load(slug)
    except Exception:  # noqa: BLE001  (a vault slug with no dataset here)
        return None


def cmd_open(args):
    ledger_days = open_ledger_days()
    vault = vault_changes()
    if vault is None:
        print("open: vault unreachable; opening ledger days without their vault section")
        vault = {}
    vault_open = {k: v for k, v in vault.items() if v.get("verdict") is None}
    wanted = dict(ledger_days)
    for k in vault_open:
        wanted.setdefault(k, [])
    ensure_labels({f"city:{s}" for s, _ in wanted} | {f"sig:{e['signature']}"
                                                       for es in wanted.values() for e in es})
    issues = {(i["slug"], i["date"]): i for i in list_issues()}
    created = reopened = 0
    for (slug, date), entries in wanted.items():
        ds = _dataset(slug)
        vrow = vault.get((slug, date))
        if (slug, date) in issues:
            iss = issues[(slug, date)]
            if iss["state"].upper() == "CLOSED" and not pending_operator_comment(comments(iss["number"])):
                gh("issue", "reopen", str(iss["number"]), "--repo", REPO)
                comment(iss["number"], "Reopened: this day is still open in the ledger. "
                        "An issue closes when a verdict is filed, not when it is closed here; "
                        "answer with a verdict comment (or `hold` with a note).")
                reopened += 1
            continue
        labels = ["flag", "needs-triage", f"city:{slug}"]
        labels += [f"sig:{e['signature']}" for e in {e["signature"]: e for e in entries}.values()]
        if not entries:
            labels.append("vault-only")
        elif vrow:
            labels.append("vault")
        if ds is not None and not ds.publish_reports:
            labels.append("licence-blocked")
        body = build_body(slug, date, entries, vrow, ds)
        url = gh("issue", "create", "--repo", REPO, "--title", title_for(slug, date, entries, vrow),
                 "--body-file", "-", *sum((["--label", l] for l in labels), []), input=body).strip()
        print(f"  opened {url}  {slug} {date}")
        created += 1
    print(f"open: {created} created, {reopened} reopened, {len(wanted)} day(s) open in all")


def _inbox(limit=0):
    """Everything waiting on someone: operator verdicts to file, days to triage."""
    ledger_days = open_ledger_days()
    items = []
    for iss in list_issues(state="open"):
        key = (iss["slug"], iss["date"])
        vault_only = "vault-only" in iss["labels"]
        item = {"number": iss["number"], "url": iss["url"], "slug": iss["slug"], "date": iss["date"],
                "vault_only": vault_only, "vault_flagged": vault_only or "vault" in iss["labels"],
                "ledger_open": key in ledger_days}
        c = pending_operator_comment(comments(iss["number"]))
        if c:
            v = parse_verdict(c["body"], vault_only=vault_only)
            item.update(kind="operator", comment_id=c["id"], comment_url=c.get("url"), **v)
        elif "needs-triage" in iss["labels"]:
            item["kind"] = "triage"
        else:
            continue  # proposed, on hold, or half-filed: waiting on the operator
        items.append(item)
    # The operator's answers first (content is waiting on them), then the
    # oldest unreviewed days.
    items.sort(key=lambda it: (it["kind"] != "operator", it["date"], it["number"]))
    return items[:limit] if limit else items


def cmd_inbox(args):
    items = _inbox(args.limit)
    if args.json:
        print(json.dumps(items, indent=2))
        return
    if not items:
        print("inbox empty")
        return
    for it in items:
        if it["kind"] == "operator":
            what = it.get("error") or f"{it.get('verdict') or ''} {('vault:' + it['vault']) if it.get('vault') else ''}".strip()
            print(f"  #{it['number']} {it['slug']} {it['date']}  operator says: {what} -- {it.get('note', '')[:80]}")
        else:
            print(f"  #{it['number']} {it['slug']} {it['date']}  needs triage")


def _file(number, slug, date, verdict, vault, note, rule, vault_note, from_comment, actor):
    """File what can be filed, post what was done, relabel. Returns the list of
    things filed (for the comment) and whether the issue is now fully answered."""
    if not from_comment:
        bad = {verdict, vault} & OWNER_ONLY
        if bad:
            raise PermissionError(f"{'/'.join(sorted(bad))} may only be filed from the owner's "
                                  f"comment (pass --from-comment)")
    else:
        cmts = comments(number)
        src = next((c for c in cmts if c["id"] == from_comment), None)
        if src is None or src.get("authorAssociation") != "OWNER" or is_bot(src):
            raise PermissionError("--from-comment must be a comment by the repository owner on this issue")
        said = parse_verdict(src["body"]) or {}
        for want, key in ((verdict, "verdict"), (vault, "vault")):
            if want in OWNER_ONLY and said.get(key) != want:
                raise PermissionError(f"the owner's comment does not say {want!r}")
    done, problems = [], []
    if verdict and verdict != "hold":
        try:
            keys = flags.review(slug, date, verdict, note, rule=rule)
            done.append(f"ledger: `{verdict}` on {len(keys)} entr{'y' if len(keys) == 1 else 'ies'}"
                        + (f"; rule: {rule}" if rule else ""))
        except (LookupError, ValueError) as e:
            problems.append(f"ledger: {e}")
    if vault:
        try:
            vault_review(slug, date, vault, vault_note or note)
            done.append(f"vault: `{vault}`")
        except Exception as e:  # noqa: BLE001
            problems.append(f"vault: {str(e).splitlines()[-1] if str(e) else e}")
    return done, problems


def _post_filed(number, actor, done, problems, note, hold=False, slug=None, date=None,
                vault_answered=False):
    lines = []
    if hold:
        lines.append(f"Held open at the operator's request. Note: {note}")
    if done:
        lines.append(f"Filed by {actor}:")
        lines += [f"- {d}" for d in done]
        lines.append(f"\nNote: {note}")
    if problems:
        lines.append("Could not file:")
        lines += [f"- {p}" for p in problems]
    if done and not hold:
        if slug and not vault_answered and _vault_question_open(slug, date):
            lines.append("\nThe vault's question about this day is still open: answer it with "
                         "a comment whose first line is `vault: real|schema|artifact`, then "
                         "your note. The issue stays open until then.")
        lines.append("\nThe city re-renders and pushes on the next hourly pass; this issue "
                     "closes with the commit once every question on it is answered.")
    comment(number, "\n".join(lines))


def _vault_question_open(slug, date):
    rows = vault_changes()
    if rows is None:
        return True  # cannot tell; say it is open rather than quietly not
    row = rows.get((slug, date))
    return row is not None and row.get("verdict") is None


def _labels_after(number, verdict, vault, hold):
    add, remove = [], ["needs-triage", "needs-operator", "on-hold"]
    if hold:
        add.append("on-hold")
    if verdict and verdict != "hold":
        add.append(f"verdict:{verdict}")
    if vault:
        add.append(f"vault:{vault}")
    relabel(number, add=add, remove=[l for l in remove if l not in add])


def cmd_file(args):
    iss = next((i for i in list_issues() if i["number"] == args.number), None)
    if iss is None:
        sys.exit(f"#{args.number} is not a flag issue")
    vault_only = "vault-only" in iss["labels"]
    if vault_only and args.verdict:
        sys.exit("a vault-only day takes --vault real|schema|artifact, not --verdict")
    if not (args.verdict or args.vault):
        sys.exit("nothing to file: give --verdict and/or --vault")
    actor = "Claude, on the operator's verdict" if args.from_comment else "Claude (headless triage)"
    ensure_labels()
    done, problems = _file(args.number, iss["slug"], iss["date"], args.verdict, args.vault,
                           args.note, args.rule or "", args.vault_note, args.from_comment, actor)
    _post_filed(args.number, actor, done, problems, args.note, slug=iss["slug"], date=iss["date"],
                vault_answered=bool(args.vault))
    _labels_after(args.number, args.verdict, args.vault, hold=False)
    for d in done:
        print(f"  filed #{args.number}: {d}")
    for p in problems:
        print(f"  PROBLEM #{args.number}: {p}")
    if problems and not done:
        sys.exit(1)


def cmd_propose(args):
    ensure_labels()
    body = (f"Claude's reading: **{args.verdict}**, but this verdict is yours to give.\n\n"
            f"{args.note}\n\n"
            "Reply with the verdict word and your note to file it, or `hold` with what is missing.")
    comment(args.number, body)
    relabel(args.number, add=["needs-operator"], remove=["needs-triage"])
    print(f"  proposed {args.verdict} on #{args.number}")


def cmd_apply(args):
    """The operator's answers that need no model: business, vault real/schema/
    artifact, hold. technical/bug need a rule made real, so they are left for
    Claude and listed."""
    ensure_labels()
    left = []
    for it in _inbox():
        if it["kind"] != "operator":
            continue
        n = it["number"]
        if it.get("error"):
            comment(n, it["error"])
            continue
        verdict, vault = it.get("verdict"), it.get("vault")
        if verdict in ("technical", "bug"):
            left.append(it)  # a rule has to be made real, not just written down
            continue
        if verdict == "hold":
            _post_filed(n, "the operator", [], [], it.get("note") or "(no note)", hold=True)
            _labels_after(n, None, None, hold=True)
            print(f"  held #{n}")
            continue
        if not it.get("note"):
            comment(n, "A verdict needs a note: one line saying what this was. Comment again "
                       "with the verdict word and the reasoning.")
            continue
        done, problems = _file(n, it["slug"], it["date"], verdict, vault, it["note"],
                               it.get("rule", ""), it.get("vault_note"), it["comment_id"], "the operator")
        _post_filed(n, "the operator", done, problems, it["note"], slug=it["slug"], date=it["date"],
                    vault_answered=bool(vault))
        _labels_after(n, verdict if done else None, vault if done else None, hold=False)
        for d in done:
            print(f"  filed #{n}: {d}")
        for p in problems:
            print(f"  PROBLEM #{n}: {p}")
    if args.json:
        print(json.dumps(left, indent=2))
    else:
        for it in left:
            print(f"  for Claude: #{it['number']} {it['slug']} {it['date']} operator says "
                  f"{it['verdict']} -- {it.get('note', '')[:80]}")
    print(f"apply: {len(left)} operator verdict(s) need a rule made real")


def _git(*args):
    proc = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    if proc.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {(proc.stderr or proc.stdout).strip()}")
    return proc.stdout.strip()


def cmd_publish(args):
    """Close what is answered: render each city whose ledger verdicts are all
    filed, commit ledger + config + docs once, push, reply with the commit."""
    ledger_days = open_ledger_days()
    vault = vault_changes()
    if vault is None:
        print("publish: vault unreachable; closing nothing this pass")
        return
    ready = []
    for iss in list_issues(state="open"):
        key = (iss["slug"], iss["date"])
        if key in ledger_days:
            continue  # a site event on this day is still unfiled
        vrow = vault.get(key)
        if vrow is not None and vrow.get("verdict") is None:
            continue  # the vault's question is still open
        ready.append(iss)
    if not ready:
        print("publish: nothing answered since last pass")
        return
    slugs = sorted({i["slug"] for i in ready if (i["slug"], i["date"]) in _reviewed_days()})
    failed = set()
    for slug in slugs:
        print(f"  rendering {slug}")
        proc = subprocess.run([sys.executable, "run.py", "report", "--city", slug],
                              capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
        if proc.returncode:
            failed.add(slug)
            print(f"  RENDER FAILED {slug}: {(proc.stderr or proc.stdout).strip()[-500:]}")
    commit_url = None
    try:
        _git("add", "flags.toml", "datasets", "docs")
        if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode:
            names = ", ".join(f"{i['slug']} {i['date']}" for i in ready if i["slug"] not in failed)
            _git("commit", "-m", f"Review flags: {names}")
            sha = _git("rev-parse", "HEAD")
            _git("push")
            commit_url = f"https://github.com/{REPO}/commit/{sha}"
            print(f"  pushed {commit_url}")
    except RuntimeError as e:
        print(f"  GIT FAILED: {e}")
        return  # leave every issue open; the next pass retries
    for iss in ready:
        if iss["slug"] in failed:
            comment(iss["number"], "Verdict filed, but re-rendering this city failed; the next "
                                   "hourly pass retries. Check logs/flags-review.log on the laptop.")
            continue
        body = "Answered. " + (f"Published in {commit_url}." if commit_url
                               else "Nothing on the site changed.")
        comment(iss["number"], body)
        gh("issue", "close", str(iss["number"]), "--repo", REPO, "--reason", "completed")
        print(f"  closed #{iss['number']} {iss['slug']} {iss['date']}")


def _reviewed_days():
    return {(f["slug"], f["date"]) for f in flags.load_ledger() if f.get("status") == "reviewed"}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("open").set_defaults(func=cmd_open)
    sp = sub.add_parser("inbox"); sp.add_argument("--json", action="store_true")
    sp.add_argument("--limit", type=int, default=0, help="at most N items (operator answers first)")
    sp.set_defaults(func=cmd_inbox)
    sp = sub.add_parser("apply"); sp.add_argument("--json", action="store_true"); sp.set_defaults(func=cmd_apply)
    sp = sub.add_parser("file")
    sp.add_argument("number", type=int)
    sp.add_argument("--verdict", choices=LEDGER_VERDICTS)
    sp.add_argument("--vault", choices=VAULT_VERDICTS)
    sp.add_argument("--note", required=True)
    sp.add_argument("--rule", default="")
    sp.add_argument("--vault-note", default="")
    sp.add_argument("--from-comment", default="", help="owner's comment id (required for business / real)")
    sp.set_defaults(func=cmd_file)
    sp = sub.add_parser("propose")
    sp.add_argument("number", type=int)
    sp.add_argument("--verdict", required=True, choices=LEDGER_VERDICTS + VAULT_VERDICTS)
    sp.add_argument("--note", required=True)
    sp.set_defaults(func=cmd_propose)
    sub.add_parser("publish").set_defaults(func=cmd_publish)
    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
