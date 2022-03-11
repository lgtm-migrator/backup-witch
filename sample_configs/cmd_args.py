LIST_APPS_AND_COPY_FILES_INTERVAL = 1800  # seconds: 30 minutes

SYNC_DELETIONS_INTERVAL = 43200  # seconds: 12 hours

NO_TRAVERSE_MAX_AGE = 86400  # seconds: 24 hours

RCLONE_FLAGS = '--fast-list --buffer-size 16M --use-mmap --s3-no-check-bucket --stats 1m --log-level INFO ' \
               '--stats-file-name-length 0 --links'

APPS_LIST_FILE_NAME = '.list_of_installed_apps.txt'

BACKUP_WITCH_REMOTE = 'CHANGE_ME-!'  # set to appropriate rclone remote, e.g. 'remote:'

DEBUG = False
