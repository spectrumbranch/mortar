from typing import Any, Optional

from PIL import ImageDraw
import PIL.Image
from PIL.Image import Image as PILImage

from mortar.font import Font, text_size


def create_text(
    text: str,
    font: Font,
    fill_color: Optional[str] = None,
    margin: tuple[int, int] = (0, 0),
    *image_args: Any,
    **image_kwargs: Any
) -> PILImage:
    text_size_ = text_size(text, font)

    image_size = (
        round(text_size_[0]) + margin[0] * 2,
        round(text_size_[1]) + margin[1] * 2,
    )

    image = PIL.Image.new('RGB', image_size, *image_args, **image_kwargs)

    draw = ImageDraw.Draw(image)

    draw.text(margin, text, fill=fill_color, font=font)

    return image
