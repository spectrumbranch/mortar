"""
This module provides the Threshold filter.
"""

from typing import Optional

import cv2 as cv
import numpy as np
import PIL
from PIL.Image import Image as PILImage

from .filter import Filter


class Threshold(Filter):
    """
    Perform thresholding on an image.
    """
    name = 'Threshold'

    def run(self,
            input: PILImage,
            threshval: float = 127,
            maxval: float = 255,
            invert: bool = False) -> Optional[PILImage]:
        img = np.array([input.getdata()], dtype='uint8')

        thresh_type = cv.THRESH_BINARY_INV if invert else cv.THRESH_BINARY
        ret, thresh = cv.threshold(img, threshval, maxval, thresh_type)

        return PIL.Image.frombytes('L', input.size, bytes(thresh))
