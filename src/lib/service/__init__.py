from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from src.lib.runner import Runner


class Service(ABC):
    def __init__(self, runner: Runner):
        self._runner = runner
        self._running = False

    @final
    async def run(self) -> None:
        if self._running:
            raise RuntimeError(f"{self.__class__} is already running")
        try:
            self._running = True
            await self._runner(self._body)
        finally:
            self._running = False

    @abstractmethod
    def _body(self) -> None:
        pass
