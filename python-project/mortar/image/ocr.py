from tempfile import NamedTemporaryFile

from PIL import Image, ImageDraw
from PIL.Image import Image as PILImage

from .filter import Filter
from ..tesseract import ocr


class OCR(Filter):
    def run(self, input: PILImage) -> PILImage:
        with NamedTemporaryFile(suffix='.png') as fi:
            input.save(fi.name)

            try:
                result = ocr(fi.name)
            except Exception:
                result = Image.new(input.mode, input.size)

                draw = ImageDraw.Draw(result)

                band_count = len(result.getbands())

                if band_count == 1:
                    fill = 128
                elif band_count == 3:
                    fill = (128, 128, 128)
                else:
                    raise Exception("todo")

                draw.text((10, 10), 'OCR failed', fill=fill, font_size=48)

        return result
