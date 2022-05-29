import asyncio
import subprocess
from dataclasses import asdict, dataclass
from glob import glob
from pathlib import Path
from typing import Callable

import pytest

from src.main import main
from src.settings import Configuration


@dataclass
class Paths:
    backup_witch_data_folder: Path
    backup_source: Path
    backup_destination: Path
    backup_destination_latest: Path
    backup_destination_previous: Path


@dataclass
class Utils:
    bootstrap_env: Callable[[Paths], None]
    config: Callable[..., Configuration]
    paths: Callable[[Configuration], Paths]


@pytest.fixture
def utils(tmp_path):
    backup_witch_data_folder = tmp_path / "backup-witch"
    backup_source = tmp_path / "backup_source"
    backup_destination = tmp_path / "backup-destination"

    _cfg = Configuration(
        BACKUP_SOURCE=backup_source.__str__(),
        BACKUP_DESTINATION=backup_destination.__str__(),
        BACKUP_INTERVAL=1,  # seconds
        BACKUP_WITCH_DATA_FOLDER=backup_witch_data_folder.__str__(),
        EXCEPTION_NOTIFY_COMMAND="exit 0",
        RCLONE_ADDITIONAL_FLAGS_LIST=pytest.testenv.RCLONE_FLAGS_LIST,
    )

    def _bootstrap_env(paths: Paths):
        paths.backup_source.mkdir()
        paths.backup_destination_latest.mkdir(parents=True)
        paths.backup_destination_previous.mkdir(parents=True)

    def _config(**kwargs):
        return Configuration(**{**asdict(_cfg), **kwargs})

    def _paths(cfg: Configuration):
        return Paths(
            backup_witch_data_folder=Path(cfg.BACKUP_WITCH_DATA_FOLDER),
            backup_source=Path(cfg.BACKUP_SOURCE),
            backup_destination=Path(cfg.BACKUP_DESTINATION),
            backup_destination_latest=Path(cfg.BACKUP_DESTINATION_LATEST),
            backup_destination_previous=Path(cfg.BACKUP_DESTINATION_PREVIOUS),
        )

    return Utils(bootstrap_env=_bootstrap_env, config=_config, paths=_paths)


async def test_normal_with_permission_error_ignore(utils):
    config = utils.config(
        RCLONE_FILTER_FLAGS_LIST=["--copy-links"],
        IGNORE_PERMISSION_DENIED_ERRORS_ON_SOURCE=True,
    )
    paths = utils.paths(config)
    utils.bootstrap_env(paths)
    symlink_to_root = paths.backup_source / "root"
    symlink_to_root.symlink_to("/root")
    file_on_backup_source_name = "first-file.txt"
    file_on_backup_source = paths.backup_source / file_on_backup_source_name
    file_on_backup_source.touch()
    file_on_backup_source.write_text("first-file")
    # test copy on first run
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(main(config), config.BACKUP_INTERVAL)
    file_on_backup_destination_latest = (
        paths.backup_destination_latest / file_on_backup_source_name
    )
    assert file_on_backup_destination_latest.exists()
    assert (
        file_on_backup_destination_latest.read_text()
        == file_on_backup_source.read_text()
    )
    # test copy on second run, with new file on backup source
    await asyncio.sleep(1)
    second_file_on_source_name = "second-file.txt"
    second_file_on_source = paths.backup_source / second_file_on_source_name
    second_file_on_source.touch()
    second_file_on_source.write_text("second-file")
    second_file_on_destination_latest = (
        paths.backup_destination_latest / second_file_on_source_name
    )
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(main(config), config.BACKUP_INTERVAL)
    assert second_file_on_destination_latest.exists()
    assert (
        second_file_on_destination_latest.read_text()
        == second_file_on_source.read_text()
    )
    # test destination to source matching
    await asyncio.sleep(1)
    glob_result = glob(
        paths.backup_destination_previous.__str__() + "/**", recursive=True
    )
    assert len(glob_result) == 1
    assert glob_result[0] == paths.backup_destination_previous.__str__() + "/"
    file_on_backup_source.unlink()
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(main(config), config.BACKUP_INTERVAL)
    assert file_on_backup_destination_latest.exists() is False
    glob_result = glob(
        paths.backup_destination_previous.__str__() + f"/*/{file_on_backup_source_name}"
    )
    assert len(glob_result) == 1
    file_on_destination_previous = Path(glob_result[0])
    assert file_on_destination_previous.name == file_on_backup_source_name


async def test_with_permission_error_respect(utils):
    config = utils.config(
        RCLONE_FILTER_FLAGS_LIST=["--copy-links"],
        IGNORE_PERMISSION_DENIED_ERRORS_ON_SOURCE=False,
    )
    paths = utils.paths(config)
    utils.bootstrap_env(paths)
    symlink_to_root = paths.backup_source / "root"
    symlink_to_root.symlink_to("/root")
    with pytest.raises(subprocess.CalledProcessError):
        await main(config)


async def test_with_no_errors_ignore(utils):
    config = utils.config(
        RCLONE_FILTER_FLAGS_LIST=["--copy-links"],
        IGNORE_PERMISSION_DENIED_ERRORS_ON_SOURCE=False,
        IGNORE_PARTIALLY_WRITTEN_FILES_UPLOAD_ERRORS=False,
    )
    paths = utils.paths(config)
    utils.bootstrap_env(paths)
    symlink_to_root = paths.backup_source / "root"
    symlink_to_root.symlink_to("/root")
    with pytest.raises(subprocess.CalledProcessError):
        await main(config)


async def test_invalid_argument_error(utils):
    config = utils.config(
        RCLONE_FILTER_FLAGS_LIST=["--filter-from />.folder/filter.txt"]
    )
    paths = utils.paths(config)
    utils.bootstrap_env(paths)
    with pytest.raises(subprocess.CalledProcessError):
        await main(config)


async def test_special_rclone_error_handling(utils):
    config = utils.config(RCLONE_ADDITIONAL_FLAGS_LIST=["-vv", "--log-level INFO"])
    paths = utils.paths(config)
    utils.bootstrap_env(paths)
    with pytest.raises(subprocess.CalledProcessError):
        await main(config)
