from __future__ import annotations

from typing import Callable, TextIO


def rclone_log_contains_not_ignored_errors(
    file: TextIO, checks: list[Callable[[str, TextIO], bool]]
) -> bool:
    for line in file:
        if "ERROR" in line and "Can't retry any of the errors" not in line:
            if all(check(line, file) for check in checks):
                return True
    return False
