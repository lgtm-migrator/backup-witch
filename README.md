<h1 align="center" style="border-bottom: none;">backup-witch</h1>
<h3 align="center">rclone backup automation tool</h3>

**backup-witch** is an easily configurable and extendable tool for performing continuous
automated backup of data with **rclone**.

Made with **python** and **bash**.

## How it works

**backup-witch** performs backup in three step:

1. Saves file, containing a list of installed apps (apt, snap, flatpak)
2. Runs ***rclone copy*** to copy files from source to destination, old versions of files are moved to destination_previous
4. Runs ***rclone move*** to match destination to source, files deleted on source are moved to destination_previous

## System requirements

Any **Linux** distro, supported by **rclone**, with several things installed:

+ For backup functionality:
    + python3
    + rclone

+ For notifying about errors:
    + notify-send

## Prerequisites

You will need to have a properly configured rclone remote to serve as backup destination.

More info -> https://rclone.org/docs/

## How to run

### Configure

To run **backup-witch**, first copy *sample_configs* folder to *src* folder and rename it to **configs**

```bash
cp -r sample_config src/config
```

Then set appropriate rclone remote as backup destination.

Corresponding config option will be in *src/config/paths.py*.

Set this option to complete path of folder on remote, without trailing slash. For example:

***src/config/paths.py***

```python
BACKUP_WITCH_DESTINATION = "dropbox:backup-witch" 
```

Now you can modify any other config options you wish to change.

### Plain run

Use _main.py_ to run **backup-witch**.

### Running as systemd service

To run **backup-witch** as **systemd** service use provided utility script _systemd-init.sh_

It will create a backup-witch.service in _~/.config/systemd/user/_, creating any required dirs automatically.

After that enable backup-witch.service

```shell
systemctl --user enable backup-witch.service
```

And start it

```shell
systemctl --user start backup-witch.service
```
