import asyncio
import subprocess
import logging

from services import BackupWitchService
from utils import State, LoggedException

try:
    from config import paths, cmd_args, filters
except ImportError as _e:
    raise RuntimeError('No config found. Check readme for how to setup your config') from _e

logging.basicConfig(filename=paths.PYTHON_LOG, level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main():
    try:
        state = State(paths.STATE_FILE)
        backup_witch_service = BackupWitchService(
            run_interval=cmd_args.LIST_APPS_AND_COPY_FILES_INTERVAL,
            state=state,
            backup_source=paths.USER_HOME,
            destination_latest=paths.CLOUD_LATEST,
            destination_previous=paths.CLOUD_PREVIOUS,
            rclone_filter=filters.RCLONE_FILTER,
            rclone_copy_log_file=paths.RCLONE_COPY_LOG,
            rclone_match_log_file=paths.RCLONE_MATCH_LOG,
            no_traverse_max_age=cmd_args.NO_TRAVERSE_MAX_AGE,
            rclone_additional_flags=cmd_args.RCLONE_FLAGS,
            apps_list_output_file=paths.APPS_LIST_FILE,
            ignore_permission_denied_errors_on_source=cmd_args.IGNORE_PERMISSION_DENIED_ERRORS_ON_SOURCE,
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
