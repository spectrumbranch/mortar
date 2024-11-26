"""
This module provides utilities for filesystem path manipulation.
"""

from pathlib import PurePath


def win_from_wsl(path: str) -> PurePath:
    """
    Convert an absolute path on a WSL system into the corresponding
    Windows path.
    """

    if not path.startswith('/mnt'):
        raise Exception('path is expected to be an absolute path on a WSL'
                        ' installation')

    parts = path.split('/')

    return PurePath(f'{parts[2]}:/{"/".join(parts[3:])}')
