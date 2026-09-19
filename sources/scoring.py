"""
Plain-code reliability scoring. No LLM involved: this decides which single source
wins for a field, based on transparent, reproducible criteria.

Criteria (see docs/SOURCES.md for the full rationale):
  1. Official organization  - fixed points; World Bank, WHO and UN Statistics are
                               all official international agencies, so this mostly
                               acts as a gate (only these three ever compete).
  2. Recency                - how recent the latest data point is.
  3. Country coverage       - how many years of non-null history exist for Uzbekistan.
  4. Published methodology  - whether the source publishes a name/definition for it.
"""
from dataclasses import dataclass
from datetime import date

from sources.common import IndicatorResult

OFFICIAL_ORG_POINTS = 10
METHODOLOGY_BONUS = 5
MAX_RECENCY_POINTS = 15
COVERAGE_CAP = 20  # years of history beyond this no longer add points


@dataclass
class ScoredCandidate:
    result: IndicatorResult
    official_points: float
    recency_points: float
    coverage_points: float
    methodology_points: float

    @property
    def total(self) -> float:
        return self.official_points + self.recency_points + self.coverage_points + self.methodology_points


def _recency_points(latest_year: int) -> float:
    years_old = date.today().year - latest_year
    return max(0, MAX_RECENCY_POINTS - years_old)


def score_candidate(result: IndicatorResult) -> ScoredCandidate:
    return ScoredCandidate(
        result=result,
        official_points=OFFICIAL_ORG_POINTS,
        recency_points=_recency_points(result.latest_year),
        coverage_points=min(result.history_years, COVERAGE_CAP),
        methodology_points=METHODOLOGY_BONUS if result.methodology_present else 0,
    )


def pick_best_source(field: str, candidates: list[dict]) -> tuple[ScoredCandidate, list[ScoredCandidate]]:
    """
    Fetch every candidate for a field, score the ones that returned real data,
    and return (winner, all_scored_candidates) sorted best-first.
    Raises RuntimeError if no candidate returned usable data.
    """
    scored: list[ScoredCandidate] = []
    for candidate in candidates:
        fetch = candidate["fetch"]
        kwargs = {k: v for k, v in candidate.items() if k not in ("fetch", "code", "label")}
        result = fetch(candidate["code"], candidate["label"], **kwargs)
        if result is not None:
            scored.append(score_candidate(result))

    if not scored:
        raise RuntimeError(f"No source returned usable data for field '{field}'")

    scored.sort(key=lambda s: s.total, reverse=True)
    return scored[0], scored


def explain_winner(field: str, winner: ScoredCandidate, all_scored: list[ScoredCandidate]) -> str:
    """Build a short, human-readable justification for why this source won, in Russian."""
    r = winner.result
    others = [s for s in all_scored if s is not winner]
    lines = [
        f"Источник «{r.source}» выбран для раздела: набрал {winner.total:.0f} баллов "
        f"из {OFFICIAL_ORG_POINTS + MAX_RECENCY_POINTS + COVERAGE_CAP + METHODOLOGY_BONUS} возможных.",
        f"— Официальная организация: +{winner.official_points:.0f} (данные международного статистического агентства).",
        f"— Актуальность: +{winner.recency_points:.0f} (последние данные за {r.latest_year} год).",
        f"— Охват по стране: +{winner.coverage_points:.0f} ({r.history_years} лет наблюдений для Узбекистана).",
        f"— Методология: +{winner.methodology_points:.0f} "
        + ("(есть опубликованное описание методологии)." if r.methodology_present else "(описание методологии не найдено)."),
    ]
    if others:
        comparison = "; ".join(f"{s.result.source} — {s.total:.0f}" for s in others)
        lines.append(f"Другие источники, рассмотренные и отклонённые: {comparison}.")
    return "\n".join(lines)
