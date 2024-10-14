import os

from mktech.io import eprint
from PIL import Image, ImageDraw
from PIL.Image import Image as PILImage
from PIL.ImageFont import FreeTypeFont

from mortar import font
from mortar.util import mktemp

from .filter import Filter
from ..tesseract import ocr

_font_name = 'reikofont'
_font_filename = 'reiko.ttf'
_font = font.load(_font_filename, 28)


class OCR(Filter):
    name = 'OCR'

    def run(self, input: PILImage) -> PILImage:
        result = Image.new(input.mode, input.size)

        draw = ImageDraw.Draw(result)

        band_count = len(result.getbands())

        fill: int | tuple[int, int, int]

        if band_count == 1:
            fill = 128
        elif band_count == 3:
            fill = (128, 128, 128)
        else:
            raise Exception("todo")

        output_path = mktemp(suffix='.png')

        input.save(output_path)

        try:
            if (not isinstance(_font, FreeTypeFont) or
                    _font.getname()[0] != _font_name):
                ocr_text = 'OCR font is not available'
            else:
                ocr_text = ocr(output_path)

            draw.text((10, 10), ocr_text, fill=fill, font=_font,
                      font_size=48)
        except Exception as ex:
            eprint(ex)
            draw.text((10, 10), 'OCR failed', fill=fill, font_size=48)

        os.remove(output_path)

        return result
