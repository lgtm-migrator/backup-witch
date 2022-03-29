from pathlib import Path

USER_HOME = Path('~/').expanduser().__str__()

BACKUP_WITCH_REMOTE = 'CHANGE_ME-!'  # set to appropriate rclone remote, e.g. 'remote:'

CLOUD_LATEST = BACKUP_WITCH_REMOTE + '/latest'

CLOUD_PREVIOUS = BACKUP_WITCH_REMOTE + '/previous'

PYTHON_LOG = USER_HOME + '/.backup-witch.python.log'

RCLONE_COPY_LOG = USER_HOME + '/.backup-witch.rclone_copy.log'

STATE_FILE = USER_HOME + '/.backup-witch.state.data'

APPS_LIST_FILE = USER_HOME + '/.list-of-installed-apps.txt'

FILES_ALL_FILE = USER_HOME + '/.backup-witch-files-all.txt'

FILES_NEW_FILE = USER_HOME + '/.backup-witch-files-new.txt'
