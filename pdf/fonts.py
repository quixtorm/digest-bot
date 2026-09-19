"""
Ensures a Unicode TTF font (DejaVu Sans, covers Cyrillic) is available locally
so the PDF can render Russian text correctly, and registers it with reportlab.
The font files are not committed to git (see .gitignore) - they are downloaded
once and cached in fonts/.
"""
import requests
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import config

TIMEOUT = 30
FONT_NAME = "DejaVuSans"
FONT_NAME_BOLD = "DejaVuSans-Bold"


def _download_if_missing(path, url) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, timeout=TIMEOUT)
    resp.raise_for_status()
    path.write_bytes(resp.content)


def ensure_fonts_registered() -> None:
    """Download the font files if needed, then register them with reportlab."""
    _download_if_missing(config.FONT_REGULAR_PATH, config.FONT_REGULAR_URL)
    _download_if_missing(config.FONT_BOLD_PATH, config.FONT_BOLD_URL)

    pdfmetrics.registerFont(TTFont(FONT_NAME, str(config.FONT_REGULAR_PATH)))
    pdfmetrics.registerFont(TTFont(FONT_NAME_BOLD, str(config.FONT_BOLD_PATH)))
