from __future__ import annotations

from typing import Callable, TextIO


def rclone_log_contains_not_ignored_errors(
    file: TextIO, checks: list[Callable[[str, TextIO], bool]]
) -> bool:
    log_file_contains_unparseable_error = True
    for line in file:
        if "ERROR" in line and "Can't retry any of the errors" not in line:
            log_file_contains_unparseable_error = False
            if all(check(line, file) for check in checks):
                return True
    return log_file_contains_unparseable_error
