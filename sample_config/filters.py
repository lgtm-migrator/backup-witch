from . import paths

from pathlib import PurePath

_exclude = ' '.join([
    # global
    '--filter "- venv/**"',
    '--filter "- env/**"',
    '--filter "- .flatpak-builder/**"',
    '--filter "- node_modules/**"',
    '--filter "- __pycache__/**"',
    '--filter "- .Trash-1000/**"',
    '--filter "- .cache/**"',
    '--filter "- .config/*/Cache/**"',
    '--filter "- .config/*/Code Cache/**"',
    '--filter "- .config/*/GPUCache/**"',
    '--filter "- .config/*/CachedData/**"',
    '--filter "- .config/*/Service Worker/**"',
    '--filter "- Cache/Cache_Data/**"',
    '--filter "- Code Cache/js/**"',
    '--filter "- Code Cache/wasm/**"',
    '--filter "- Service Worker/CacheStorage/**"',
    '--filter "- Service Worker/ScriptCache/**"',
    # relative
    '--filter "- /.local/share/Trash/**"',
    '--filter "- /.mozilla/firefox/*/storage/**"',
    '--filter "- /.var/app/*/cache/**"',
    # absolute
    f'--filter "- {PurePath(paths.STATE_FILE).name}"',
    f'--filter "- {PurePath(paths.PYTHON_LOG).name}"',
    f'--filter "- {PurePath(paths.RCLONE_COPY_LOG).name}"',
    f'--filter "- {PurePath(paths.RCLONE_MATCH_LOG).name}"',
])

_include = ' '.join([
    '--filter "+ /**"',
])

_dont_include_anything_else = '--filter "- **"'

RCLONE_FILTER = f'{_exclude} {_include} {_dont_include_anything_else}'
