"""World Bank Indicators API (api.worldbank.org/v2). No API key required."""
import requests

import config
from sources.common import IndicatorResult

BASE_URL = "https://api.worldbank.org/v2"
TIMEOUT = 20


def fetch_indicator(code: str, label: str, country: str = config.COUNTRY_ISO3) -> IndicatorResult | None:
    """
    Fetch the latest and previous non-null values for a World Bank indicator.
    Returns None if the country has no usable data for this indicator.
    """
    url = f"{BASE_URL}/country/{country}/indicator/{code}"
    resp = requests.get(url, params={"format": "json", "per_page": 100}, timeout=TIMEOUT)
    resp.raise_for_status()
    payload = resp.json()
    if len(payload) < 2 or not payload[1]:
        return None

    rows = payload[1]  # already sorted newest-year-first by the API
    non_null = [r for r in rows if r.get("value") is not None]
    if not non_null:
        return None

    latest = non_null[0]
    previous = non_null[1] if len(non_null) > 1 else None
    last_updated = payload[0].get("lastupdated", "")

    methodology_present = _has_methodology(code)

    return IndicatorResult(
        source="World Bank",
        code=code,
        label=label,
        latest_value=latest["value"],
        latest_year=int(latest["date"]),
        previous_value=previous["value"] if previous else None,
        previous_year=int(previous["date"]) if previous else None,
        history_years=len(non_null),
        last_updated=last_updated,
        methodology_present=methodology_present,
        url=f"https://data.worldbank.org/indicator/{code}?locations={config.COUNTRY_ISO2}",
    )


def _has_methodology(code: str) -> bool:
    """Check whether World Bank publishes a source note (methodology) for this indicator."""
    try:
        resp = requests.get(f"{BASE_URL}/indicator/{code}", params={"format": "json"}, timeout=TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()
        if len(payload) < 2 or not payload[1]:
            return False
        note = payload[1][0].get("sourceNote", "")
        return bool(note and note.strip())
    except requests.RequestException:
        return False
