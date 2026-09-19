#!/usr/bin/env python3
"""
World Problems Digest - weekly bot.

Picks this week's 2 fields (rotation), fetches real statistics from official
APIs, picks the most reliable source per field with plain code (no LLM),
asks Claude for IT-solvable problems, reviews the draft with a second Claude
pass, builds a PDF, and sends it over Telegram.

Usage:
    python main.py               # real run: sends the PDF to Telegram
    python main.py --dry-run     # saves the PDF to output/ and sends nothing
"""
import argparse
import sys
from datetime import date

import config
import state
from llm.analyst import analyze_field
from llm.improvements import generate_improvements
from llm.reviewer import review_field_analysis, review_improvements
from pdf.builder import ReportSection, build_pdf
from sources.registry import FIELD_INDICATORS
from sources.scoring import explain_winner, pick_best_source
from telegram.send import send_pdf


def build_report_section(field_key: str) -> ReportSection:
    field_label = config.FIELD_LABELS_RU[field_key]
    candidates = FIELD_INDICATORS[field_key]

    winner, all_scored = pick_best_source(field_key, candidates)
    explanation = explain_winner(field_key, winner, all_scored)
    print(f"\n[{field_label}] {explanation}")

    draft = analyze_field(field_label, winner.result)
    reviewed = review_field_analysis(field_label, winner.result, draft)

    return ReportSection(
        field_label=field_label,
        indicator=winner.result,
        source_explanation=explanation,
        analysis=reviewed,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="World Problems Digest weekly bot")
    parser.add_argument("--dry-run", action="store_true", help="Save the PDF locally instead of sending it to Telegram")
    args = parser.parse_args()

    this_week_fields = state.fields_for_this_week(advance=True)
    print(f"This week's fields: {this_week_fields}")

    sections = [build_report_section(field_key) for field_key in this_week_fields]

    field_labels = [s.field_label for s in sections]
    improvements_draft = generate_improvements(field_labels)
    improvements = review_improvements(improvements_draft)

    generated_date = date.today().isoformat()
    output_path = config.OUTPUT_DIR / f"world-problems-digest-{generated_date}.pdf"
    build_pdf(sections, improvements, generated_date, output_path)
    print(f"\nPDF built: {output_path}")

    if args.dry_run:
        print("Dry run: not sending to Telegram.")
    else:
        caption = f"World Problems Digest - {generated_date}"
        send_pdf(output_path, caption=caption)
        print("Sent to Telegram.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
