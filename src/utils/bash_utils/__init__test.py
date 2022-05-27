import subprocess

import pytest

from src.utils.bash_utils import BashScript, run_bash_script


class MultilineEchoScript(BashScript):
    def __init__(self, first_line: str, second_line: str):
        code = f"""
        echo '{first_line}'
        echo '{second_line}'
        """
        super().__init__("multiline-echo-script", code)


def test():
    first_echo_line = "First line"
    second_echo_line = "Second line"
    assert (
        run_bash_script(MultilineEchoScript(first_echo_line, second_echo_line)).stdout
        == f"{first_echo_line}\n{second_echo_line}\n"
    )
    assert run_bash_script(BashScript("test simple", "exit 0")).returncode == 0
    with pytest.raises(subprocess.CalledProcessError):
        run_bash_script(BashScript("test error", "exit 1"))
    assert (
        run_bash_script(
            BashScript("test with error handler", "exit 1"),
            error_handler=lambda e: e,
        ).returncode
        == 1
    )

    def error_handler_with_raise(_):
        raise ZeroDivisionError()

    with pytest.raises(ZeroDivisionError):
        run_bash_script(
            BashScript("test with error handler with raise", "exit 1"),
            error_handler=error_handler_with_raise,
        )
