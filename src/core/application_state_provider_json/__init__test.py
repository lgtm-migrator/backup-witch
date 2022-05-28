import json

from src.core.application_state_provider_json import ApplicationStateProviderJSON

test_state = {"test_object_key": "test-object", "test_object_value": "test-value"}


def test_clean_state(tmp_path):
    json_file = tmp_path / "state.json"
    state_provider = ApplicationStateProviderJSON(json_file.__str__())
    assert state_provider.load_state({}) == {}
    assert json_file.exists()
    assert json_file.read_text() == ""


def test_existing_state(tmp_path):
    json_file = tmp_path / "state.json"
    json_file.write_text(json.dumps(test_state))
    state_provider = ApplicationStateProviderJSON(json_file.__str__())
    assert state_provider.load_state({}) == test_state


def test_state_save(tmp_path):
    json_file = tmp_path / "state.json"
    state_provider = ApplicationStateProviderJSON(json_file.__str__())
    assert json_file.read_text() == ""
    state_provider.save_state(test_state)
    assert json_file.read_text() == json.dumps(test_state)
    assert state_provider.load_state({}) == test_state
