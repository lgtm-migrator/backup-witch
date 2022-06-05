from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Callable

from src.core.rclone_copy_files import RcloneCopyFilesToDestinationScript
from src.core.rclone_match_destination_to_source import (
    RcloneMatchDestinationToSourceScript,
)
from src.lib.application_state import ApplicationState
from src.lib.interval_runner import IntervalRunner
from src.lib.scoped_state import ScopedState
from src.lib.service import Service
from src.plugins.pre_backup_hooks.save_list_of_installed_apps import (
    SaveListOfInstalledAppsScript,
)
from src.settings import Configuration
from src.utils.bash_utils import run_bash_script
from src.utils.time_utils import seconds_passed_from_time_stamp_till_now, time_stamp


class BackupService(Service):
    def __init__(self, application_state: ApplicationState, config: Configuration):
        self._state = ScopedState(application_state, "backup-service:")
        super().__init__(
            IntervalRunner(config.BACKUP_INTERVAL, self._state)
        )  # todo oneshot runner
        self._backup_source = config.BACKUP_SOURCE
        self._destination_latest = config.BACKUP_DESTINATION_LATEST
        self._destination_previous = config.BACKUP_DESTINATION_PREVIOUS
        self._rclone_filter_flags = config.RCLONE_FILTER_FLAGS_STR
        self._rclone_copy_log_file = config.RCLONE_COPY_LOG_FILE
        self._rclone_match_log_file = config.RCLONE_MATCH_LOG_FILE
        self._no_traverse_max_age = config.NO_TRAVERSE_MAX_AGE
        self._rclone_additional_flags = config.RCLONE_ADDITIONAL_FLAGS_STR
        self._apps_list_output_file = config.APPS_LIST_FILE
        self._ignore_permission_denied_errors_on_source = (
            config.IGNORE_PERMISSION_DENIED_ERRORS_ON_SOURCE
        )
        self._ignore_partially_written_files_upload_errors = (
            config.IGNORE_PARTIALLY_WRITTEN_FILES_UPLOAD_ERRORS
        )
        self._checkers_for_ignored_errors: list[Callable[[str], bool]] = []
        if self._ignore_permission_denied_errors_on_source:
            self._checkers_for_ignored_errors.append(lambda l: "permission denied" in l)
        if self._ignore_partially_written_files_upload_errors:
            self._checkers_for_ignored_errors.append(
                lambda l: "source file is being updated" in l
            )

    def _body(self):
        if self._apps_list_output_file:
            run_bash_script(SaveListOfInstalledAppsScript(self._apps_list_output_file))
        seconds_passed_from_last_backup_run_start = (
            seconds_passed_from_time_stamp_till_now(
                self._state.get("last_backup_run_start_time_stamp", "")
            )
        )
        rclone_additional_flags = self._rclone_additional_flags
        if seconds_passed_from_last_backup_run_start <= self._no_traverse_max_age:
            rclone_additional_flags += " --no-traverse"
        backup_run_start_time_stamp = time_stamp()
        self._copy_files_to_destination(
            seconds_passed_from_last_backup_run_start,
            backup_run_start_time_stamp,
            rclone_additional_flags,
        )
        self._match_destination_to_source(
            backup_run_start_time_stamp, rclone_additional_flags
        )
        self._state.set(
            key="last_backup_run_start_time_stamp", value=backup_run_start_time_stamp
        )

    def _copy_files_to_destination(
        self,
        seconds_passed_from_last_backup_run_start: int,
        backup_run_start_time_stamp: str,
        rclone_additional_flags: str,
    ):
        rclone_copy_files_filter = f"--max-age {seconds_passed_from_last_backup_run_start}s {self._rclone_filter_flags}"
        run_bash_script(
            RcloneCopyFilesToDestinationScript(
                self._backup_source,
                self._destination_latest,
                self._destination_previous,
                backup_run_start_time_stamp,
                self._rclone_copy_log_file,
                rclone_copy_files_filter,
                rclone_additional_flags,
            ),
            error_handler=self._rclone_copy_files_error_handler,
        )

    def _match_destination_to_source(
        self,
        backup_run_start_time_stamp: str,
        rclone_additional_flags: str,
    ):
        run_bash_script(
            RcloneMatchDestinationToSourceScript(
                self._backup_source,
                self._destination_latest,
                self._destination_previous,
                backup_run_start_time_stamp,
                self._rclone_match_log_file,
                self._rclone_filter_flags,
                rclone_additional_flags,
            )
        )

    def _rclone_copy_files_error_handler(self, err: subprocess.CalledProcessError):
        if not self._checkers_for_ignored_errors:
            raise err
        try:
            if self._rclone_log_contains_not_ignored_errors():
                raise err
        except RcloneLogFileIsEmptyError:
            raise err

    def _rclone_log_contains_not_ignored_errors(self) -> bool:
        log_file_contains_unparseable_error = True
        if Path(self._rclone_copy_log_file).stat().st_size == 0:
            raise RcloneLogFileIsEmptyError
        with open(self._rclone_copy_log_file) as log_file:
            for line in log_file:
                if "ERROR" in line and "Can't retry any of the errors" not in line:
                    log_file_contains_unparseable_error = False
                    if not any(
                        is_ignored(line)
                        for is_ignored in self._checkers_for_ignored_errors
                    ):
                        return True
        return log_file_contains_unparseable_error


class RcloneLogFileIsEmptyError(Exception):
    pass
