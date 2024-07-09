import os
import sys

from mortar.path import win_from_wsl
import mortar.process as process

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


def ocr(path_) -> str:
    """ Generate OCR text from an image in the same way MORT does. """

    path = win_from_wsl(path_)
    out_stem = 'out'
    out_name = f'{out_stem}.txt'

    process.run(_tess_cmd + [path, out_stem])

    with open(out_name, 'r') as fi:
        result = fi.read()

    os.remove(out_name)

    return result


def main() -> None:
    if len(sys.argv) < 2:
        raise Exception('path to image file is required')

    print(ocr(sys.argv[1]))


if __name__ == '__main__':
    main()
