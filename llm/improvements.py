"""Generates the separate "What could be improved" section (no statistics, just UX)."""
from string import Template

import config
from llm.client import get_client
from llm.schemas import ImprovementsOutput

PROMPT_PATH = config.PROMPTS_DIR / "improvements.md"


def generate_improvements(field_labels: list[str]) -> ImprovementsOutput:
    template = Template(PROMPT_PATH.read_text(encoding="utf-8"))
    prompt = template.safe_substitute(
        REPORT_LANGUAGE=config.REPORT_LANGUAGE,
        COUNTRY_NAME=config.COUNTRY_NAME,
        FIELD_LABELS=", ".join(field_labels),
    )

    client = get_client()
    response = client.messages.parse(
        model=config.CLAUDE_MODEL,
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
        output_format=ImprovementsOutput,
    )
    return response.parsed_output
