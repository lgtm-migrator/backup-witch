import asyncio
import logging
import subprocess
from pathlib import Path

from src.core.backup_service import BackupService
from src.lib.application_state import ApplicationState
from src.lib.json_application_state_provider import JSONApplicationStateProvider
from src.settings import Configuration


async def main(config: Configuration):
    try:
        Path(config.BACKUP_WITCH_DATA_FOLDER).mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=config.PYTHON_LOG_FILE,
            level=logging.WARNING,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        application_state = ApplicationState(
            JSONApplicationStateProvider(config.STATE_FILE)
        )
        backup_service = BackupService(
            application_state=application_state, config=config
        )
        await backup_service.run()
    except BaseException as e:
        stderr = ""
        if type(e) == subprocess.CalledProcessError:
            e: subprocess.CalledProcessError
            stderr = f"stderr:\n{e.stderr}\n"
        logging.critical(f"repr(e):\n{repr(e)}\n{stderr}---")
        if notify_command := config.EXCEPTION_NOTIFY_COMMAND:
            subprocess.run(
                notify_command,
                shell=True,
                check=True,
            )
        raise e


if __name__ == "__main__":  # pragma: no cover
    try:
        from config import CONFIG
    except ImportError as err:
        raise RuntimeError(
            'No config found. Check "How to run" section of readme'
        ) from err
    asyncio.run(main(CONFIG))
