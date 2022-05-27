from __future__ import annotations

import re
import subprocess
from abc import ABC
from typing import Callable


class BashScript(ABC):
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = re.sub("  +", " ", code)


BashScriptErrorHandler = Callable[[subprocess.CalledProcessError], None]


def run_bash_script(
    script: BashScript,
    *,
    cwd: str = "/",
    bash_exe: str = "/bin/bash",
    error_handler: BashScriptErrorHandler | None = None,
) -> subprocess.CompletedProcess | subprocess.CalledProcessError:
    try:
        return subprocess.run(
            f"({script.code})",
            cwd=cwd,
            shell=True,
            executable=bash_exe,
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        if error_handler:
            error_handler(e)
            return e
        else:
            raise e
