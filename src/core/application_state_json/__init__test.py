import json

import pytest

from src.core.application_state_json import ApplicationStateJson


def test(tmp_path):
    with pytest.raises(RuntimeError):
        ApplicationStateJson()
    state_save_file_path = tmp_path / "state.json"
    ApplicationStateJson.init(state_save_file_path.__str__())
    with pytest.raises(RuntimeError):
        ApplicationStateJson.init(state_save_file_path.__str__())
    assert state_save_file_path.exists()
    assert state_save_file_path.read_text() == ""
    new_object_key = "test-object"
    new_object_value = "test-value"
    ApplicationStateJson.set(new_object_key, new_object_value)
    assert ApplicationStateJson.get(new_object_key, None) == new_object_value
    assert state_save_file_path.read_text() == json.dumps(
        {new_object_key: new_object_value}
    )
