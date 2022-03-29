from utils import time_stamp


def rclone_copy_files(destination: str,
                      backup_dir: str,
                      log_file: str,
                      files_new_file: str,
                      additional_rclone_flags: str = '') -> str:
    command = f'rclone copy ./ {destination} ' \
              f'--backup-dir {backup_dir}/{time_stamp()} ' \
              f'--log-file={log_file} ' \
              f'{additional_rclone_flags} --links ' \
              f'--files-from-raw {files_new_file}'
    return command


def rclone_files_list(output_file: str, filters: str) -> str:
    command = f'rclone lsf ./ -R --files-only --links {filters} > {output_file}'
    return command


def save_list_of_installed_apps(output_file: str) -> str:
    flatpak_list = f'flatpak list --app >> {output_file}'
    snap_list = f'snap list >> {output_file}'
    apt_list = f'apt-mark showmanual >> {output_file}'
    divider = f"echo '---' >> {output_file}"
    command = f'{truncate_file(output_file)} ' \
              f'&& {flatpak_list} ' \
              f'&& {divider} ' \
              f'&& {snap_list} ' \
              f'&& {divider} ' \
              f'&& {apt_list}'
    return command


def truncate_file(file_path: str) -> str:
    return f'truncate -s 0 {file_path}'
