from src.settings import Configuration, UNIX_HOME_FOLDER

CONFIG = Configuration(
    BACKUP_SOURCE=UNIX_HOME_FOLDER,

    BACKUP_DESTINATION_LATEST='example-remote:@backup-witch/latest',

    BACKUP_DESTINATION_PREVIOUS='example-remote:@backup-witch/previous',
)
