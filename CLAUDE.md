# world-problems-digest

## Purpose
A weekly bot that fetches real statistics for Uzbekistan from three official
statistics APIs (World Bank, WHO GHO, UN SDG), picks the most reliable source
per field with plain code, asks Claude for up to 3 IT-solvable problems per
field, reviews the draft with a second Claude pass, builds a PDF report in
Russian, and sends it via Telegram.

## Stack
Python 3.12, `requests`, `anthropic` (model `claude-sonnet-5`), `reportlab`
(PDF), `pydantic` (structured LLM output), `pytest` (tests). No database - a
single `state.json` file tracks field rotation.

## How to run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your keys
export $(grep -v '^#' .env | xargs)   # or use direnv / python-dotenv manually

python main.py --dry-run   # saves PDF to output/, sends nothing
python main.py             # real run: sends the PDF to Telegram
pytest tests/              # unit tests, no network calls
```

## Standing rules
- Never invent numbers. All figures in the report must come from the fetched
  API data (`sources/`); the LLM prompts and reviewer pass exist specifically
  to enforce this - see `prompts/reviewer.md`.
- Never commit secrets. `.env` and `fonts/`/`output/` are gitignored; secrets
  live in GitHub Actions Secrets in CI.
- Do not add new dependencies without asking the user first.
- Keep code simple and commented - comment only the non-obvious "why", not
  the "what".
- Update `PROGRESS.md` after every finished step (what's done, what's next,
  open questions).

## See also
- `docs/SOURCES.md` - exact API endpoints, indicator codes, scoring rules.
- `PROGRESS.md` - current status and open questions.
- `README.md` - full beginner setup guide.
