import pytest
from dataclasses import dataclass


@dataclass
class TestEnv:
    """
    for ide autocompletion
    """

    RCLONE_FlAGS: str = '-vv --fast-list --buffer-size 16M --use-mmap ' \
                        '--stats-file-name-length 0 --retries 1'


def pytest_configure():
    pytest.testenv = TestEnv()
