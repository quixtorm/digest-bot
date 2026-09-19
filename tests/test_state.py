import config
import state


def test_rotation_cycles_through_all_pairs(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "STATE_FILE", tmp_path / "state.json")

    seen_pairs = []
    for _ in range(config.NUM_PAIRS if hasattr(config, "NUM_PAIRS") else state.NUM_PAIRS):
        seen_pairs.append(tuple(state.fields_for_this_week(advance=True)))

    # Every pair of fields should be distinct, and together cover all 8 fields exactly once each.
    all_fields = [f for pair in seen_pairs for f in pair]
    assert sorted(all_fields) == sorted(config.FIELDS)
    assert len(set(seen_pairs)) == state.NUM_PAIRS


def test_rotation_wraps_around(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "STATE_FILE", tmp_path / "state.json")

    first_cycle = [tuple(state.fields_for_this_week(advance=True)) for _ in range(state.NUM_PAIRS)]
    second_cycle = [tuple(state.fields_for_this_week(advance=True)) for _ in range(state.NUM_PAIRS)]
    assert first_cycle == second_cycle


def test_advance_false_does_not_persist(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "STATE_FILE", tmp_path / "state.json")

    first = state.fields_for_this_week(advance=False)
    second = state.fields_for_this_week(advance=False)
    assert first == second
