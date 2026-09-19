"""WHO Global Health Observatory OData API (ghoapi.azureedge.net/api). No API key required."""
import requests

import config
from sources.common import IndicatorResult

BASE_URL = "https://ghoapi.azureedge.net/api"
TIMEOUT = 20


def fetch_indicator(code: str, label: str, country: str = config.COUNTRY_ISO3) -> IndicatorResult | None:
    """
    Fetch the latest and previous non-null "both sexes" values for a WHO GHO indicator.
    Returns None if the country has no usable data for this indicator.
    """
    filter_expr = f"SpatialDim eq '{country}' and Dim1 eq 'SEX_BTSX'"
    params = {"$filter": filter_expr, "$orderby": "TimeDim desc", "$top": 100}
    resp = requests.get(f"{BASE_URL}/{code}", params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    rows = resp.json().get("value", [])

    if not rows:
        # Some indicators have no sex breakdown at all; retry without the Dim1 filter.
        params = {"$filter": f"SpatialDim eq '{country}'", "$orderby": "TimeDim desc", "$top": 100}
        resp = requests.get(f"{BASE_URL}/{code}", params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        rows = resp.json().get("value", [])

    non_null = [r for r in rows if r.get("NumericValue") is not None]
    if not non_null:
        return None

    latest = non_null[0]
    previous = non_null[1] if len(non_null) > 1 else None

    return IndicatorResult(
        source="WHO GHO",
        code=code,
        label=label,
        latest_value=latest["NumericValue"],
        latest_year=int(latest["TimeDim"]),
        previous_value=previous["NumericValue"] if previous else None,
        previous_year=int(previous["TimeDim"]) if previous else None,
        history_years=len(non_null),
        last_updated=latest.get("Date", ""),
        methodology_present=_has_methodology(code),
        url=f"https://www.who.int/data/gho/data/indicators/indicator-details/GHO/{code}",
    )


def _has_methodology(code: str) -> bool:
    """Check whether WHO GHO publishes a name/definition for this indicator code."""
    try:
        resp = requests.get(
            f"{BASE_URL}/Indicator",
            params={"$filter": f"IndicatorCode eq '{code}'"},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        rows = resp.json().get("value", [])
        return bool(rows and rows[0].get("IndicatorName", "").strip())
    except requests.RequestException:
        return False
