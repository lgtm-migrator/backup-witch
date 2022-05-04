from src.utils import BashScript


class RcloneMatchDestinationToSourceScript(BashScript):
    def __init__(self,
                 source: str,
                 destination: str,
                 backup_dir: str,
                 time_stamp: str,
                 log_file: str,
                 filters: str = '',
                 additional_rclone_flags: str = ''):
        code = f'''
        source_listing=$(rclone lsf -R --files-only --links {filters} "{source}")
        destination_listing=$(rclone lsf -vv -R --files-only --links "{destination}")
        files_to_move=$(comm -13 <(sort <(echo -e "$source_listing")) <(sort <(echo -e "$destination_listing")))
        set -o pipefail
        rclone move "{destination}" \
        "{backup_dir}/{time_stamp}" \
        --files-from-raw <(echo -e "$files_to_move") \
        {additional_rclone_flags}\
        2>&1 \
        | tee "{log_file}"
        '''
        super().__init__('rclone-match-destination-to-source', code)
