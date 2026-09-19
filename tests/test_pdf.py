"""
Smoke test for the PDF builder: renders a page with Russian (Cyrillic) text
and checks the output isn't empty and has the embedded Unicode font.
Downloads the font on first run if not already cached in fonts/ (needs network).
"""
from pdf.builder import ReportSection, build_pdf
from llm.schemas import FieldAnalysis, ImprovementItem, ImprovementsOutput, Problem, Solution
from sources.common import IndicatorResult


def test_build_pdf_with_cyrillic_text(tmp_path):
    indicator = IndicatorResult(
        source="World Bank",
        code="TEST.CODE",
        label="Тестовый показатель",
        latest_value=50.0,
        latest_year=2024,
        previous_value=45.0,
        previous_year=2023,
        history_years=10,
        last_updated="2024-01-01",
        methodology_present=True,
        url="https://example.com",
    )
    problem = Problem(
        title="Пример проблемы",
        explanation="Простое объяснение по-русски, как для школьника.",
        solution_obvious=Solution(description="Простое решение", stack_and_apis="Python, requests", first_step_tonight="Открыть API и посмотреть данные"),
        solution_creative=Solution(description="Нестандартное решение", stack_and_apis="LLM + Telegram Bot API", first_step_tonight="Написать прототип бота"),
    )
    section = ReportSection(
        field_label="Здоровье",
        indicator=indicator,
        source_explanation="Источник выбран, потому что данные самые свежие и есть методология.",
        analysis=FieldAnalysis(problems=[problem]),
    )
    improvements = ImprovementsOutput(items=[ImprovementItem(title="Улучшение", description="Описание того, что можно улучшить.")])

    output_path = tmp_path / "test.pdf"
    build_pdf([section], improvements, "2026-09-19", output_path)

    assert output_path.exists()
    data = output_path.read_bytes()
    assert len(data) > 1000
    assert data.startswith(b"%PDF")
    assert b"DejaVuSans" in data  # confirms the Unicode font is embedded, not a fallback font
