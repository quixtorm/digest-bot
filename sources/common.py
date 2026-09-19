"""Shared data shape returned by every source module (worldbank/who_gho/un_sdg)."""
from dataclasses import dataclass


@dataclass
class IndicatorResult:
    source: str            # "World Bank" | "WHO GHO" | "UN SDG"
    code: str               # indicator/series code used
    label: str              # human-readable indicator name
    latest_value: float
    latest_year: int
    previous_value: float | None
    previous_year: int | None
    history_years: int      # count of non-null observations found (coverage proxy)
    last_updated: str       # ISO date string the API reports for the data, used for recency
    methodology_present: bool  # does the API publish a name/definition for this indicator
    url: str                 # link a human can open to see the source data

    @property
    def change(self) -> float | None:
        if self.previous_value is None:
            return None
        return self.latest_value - self.previous_value
