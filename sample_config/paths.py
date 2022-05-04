from pathlib import Path

USER_HOME = Path('~/').expanduser().__str__()

BACKUP_WITCH_DESTINATION = 'CHANGE_ME-!'  # for example: 'remote:backup-witch-folder'

CLOUD_LATEST = BACKUP_WITCH_DESTINATION + '/latest'

CLOUD_PREVIOUS = BACKUP_WITCH_DESTINATION + '/previous'

PYTHON_LOG = USER_HOME + '/.backup-witch.python.log'

RCLONE_COPY_LOG = USER_HOME + '/.backup-witch.rclone-copy.log'

RCLONE_MATCH_LOG = USER_HOME + '/.backup-witch.rclone-match.log'

STATE_FILE = USER_HOME + '/.backup-witch.state.data'

APPS_LIST_FILE = USER_HOME + '/.list-of-installed-apps.txt'
