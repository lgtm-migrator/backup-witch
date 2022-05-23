from src.bash_scripts.save_list_of_installed_apps import SaveListOfInstalledAppsScript
from src.utils.bash_utils import run_bash_script


def test(tmp_path):
    output_file = tmp_path / "apps-list.txt"
    run_bash_script(SaveListOfInstalledAppsScript(output_file.__str__()))
    assert output_file.exists()
    assert output_file.read_text()
