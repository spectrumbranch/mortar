from typing import Any

import PIL.Image
from PIL import ImageDraw

from mortar.font import Font, text_size
from mortar.image.image import Image


def create_text(
    text: str,
    font: Font,
    fill_color: str | None = None,
    margin: tuple[int, int] = (0, 0),
    *image_args: Any,
    **image_kwargs: Any
) -> Image:
    """
    Draw a text string onto a new Image and return it. A Font object is
    required. Optionally, a fill color and horizontal and vertical margins can
    be specified.

    Extra arguments are passed verbatim to the PIL.Image.new function.
    """

    text_size_ = text_size(text, font)

    image_size = (
        round(text_size_[0]) + margin[0] * 2,
        round(text_size_[1]) + margin[1] * 2,
    )

    image = PIL.Image.new('RGB', image_size, *image_args, **image_kwargs)

    draw = ImageDraw.Draw(image)

    draw.text(  # pyright: ignore[reportUnknownMemberType]
        margin, text, fill=fill_color, font=font
    )

    return Image.from_pil_image(image)
