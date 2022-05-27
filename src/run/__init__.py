import logging
import subprocess

from src.core.application_state_json import ApplicationStateJson
from src.core.backup_service import BackupService
from src.settings import Configuration


async def run(config: Configuration):
    try:
        ApplicationStateJson.init(config.STATE_FILE)
        backup_service = BackupService(
            application_state=ApplicationStateJson, config=config
        )
        await backup_service.run()
    except BaseException as e:
        stderr = ""
        if type(e) == subprocess.CalledProcessError:
            e: subprocess.CalledProcessError
            stderr = f"stderr:\n{e.stderr}\n"
        logging.critical(f"repr(e):\n{repr(e)}\n{stderr}---")
        subprocess.run(
            f'notify-send "backup_witch" "Exception Occurred\nCheck log -> {config.PYTHON_LOG_FILE}" -u critical',
            shell=True,
            check=False,
        )
        raise e
