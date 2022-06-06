from typing import Any

from src.lib.state import State


class ScopedState(State):
    def __init__(self, state: State, scope: str):
        self._state = state
        self._scope = scope

    def get(self, key: str, default_value: Any):
        return self._state.get(self._scope + key, default_value)

    def set(self, key: str, value: str):
        self._state.set(self._scope + key, value)
