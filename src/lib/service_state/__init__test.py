from src.lib.application_state import ApplicationState
from src.lib.application_state_provider_json import ApplicationStateProviderJSON
from src.lib.service_state import ServiceState


def test(tmp_path):
    state_save_file_path = tmp_path / "state.json"
    application_state = ApplicationState(
        ApplicationStateProviderJSON(state_save_file_path.__str__())
    )
    key_prefix = "test-key-prefix:"
    service_state = ServiceState(application_state, key_prefix)
    new_object_key = "test-object"
    new_object_value = "test-value"
    service_state.set(new_object_key, new_object_value)
    received_value = service_state.get(new_object_key, None)
    assert received_value is not None
    assert received_value == application_state.get(key_prefix + new_object_key, None)
