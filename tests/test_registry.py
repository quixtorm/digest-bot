import config
from sources.registry import FIELD_INDICATORS


def test_every_field_has_candidates():
    for field in config.FIELDS:
        assert field in FIELD_INDICATORS, f"missing registry entry for field '{field}'"
        assert len(FIELD_INDICATORS[field]) > 0, f"no candidate indicators for field '{field}'"


def test_every_candidate_has_required_keys():
    for field, candidates in FIELD_INDICATORS.items():
        for candidate in candidates:
            assert callable(candidate["fetch"]), f"'fetch' must be callable for {field}"
            assert candidate["code"], f"missing code for {field}"
            assert candidate["label"], f"missing label for {field}"


def test_every_field_has_a_russian_label():
    for field in config.FIELDS:
        assert field in config.FIELD_LABELS_RU, f"missing Russian label for field '{field}'"
