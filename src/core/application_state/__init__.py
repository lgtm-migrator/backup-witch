from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, final


class ApplicationState(ABC):
    @final
    def __init__(self):
        raise RuntimeError("ApplicationState can't be instanced")

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
