"""The GitHub side of the flag queue: a comment becomes a verdict only when it
is unmistakably one, only the owner's comments count, the two verdicts that
make a public claim cannot be filed without the owner's comment, and filing
edits the ledger in place without disturbing anything around the entry.
"""

import os
import sys
import tempfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import flag_issues as fi  # noqa: E402
from src import flags  # noqa: E402


# ---- parsing the operator's comment ----

def test_first_line_names_the_verdict_and_the_rest_is_the_note():
    v = fi.parse_verdict("technical: 1:1 recode of ARN on all rows\nno address moved")
    assert v["verdict"] == "technical"
    assert v["note"] == "1:1 recode of ARN on all rows no address moved"
    assert v["vault"] is None


def test_verdict_prefix_and_case_are_tolerated():
    assert fi.parse_verdict("Verdict: Business -- new subdivision")["verdict"] == "business"
    assert fi.parse_verdict("BUG\nreplayed batch")["verdict"] == "bug"


def test_vault_and_rule_lines_are_picked_out():
    v = fi.parse_verdict("business: county annexed the township\n"
                         "vault: real -- 6,222 addresses arrived\n"
                         "rule: none needed")
    assert v == {"verdict": "business", "vault": "real", "rule": "none needed",
                 "note": "county annexed the township", "vault_note": "6,222 addresses arrived"}


def test_vault_note_falls_back_to_the_note():
    v = fi.parse_verdict("technical: field blip\nvault: schema")
    assert v["vault_note"] == "field blip"


def test_conversation_is_not_a_verdict():
    assert fi.parse_verdict("Is this the same as last month?") is None
    assert fi.parse_verdict("I think this is business, but let me check") is None
    assert fi.parse_verdict("") is None


def test_vault_only_day_refuses_a_ledger_word():
    v = fi.parse_verdict("technical: nine fields came and went", vault_only=True)
    assert "error" in v
    v = fi.parse_verdict("schema: nine fields came and went", vault_only=True)
    assert v["vault"] == "schema" and v["verdict"] is None


def test_hold_is_a_verdict_that_files_nothing():
    v = fi.parse_verdict("hold -- need to see the county's news page first")
    assert v["verdict"] == "hold" and v["note"].startswith("need to see")


# ---- whose comment counts ----

def _c(body, when, assoc="OWNER", cid="c"):
    return {"id": cid, "body": body, "createdAt": when, "authorAssociation": assoc}


def test_only_the_owners_verdict_after_the_bots_last_word_is_pending():
    bot = _c(fi.BOT_MARK + "\nFiled by Claude", "2026-09-09T20:00:00Z", cid="b")
    stale = _c("business: old answer", "2026-09-09T19:00:00Z", cid="old")
    stranger = _c("business: publish it!", "2026-09-09T21:00:00Z", assoc="NONE", cid="x")
    assert fi.pending_operator_comment([bot, stale, stranger]) is None
    fresh = _c("technical: ARN recode", "2026-09-09T21:30:00Z", cid="new")
    assert fi.pending_operator_comment([bot, stale, stranger, fresh])["id"] == "new"


def test_a_remark_from_the_owner_is_not_pending():
    assert fi.pending_operator_comment([_c("hm, odd", "2026-09-09T21:00:00Z")]) is None


# ---- the owner-only gate ----

def test_business_and_real_need_the_owners_comment(monkeypatch):
    with pytest.raises(PermissionError):
        fi._file(1, "x", "2026-01-01", "business", None, "n", "", "", "", "Claude")
    with pytest.raises(PermissionError):
        fi._file(1, "x", "2026-01-01", None, "real", "n", "", "", "", "Claude")
    monkeypatch.setattr(fi, "comments", lambda n: [
        _c("technical: recode", "2026-09-09T21:00:00Z", cid="op")])
    with pytest.raises(PermissionError):  # the owner said technical, not business
        fi._file(1, "x", "2026-01-01", "business", None, "n", "", "", "op", "Claude")


# ---- filing edits the ledger in place ----

LEDGER = '''# header comment that must survive

[[flag]]
slug = "simcoe"
date = "2026-08-26"
signature = "mass-modified"
fields = ["ARN"]
scope = "90 rows changed the same field set [ARN]"
detail = "top: 'a' -> 'b' (71)"
detected = "2026-08-26"
status = "open"

[[flag]]
slug = "simcoe"
date = "2026-08-28"
signature = "mass-modified"
fields = ["ARN"]
scope = "395 rows"
detected = "2026-08-28"
status = "reviewed"
verdict = "technical"
reviewed = "2026-09-01"
rule = "already done"
note = "earlier"

[[flag]]
slug = "renfrew"
date = "2026-08-28"
signature = "mass-added"
scope = "6,269 added in one day"
detected = "2026-08-28"
status = "open"
'''


def _ledger(tmp):
    p = os.path.join(tmp, "flags.toml")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(LEDGER)
    return p


def test_review_closes_only_the_open_entries_for_that_day():
    with tempfile.TemporaryDirectory() as tmp:
        p = _ledger(tmp)
        keys = flags.review("simcoe", "2026-08-26", "technical", "1:1 recode", rule="ignore ARN",
                            reviewed="2026-09-09", path=p)
        assert keys == [("simcoe", "2026-08-26", "mass-modified", "ARN")]
        text = open(p, encoding="utf-8").read()
        assert text.startswith("# header comment that must survive\n")
        assert 'note = "earlier"' in text            # the reviewed entry untouched
        assert text.count('status = "open"') == 1    # renfrew still open
        entries = flags.load_ledger(p)
        done = next(e for e in entries if e["date"] == "2026-08-26")
        assert done["status"] == "reviewed" and done["verdict"] == "technical"
        assert done["rule"] == "ignore ARN" and done["reviewed"] == "2026-09-09"
        assert done["detail"] == "top: 'a' -> 'b' (71)"  # identity fields kept


def test_review_refuses_a_quiet_day_and_a_technical_without_a_rule():
    with tempfile.TemporaryDirectory() as tmp:
        p = _ledger(tmp)
        with pytest.raises(LookupError):
            flags.review("simcoe", "2026-08-27", "technical", "n", rule="r", path=p)
        with pytest.raises(LookupError):  # already reviewed: never rewritten from code
            flags.review("simcoe", "2026-08-28", "business", "n", path=p)
        with pytest.raises(ValueError):
            flags.review("renfrew", "2026-08-28", "technical", "n", path=p)
        with pytest.raises(ValueError):
            flags.review("renfrew", "2026-08-28", "business", "", path=p)
        assert open(p, encoding="utf-8").read() == LEDGER  # nothing written on refusal


def test_business_needs_no_rule():
    with tempfile.TemporaryDirectory() as tmp:
        p = _ledger(tmp)
        flags.review("renfrew", "2026-08-28", "business", "new subdivision", path=p)
        e = next(e for e in flags.load_ledger(p) if e["slug"] == "renfrew")
        assert e["verdict"] == "business" and e["rule"] == ""
