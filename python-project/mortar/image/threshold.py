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
