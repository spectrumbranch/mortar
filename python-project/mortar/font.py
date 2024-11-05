"""
This module provides font management.
"""

from importlib import resources

from PIL import ImageFont
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
