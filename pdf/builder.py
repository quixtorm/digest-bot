"""
Builds the weekly A4 PDF report with reportlab (pure Python, no system packages
needed - works on GitHub Actions). Uses an embedded Unicode font so Russian
(Cyrillic) text renders correctly.
"""
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

import config
from llm.schemas import FieldAnalysis, ImprovementsOutput
from pdf.fonts import FONT_NAME, FONT_NAME_BOLD, ensure_fonts_registered
from sources.common import IndicatorResult


@dataclass
class ReportSection:
    field_label: str
    indicator: IndicatorResult
    source_explanation: str
    analysis: FieldAnalysis


def _styles() -> dict[str, ParagraphStyle]:
    return {
        "title": ParagraphStyle("title", fontName=FONT_NAME_BOLD, fontSize=20, leading=24, spaceAfter=10),
        "subtitle": ParagraphStyle("subtitle", fontName=FONT_NAME, fontSize=12, leading=16, spaceAfter=14, textColor="#444444"),
        "h1": ParagraphStyle("h1", fontName=FONT_NAME_BOLD, fontSize=16, leading=20, spaceBefore=18, spaceAfter=8),
        "h2": ParagraphStyle("h2", fontName=FONT_NAME_BOLD, fontSize=13, leading=17, spaceBefore=12, spaceAfter=4),
        "body": ParagraphStyle("body", fontName=FONT_NAME, fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=6),
        "data": ParagraphStyle("data", fontName=FONT_NAME, fontSize=11, leading=15, spaceAfter=6),
        "small": ParagraphStyle("small", fontName=FONT_NAME, fontSize=11, leading=14, textColor="#555555", spaceAfter=8),
        "bullet": ParagraphStyle("bullet", fontName=FONT_NAME, fontSize=11, leading=15, leftIndent=12, spaceAfter=4),
    }


def _summary_line(section: ReportSection) -> str:
    ind = section.indicator
    if ind.change is None:
        trend = f"{ind.latest_value:.1f} ({ind.latest_year})"
    else:
        arrow = "↑" if ind.change > 0 else ("↓" if ind.change < 0 else "→")
        trend = f"{ind.latest_value:.1f} {arrow} (было {ind.previous_value:.1f} в {ind.previous_year}, сейчас {ind.latest_year})"
    return f"<b>{section.field_label}</b>: {ind.label} - {trend}"


def _indicator_block(indicator: IndicatorResult) -> str:
    change_str = "нет данных"
    if indicator.change is not None:
        sign = "+" if indicator.change >= 0 else ""
        change_str = f"{sign}{indicator.change:.2f}"
    prev = f"{indicator.previous_value:.2f} ({indicator.previous_year})" if indicator.previous_value is not None else "нет данных"
    return (
        f"<b>{indicator.label}</b><br/>"
        f"Текущее значение: {indicator.latest_value:.2f} - данные за {indicator.latest_year} год.<br/>"
        f"Предыдущее значение: {prev}. Изменение: {change_str}.<br/>"
        f"Источник: {indicator.source} ({indicator.code}). "
        f"<link href='{indicator.url}'>{indicator.url}</link>"
    )


def build_pdf(sections: list[ReportSection], improvements: ImprovementsOutput, generated_date: str, output_path: Path) -> None:
    ensure_fonts_registered()
    styles = _styles()

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        title="World Problems Digest",
    )

    story = []

    # --- First page: title + short summary -----------------------------
    story.append(Paragraph("World Problems Digest", styles["title"]))
    story.append(Paragraph(f"Еженедельный отчёт - {generated_date}", styles["subtitle"]))
    story.append(Paragraph("Кратко за эту неделю:", styles["h2"]))
    for section in sections:
        story.append(Paragraph(_summary_line(section), styles["bullet"]))
    story.append(Spacer(1, 10))

    # --- One section per field ------------------------------------------
    for section in sections:
        story.append(Paragraph(section.field_label, styles["h1"]))
        story.append(Paragraph("Почему выбран этот источник данных", styles["h2"]))
        for line in section.source_explanation.split("\n"):
            story.append(Paragraph(line, styles["small"]))
        story.append(Paragraph("Данные", styles["h2"]))
        story.append(Paragraph(_indicator_block(section.indicator), styles["data"]))

        if section.analysis.problems:
            story.append(Paragraph("Проблемы, которые можно решить с помощью IT", styles["h2"]))
        for i, problem in enumerate(section.analysis.problems, start=1):
            story.append(Paragraph(f"{i}. {problem.title}", styles["h2"]))
            story.append(Paragraph(problem.explanation, styles["body"]))
            story.append(Paragraph(
                f"<b>Решение 1 (простое):</b> {problem.solution_obvious.description}<br/>"
                f"Стек/API: {problem.solution_obvious.stack_and_apis}<br/>"
                f"Первый шаг сегодня вечером: {problem.solution_obvious.first_step_tonight}",
                styles["body"],
            ))
            story.append(Paragraph(
                f"<b>Решение 2 (нестандартное):</b> {problem.solution_creative.description}<br/>"
                f"Стек/API: {problem.solution_creative.stack_and_apis}<br/>"
                f"Первый шаг сегодня вечером: {problem.solution_creative.first_step_tonight}",
                styles["body"],
            ))

    # --- Improvements section --------------------------------------------
    if improvements.items:
        story.append(Paragraph("Что можно улучшить", styles["h1"]))
        for item in improvements.items:
            story.append(Paragraph(item.title, styles["h2"]))
            story.append(Paragraph(item.description, styles["body"]))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story)
