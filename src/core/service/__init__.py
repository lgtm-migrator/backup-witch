import asyncio
from abc import ABC, abstractmethod
from typing import Type

from src.core.application_state import ApplicationState
from src.core.service_state import ServiceState
from src.utils.time_utils import seconds_passed_from_time_stamp_till_now, time_stamp


class Service(ABC):
    def __init__(self,
                 run_interval: int,
                 application_state: Type[ApplicationState],
                 state_key_prefix: str):
        self._run_interval = run_interval
        self._state = ServiceState(application_state, state_key_prefix)

    async def run(self):
        while 1:
            interval_delta = self._get_interval_delta()
            if interval_delta <= 0:
                await self._body()
                self._state.set(
                    key='last_run_end_time_stamp',
                    value=time_stamp()
                )
                await asyncio.sleep(self._run_interval)
            else:
                await asyncio.sleep(interval_delta)

    def _get_interval_delta(self) -> int:
        return self._run_interval - seconds_passed_from_time_stamp_till_now(
            self._state.get('last_run_end_time_stamp', '')
        )

    @abstractmethod
    async def _body(self):
        pass
