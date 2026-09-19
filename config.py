"""
Central configuration for world-problems-digest.
Change values here rather than scattering constants through the code.
"""
import os
from pathlib import Path

# --- Report language -------------------------------------------------------
# Every prompt and PDF section is written in this language.
REPORT_LANGUAGE = "Russian"

# --- Country used for all indicator numbers ---------------------------------
COUNTRY_NAME = "Uzbekistan"
COUNTRY_ISO2 = "UZ"        # World Bank country code
COUNTRY_ISO3 = "UZB"       # World Bank / WHO GHO SpatialDim code
COUNTRY_SDG_AREA_CODE = "860"  # UN SDG geoAreaCode for Uzbekistan

# --- Claude API ---------------------------------------------------------
CLAUDE_MODEL = "claude-sonnet-5"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# --- Telegram -------------------------------------------------------------
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# --- The 8 rotating fields, in fixed order -------------------------------
# The order here defines the rotation pairs: (0,1), (2,3), (4,5), (6,7).
FIELDS = [
    "health",
    "education",
    "climate and energy",
    "water and food",
    "poverty and finance",
    "internet access",
    "urban environment",
    "labor market",
]

# Russian labels for the field names, used in the report itself.
FIELD_LABELS_RU = {
    "health": "Здоровье",
    "education": "Образование",
    "climate and energy": "Климат и энергия",
    "water and food": "Вода и питание",
    "poverty and finance": "Бедность и финансы",
    "internet access": "Доступ в интернет",
    "urban environment": "Городская среда",
    "labor market": "Рынок труда",
}

# --- Paths ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
STATE_FILE = BASE_DIR / "state.json"
FONTS_DIR = BASE_DIR / "fonts"
OUTPUT_DIR = BASE_DIR / "output"
PROMPTS_DIR = BASE_DIR / "prompts"

# --- Fonts (downloaded on first run if missing, see pdf/fonts.py) ----------
FONT_REGULAR_PATH = FONTS_DIR / "DejaVuSans.ttf"
FONT_BOLD_PATH = FONTS_DIR / "DejaVuSans-Bold.ttf"
FONT_REGULAR_URL = (
    "https://raw.githubusercontent.com/senotrusov/dejavu-fonts-ttf/master/ttf/DejaVuSans.ttf"
)
FONT_BOLD_URL = (
    "https://raw.githubusercontent.com/senotrusov/dejavu-fonts-ttf/master/ttf/DejaVuSans-Bold.ttf"
)

# How many problems the analyst LLM should propose per field (task says "up to 3").
MAX_PROBLEMS_PER_FIELD = 3
