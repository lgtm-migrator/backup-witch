from src.utils import BashScript


class SaveListOfInstalledAppsScript(BashScript):
    def __init__(self,
                 output_file: str):
        code = f'''
        list=$'---flatpak\n'
        list+=$(flatpak list --app)+$'\n'
        list+=$'---snap\n'
        list+=$(snap list)+$'\n'
        list+=$'---apt\n'
        list+=$(apt-mark showmanual)+$'\n'
        delta=$(comm -3 <(sort <(echo -e "$list")) <(sort "{output_file}"))
        if [[ $delta ]]; then
          echo -n "$list" > "{output_file}"
        fi
        '''
        super().__init__('save-list-of-installed-apps', code)
