import asyncio
import subprocess
import logging

from services import SaveListOfInstalledAppsAndCopyFilesToCloud, SyncDeletionsOfFilesToCloud
from configs import paths, cmd_args, filters
from utils import State, LoggedException

logging.basicConfig(filename=paths.PYTHON_LOG, level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main():
    try:
        state = State(paths.STATE_FILE)
        # region services init
        copy_command_args = SaveListOfInstalledAppsAndCopyFilesToCloud.CopyCommandArguments(
            destination=paths.CLOUD_CURRENT,
            backup_dir=paths.CLOUD_BACKUPS,
            no_traverse_max_age=cmd_args.NO_TRAVERSE_MAX_AGE,
            log_file=paths.RCLONE_COPY_LOG,
            filters=filters.RCLONE_FILTER,
            additional_rclone_flags=cmd_args.RCLONE_FLAGS
        )
        apps_list_command_args = SaveListOfInstalledAppsAndCopyFilesToCloud.AppsListCommandArguments(
            file_name=cmd_args.APPS_LIST_FILE_NAME
        )
        save_list_of_installed_apps_and_copy_files_to_cloud = SaveListOfInstalledAppsAndCopyFilesToCloud(
            run_interval=cmd_args.LIST_APPS_AND_COPY_FILES_INTERVAL,
            state=state,
            state_key_prefix='list-apps-copy-files:',
            copy_command_cwd=paths.USER_HOME,
            copy_command_args=copy_command_args,
            apps_list_command_cwd=paths.USER_HOME,
            apps_list_command_args=apps_list_command_args
        )
        sync_command_args = SyncDeletionsOfFilesToCloud.SyncCommandArguments(
            destination=paths.CLOUD_CURRENT,
            backup_dir=paths.CLOUD_BACKUPS,
            log_file=paths.RCLONE_SYNC_LOG,
            filters=filters.RCLONE_FILTER,
            additional_rclone_flags=cmd_args.RCLONE_FLAGS
        )
        sync_deletes_of_files_to_cloud = SyncDeletionsOfFilesToCloud(
            run_interval=cmd_args.SYNC_DELETIONS_INTERVAL,
            state=state,
            state_key_prefix='sync-deletions:',
            sync_command_cwd=paths.USER_HOME,
            sync_command_args=sync_command_args
        )
        # endregion
        await asyncio.gather(
            save_list_of_installed_apps_and_copy_files_to_cloud.run(),
            sync_deletes_of_files_to_cloud.run()
        )
    except asyncio.exceptions.CancelledError as e:  # raised by KeyboardInterrupt
        raise e
    except BaseException as e:
        if type(e) != LoggedException:
            logging.critical(repr(e))
        subprocess.run(
            f'notify-send "backup_witch" "Exception Occurred\nCheck log -> {paths.PYTHON_LOG}" -u critical',
            shell=True,
            check=False)
        raise e


if __name__ == '__main__':
    asyncio.run(main())
