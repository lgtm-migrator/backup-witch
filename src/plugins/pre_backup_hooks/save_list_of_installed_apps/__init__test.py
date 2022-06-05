from src.plugins.pre_backup_hooks.save_list_of_installed_apps import (
    SaveListOfInstalledAppsHook,
)


def test(tmp_path):
    output_file = tmp_path / "apps-list.txt"
    SaveListOfInstalledAppsHook(output_file.__str__())()
    assert output_file.exists()
    assert output_file.read_text()
