from __future__ import annotations

from typing import Any

from src.lib.application_state_provider import ApplicationStateProvider


class ApplicationState:
    def __init__(self, provider: ApplicationStateProvider):
        self._provider = provider
        self._data = provider.load_state({})

    def set(self, key: str, value: str):
        self._data[key] = value
        self._provider.save_state(self._data)

    def get(self, key: str, default_value: Any):
        return self._data.get(key, default_value)
