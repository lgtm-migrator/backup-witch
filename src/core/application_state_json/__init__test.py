import json

import pytest

from src.core.application_state_json import ApplicationStateJson

test_object_key = "test-object"
test_object_value = "test-value"


def test_init_semantics(tmp_path):
    with pytest.raises(RuntimeError):
        ApplicationStateJson()
    state_save_file_path = tmp_path / "state.json"
    ApplicationStateJson.init(state_save_file_path.__str__())
    with pytest.raises(RuntimeError):
        ApplicationStateJson.init(state_save_file_path.__str__())


def test_clean_state(tmp_path):
    state_save_file_path = tmp_path / "state.json"
    assert state_save_file_path.exists() is False
    ApplicationStateJson.init(state_save_file_path.__str__())
    assert state_save_file_path.exists()
    assert state_save_file_path.read_text() == ""
    assert ApplicationStateJson.get(test_object_key, None) is None


def test_state_set(tmp_path):
    state_save_file_path = tmp_path / "state.json"
    ApplicationStateJson.init(state_save_file_path.__str__())
    ApplicationStateJson.set(test_object_key, test_object_value)
    assert ApplicationStateJson.get(test_object_key, None) == test_object_value
    assert state_save_file_path.read_text() == json.dumps(
        {test_object_key: test_object_value}
    )


def test_existing_state(tmp_path):
    state_save_file_path = tmp_path / "state.json"
    state_save_file_path.write_text(json.dumps({test_object_key: test_object_value}))
    ApplicationStateJson.init(state_save_file_path.__str__())
    assert ApplicationStateJson.get(test_object_key, None) == test_object_value
