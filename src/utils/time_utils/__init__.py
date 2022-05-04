from datetime import datetime, timezone


def time_stamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(' ', 'seconds')


def seconds_passed_from_time_stamp_till_now(stamp: str) -> int:
    t_now = datetime.now(timezone.utc).astimezone()
    if not stamp:
        return int(t_now.timestamp())
    t_of_stamp = datetime.fromisoformat(stamp).astimezone()
    return (t_now - t_of_stamp).seconds
