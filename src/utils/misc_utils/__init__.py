from __future__ import annotations

from typing import Callable, TextIO


def rclone_log_contains_not_ignored_errors(file: TextIO, checks: list[Callable[[str, TextIO], bool]]) -> bool:
    no_errors_encountered = True
    for line in file:
        if 'ERROR' in line and "Can't retry any of the errors" not in line:
            no_errors_encountered = False
            if all(check(line, file) for check in checks):
                return True
    if no_errors_encountered:  # todo remove this? as there are errors, which don't have 'ERROR' in them
        raise Unexpected('Rclone log was checked for not ignored errors but no errors were encountered')
    return False


class LoggedException(Exception):
    pass


class Unexpected(Exception):
    pass
