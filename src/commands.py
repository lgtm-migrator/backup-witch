from utils import time_stamp


def rclone_copy_files(destination: str,
                      backup_dir: str,
                      no_traverse_max_age: int,
                      seconds_passed_from_last_run_start: int,
                      log_file: str,
                      filters: str,
                      additional_rclone_flags: str = ''):
    flags = f'--max-age {seconds_passed_from_last_run_start}s {additional_rclone_flags}'
    if seconds_passed_from_last_run_start <= no_traverse_max_age:
        flags += ' --no-traverse'
    command = f'rclone copy ./ {destination} --backup-dir {backup_dir}/edits/{time_stamp()}' \
              f' --log-file={log_file} {flags} {filters}'
    return command


def rclone_sync_deletions(destination: str,
                          backup_dir: str,
                          log_file: str,
                          filters: str,
                          additional_rclone_flags: str = ''):
    flags = f'--max-transfer 0 --delete-before {additional_rclone_flags}'
    command = f'rclone sync ./ {destination} --backup-dir {backup_dir}/deletes/{time_stamp()}' \
              f' --log-file={log_file} {flags} {filters}'
    return command


def save_list_of_installed_apps(file_name: str = 'installed_apps.txt'):
    flatpak_list = f'flatpak list --app >> {file_name}'
    snap_list = f'snap list >> {file_name}'
    apt_list = f'apt-mark showmanual >> {file_name}'
    devider = f"echo '---' >> {file_name}"
    command = f'{truncate_file(file_name)} && {flatpak_list} && {devider} && {snap_list} && {devider} && {apt_list}'
    return command


def truncate_file(file_path: str):
    return f'truncate -s 0 {file_path}'
