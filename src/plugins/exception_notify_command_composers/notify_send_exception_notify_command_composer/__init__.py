from src.settings import Configuration


def notify_send_exception_notify_command_composer(config: Configuration) -> str:
    return (
        f'notify-send "backup_witch" "Exception Occurred\n'
        f'Check log -> {config.PYTHON_LOG_FILE}" -u critical'
    )
