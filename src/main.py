import asyncio
import logging
import subprocess

from src.core.application_state_json import ApplicationStateJson
from src.core.backup_service import BackupService

try:
    from config import CONFIG
except ImportError as err:
    raise RuntimeError('No config found. Check "How to run" section of readme') from err

logging.basicConfig(
    filename=CONFIG.PYTHON_LOG_FILE,
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


async def main():
    try:
        ApplicationStateJson.init(CONFIG.STATE_FILE)
        backup_service = BackupService(
            application_state=ApplicationStateJson, config=CONFIG
        )
        await backup_service.run()
    except BaseException as e:
        stderr = ""
        if type(e) == subprocess.CalledProcessError:
            e: subprocess.CalledProcessError
            stderr = f"stderr:\n{e.stderr}\n"
        logging.critical(f"repr(e):\n{repr(e)}\n{stderr}---")
        subprocess.run(
            f'notify-send "backup_witch" "Exception Occurred\nCheck log -> {CONFIG.PYTHON_LOG_FILE}" -u critical',
            shell=True,
            check=False,
        )
        raise e


if __name__ == "__main__":
    asyncio.run(main())
