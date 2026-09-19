"""Thin wrapper around the Anthropic SDK so the rest of the code doesn't import it directly."""
import anthropic

import config


def get_client() -> anthropic.Anthropic:
    api_key = config.ANTHROPIC_API_KEY or None  # None lets the SDK resolve from env itself
    return anthropic.Anthropic(api_key=api_key)
