<h1 align="center" style="border-bottom: none;">backup-witch</h1>
<h3 align="center">rclone backup automation tool</h3>

**backup-witch** is an easily configurable and extendable backup script for performing regular
automated backups of data from user home folder to remote destination.

Made with **rclone**, **python** and **bash**.
## How it works

**backup-witch** performs backup in three steps.

1. Generates and saves a text file containing list of installed apps
2. Runs *rclone copy* to copy new files and modifications of existing files to remote destination
3. Runs *rclone sync* to sync local file system structure to remote destination, i.e. deletions of files

## Script structure

+ *main.py* - script start file, where all services get initialized and run
+ *services.py* - contains code of each service
+ *commands.py* - contains bash command composers, for every designated action
+ *utils.py* - contains utility functions and classes

## System requirements

Any **Debian** based distro with several things installed, if you don't want to modify the script.

For backup functionality: 
+ python3
+ rclone

For generating a list of installed apps:
+ snapd
+ flatpak
+ apt

For notifying about errors:
+ notify-send

If you have skills in **python** and **bash** scripting, you can easily adjust **backup-witch** 
according to your use case and needs.

Backup functionality requires only python3 and rclone. So possibly can even work on Windows. 

## Prerequisites

You will need a properly configured rclone remote to be used as backup destination.

More info -> https://rclone.org/docs/

## How to run

To run **backup-witch**, first copy *sample_configs* folder to *src* folder and rename it to **configs**

```bash
cp -r sample_configs src/configs
```

Then set appropriate configs, and modify any you wish to change.

After that use _main.py_ to run **backup-witch**.

You can use it in combination with systemd, to create a systemd service.