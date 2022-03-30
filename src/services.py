import subprocess

from commands import rclone_files_list, save_list_of_installed_apps, rclone_copy_files, \
    truncate_file
from utils import State, rclone_log_contains_not_ignored_errors, run_command, Service, \
    seconds_passed_from_time_stamp_till_now, \
    time_stamp

import copy


class BackupWitchService(Service):

    def __init__(self,
                 run_interval: int,
                 state: State,
                 state_key_prefix: str,
                 backup_cwd: str,
                 destination_latest: str,
                 destination_previous: str,
                 rclone_filter: str,
                 rclone_log_file: str,
                 no_traverse_max_age: int,
                 files_all_file: str,
                 files_new_file: str,
                 additional_rclone_flags: str,
                 apps_list_output_file: str,
                 *,
                 ignore_permission_denied_errors_on_source: bool = False,
                 ignore_partially_written_files_upload_errors: bool = False):
        super().__init__(run_interval, state, state_key_prefix)
        self._backup_cwd = backup_cwd
        self._destination_latest = destination_latest
        self._destination_previous = destination_previous
        self._rclone_filter = rclone_filter
        self._rclone_log_file = rclone_log_file
        self._no_traverse_max_age = no_traverse_max_age
        self._files_list_all_command = rclone_files_list(files_all_file, rclone_filter)
        self._files_new_file = files_new_file
        self._additional_rclone_flags = additional_rclone_flags
        self._apps_list_command = save_list_of_installed_apps(apps_list_output_file)
        self._truncate_log_command = truncate_file(rclone_log_file)
        self._ignore_permission_denied_errors_on_source = ignore_permission_denied_errors_on_source
        self._ignore_partially_written_files_upload_errors = ignore_partially_written_files_upload_errors

    async def _body(self):
        run_command(title='truncate rclone copy log file',
                    command=self._truncate_log_command,
                    cwd='/')
        run_command(title='save list of installed apps',
                    command=self._apps_list_command,
                    cwd='/')
        run_command(title='save list of all files',
                    command=self._files_list_all_command,
                    cwd=self._backup_cwd,
                    called_process_error_handler=self._files_list_command_error_handler)
        seconds_passed_from_last_copy_run_start = seconds_passed_from_time_stamp_till_now(
            self._state_manager.get('last_run_start_time_stamp', '')
        )
        run_command(title='save list of files for upload',
                    command=self._list_of_new_files_command(seconds_passed_from_last_copy_run_start),
                    cwd=self._backup_cwd,
                    called_process_error_handler=self._files_list_command_error_handler)
        run_start_time_stamp = time_stamp()
        run_command(title='copy files to cloud',
                    command=self._copy_command(seconds_passed_from_last_copy_run_start),
                    cwd=self._backup_cwd,
                    called_process_error_handler=self._copy_command_error_handler)
        self._state_manager.set(
            key='last_run_start_time_stamp',
            value=run_start_time_stamp
        )

    def _files_list_command_error_handler(self, e: subprocess.CalledProcessError) -> bool:
        if self._ignore_permission_denied_errors_on_source and e.returncode == 6:
            return False
        return True

    def _copy_command_error_handler(self, _: subprocess.CalledProcessError) -> bool:
        checks_for_not_ignored_errors = []
        if self._ignore_permission_denied_errors_on_source:
            checks_for_not_ignored_errors.append(lambda l, _: 'permission denied' not in l)
        if self._ignore_partially_written_files_upload_errors:
            checks_for_not_ignored_errors.append(lambda l, _: 'source file is being updated' not in l)
            checks_for_not_ignored_errors.append(lambda _, f: 'BadDigest' not in f.readline())
        if checks_for_not_ignored_errors:
            with open(self._rclone_log_file) as file:
                return rclone_log_contains_not_ignored_errors(file, checks_for_not_ignored_errors)
        return True

    def _list_of_new_files_command(self, seconds_passed_from_last_copy_run_start: int) -> str:
        rclone_filter = f'--max-age {seconds_passed_from_last_copy_run_start}s {self._rclone_filter}'
        return rclone_files_list(self._files_new_file, rclone_filter)

    def _copy_command(self, seconds_passed_from_last_copy_run_start: int) -> str:
        flags = self._additional_rclone_flags
        if seconds_passed_from_last_copy_run_start <= self._no_traverse_max_age:
            flags += ' --no-traverse'
        return rclone_copy_files(
            destination=self._destination_latest,
            backup_dir=self._destination_previous,
            log_file=self._rclone_log_file,
            files_new_file=self._files_new_file,
            additional_rclone_flags=flags
        )
