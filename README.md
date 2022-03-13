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

Any **Debian** based distro with several things installed.

For backup functionality: 
+ python 3
+ rclone

For generating a list of installed apps:
+ notify-send
+ snapd
+ flatpak
+ apt

## Prerequisites

You will need a properly configured rclone remote to be used as backup destination.

More info -> https://rclone.org/docs/
