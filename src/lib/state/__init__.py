from abc import abstractmethod
from typing import Any, Protocol


class State(Protocol):
    @abstractmethod
    def get(self, key: str, default_value: Any):
        pass

    @abstractmethod
    def set(self, key: str, value: str):
        pass
