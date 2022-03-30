import asyncio
import subprocess
import logging

from services import BackupWitchService
from configs import paths, cmd_args, filters
from utils import State, LoggedException

logging.basicConfig(filename=paths.PYTHON_LOG, level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main():
    try:
        state = State(paths.STATE_FILE)
        backup_witch_service = BackupWitchService(
            run_interval=cmd_args.LIST_APPS_AND_COPY_FILES_INTERVAL,
            state=state,
            state_key_prefix='list-apps-copy-files:',
            backup_cwd=paths.USER_HOME,
            destination_latest=paths.CLOUD_LATEST,
            destination_previous=paths.CLOUD_PREVIOUS,
            rclone_filter=filters.RCLONE_FILTER,
            rclone_log_file=paths.RCLONE_COPY_LOG,
            no_traverse_max_age=cmd_args.NO_TRAVERSE_MAX_AGE,
            files_all_file=paths.FILES_ALL_FILE,
            files_new_file=paths.FILES_NEW_FILE,
            additional_rclone_flags=cmd_args.RCLONE_FLAGS,
            apps_list_output_file=paths.APPS_LIST_FILE,
            ignore_permission_denied_errors_on_source=cmd_args.IGNORE_PERMISSION_DENIED_ERRORS_ON_SOURCE,
            ignore_partially_written_files_upload_errors=cmd_args.IGNORE_PARTIALLY_WRITTEN_FILES_UPLOAD_ERRORS
        )
        await backup_witch_service.run()
    except BaseException as e:
        if cmd_args.DEBUG:
            raise e
        if type(e) != LoggedException:
            logging.critical(repr(e))
        subprocess.run(
            f'notify-send "backup_witch" "Exception Occurred\nCheck log -> {paths.PYTHON_LOG}" -u critical',
            shell=True,
            check=False)
        raise e


if __name__ == '__main__':
    asyncio.run(main())
