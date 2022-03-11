from __future__ import annotations

import logging
import subprocess
import json
import asyncio
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import Final


# region time

def time_stamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def seconds_passed_from_time_stamp_till_now(stamp: str) -> int:
    t_now = datetime.now(timezone.utc).astimezone()
    if not stamp:
        return int(t_now.timestamp())
    t_of_stamp = datetime.fromisoformat(stamp).astimezone()
    return (t_now - t_of_stamp).seconds


# endregion

# region state

class State:
    def __init__(self, save_file_path: str):
        self._save_file_path = save_file_path
        self.data: Final[dict] = self._load_state_from_file() or {}

    def update_state(self, key: str, value: str):
        self.data[key] = value
        self._save_state_to_file()

    def _load_state_from_file(self) -> dict | None:
        subprocess.run(f'touch -a {self._save_file_path}',
                       check=True,
                       shell=True)
        state_file_contents = subprocess.run(f'cat {self._save_file_path}',
                                             shell=True,
                                             check=True,
                                             stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        if not state_file_contents:
            return None
        return json.loads(state_file_contents)

    def _save_state_to_file(self):
        subprocess.run(f"echo '{json.dumps(self.data)}' > {self._save_file_path}",
                       check=True,
                       shell=True)


# endregion

# region run utils

def run_command(title: str, command: str, cwd: str):
    try:
        subprocess.run(command,
                       cwd=cwd,
                       shell=True,
                       check=True,
                       capture_output=True)
    except subprocess.CalledProcessError as e:
        logging.critical(f'{title} failed\n'
                         f'repr(e): {repr(e)}\n'
                         f'stderr: {e.stderr or "stderr is empty, check rclone log-file"}\n')
        raise LoggedException(f'{title} failed') from e


# endregion

# region service

class ServiceStateManager:
    def __init__(self,
                 state: State,
                 key_prefix: str):
        self._state = state
        self._key_prefix = key_prefix

    def get(self, key: str, default_value):
        return self._state.data.get(self._key_prefix + key, default_value)

    def set(self, key: str, value: str):
        self._state.update_state(self._key_prefix + key, value)


class Service(ABC):
    def __init__(self,
                 run_interval: int,
                 state: State,
                 state_key_prefix: str):
        self._run_interval = run_interval
        self._state_manager = ServiceStateManager(state, state_key_prefix)

    async def run(self):
        while 1:
            interval_delta = self._get_interval_delta()
            if interval_delta <= 0:
                await self._body()
                self._state_manager.set(
                    key='last_run_end_time_stamp',
                    value=time_stamp()
                )
                await asyncio.sleep(self._run_interval)
            else:
                await asyncio.sleep(interval_delta)

    def _get_interval_delta(self) -> int:
        return self._run_interval - seconds_passed_from_time_stamp_till_now(
            self._state_manager.get('last_run_end_time_stamp', '')
        )

    @abstractmethod
    async def _body(self):
        pass


# endregion


# region exceptions

class LoggedException(Exception):
    pass

# endregion
