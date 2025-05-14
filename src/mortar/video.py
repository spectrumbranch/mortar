"""
This module extracts screenshots from a collection of video files.
"""

from os import makedirs, walk
from pathlib import Path

from mortar.config import get_config
from mortar.process import run


def _flatten(entry: tuple[str, list[str], list[str]]) -> list[Path]:
    dir = entry[0]
    files = entry[2]

    return [Path(dir, file) for file in files]


def _files(input_path: Path | None) -> list[Path]:
    """
    Collects a list of the filepaths for all files in `input`, else
    `config.data`.

    Assumes filepaths are WSL for passing into ffmpeg.
    """

    config = get_config()

    data = Path(config.data) if input_path is None else input_path

    top = Path(data, 'jp')

    dirs = list(walk(top))

    with_files = list(filter(lambda x: len(x[2]) != 0, dirs))

    files = [_flatten(x) for x in with_files]

    flat_files = [x for xs in files for x in xs]

    return flat_files


def extract_frames(input_path: Path | None = None) -> int:
    """
    For each of the mkv files in the dataset, extract png images from the file
    at a rate of 1 image per second.

    Reads optional terminal argument `-i/--input INPUT`.

    Assumes that videos must be in an `INPUT/jp` subfolder.
    """

    files = _files(input_path)

    mkv_files = list(filter(lambda x: x.suffix == '.mkv', files))

    failed = False

    for index, file in enumerate(mkv_files):
        parent = file.parent
        out_dir = Path(parent, 'png')
        out_template = Path(out_dir, f'{file.stem}-%04d.png')

        makedirs(out_dir, exist_ok=True)

        command = [
            'ffmpeg',
            '-i',
            file,
            '-r',
            '1',
            out_template,
            '-loglevel',
            'error'
        ]

        print(f'{file.name}... ({index + 1}/{len(mkv_files)})')

        process_exit_code = run(command).returncode

        if process_exit_code != 0:
            failed = True

    return 1 if failed else 0
