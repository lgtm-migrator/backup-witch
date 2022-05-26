import asyncio

from typing_extensions import Type

from src.core.application_state import ApplicationState
from src.core.application_state_json import ApplicationStateJson
from src.core.service import Service


class CountService(Service):
    def __init__(
        self,
        run_interval: int,
        application_state: Type[ApplicationState],
        initial_value: int,
    ):
        super().__init__(run_interval, application_state, "count-service:")
        self._value = initial_value

    async def _body(self):
        self._value += 1

    def get_value(self) -> int:
        return self._value


async def test(tmp_path):
    state_save_file_path = tmp_path / "state.json"
    ApplicationStateJson.init(state_save_file_path.__str__())
    run_interval = 1  # seconds
    initial_counter_value = 0
    count_service = CountService(
        run_interval, ApplicationStateJson, initial_counter_value
    )
    system_run_time = 1  # seconds
    service_run = asyncio.create_task(count_service.run())
    await asyncio.sleep(system_run_time)
    service_run.cancel()
    expected_counter_value = initial_counter_value + system_run_time / run_interval
    assert count_service.get_value() == expected_counter_value
