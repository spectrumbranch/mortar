"""
This module provides an interface for performing OCR operations using
Tesseract.

The Tesseract instance may be invoked either locally, or on a remote host over
an SSH connection.
"""

import os
import shlex
from enum import StrEnum, auto
from pathlib import PurePath
from tempfile import mkstemp

import mortar.process as process
from mortar.path import win_from_wsl
from mortar.ssh import SSH

from .config import get_config


class ExecutionEnv(StrEnum):
    LOCAL = auto()
    SSH = auto()
    WSL = auto()


def _build_tess_cmd() -> list[str]:
    config = get_config()

    tessdata_dir: str | None = None
    command: str

    match config.execution_env:
        case (ExecutionEnv.LOCAL | ExecutionEnv.WSL):
            command = str(config.tesseract.bin_path)

            if config.tesseract.tessdata_dir is not None:
                tessdata_dir = str(config.tesseract.tessdata_dir)
        case ExecutionEnv.SSH:
            command = str(config.tesseract.ssh.bin_path)

            if config.tesseract.tessdata_dir is not None:
                tessdata_dir = str(config.tesseract.ssh.tessdata_dir)
        case _:
            raise NotImplementedError

    match config.execution_env:
        case ExecutionEnv.SSH:
            command = shlex.quote(command)

            if tessdata_dir is not None:
                tessdata_dir = shlex.quote(tessdata_dir)
        case _:
            pass

    result = [
        command,
        '-l', 'jpn',
        '--psm', '3',
        '--oem', '1',
    ]  # yapf: disable

    if tessdata_dir:
        result += ['--tessdata-dir', tessdata_dir]

    return result


def tesseract_ssh(command: list[str], path_: str) -> str:
    """
    Generate OCR text from an image using Tesseract, and return the string.

    Tesseract is executed on the remote host defined in configuration.
    """

    config = get_config()

    ssh = SSH(host=config.ssh.host, port=config.ssh.port)
    path = PurePath(path_)

    temp_win = "C:/Windows/Temp"
    temp_nix = '/mnt/c/Windows/Temp'

    _ = ssh.scp_to(str(path), f'{temp_nix}/{path.name}')
    _ = ssh.run(
        [' '.join(command) + f' "{temp_win}\\{path.name}" "{temp_win}\\out"']
    )

    (_, out_path) = mkstemp()

    _ = ssh.scp_from(f'{temp_nix}/out.txt', out_path)
    _ = ssh.run(['rm', f'{temp_nix}/{path.name}'])

    with open(out_path, 'r') as fi:
        result = fi.read()

    os.remove(out_path)

    return result


def tesseract(command: list[str], path_: str) -> str:
    """
    Generate OCR text from an image using Tesseract, and return the string.

    This function assumes that the module is running in a WSL environment.
    When building the command line, it makes the path manipulations required to
    run Windows executables from WSL.
    """

    config = get_config()

    match config.execution_env:
        case ExecutionEnv.WSL:
            path = win_from_wsl(path_)
        case _:
            path = path_

    out_stem = 'out'
    out_name = f'{out_stem}.txt'

    _ = process.run(command + [path, out_stem])

    with open(out_name, 'r') as fi:
        result = fi.read()

    os.remove(out_name)

    return result


def ocr(path: str) -> str:
    """
    Generate OCR text from an image using Tesseract, and return the string.

    TODO update

    If use_ssh = True in configuration, the operation is performed over an SSH
    connection. Otherwise, it is done in the local WSL environment.
    """

    config = get_config()

    command = _build_tess_cmd()

    match config.execution_env:
        case (ExecutionEnv.LOCAL | ExecutionEnv.WSL):
            result = tesseract(command, path)
        case ExecutionEnv.SSH:
            result = tesseract_ssh(command, path)
        case _:
            raise NotImplementedError

    return result


def print_ocr(path: str) -> None:
    """
    Generate OCR text from an image using Tesseract, and print the OCR result.
    """

    print(ocr(path))
