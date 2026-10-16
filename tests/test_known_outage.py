"""A source that has been down for days must not fail every run: the exit code
has to keep meaning "something new broke" (west-parry-sound, 2026-09-24..10-15,
reddened 21 of 22 runs)."""

import argparse

import pytest

import run
from src import fetch, registry


def _ds(slug, **kw):
    return registry.Dataset(slug=slug, provider="P", data_url="http://x/0",
                            access="arcgis", format="geojson", **kw)


def _args():
    return argparse.Namespace(jobs=1, force=False, no_report=True)


def _run(monkeypatch, datasets, failing, streaks):
    monkeypatch.setattr(run, "_resolve", lambda a: datasets)
    monkeypatch.setattr(fetch, "failure_streaks", lambda: streaks)
    seen = []

    def _serial(ds_list, args):
        seen.extend(d.slug for d in ds_list)
        return ([d for d in ds_list if d.slug not in failing],
                [d for d in ds_list if d.slug in failing])

    monkeypatch.setattr(run, "_update_serial", _serial)
    with pytest.raises(SystemExit) as e:
        run.cmd_update(_args())
        raise SystemExit(0)
    return e.value.code, seen


def test_only_a_known_outage_failed(monkeypatch):
    code, _ = _run(monkeypatch, [_ds("wps"), _ds("guelph")], {"wps"},
                   {"wps": {"days": 15}})
    assert code == run.EXIT_OUTAGE_ONLY


def test_a_fresh_failure_still_fails_the_run(monkeypatch):
    code, _ = _run(monkeypatch, [_ds("wps"), _ds("guelph")], {"wps", "guelph"},
                   {"wps": {"days": 15}, "guelph": {"days": 1}})
    assert code == "update failed for: guelph"


def test_two_days_down_is_still_news(monkeypatch):
    code, _ = _run(monkeypatch, [_ds("simcoe")], {"simcoe"}, {"simcoe": {"days": 2}})
    assert code == "update failed for: simcoe"


def test_a_failure_outside_the_vault_has_no_streak(monkeypatch):
    # An import refusal fails the city with every vault pull 'done'.
    code, _ = _run(monkeypatch, [_ds("york")], {"york"}, {})
    assert code == "update failed for: york"


def test_an_unreadable_vault_counts_nothing_as_known(monkeypatch):
    monkeypatch.setattr(run, "_resolve", lambda a: [_ds("wps")])

    def _boom():
        raise RuntimeError("ADDRESSVAULT_DIR not set")

    monkeypatch.setattr(fetch, "failure_streaks", _boom)
    monkeypatch.setattr(run, "_update_serial", lambda l, a: ([], list(l)))
    with pytest.raises(SystemExit) as e:
        run.cmd_update(_args())
    assert e.value.code == "update failed for: wps"


def test_a_paused_source_is_not_pulled(monkeypatch):
    code, seen = _run(monkeypatch, [_ds("wps", enabled=False), _ds("guelph")],
                      set(), {})
    assert code == 0
    assert seen == ["guelph"]


def test_enabled_defaults_on_and_parses_from_toml(tmp_path):
    assert all(ds.enabled for ds in registry.load_all())
    p = tmp_path / "wps.toml"
    p.write_text(chr(10).join([
        'slug = "wps"', 'provider = "P"', 'data_url = "http://x/0"',
        'access = "arcgis"', 'format = "geojson"', "enabled = false", ""]))
    assert registry._parse(str(p)).enabled is False
