<h1 align="center" style="border-bottom: none;">backup-witch</h1>
<h3 align="center">rclone backup automation tool</h3>

**backup-witch** is an easily configurable and extendable backup script for performing regular
automated backups of data from user home folder to remote destination.

Made with **rclone**, **python** and **bash**.
## How it works

**backup-witch** performs backup in four steps.

1. Saves list of installed apps
2. Saves list of all files, i.e. source directory structure
3. Saves list of new files, i.e. a list of files for upload by current backup
   + This list includes new files, as well as existing files, which were modified since last backup
4. Runs *rclone copy* to copy files from source to backup destination

## Script structure

+ *main.py* - script start file
+ *services.py* - contains code for script services
+ *commands.py* - contains bash command composers, for every designated action
+ *utils.py* - contains utility functions and classes

## System requirements

Any **Debian** based distro with several things installed, **if you don't want to modify the script**.

Otherwise, you can easily adjust **backup-witch** according to your use case and needs.
Backup functionality most likely will work even on **Windows**.

### Dependencies

For backup functionality: 
+ python3
+ rclone

For generating a list of installed apps:
+ snapd
+ flatpak
+ apt

For notifying about errors:
+ notify-send

## Prerequisites

You will need to have a properly configured rclone remote for backup destination.

More info -> https://rclone.org/docs/

Corresponding config option in *cmd_args.py* is BACKUP_WITCH_DESTINATION.

Set this option to complete path of folder on remote, without trailing slash. For example: 

```python
BACKUP_WITCH_DESTINATION="dropbox:backup-witch" 
```

## How to run

### Configure

To run **backup-witch**, first copy *sample_configs* folder to *src* folder and rename it to **configs**

```bash
cp -r sample_configs src/configs
```

Then set appropriate configs, and modify any you wish to change.

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
