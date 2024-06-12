from os.path import isfile
import platform
from tempfile import mkstemp
import time


_windows_temp = '/mnt/c/Windows/Temp'


def system() -> str:
    if isfile('/proc/sys/fs/binfmt_misc/WSLInterop'):
        return 'wsl'
    else:
        return platform.system()


def mktemp(*args, **kwargs) -> str:
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
