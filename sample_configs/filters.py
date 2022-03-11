_exclude = ' '.join([
    # global
    '--filter "- venv/**"',
    '--filter "- env/**"',
    '--filter "- .flatpak-builder/**"',
    '--filter "- node_modules/**"',
    '--filter "- __pycache__/**"',
    '--filter "- .Trash-1000/**"',
    # relative
    '--filter "- /.local/share/Trash/**"',
])

_include = ' '.join([
    '--filter "+ /**"',
])

_dont_include_anything_else = '--filter "- **"'

RCLONE_FILTER = f'{_exclude} {_include} {_dont_include_anything_else}'
