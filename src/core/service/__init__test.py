import asyncio
from typing import Type

import pytest

from src.core.application_state import ApplicationState
from src.core.application_state_json import ApplicationStateJson
from src.core.service import Service


class CountService(Service):
    def __init__(
        self,
        run_interval: int,
        application_state: Type[ApplicationState],
        initial_value: int,
        step: int,
    ):
        super().__init__(run_interval, application_state, "count-service:")
        self._value = initial_value
        self._step = step

    async def _body(self):
        self._value += self._step

    def get_value(self) -> int:
        return self._value


async def test(tmp_path):
    state_save_file_path = tmp_path / "state.json"
    ApplicationStateJson.init(state_save_file_path.__str__())
    run_interval = 2  # seconds
    initial_counter_value = 0
    counter_step = 1
    count_service = CountService(
        run_interval, ApplicationStateJson, initial_counter_value, counter_step
    )
    run_process = asyncio.create_task(count_service.run())
    with pytest.raises(RuntimeError):
        # test that exception is thrown, when trying to run already running service
        await asyncio.create_task(count_service.run())
    run_process.cancel()
    try:
        await run_process
    except asyncio.CancelledError:
        pass
    with pytest.raises(asyncio.TimeoutError):
        # make service body run for less than a run_interval to create time delta
        await asyncio.wait_for(count_service.run(), run_interval - 1)
    counter_value_after_first_run = count_service.get_value()
    assert counter_value_after_first_run == initial_counter_value + counter_step
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(count_service.run(), run_interval)
    assert count_service.get_value() == counter_value_after_first_run + counter_step
