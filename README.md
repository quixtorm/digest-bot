# World Problems Digest

A weekly bot that sends you a PDF report on Telegram. Each week it covers 2 of
8 topics (health, education, climate & energy, water & food, poverty &
finance, internet access, urban environment, labor market), rotating so all 8
get covered every 4 weeks. It uses only real numbers from three official
statistics APIs (World Bank, WHO, UN SDG), then asks Claude to suggest
IT-solvable problems and realistic solutions for each one.

This guide assumes Ubuntu/WSL and a terminal (bash).

## 1. Get the code running locally

```bash
cd world-problems-digest
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Create your `.env` file

```bash
cp .env.example .env
```

Open `.env` in an editor and you'll see three empty variables to fill in:
`ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

### Getting an Anthropic API key
Sign in at https://console.anthropic.com, create an API key, and paste it as
`ANTHROPIC_API_KEY`.

### Creating a Telegram bot with @BotFather
1. Open Telegram, search for **@BotFather**, and start a chat.
2. Send `/newbot` and follow the prompts (choose a name and a username ending
   in `bot`).
3. BotFather replies with a token like `123456789:AAExample-Token`. Put that
   in `TELEGRAM_BOT_TOKEN`.

### Finding your chat_id
The bot can only message you after you've messaged it first.
1. Search for your new bot in Telegram (by the username you gave it) and send
   it any message, e.g. `/start`.
2. In your browser, open:
   `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   (replace `<YOUR_BOT_TOKEN>` with your real token).
3. Look for `"chat":{"id":123456789,...}` in the JSON response - that number
   is your `TELEGRAM_CHAT_ID`.
4. If you don't see anything, make sure you sent the bot a message first, then
   refresh the URL.

## 3. Load the `.env` file into your shell

```bash
export $(grep -v '^#' .env | xargs)
```
(Run this in every new terminal session before running the bot locally - or
use a tool like `direnv` if you prefer.)

## 4. Try a dry run

This fetches real data, calls Claude, builds a PDF, but does **not** send
anything to Telegram - the PDF is saved in `output/` instead:

```bash
python main.py --dry-run
```

Open the PDF (e.g. `output/world-problems-digest-2026-09-19.pdf`) and check
it looks right - especially that Russian text displays correctly.

## 5. Run the tests

```bash
pytest tests/
```
These don't call the network or the LLM - they check the rotation logic, the
reliability scoring, and that every field has indicators registered.

## 6. Send a real report

```bash
python main.py
```
This does everything the dry run does, plus sends the PDF to your
`TELEGRAM_CHAT_ID` via the bot.

## 7. Automate it weekly with GitHub Actions

1. Push this repository to GitHub.
2. In the repo, go to **Settings -> Secrets and variables -> Actions -> New
   repository secret**, and add all three:
   - `ANTHROPIC_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. That's it - `.github/workflows/weekly.yml` runs every Monday at 08:00
   Tashkent time. You can also trigger it manually any time from the
   **Actions** tab -> **Weekly digest** -> **Run workflow**.

The workflow commits the updated `state.json` (which field pair is next) back
to the repository after each successful run, so the rotation persists between
runs without needing a database.

## Project layout

See `CLAUDE.md` for a quick orientation and `docs/SOURCES.md` for exactly
which API endpoints and indicator codes are used, and how to add a new field.
The three LLM prompts live as plain markdown in `prompts/` - edit the wording
there without touching any Python code.
