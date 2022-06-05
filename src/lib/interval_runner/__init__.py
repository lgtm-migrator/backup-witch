import asyncio

from src.lib.runner import Runner
from src.lib.scoped_state import ScopedState
from src.lib.state import State
from src.utils.time_utils import seconds_passed_from_time_stamp_till_now, time_stamp


class IntervalRunner(Runner):
    def __init__(self, run_interval: int, master_state: State):
        self._state = ScopedState(master_state, "interval-scheduler:")
        self._run_interval = run_interval

    async def __call__(self, operation):
        while True:
            interval_delta = self._get_interval_delta()
            if interval_delta <= 0:
                operation()
                self._state.set(key="last_run_end_time_stamp", value=time_stamp())
                await asyncio.sleep(self._run_interval)
            else:
                await asyncio.sleep(interval_delta)

    def _get_interval_delta(self) -> int:
        return self._run_interval - seconds_passed_from_time_stamp_till_now(
            self._state.get("last_run_end_time_stamp", "")
        )
