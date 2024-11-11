"""
This module is an application that extracts screenshots from a collection of
video files.
"""

import argparse
from os import makedirs, walk
from pathlib import Path

from mortar.config import config
from mortar.process import run


def _flatten(entry) -> list[Path]:
    dir = entry[0]
    files = entry[2]

    return [Path(dir, file) for file in files]


def _files(input: str) -> list[Path]:
    """
    Collects a list of the filepaths for all files in `input`,
    else `config.data`, else defaults to `'.'`.

    Assumes filepaths are WSL for passing into ffmpeg.
    """

    if input is not None:
        data = input
    elif config.data is not None:
        data = config.data
    else:
        data = '.'

    top = Path(data, 'jp')

    dirs = list(walk(top))

    with_files = list(filter(lambda x: len(x[2]) != 0, dirs))

    files = [_flatten(x) for x in with_files]

    flat_files = [x for xs in files for x in xs]

    return flat_files


def extract_frames() -> None:
    """
    For each of the mkv files in the dataset, extract png images from the file
    at a rate of 1 image per second.

    Reads optional terminal argument `-i/--input INPUT`.

    Assumes that videos must be in an `INPUT/jp` subfolder.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        help='input folder to look for video files in. Videos must be in'
             '`INPUT/jp` subfolder')
    args = parser.parse_args()
    input = args.input

    files = _files(input)

    mkv_files = list(filter(lambda x: x.suffix == '.mkv', files))

    for file in mkv_files:
        parent = file.parent
        out_dir = Path(parent, 'png')
        out_template = Path(out_dir, f'{file.stem}-%02d.png')

        makedirs(out_dir, exist_ok=True)

        command = ['ffmpeg', '-i', file, '-r', '1',
                   out_template, '-loglevel', 'error']

        print(f'{file.name}...')

        run(command)


def main() -> None:
    extract_frames()
