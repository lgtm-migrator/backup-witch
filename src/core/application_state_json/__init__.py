from __future__ import annotations

import json
from pathlib import Path
from typing import final, Any

from src.core.application_state import ApplicationState


@final
class ApplicationStateJson(ApplicationState):
    __save_file_path: Path
    __data: dict
    __initialized: bool = False

    def __init__(self):
        raise RuntimeError('ApplicationState can\'t be instanced')

    @classmethod
    def init(cls, save_file_path: str):
        if cls.__initialized:
            raise RuntimeError('ApplicationState is already initialized')
        cls.__save_file_path = Path(save_file_path)
        cls.__data = cls._load_state_from_file() or {}
        cls.__initialized = True

    @classmethod
    def set(cls, key: str, value: str):
        cls.__data[key] = value
        cls._save_state_to_file()

    @classmethod
    def get(cls, key: str, default_value: Any):
        return cls.__data.get(key, default_value)

    @classmethod
    def _load_state_from_file(cls) -> dict | None:
        cls.__save_file_path.touch(exist_ok=True)
        if state_file_contents := cls.__save_file_path.read_text():
            return json.loads(state_file_contents)
        else:
            return None

    @classmethod
    def _save_state_to_file(cls):
        cls.__save_file_path.write_text(
            json.dumps(cls.__data)
        )
