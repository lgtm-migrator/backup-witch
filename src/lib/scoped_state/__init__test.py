from src.lib.application_state import ApplicationState
from src.lib.json_application_state_provider import JSONApplicationStateProvider
from src.lib.scoped_state import ScopedState


def test(tmp_path):
    state_save_file_path = tmp_path / "state.json"
    application_state = ApplicationState(
        JSONApplicationStateProvider(state_save_file_path.__str__())
    )
    key_prefix = "test-key-prefix:"
    service_state = ScopedState(application_state, key_prefix)
    new_object_key = "test-object"
    new_object_value = "test-value"
    service_state.set(new_object_key, new_object_value)
    received_value = service_state.get(new_object_key, None)
    assert received_value is not None
    assert received_value == application_state.get(key_prefix + new_object_key, None)
