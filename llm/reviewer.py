"""Second LLM pass: drops unrealistic solutions and any figure not present in the API data."""
from string import Template

import config
from llm.analyst import format_data_block
from llm.client import get_client
from llm.schemas import FieldAnalysis, ImprovementsOutput
from sources.common import IndicatorResult

PROMPT_PATH = config.PROMPTS_DIR / "reviewer.md"


def review_field_analysis(field_label: str, indicator: IndicatorResult, draft: FieldAnalysis) -> FieldAnalysis:
    template = Template(PROMPT_PATH.read_text(encoding="utf-8"))
    prompt = template.safe_substitute(
        REPORT_LANGUAGE=config.REPORT_LANGUAGE,
        COUNTRY_NAME=config.COUNTRY_NAME,
        DATA_BLOCK=format_data_block(indicator),
        DRAFT_JSON=draft.model_dump_json(indent=2),
    )

    client = get_client()
    response = client.messages.parse(
        model=config.CLAUDE_MODEL,
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
        output_format=FieldAnalysis,
    )
    return response.parsed_output


def review_improvements(draft: ImprovementsOutput) -> ImprovementsOutput:
    """Realism-only pass for the 'What could be improved' section (no numeric claims to check)."""
    template = Template(PROMPT_PATH.read_text(encoding="utf-8"))
    prompt = template.safe_substitute(
        REPORT_LANGUAGE=config.REPORT_LANGUAGE,
        COUNTRY_NAME=config.COUNTRY_NAME,
        DATA_BLOCK="(this section does not cite statistics, so there are no numbers to check)",
        DRAFT_JSON=draft.model_dump_json(indent=2),
    )

    client = get_client()
    response = client.messages.parse(
        model=config.CLAUDE_MODEL,
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
        output_format=ImprovementsOutput,
    )
    return response.parsed_output
