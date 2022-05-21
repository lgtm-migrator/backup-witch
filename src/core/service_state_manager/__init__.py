from src.core.state import State


class ServiceStateManager:
    def __init__(self,
                 state: State,
                 key_prefix: str):
        self._state = state
        self._key_prefix = key_prefix

    def get(self, key: str, default_value):
        return self._state.data.get(self._key_prefix + key, default_value)

    def set(self, key: str, value: str):
        self._state.update_state(self._key_prefix + key, value)
