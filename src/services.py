from commands import save_list_of_installed_apps, rclone_copy_files, \
    rclone_sync_deletions, truncate_file
from utils import State, run_command, run_command_with_retries, Service, seconds_passed_from_time_stamp_till_now, \
    time_stamp
from typing import TypedDict


class SaveListOfInstalledAppsAndCopyFilesToCloud(Service):
    class CopyCommandArguments(TypedDict):
        destination: str
        backup_dir: str
        log_file: str
        no_traverse_max_age: int
        filters: str
        additional_rclone_flags: str

    class AppsListCommandArguments(TypedDict):
        file_name: str

    def __init__(self,
                 run_interval: int,
                 state: State,
                 state_key_prefix: str,
                 copy_command_cwd: str,
                 copy_command_retry_interval: int,
                 copy_command_args: CopyCommandArguments,
                 apps_list_command_cwd: str,
                 apps_list_command_args: AppsListCommandArguments):
        super().__init__(run_interval, state, state_key_prefix)
        self._apps_list_command = save_list_of_installed_apps(**apps_list_command_args)
        self._apps_list_command_cwd = apps_list_command_cwd
        self._copy_command_args = copy_command_args
        self._copy_command_cwd = copy_command_cwd
        self._copy_command_retry_interval = copy_command_retry_interval
        self._truncate_log_command = truncate_file(self._copy_command_args['log_file'])

    async def _body(self):
        run_command(title='save list of installed apps',
                    command=self._apps_list_command,
                    cwd=self._apps_list_command_cwd)
        run_command(title='truncate rclone copy log file',
                    command=self._truncate_log_command,
                    cwd='/')
        copy_command_args = {
            'seconds_passed_from_last_run_start': seconds_passed_from_time_stamp_till_now(
                self._state_manager.get('last_run_start_time_stamp', '')
            ),
            **self._copy_command_args
        }
        copy_command = rclone_copy_files(**copy_command_args)
        run_start_time_stamp = time_stamp()
        await run_command_with_retries(title='copy files to cloud',
                                       command=copy_command,
                                       retry_interval=self._copy_command_retry_interval,
                                       cwd=self._copy_command_cwd)
        self._state_manager.set(
            key='last_run_start_time_stamp',
            value=run_start_time_stamp
        )


class SyncDeletionsOfFilesToCloud(Service):
    class SyncCommandArguments(TypedDict):
        destination: str
        backup_dir: str
        log_file: str
        filters: str
        additional_rclone_flags: str

    def __init__(self,
                 run_interval: int,
                 state: State,
                 state_key_prefix: str,
                 sync_command_cwd: str,
                 sync_command_retry_interval: int,
                 sync_command_args: SyncCommandArguments):
        super().__init__(run_interval, state, state_key_prefix)
        self._sync_command_cwd = sync_command_cwd
        self._sync_command_retry_interval = sync_command_retry_interval
        self._sync_command = rclone_sync_deletions(**sync_command_args)
        self._truncate_log_command = truncate_file(sync_command_args['log_file'])

    async def _body(self):
        run_command(title='truncate rclone sync log file',
                    command=self._truncate_log_command,
                    cwd='/')
        await run_command_with_retries(title='sync deletes and renames to cloud',
                                       command=self._sync_command,
                                       retry_interval=self._sync_command_retry_interval,
                                       cwd=self._sync_command_cwd)
