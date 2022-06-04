from src.utils.bash_utils import BashScript


class RcloneMatchDestinationToSourceScript(BashScript):
    def __init__(
        self,
        source: str,
        destination: str,
        backup_dir: str,
        time_stamp: str,
        log_file: str,
        filter_flags: str = "",
        additional_rclone_flags: str = "",
    ):
        code = f"""
        source_listing=$(rclone lsf -R --files-only {filter_flags} "{source}")
        destination_listing=$(rclone lsf -R --files-only "{destination}")
        files_to_move=$(comm -13 <(sort <(echo -e "$source_listing")) <(sort <(echo -e "$destination_listing")))
        if [[ $files_to_move ]]; then
            set -o pipefail
            rclone move "{destination}" "{backup_dir}/{time_stamp}" \
            --files-from-raw <(echo -e "$files_to_move") \
            {additional_rclone_flags}\
            2>&1 \
            | tee "{log_file}"
        fi
        """
        super().__init__("rclone-match-destination-to-source", code)
