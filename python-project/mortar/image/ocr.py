"""
This module provides the OCR filter.
"""

import os

from PIL.Image import Image as PILImage

from mortar.util import mktemp

from .filter import Filter
from ..tesseract import ocr


class OCR(Filter):
    """ Perform OCR on an image. """

    name = 'OCR'

    def run(self, input: PILImage) -> str:
        """
        Perform OCR on an image and return the result.
        """

        output_path = mktemp(suffix='.png')

        input.save(output_path)

        ocr_text = ocr(output_path)

        os.remove(output_path)

        return ocr_text
