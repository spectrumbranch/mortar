"""
This module provides pipeline filters.

A filter accepts an input, performs an operation on it, and returns the
processed output.
"""

from copy import copy
import os
from typing import Any, Optional

import cv2 as cv
from mktech.validate import ensure_type
import numpy as np

from mortar.image import Image
from mortar.tesseract import ocr
from mortar.util import mktemp


class Filter:
    """
    Base class which any image filter inherits.
    """

    name = 'Filter'
    enabled = True
    _input_type: Any = Any

    def __init__(self) -> None:
        self._input = None

        self.enabled = True

    def info(self) -> str:
        """ Return the name of the filter. """
        return self.name

    def run(self, input: Any) -> Any:
        """ Run the filter and return the resulting image. """

        ensure_type(input, self._input_type)

        self._input = copy(input)

        return None


class Crop(Filter):
    """ Crop an image to a specified box. """

    name = 'Crop'
    _input_type = Image

    def __init__(self, coords: tuple[int, int, int, int]) -> None:
        super().__init__()

        self._coords = coords

    def info(self) -> str:
        return f'{self.name} box={self._coords}'

    def run(self, input: Image) -> Optional[Image]:
        super().run(input)

        if self._input is None:
            result = None
        else:
            result = self._input.crop(self._coords)

        return result

    def __repr__(self) -> str:
        return (f'<{self.__class__.__module__} {self.__class__.__name__}'
                f' coords={self._coords} at 0x{id(self):X}>')


class Gray(Filter):
    """ Convert an image to 8-bit grayscale mode. """

    name = 'Gray'
    _input_type = Image

    def run(self, input: Image) -> Optional[Image]:
        super().run(input)

        if self._input is None:
            result = None
        else:
            result = self._input.convert("L")

        return result


class Invert(Filter):
    """ Invert an image channel. """

    name = 'Invert'
    _input_type = Image

    def run(self, input: Image) -> Optional[Image]:
        super().run(input)

        if self._input is None:
            result = None
        else:
            result = Image.invert(self._input)

        return result


class OCR(Filter):
    """ Perform OCR on an image. """

    name = 'OCR'
    _input_type = Image

    def run(self, input: Image) -> Optional[str]:
        """
        Perform OCR on an image and return the result.
        """

        super().run(input)

        if self._input is None:
            result = None
        else:
            output_path = mktemp(suffix='.png')

            self._input.save(output_path)

            result = ocr(output_path)

            os.remove(output_path)

        return result


class Threshold(Filter):
    """
    Perform thresholding on an image.
    Must be a grayscale image (image.mode in ['1', 'L'])
    """

    name = 'Threshold'
    _input_type = Image

    def __init__(self,
                 threshval: float = 127,
                 maxval: float = 255,
                 invert: bool = False) -> None:
        self.threshval = threshval
        self.maxval = maxval
        self.invert = invert

    def run(self, input: Image) -> Optional[Image]:
        super().run(input)

        if self._input is None or self._input.mode not in ['1', 'L']:
            result = None
        else:
            img = np.array([self._input.getdata()], dtype='uint8')

            thresh_type = (cv.THRESH_BINARY_INV if self.invert
                           else cv.THRESH_BINARY)
            _, thresh = cv.threshold(img, self.threshval, self.maxval,
                                     thresh_type)

            result = Image.frombytes('L', self._input.size, bytes(thresh))

        return result
