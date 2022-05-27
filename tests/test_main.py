import asyncio

import pytest

from src.main import main
from src.settings import Configuration


async def test(tmp_path):
    backup_witch_data_folder = tmp_path / "backup-witch"
    backup_source = tmp_path / "backup_source"
    backup_destination = tmp_path / "backup-destination"
    backup_destination_latest = backup_destination / "latest"
    backup_destination_previous = backup_destination / "previous"
    backup_source.mkdir()
    backup_destination_latest.mkdir(parents=True)
    backup_destination_previous.mkdir(parents=True)
    run_interval = 1  # seconds
    config = Configuration(
        BACKUP_SOURCE=backup_source.__str__(),
        BACKUP_DESTINATION_LATEST=backup_destination_latest.__str__(),
        BACKUP_DESTINATION_PREVIOUS=backup_destination_previous.__str__(),
        BACKUP_WITCH_DATA_FOLDER=backup_witch_data_folder.__str__(),
        EXCEPTION_NOTIFY_COMMAND="exit 0",
    )
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(main(config), run_interval * 2)
    # todo improve
