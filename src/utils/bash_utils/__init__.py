from __future__ import annotations

import logging
import re
import subprocess
from abc import ABC
from typing import Callable

from src.utils.misc_utils import LoggedException


class BashScript(ABC):
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = re.sub("  +", " ", code)


def run_bash_script(
    script: BashScript,
    *,
    cwd: str = "/",
    bash_exe: str = "/bin/bash",
    on_error_handler: Callable[[subprocess.CalledProcessError], bool] | None = None,
):
    try:
        subprocess.run(
            f"({script.code})",
            cwd=cwd,
            shell=True,
            executable=bash_exe,
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        logged_exception = True
        if on_error_handler:
            logged_exception = on_error_handler(e)
        if logged_exception:
            logging.critical(
                f"{script.name} failed\n"
                f"repr(e):\n{repr(e)}\n"
                f"stderr:\n{e.stderr}\n"
                f"---"
            )
            raise LoggedException(f"run_bash_script failed - {script.name}") from e
