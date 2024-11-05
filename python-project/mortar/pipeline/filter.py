"""
This module provides pipeline filters.

A filter accepts an input, performs an operation on it, and returns the
processed output.
"""

import os
from typing import Any, Optional

import cv2 as cv
import numpy as np
import PIL
from PIL import ImageChops
from PIL.Image import Image as PILImage

from mortar.tesseract import ocr
from mortar.util import mktemp


class Filter:
    """
    Base class which any image filter inherits.
    """

    name = 'Filter'
    enabled = True

    def __init__(self) -> None:
        self.enabled = True

    def info(self) -> str:
        """ Return the name of the filter. """
        return self.name

    def run(self, input: PILImage) -> Any:
        """ Run the filter and return the resulting image. """
        return None


class Crop(Filter):
    """ Crop an image to a specified box. """
    name = 'Crop'

    def __init__(self, coords: tuple[int, int, int, int]) -> None:
        self._coords = coords

    def info(self) -> str:
        return f'{self.name} box={self._coords}'

    def run(self, input: PILImage) -> Optional[PILImage]:
        return input.crop(self._coords)

    def __repr__(self) -> str:
        return (f'<{self.__class__.__module__} {self.__class__.__name__}'
                f' coords={self._coords} at 0x{id(self):X}>')


class Gray(Filter):
    """ Convert an image to 8-bit grayscale mode. """

    name = 'Gray'

    def run(self, input: PILImage) -> Optional[PILImage]:
        return input.convert("L")


class Invert(Filter):
    """ Invert an image channel. """

    name = 'Invert'

    def run(self, input: PILImage) -> Optional[PILImage]:
        return ImageChops.invert(input)


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


class Threshold(Filter):
    """
    Perform thresholding on an image.
    Must be a grayscale image (image.mode in ['1', 'L'])
    """
    name = 'Threshold'

    def __init__(self,
                 threshval: float = 127,
                 maxval: float = 255,
                 invert: bool = False):
        self.threshval = threshval
        self.maxval = maxval
        self.invert = invert

    def run(self, input: PILImage) -> Optional[PILImage]:
        img = np.array([input.getdata()], dtype='uint8')

        if input.mode not in ['1', 'L']:
            return None

        thresh_type = cv.THRESH_BINARY_INV if self.invert else cv.THRESH_BINARY
        _, thresh = cv.threshold(img, self.threshval, self.maxval, thresh_type)

        return PIL.Image.frombytes('L', input.size, bytes(thresh))
