from __future__ import annotations

import json
from pathlib import Path

from src.lib.application_state_provider import ApplicationStateProvider


class ApplicationStateProviderJSON(ApplicationStateProvider):
    def __init__(self, json_file_path: str):
        self._json_file_path = Path(json_file_path)
        self._json_file_path.touch(exist_ok=True)

    def load_state(self, default: dict) -> dict:
        if state_file_contents := self._json_file_path.read_text():
            return json.loads(state_file_contents)
        return default

    def save_state(self, state: dict):
        self._json_file_path.write_text(json.dumps(state))
