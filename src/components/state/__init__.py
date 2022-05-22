from __future__ import annotations

import json
from pathlib import Path
from typing import Final


class State:
    def __init__(self, save_file_path: str):
        self._save_file_path = Path(save_file_path)
        self.data: Final[dict] = self._load_state_from_file() or {}

    def update_state(self, key: str, value: str):
        self.data[key] = value
        self._save_state_to_file()

    def _load_state_from_file(self) -> dict | None:
        self._save_file_path.touch(exist_ok=True)
        if state_file_contents := self._save_file_path.read_text():
            return json.loads(state_file_contents)
        else:
            return None

    def _save_state_to_file(self):
        self._save_file_path.write_text(json.dumps(self.data))
