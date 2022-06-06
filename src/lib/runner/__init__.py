from abc import abstractmethod
from typing import Callable, Protocol


class Runner(Protocol):
    @abstractmethod
    async def __call__(self, operation: Callable[[], None]):
        pass
