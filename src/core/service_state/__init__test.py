from src.core.application_state_json import ApplicationStateJson
from src.core.service_state import ServiceState


def test(tmp_path):
    state_save_file_path = tmp_path / "state.json"
    ApplicationStateJson.init(state_save_file_path.__str__())
    key_prefix = "test-key-prefix:"
    service_state = ServiceState(ApplicationStateJson, key_prefix)
    new_object_key = "test-object"
    new_object_value = "test-value"
    service_state.set(new_object_key, new_object_value)
    received_value = service_state.get(new_object_key, None)
    assert received_value is not None
    assert received_value == ApplicationStateJson.get(key_prefix + new_object_key, None)
