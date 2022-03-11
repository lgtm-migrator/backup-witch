from pathlib import Path
from .cmd_args import BACKUP_WITCH_REMOTE

USER_HOME = Path('~/').expanduser().__str__()

CLOUD_CURRENT = BACKUP_WITCH_REMOTE + '/current'

CLOUD_BACKUPS = BACKUP_WITCH_REMOTE + '/backups'

PYTHON_LOG = USER_HOME + '/.backup_witch.python.log'

RCLONE_COPY_LOG = USER_HOME + '/.backup_witch.rclone_copy.log'

RCLONE_SYNC_LOG = USER_HOME + '/.backup_witch.rclone_sync.log'

STATE_FILE = USER_HOME + '/.backup_witch.state.data'
