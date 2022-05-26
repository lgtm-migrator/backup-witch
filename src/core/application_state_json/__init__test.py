import json

from src.core.application_state_json import ApplicationStateJson

test_object_key = "test-object"
test_object_value = "test-value"


def test_clean_state(tmp_path):
    state_save_file_path = tmp_path / "state.json"
    ApplicationStateJson.init(state_save_file_path.__str__())
    assert state_save_file_path.exists()
    assert state_save_file_path.read_text() == ""
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
