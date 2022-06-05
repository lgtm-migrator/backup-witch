from src.plugins.exception_notify_command_composers.notify_send_exception_notify_command_composer import (
    notify_send_exception_notify_command_composer,
)
from src.plugins.pre_backup_hooks.save_list_of_installed_apps import (
    SaveListOfInstalledAppsHook,
)
from src.settings import UNIX_HOME_FOLDER, Configuration

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
    ],
    PRE_BACKUP_HOOKS=[
        SaveListOfInstalledAppsHook(UNIX_HOME_FOLDER + "/.list-of-installed-apps.txt")
    ],
    EXCEPTION_NOTIFY_COMMAND_COMPOSER=notify_send_exception_notify_command_composer,
)
