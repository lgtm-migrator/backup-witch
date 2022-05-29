from __future__ import annotations

from pathlib import Path
from typing import Callable, TextIO


def rclone_log_contains_not_ignored_errors(
    log_file_path: str, checks: list[Callable[[str, TextIO], bool]]
) -> bool:
    log_file_contains_unparseable_error = True
    if Path(log_file_path).stat().st_size == 0:
        raise RcloneLogFileIsEmptyError
    with open(log_file_path) as log_file:
        for line in log_file:
            if "ERROR" in line and "Can't retry any of the errors" not in line:
                log_file_contains_unparseable_error = False
                if all(check(line, log_file) for check in checks):
                    return True
    return log_file_contains_unparseable_error


class RcloneLogFileIsEmptyError(Exception):
    pass
