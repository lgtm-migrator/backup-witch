import asyncio
import logging

from src.run import run

try:
    from config import CONFIG
except ImportError as err:
    raise RuntimeError('No config found. Check "How to run" section of readme') from err

logging.basicConfig(
    filename=CONFIG.PYTHON_LOG_FILE,
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


if __name__ == "__main__":
    asyncio.run(run(config=CONFIG))
