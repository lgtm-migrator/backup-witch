import pytest

from src.core.backup_service import BackupService


def test():
    with pytest.raises(TypeError):
        BackupService()
    # todo finish
