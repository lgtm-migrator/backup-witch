from abc import ABC, abstractmethod


class ApplicationStateProvider(ABC):
    @abstractmethod
    def load_state(self, default: dict) -> dict:
        pass

    @abstractmethod
    def save_state(self, state: dict) -> None:
        pass
