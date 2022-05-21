from dataclasses import dataclass
from pathlib import Path

UNIX_HOME_FOLDER = Path('~/').expanduser().__str__()

BACKUP_WITCH_DATA_FOLDER = UNIX_HOME_FOLDER + '/.cache/backup-witch'


@dataclass
class Configuration:
    BACKUP_SOURCE: str

    BACKUP_DESTINATION_LATEST: str

    BACKUP_DESTINATION_PREVIOUS: str

    LIST_APPS_AND_COPY_FILES_INTERVAL: int = 900  # seconds: 15 minutes

    NO_TRAVERSE_MAX_AGE: int = 86400  # seconds: 24 hours

    RCLONE_FLAGS: str = ''  # todo switch to using a list of flags

    RCLONE_FILTER: str = ''  # todo switch to --filter-from

    PYTHON_LOG_FILE: str = BACKUP_WITCH_DATA_FOLDER + '/python.log',

    RCLONE_COPY_LOG_FILE: str = BACKUP_WITCH_DATA_FOLDER + '/rclone-copy.log',

    RCLONE_MATCH_LOG_FILE: str = BACKUP_WITCH_DATA_FOLDER + '/rclone-match.log',

    STATE_FILE: str = BACKUP_WITCH_DATA_FOLDER + '/state.json',

    APPS_LIST_FILE: str = UNIX_HOME_FOLDER + '/.list-of-installed-apps.txt'

    IGNORE_PERMISSION_DENIED_ERRORS_ON_SOURCE: bool = True

    DEBUG: bool = False
