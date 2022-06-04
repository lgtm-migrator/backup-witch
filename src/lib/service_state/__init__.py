from src.lib.application_state import ApplicationState


class ServiceState:
    def __init__(self, application_state: ApplicationState, key_prefix: str):
        self._application_state = application_state
        self._key_prefix = key_prefix

    def get(self, key: str, default_value):
        return self._application_state.get(self._key_prefix + key, default_value)

    def set(self, key: str, value: str):
        self._application_state.set(self._key_prefix + key, value)
