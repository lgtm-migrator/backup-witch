from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ApplicationState(ABC):
    @classmethod
    @abstractmethod
    def init(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def set(cls, key: str, value: str):
        pass

    @classmethod
    @abstractmethod
    def get(cls, key: str, default_value: Any):
        pass
