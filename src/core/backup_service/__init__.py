import subprocess

from src.bash_scripts.rclone_copy_files import RcloneCopyFilesScript
from src.bash_scripts.rclone_match_destination_to_source import RcloneMatchDestinationToSourceScript
from src.bash_scripts.save_list_of_installed_apps import SaveListOfInstalledAppsScript
from src.components.service import Service
from src.components.state import State
from src.utils.bash_utils import run_bash_script
from src.utils.misc_utils import rclone_log_contains_not_ignored_errors
from src.utils.time_utils import seconds_passed_from_time_stamp_till_now, time_stamp


class BackupService(Service):

    def __init__(self,
                 # region super args
                 run_interval: int,
                 state: State,
                 # endregion
                 backup_source: str,
                 destination_latest: str,
                 destination_previous: str,
                 rclone_filter_flags: str,
                 rclone_copy_log_file: str,
                 rclone_match_log_file: str,
                 no_traverse_max_age: int,
                 rclone_additional_flags: list,
                 apps_list_output_file: str,
                 *,
                 ignore_permission_denied_errors_on_source: bool = False,
                 ignore_partially_written_files_upload_errors: bool = True):
        super().__init__(run_interval, state, 'backup-witch-service:')
        self._backup_source = backup_source
        self._destination_latest = destination_latest
        self._destination_previous = destination_previous
        self._rclone_filter_flags = rclone_filter_flags
        self._rclone_copy_log_file = rclone_copy_log_file
        self._rclone_match_log_file = rclone_match_log_file
        self._no_traverse_max_age = no_traverse_max_age
        self._rclone_additional_flags = ' '.join(rclone_additional_flags)
        self._apps_list_output_file = apps_list_output_file
        self._ignore_permission_denied_errors_on_source = ignore_permission_denied_errors_on_source
        self._ignore_partially_written_files_upload_errors = ignore_partially_written_files_upload_errors

    async def _body(self):
        run_bash_script(
            SaveListOfInstalledAppsScript(
                self._apps_list_output_file
            )
        )
        seconds_passed_from_last_backup_run_start = seconds_passed_from_time_stamp_till_now(
            self._state_manager.get('last_backup_run_start_time_stamp', '')
        )
        rclone_copy_files_filter = f'--max-age {seconds_passed_from_last_backup_run_start}s {self._rclone_filter_flags}'
        rclone_additional_flags = self._rclone_additional_flags
        if seconds_passed_from_last_backup_run_start <= self._no_traverse_max_age:
            rclone_additional_flags += ' --no-traverse'
        backup_run_start_time_stamp = time_stamp()
        run_bash_script(
            RcloneCopyFilesScript(
                self._backup_source,
                self._destination_latest,
                self._destination_previous,
                backup_run_start_time_stamp,
                self._rclone_copy_log_file,
                rclone_copy_files_filter,
                rclone_additional_flags
            ),
            on_error_handler=self._rclone_copy_files_error_handler
        )
        run_bash_script(
            RcloneMatchDestinationToSourceScript(
                self._backup_source,
                self._destination_latest,
                self._destination_previous,
                backup_run_start_time_stamp,
                self._rclone_match_log_file,
                self._rclone_filter_flags,
                rclone_additional_flags
            )
        )
        self._state_manager.set(
            key='last_backup_run_start_time_stamp',
            value=backup_run_start_time_stamp
        )

    def _rclone_copy_files_error_handler(self, _: subprocess.CalledProcessError) -> bool:
        checks_for_not_ignored_errors = []
        if self._ignore_permission_denied_errors_on_source:
            checks_for_not_ignored_errors.append(lambda l, _: 'permission denied' not in l)
        if self._ignore_partially_written_files_upload_errors:
            checks_for_not_ignored_errors.append(lambda l, _: 'source file is being updated' not in l)
            checks_for_not_ignored_errors.append(lambda _, f: 'BadDigest' not in f.readline())
        if checks_for_not_ignored_errors:
            with open(self._rclone_copy_log_file) as file:
                return rclone_log_contains_not_ignored_errors(file, checks_for_not_ignored_errors)
        return True
