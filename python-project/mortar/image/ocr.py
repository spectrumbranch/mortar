from importlib import resources
from tempfile import NamedTemporaryFile

from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as PILImage

from .filter import Filter
from ..tesseract import ocr


_resources = resources.files('mortar.resources.fonts')

for it in _resources.iterdir():
    if it.name == 'reiko.ttf':
        with resources.as_file(it) as path:
            _reiko_font = ImageFont.truetype(str(path), size=28)


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

        with NamedTemporaryFile(suffix='.png') as fi:
            input.save(fi.name)

            try:
                ocr_text = ocr(fi.name)

                draw.text((10, 10), ocr_text, fill=fill, font=_reiko_font,
                          font_size=48)
            except Exception:
                draw.text((10, 10), 'OCR failed', fill=fill, font_size=48)

        return result
