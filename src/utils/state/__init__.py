from __future__ import annotations

import json
import subprocess
from typing import Final


class State:
    def __init__(self, save_file_path: str):
        self._save_file_path = save_file_path
        self.data: Final[dict] = self._load_state_from_file() or {}

    def update_state(self, key: str, value: str):
        self.data[key] = value
        self._save_state_to_file()

    def _load_state_from_file(self) -> dict | None:
        subprocess.run(f'touch -a {self._save_file_path}',  # todo switch to pathlib read_text, write_text
                       check=True,
                       shell=True)
        state_file_contents = subprocess.run(f'cat {self._save_file_path}',
                                             shell=True,
                                             check=True,
                                             text=True,
                                             stdout=subprocess.PIPE).stdout.strip()
        if not state_file_contents:
            return None
        return json.loads(state_file_contents)

    def _save_state_to_file(self):
        subprocess.run(f"echo '{json.dumps(self.data)}' > {self._save_file_path}",
                       shell=True,
                       check=True,
                       text=True)
