"""Sends the finished PDF via the Telegram Bot API (sendDocument)."""
from pathlib import Path

import requests

import config

TIMEOUT = 60


def send_pdf(pdf_path: Path, caption: str = "") -> None:
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        raise RuntimeError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in the environment")

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendDocument"
    with open(pdf_path, "rb") as f:
        files = {"document": (pdf_path.name, f, "application/pdf")}
        data = {"chat_id": config.TELEGRAM_CHAT_ID, "caption": caption}
        resp = requests.post(url, data=data, files=files, timeout=TIMEOUT)

    resp.raise_for_status()
    result = resp.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API returned an error: {result}")
