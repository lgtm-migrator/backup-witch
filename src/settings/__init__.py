from dataclasses import dataclass, field
from pathlib import Path

UNIX_HOME_FOLDER = Path("~/").expanduser().__str__()


@dataclass
class Configuration:
    BACKUP_SOURCE: str

    BACKUP_DESTINATION_LATEST: str

    BACKUP_DESTINATION_PREVIOUS: str

    BACKUP_INTERVAL: int = 900  # seconds: 15 minutes

    NO_TRAVERSE_MAX_AGE: int = 86400  # seconds: 24 hours

    RCLONE_FILTER_FLAGS: str = ""

    RCLONE_ADDITIONAL_FLAGS: list = field(default_factory=list)

    BACKUP_WITCH_DATA_FOLDER: str = UNIX_HOME_FOLDER + "/.cache/backup-witch"

    APPS_LIST_FILE: str = UNIX_HOME_FOLDER + "/.list-of-installed-apps.txt"

    IGNORE_PERMISSION_DENIED_ERRORS_ON_SOURCE: bool = True

    IGNORE_PARTIALLY_WRITTEN_FILES_UPLOAD_ERRORS: bool = True

    EXCEPTION_NOTIFY_COMMAND: str = ""

    PYTHON_LOG_FILE: str = field(init=False)

    RCLONE_COPY_LOG_FILE: str = field(init=False)

    RCLONE_MATCH_LOG_FILE: str = field(init=False)

    STATE_FILE: str = field(init=False)

    def __post_init__(self):
        self.PYTHON_LOG_FILE: str = self.BACKUP_WITCH_DATA_FOLDER + "/python.log"

        self.RCLONE_COPY_LOG_FILE: str = (
            self.BACKUP_WITCH_DATA_FOLDER + "/rclone-copy.log"
        )

        self.RCLONE_MATCH_LOG_FILE: str = (
            self.BACKUP_WITCH_DATA_FOLDER + "/rclone-match.log"
        )

        self.STATE_FILE: str = self.BACKUP_WITCH_DATA_FOLDER + "/state.json"

        if not self.EXCEPTION_NOTIFY_COMMAND:  # pragma: no cover
            self.EXCEPTION_NOTIFY_COMMAND = (  # pragma: no cover
                f'notify-send "backup_witch" "Exception Occurred\n'
                f'Check log -> {self.PYTHON_LOG_FILE}" -u critical '
            )
