# Progress

## Done
- [x] Verified all three APIs respond with real Uzbekistan data (World Bank,
      WHO GHO, and UN SDG - found and documented the correct SDG endpoint,
      `Series/Data`, since `Indicator/PageOfData` 404s).
- [x] Project structure, `config.py`, `state.py` (rotation).
- [x] Source modules: `sources/worldbank.py`, `sources/who_gho.py`,
      `sources/un_sdg.py`, `sources/common.py` (shared `IndicatorResult`).
- [x] `sources/registry.py` - field -> indicator map, all codes verified
      against live Uzbekistan data before being added.
- [x] `sources/scoring.py` - plain-code reliability scoring + explanation text.
- [x] LLM passes: `llm/analyst.py`, `llm/reviewer.py`, `llm/improvements.py`,
      using `client.messages.parse()` with Pydantic schemas (`llm/schemas.py`)
      for reliable structured output.
- [x] Prompts as editable markdown: `prompts/analyst.md`, `prompts/reviewer.md`,
      `prompts/improvements.md`.
- [x] PDF builder: `pdf/builder.py` + `pdf/fonts.py` (downloads DejaVu Sans on
      first run for Cyrillic support).
- [x] Telegram sender: `telegram/send.py`.
- [x] `main.py` orchestrator with `--dry-run`.
- [x] Unit tests: `tests/test_scoring.py`, `tests/test_state.py`,
      `tests/test_registry.py` (no network calls).
- [x] GitHub Actions workflow (`.github/workflows/weekly.yml`), cron +
      `workflow_dispatch`, commits `state.json` back after a run.
- [x] Docs: `CLAUDE.md`, `docs/SOURCES.md`, `README.md`, `.env.example`,
      `.gitignore`.

- [x] Ran `python main.py --dry-run` with a real `ANTHROPIC_API_KEY` (health +
      education fields) - inspected the 6-page PDF page by page: correct
      sourced numbers, Cyrillic renders cleanly, realistic problems/solutions.
      Had to raise `max_tokens` from 4000 to 8000 on the analyst/reviewer
      calls - the first attempt truncated mid-JSON.
- [x] Created the Telegram bot (@digest_quixy_bot) via @BotFather, found the
      chat_id via `getUpdates`, and sent the reviewed PDF for real - delivered
      successfully.

## Next
- [ ] Add the three secrets (`ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`,
      `TELEGRAM_CHAT_ID`) to GitHub Actions and trigger `workflow_dispatch`
      once to confirm the end-to-end flow there too, including the
      `state.json` auto-commit step.
- [ ] Consider whether `max_tokens=8000` is comfortably enough headroom once
      real reports regularly produce 3 problems per field (so far only tested
      with fields that produced 2-3).

## Open questions
- Some World Bank/SDG indicator codes in `docs/SOURCES.md` were chosen as the
  best available proxy for a field (e.g. maternal mortality for `health`'s SDG
  candidate) - reasonable, but worth a look if a field's report reads oddly.
- `state.json` is updated by the GitHub Actions workflow committing directly
  back to the repo (simplest option, no extra infrastructure). If that's not
  desired, an alternative (Actions cache, a gist, a tiny external store) would
  need to replace the `git commit && git push` step in `weekly.yml`.
