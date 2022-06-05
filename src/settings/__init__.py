from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from src.utils.bash_utils import BashScriptErrorHandler

UNIX_HOME_FOLDER = Path("~/").expanduser().__str__()


@dataclass
class Configuration:
    BACKUP_SOURCE: str

    BACKUP_DESTINATION: str

    BACKUP_INTERVAL: int | None = 900  # seconds: 15 minutes

    NO_TRAVERSE_MAX_AGE: int = 86400  # seconds: 24 hours

    RCLONE_FILTER_FLAGS_LIST: list[str] = field(default_factory=list)

    RCLONE_ADDITIONAL_FLAGS_LIST: list[str] = field(default_factory=list)

    BACKUP_WITCH_DATA_FOLDER: str = UNIX_HOME_FOLDER + "/.backup-witch"

    IGNORE_PERMISSION_DENIED_ERRORS_ON_SOURCE: bool = True

    IGNORE_PARTIALLY_WRITTEN_FILES_UPLOAD_ERRORS: bool = True

    EXCEPTION_NOTIFY_COMMAND_COMPOSER: Callable[[Configuration], str] | None = None

    RCLONE_COPY_FILES_ERROR_HANDLER: BashScriptErrorHandler | None = None

    RCLONE_MATCH_DESTINATION_TO_SOURCE_ERROR_HANDLER: BashScriptErrorHandler | None = (
        None
    )

    PRE_BACKUP_HOOKS: list[Callable[[], None]] = field(default_factory=list)

    POST_BACKUP_HOOKS: list[Callable[[], None]] = field(default_factory=list)

    def __post_init__(self):
        if self.BACKUP_INTERVAL is not None and self.BACKUP_INTERVAL < 1:
            raise RuntimeError(
                f"InvalidSetting: BACKUP_INTERVAL can't be lower than 1.\n"
                f"BACKUP_INTERVAL is set to {self.BACKUP_INTERVAL}."
            )

        self.RCLONE_ADDITIONAL_FLAGS_STR = " ".join(self.RCLONE_ADDITIONAL_FLAGS_LIST)

        self.RCLONE_FILTER_FLAGS_STR = " ".join(self.RCLONE_FILTER_FLAGS_LIST)

        if any(
            [
                "--max-age" in self.RCLONE_ADDITIONAL_FLAGS_STR,
                "--min-age" in self.RCLONE_ADDITIONAL_FLAGS_STR,
                "--max-age" in self.RCLONE_FILTER_FLAGS_STR,
                "--min-age" in self.RCLONE_FILTER_FLAGS_STR,
            ]
        ):
            raise RuntimeError(
                "rclone --max-age or --min-age filters should not be used!"
            )

        self.BACKUP_DESTINATION_LATEST: str = self.BACKUP_DESTINATION + "/latest"

        self.BACKUP_DESTINATION_PREVIOUS: str = self.BACKUP_DESTINATION + "/previous"

        self.PYTHON_LOG_FILE: str = self.BACKUP_WITCH_DATA_FOLDER + "/python.log"

        self.RCLONE_COPY_LOG_FILE: str = (
            self.BACKUP_WITCH_DATA_FOLDER + "/rclone-copy.log"
        )

        self.RCLONE_MATCH_LOG_FILE: str = (
            self.BACKUP_WITCH_DATA_FOLDER + "/rclone-match.log"
        )

        self.STATE_FILE: str = self.BACKUP_WITCH_DATA_FOLDER + "/state.json"

        self.EXCEPTION_NOTIFY_COMMAND = (
            None
            if self.EXCEPTION_NOTIFY_COMMAND_COMPOSER is None
            else self.EXCEPTION_NOTIFY_COMMAND_COMPOSER(self)
        )
