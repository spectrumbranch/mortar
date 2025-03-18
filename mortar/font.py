"""
This module provides font management.
"""

from importlib import resources

import PIL.Image
from PIL import ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

Font = FreeTypeFont


def load(path: str, size: int) -> Font:
    """
    Load a font from the specified file in mortar.resources.fonts. It is an
    error if the file does not exist.
    """

    font_resources = resources.files('mortar.resources.fonts')

    font = ImageFont.truetype(str(font_resources.joinpath(path)), size=size)

    if font is None:
        raise FileNotFoundError(f"Could not load font {path}.")

    return font


def text_size(text: str, font: Font) -> tuple[float, float]:
    """
    Calculate the dimensions required to display a string using a given font.
    Returns a tuple representing (width, height) of the string, in pixels.
    """

    draw = ImageDraw.Draw(PIL.Image.new('RGB', (0, 0)))

    lines = text.split('\n')

    lengths = [draw.textlength(it, font=font) for it in lines]

    return (float(max(lengths)), font.size * len(lines))
