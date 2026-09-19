"""First LLM pass: turns real fetched statistics into up to 3 IT-solvable problems."""
from string import Template

import config
from llm.client import get_client
from llm.schemas import FieldAnalysis
from sources.common import IndicatorResult

PROMPT_PATH = config.PROMPTS_DIR / "analyst.md"


def format_data_block(indicator: IndicatorResult) -> str:
    """Render the verified numbers exactly as the LLM is allowed to cite them."""
    change_str = "n/a"
    if indicator.change is not None:
        sign = "+" if indicator.change >= 0 else ""
        change_str = f"{sign}{indicator.change:.2f} (vs {indicator.previous_year})"
    return (
        f"- Indicator: {indicator.label}\n"
        f"- Source: {indicator.source} ({indicator.code})\n"
        f"- Latest value: {indicator.latest_value:.2f}, year {indicator.latest_year}\n"
        f"- Previous value: "
        + (f"{indicator.previous_value:.2f}, year {indicator.previous_year}" if indicator.previous_value is not None else "n/a")
        + "\n"
        f"- Change: {change_str}\n"
        f"- Source link: {indicator.url}\n"
    )


def analyze_field(field_label: str, indicator: IndicatorResult) -> FieldAnalysis:
    template = Template(PROMPT_PATH.read_text(encoding="utf-8"))
    prompt = template.safe_substitute(
        REPORT_LANGUAGE=config.REPORT_LANGUAGE,
        FIELD_LABEL=field_label,
        COUNTRY_NAME=config.COUNTRY_NAME,
        DATA_BLOCK=format_data_block(indicator),
        MAX_PROBLEMS=str(config.MAX_PROBLEMS_PER_FIELD),
    )

    client = get_client()
    response = client.messages.parse(
        model=config.CLAUDE_MODEL,
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
        output_format=FieldAnalysis,
    )
    return response.parsed_output
