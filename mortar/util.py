"""
This module provides miscellaneous utilities that don't obviously fit into
other existing modules.
"""

from os.path import isfile
import platform
from tempfile import mkstemp
import time


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


def mktemp(*args, **kwargs) -> str:
    """
    Make a temporary file, taking the host system into account.

    If the host system is WSL, the file is created in the global Windows
    temporary directory.

    Otherwise, this function delegates to tempfile.mkstemp. args and kwargs are
    passed through.
    """

    if system() == 'wsl':
        now = time.time()

        if 'suffix' not in kwargs:
            suffix = ''
        else:
            suffix = kwargs['suffix']

        output_path = f'{_windows_temp}/{now}{suffix}'

        open(output_path, 'w')
    else:
        (_, output_path) = mkstemp(*args, **kwargs)

    return output_path
