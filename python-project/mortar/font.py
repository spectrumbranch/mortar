from importlib import resources
from typing import Optional

from PIL import ImageFont
from PIL.ImageFont import ImageFont as PILImageFont, FreeTypeFont

from mortar import log

_resources = resources.files('mortar.resources.fonts')

Font = PILImageFont | FreeTypeFont


def load(path: str, size: int) -> Font:
    font: Optional[Font] = None

    for it in _resources.iterdir():
        if it.name == path:
            with resources.as_file(it) as resource_path:
                font = ImageFont.truetype(str(resource_path),
                                          size=size)

    if font is None:
        font = ImageFont.load_default(size)

        log.error(f"Could not load font {path}. Using system default.")

    return font
