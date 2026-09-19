from datetime import date

from sources.common import IndicatorResult
from sources.scoring import score_candidate


def make_result(latest_year, history_years, methodology_present, source="World Bank"):
    return IndicatorResult(
        source=source,
        code="TEST.CODE",
        label="Test indicator",
        latest_value=42.0,
        latest_year=latest_year,
        previous_value=40.0,
        previous_year=latest_year - 1,
        history_years=history_years,
        last_updated="2026-01-01",
        methodology_present=methodology_present,
        url="https://example.com",
    )


def test_more_recent_data_scores_higher():
    this_year = date.today().year
    recent = score_candidate(make_result(this_year, 10, True))
    old = score_candidate(make_result(this_year - 10, 10, True))
    assert recent.total > old.total


def test_more_history_scores_higher():
    this_year = date.today().year
    long_history = score_candidate(make_result(this_year, 20, True))
    short_history = score_candidate(make_result(this_year, 2, True))
    assert long_history.total > short_history.total


def test_methodology_bonus_applied():
    this_year = date.today().year
    with_methodology = score_candidate(make_result(this_year, 5, True))
    without_methodology = score_candidate(make_result(this_year, 5, False))
    assert with_methodology.total > without_methodology.total


def test_change_property():
    result = make_result(2024, 5, True)
    assert result.change == 2.0
