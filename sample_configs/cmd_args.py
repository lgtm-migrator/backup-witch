LIST_APPS_AND_COPY_FILES_INTERVAL = 900  # seconds: 15 minutes

NO_TRAVERSE_MAX_AGE = 86400  # seconds: 24 hours

RCLONE_FLAGS = '--fast-list --drive-chunk-size 64M --transfers 10 --buffer-size 16M --use-mmap ' \
               '--s3-no-check-bucket --stats 1m --log-level INFO --stats-file-name-length 0  --retries 1'

IGNORE_PERMISSION_DENIED_ERRORS_ON_SOURCE = True

IGNORE_PARTIALLY_WRITTEN_FILES_UPLOAD_ERRORS = True

DEBUG = False
