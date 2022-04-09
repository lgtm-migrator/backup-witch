from utils import time_stamp


def rclone_copy_files(destination: str,
                      backup_dir: str,
                      log_file: str,
                      files_new_file: str,
                      additional_rclone_flags: str = '') -> str:
    command = f'rclone copy ./ {destination} ' \
              f'--backup-dir "{backup_dir}/{time_stamp()}" ' \
              f'--log-file={log_file} ' \
              f'{additional_rclone_flags} --links ' \
              f'--files-from-raw {files_new_file}'
    return command


def rclone_files_list(output_file: str, filters: str) -> str:
    command = f'rclone lsf ./ -R --files-only --links {filters} > {output_file}'
    return command


def save_list_of_installed_apps(output_file: str) -> str:
    apps_list = 'list=""'
    flatpak_list = f"list+=$(flatpak list --app)+$'\n'"
    snap_list = f"list+=$(snap list)+$'\n'"
    apt_list = f"list+=$(apt-mark showmanual)+$'\n'"
    divider = f"list+=$'---\n'"
    save_apps_list_to_file = f'echo "$list" >> {output_file}'
    command = f'{apps_list} ' \
              f'&& {flatpak_list} ' \
              f'&& {divider}' \
              f'&& {snap_list} ' \
              f'&& {divider} ' \
              f'&& {apt_list};' \
              f'if [[ "$(< {output_file})" != "$list" ]]; ' \
              f'then {truncate_file(output_file)} ' \
              f'&& {save_apps_list_to_file}; ' \
              f'fi'
    return command


def truncate_file(file_path: str) -> str:
    return f'truncate -s 0 {file_path}'
