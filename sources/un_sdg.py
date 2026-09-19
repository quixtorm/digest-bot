"""
UN SDG Global Database API (unstats.un.org/sdgapi). No API key required.

Note: the official docs sometimes point at "Indicator/PageOfData", which returns
404 on the current API. The working endpoint (confirmed against the API's own
swagger.json) is "Series/Data".
"""
import requests

import config
from sources.common import IndicatorResult

BASE_URL = "https://unstats.un.org/sdgapi/v1/sdg"
TIMEOUT = 20

# Values that mean "no breakdown / total" for a given dimension. Series are often
# reported broken down by sex, age, or urban/rural location; we prefer the row
# combination that is closest to an overall total.
TOTAL_MARKERS = {"_T", "ALLAREA", "BOTHSEX", "ALLAGE"}


def fetch_indicator(series_code: str, label: str, description: str = "") -> IndicatorResult | None:
    """
    Fetch the latest and previous values for a UN SDG series for Uzbekistan,
    preferring the "total" breakdown when a series has multiple disaggregations.
    Returns None if there is no usable data.
    """
    params = {
        "seriesCode": series_code,
        "areaCode": config.COUNTRY_SDG_AREA_CODE,
        "pageSize": 500,
    }
    resp = requests.get(f"{BASE_URL}/Series/Data", params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    rows = resp.json().get("data", [])
    if not rows:
        return None

    # Group rows by their disaggregation combo (everything except "Reporting Type").
    groups: dict[tuple, list[dict]] = {}
    for row in rows:
        if row.get("value") is None or row.get("timePeriodStart") is None:
            continue
        dims = {k: v for k, v in row.get("dimensions", {}).items() if k != "Reporting Type"}
        combo = tuple(sorted(dims.items()))
        groups.setdefault(combo, []).append(row)

    if not groups:
        return None

    def total_score(combo: tuple) -> int:
        return sum(1 for _, v in combo if v in TOTAL_MARKERS)

    best_combo = max(groups.keys(), key=total_score)
    points = sorted(groups[best_combo], key=lambda r: r["timePeriodStart"], reverse=True)

    latest = points[0]
    previous = points[1] if len(points) > 1 else None

    return IndicatorResult(
        source="UN SDG",
        code=series_code,
        label=label,
        latest_value=float(latest["value"]),
        latest_year=int(latest["timePeriodStart"]),
        previous_value=float(previous["value"]) if previous else None,
        previous_year=int(previous["timePeriodStart"]) if previous else None,
        history_years=len(points),
        last_updated=latest.get("timePeriodStart", ""),
        methodology_present=bool(description.strip()),
        url=f"https://unstats.un.org/sdgs/dataportal/database/indicators?series={series_code}",
    )
