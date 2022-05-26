import pytest

from src.core.application_state import ApplicationState


class ApplicationStateDummy(ApplicationState):
    @classmethod
    def init(cls, *args, **kwargs):
        pass

    @classmethod
    def set(cls, key: str, value: str):
        pass

    @classmethod
    def get(cls, key: str, default_value: None):
        pass


def test():
    with pytest.raises(RuntimeError):
        ApplicationStateDummy()
