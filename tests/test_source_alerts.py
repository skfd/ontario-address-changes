"""Source alerts open one issue per condition per city and close it by themselves."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools"))

import source_alerts as sa  # noqa: E402

DOWN = {"wps": {"days": 15, "since": "2026-10-02", "last_good": "2026-10-01",
                "detail": "arcgis error 500: Service not started"}}
STALE = {"peel-region": {"since": "2026-06-27", "days": 111, "pulls": 107}}


def test_new_conditions_open_and_existing_issues_are_left_alone():
    acts = sa.plan(DOWN, STALE, open_down={}, open_stale={"peel-region": 41})
    assert [(v, k, s) for v, k, s, _ in acts] == [("open", "down", "wps")]
    title, body = acts[0][3]
    assert title == "wps: source down since 2026-10-02"
    assert "<!-- source-alert: down wps -->" in body
    assert "15 pull days" in body and "Service not started" in body


def test_a_recovered_city_closes_its_issue():
    acts = sa.plan({}, {}, open_down={"wps": 40}, open_stale={"peel-region": 41})
    assert [(v, k, s, p) for v, k, s, p in acts] == [
        ("close", "down", "wps", 40), ("close", "stale", "peel-region", 41)]


def test_the_marker_round_trips():
    _, body = sa._down_issue("west-parry-sound", DOWN["wps"])
    assert list(sa._marked_slugs(body, "down")) == ["west-parry-sound"]
    assert list(sa._marked_slugs(body, "stale")) == []


def test_quiet_hours_touch_nothing(monkeypatch, capsys):
    class _Night:
        @staticmethod
        def now():
            from datetime import datetime
            return datetime(2026, 10, 17, 3, 0)

    monkeypatch.setattr(sa, "datetime", _Night)
    monkeypatch.setattr(sa, "collect", lambda: (_ for _ in ()).throw(AssertionError))
    sa.sync()
    assert "quiet hours" in capsys.readouterr().out
