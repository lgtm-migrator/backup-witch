import asyncio
import logging
import subprocess
from pathlib import Path

from src.core.application_state_json import ApplicationStateJson
from src.core.backup_service import BackupService
from src.settings import Configuration


async def main(config: Configuration):
    try:
        logging.basicConfig(
            filename=config.PYTHON_LOG_FILE,
            level=logging.WARNING,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        Path(config.BACKUP_WITCH_DATA_FOLDER).mkdir(parents=True, exist_ok=True)
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
            config.EXCEPTION_NOTIFY_COMMAND,
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
