import pytest


class TestEnv:
    def __init__(self):
        self.RCLONE_FLAGS_LIST: list = [
            "-vv",
            "--fast-list",
            "--buffer-size 16M",
            "--use-mmap",
            "--stats-file-name-length 0",
            "--stats-file-name-length 0",
            "--retries 1",
        ]
        self.RCLONE_FlAGS_STR: str = " ".join(self.RCLONE_FLAGS_LIST)


def pytest_configure():
    pytest.testenv = TestEnv()
