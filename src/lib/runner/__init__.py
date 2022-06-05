from abc import abstractmethod
from typing import Protocol, Callable


class Runner(Protocol):
    @abstractmethod
    async def __call__(self, operation: Callable[[], None]):
        pass
