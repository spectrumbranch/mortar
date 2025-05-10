"""
This module provides miscellaneous utilities that don't obviously fit into
other existing modules.
"""

import platform
import time
from os import PathLike
from os.path import isfile
from tempfile import mkstemp
from typing import Any

_windows_temp = '/mnt/c/Windows/Temp'


def system() -> str:
    """
    Return a string representing the host system. This is either 'wsl' for a
    WSL system, or another string determined by the Python platform.system()
    function.
    """

    if isfile('/proc/sys/fs/binfmt_misc/WSLInterop'):
        return 'wsl'
    else:
        return platform.system()


def mktemp(
    suffix: str | None = None,
    prefix: str | None = None,
    dir: str | PathLike[str] | None = None,
    **kwargs: Any  # pyright: ignore[reportAny,reportExplicitAny]
) -> str:
    """
    Make a temporary file, taking the host system into account.

    If the host system is WSL, the file is created in the global Windows
    temporary directory.

    Otherwise, this function delegates to tempfile.mkstemp. args and kwargs are
    passed through.
    """

    if system() == 'wsl':
        now = time.time()

        if suffix is None:
            suffix = ''

        output_path = f'{_windows_temp}/{now}{suffix}'

        _ = open(output_path, 'w')
    else:
        _, output_path = mkstemp(suffix, prefix, dir, **kwargs)  # pyright: ignore[reportAny] # noqa: E501

    return output_path
