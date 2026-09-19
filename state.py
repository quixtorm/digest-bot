"""
Tracks which pair of fields is due this week (state.json), so each run
picks the next pair in rotation instead of repeating the same fields.
"""
import json

import config

NUM_PAIRS = len(config.FIELDS) // 2  # 4 pairs out of 8 fields


def load_rotation_index() -> int:
    """Return the current rotation index (0..NUM_PAIRS-1), defaulting to 0."""
    if not config.STATE_FILE.exists():
        return 0
    with open(config.STATE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("rotation_index", 0) % NUM_PAIRS


def save_rotation_index(index: int) -> None:
    """Persist the next rotation index to state.json."""
    with open(config.STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"rotation_index": index % NUM_PAIRS}, f, ensure_ascii=False, indent=2)


def fields_for_this_week(advance: bool = True) -> list[str]:
    """
    Return the two field names due this week, based on the current rotation
    index. If advance=True, also saves the incremented index for next week.
    """
    index = load_rotation_index()
    pair = config.FIELDS[index * 2 : index * 2 + 2]
    if advance:
        save_rotation_index(index + 1)
    return pair
