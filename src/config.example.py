from src.settings import Configuration, UNIX_HOME_FOLDER

CONFIG = Configuration(
    BACKUP_SOURCE=UNIX_HOME_FOLDER,
    BACKUP_DESTINATION="example-remote:@backup-witch",
    RCLONE_FILTER_FLAGS_LIST=["--links"],
    RCLONE_ADDITIONAL_FLAGS_LIST=[
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
