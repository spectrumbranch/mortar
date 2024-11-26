"""
This module provides an interface for performing OCR operations using
Tesseract.

The Tesseract instance may be invoked either locally, or on a remote host over
an SSH connection.
"""

import os
from pathlib import PurePath
import shlex
import sys
from tempfile import mkstemp

from mortar.config import config
from mortar.path import win_from_wsl
import mortar.process as process
from mortar.ssh import SSH

_tess_env = {
    'command': os.environ['TESSERACT'],
    'data': os.environ['TESSERACT_DATA']
}

_tess_cmd = [
    _tess_env['command'],
    '-l', 'jpn',
    '--tessdata-dir', f"{(_tess_env['data'])}",
    '--psm', '3',
    '--oem', '1'
]


def tesseract_ssh(path_: str) -> str:
    """
    Generate OCR text from an image using Tesseract, and return the string.

    Tesseract is executed on the remote host defined in configuration.
    """

    tess_cmd = (f"{_tess_env['command']}"
                f" -l jpn --tessdata-dir {shlex.quote(_tess_env['data'])}")

    ssh = SSH(host=config.ssh.host, port=config.ssh.port)
    path = PurePath(path_)

    temp_win = "C:/Windows/Temp"
    temp_nix = '/mnt/c/Windows/Temp'

    ssh.scp_to(str(path), f'{temp_nix}/{path.name}')
    ssh.run([tess_cmd + f' "{temp_win}\\{path.name}" "{temp_win}\\out"'])

    (_, out_path) = mkstemp()

    ssh.scp_from(f'{temp_nix}/out.txt', out_path)
    ssh.run(['rm', f'{temp_nix}/{path.name}'])

    with open(out_path, 'r') as fi:
        result = fi.read()

    os.remove(out_path)

    return result


def tesseract_wsl(path_: str) -> str:
    """
    Generate OCR text from an image using Tesseract, and return the string.

    This function assumes that the module is running in a WSL environment.
    When building the command line, it makes the path manipulations required to
    run Windows executables from WSL.
    """

    path = win_from_wsl(path_)
    out_stem = 'out'
    out_name = f'{out_stem}.txt'

    process.run(_tess_cmd + [path, out_stem])

    with open(out_name, 'r') as fi:
        result = fi.read()

    os.remove(out_name)

    return result


def ocr(path: str) -> str:
    """
    Generate OCR text from an image in the same way MORT does.

    If use_ssh = True in configuration, the operation is performed over an SSH
    connection. Otherwise, it is done in the local WSL environment.
    """

    if config.ssh.use_ssh:
        result = tesseract_ssh(path)
    else:
        result = tesseract_wsl(path)

    return result


def main() -> None:
    if len(sys.argv) < 2:
        raise Exception('path to image file is required')

    print(ocr(sys.argv[1]))


if __name__ == '__main__':
    main()
