"""
This module provides font management.
"""
from os.path import isfile

import PIL.Image
from mktech.error import Err, Ok
from mktech.resources import resource_path
from PIL import ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

Font = FreeTypeFont


def load(path: str, size: int) -> Font:
    """
    Load a font from the specified file in mortar.resources.fonts. It is an
    error if the file does not exist.
    """

    match resource_path('mortar.resources.fonts', path):
        case Err(e):
            raise e
        case Ok(font_path):
            if not isfile(font_path):
                raise FileNotFoundError(f"Could not load font {path}.")

            result = ImageFont.truetype(str(font_path), size=size)

    return result


def text_size(text: str, font: Font) -> tuple[float, float]:
    """
    Calculate the dimensions required to display a string using a given font.
    Returns a tuple representing (width, height) of the string, in pixels.
    """

    draw = ImageDraw.Draw(PIL.Image.new('RGB', (0, 0)))

    lines = text.split('\n')

    lengths = [draw.textlength(it, font=font) for it in lines]

    return (float(max(lengths)), font.size * len(lines))
