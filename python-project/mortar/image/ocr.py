from tempfile import NamedTemporaryFile

from PIL.Image import Image

from .image import Filter
from ..tesseract import ocr


class OCR(Filter):
    def run(self, input: Image) -> str:
        with NamedTemporaryFile(suffix='.png') as fi:
            input.save(fi.name)

            result = ocr(fi.name)

        return result


