import asyncio
import logging
import subprocess

from src.core.application_state_json import ApplicationStateJson
from src.core.backup_service import BackupService
from src.settings import RunOptions
from utils.misc_utils import LoggedException

try:
    from config import RUN_OPTIONS
except ImportError:
    RUN_OPTIONS = RunOptions()

try:
    from config import CONFIG
except ImportError as err:
    raise RuntimeError('No config found. Check "How to run" section of readme') from err

logging.basicConfig(filename=CONFIG.PYTHON_LOG_FILE, level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main():
    try:
        ApplicationStateJson.init(CONFIG.STATE_FILE)
        backup_witch_service = BackupService(
            application_state=ApplicationStateJson,
            config=CONFIG
        )
        await backup_witch_service.run()
    except BaseException as e:
        if RUN_OPTIONS.DEBUG:
            raise e
        if type(e) != LoggedException:
            logging.critical(repr(e))
        subprocess.run(
            f'notify-send "backup_witch" "Exception Occurred\nCheck log -> {CONFIG.PYTHON_LOG_FILE}" -u critical',
            shell=True,
            check=False)
        raise e


if __name__ == '__main__':
    asyncio.run(main())
