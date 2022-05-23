from src.settings import Configuration, UNIX_HOME_FOLDER, RunOptions

RUN_OPTIONS = RunOptions(DEBUG=False)

CONFIG = Configuration(
    BACKUP_SOURCE=UNIX_HOME_FOLDER,
    BACKUP_DESTINATION_LATEST="example-remote:@backup-witch/latest",
    BACKUP_DESTINATION_PREVIOUS="example-remote:@backup-witch/previous",
    RCLONE_ADDITIONAL_FLAGS=[
        "--fast-list",
        "--drive-chunk-size 64M",
        "--transfers 10",
        "--buffer-size 16M",
        "--use-mmap",
        "--s3-no-check-bucket",
        "--stats 1m",
        "--log-level INFO",
        "--stats-file-name-length 0",
        "--retries 1",
    ],
)
