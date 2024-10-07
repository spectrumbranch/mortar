from typing import Optional

import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import PIL
from PIL.Image import Image as PILImage

from .filter import Filter


class Threshold(Filter):
    name = 'Threshold'

    def run(self, input: PILImage) -> Optional[PILImage]:
        img = np.array([input.getdata()], dtype='uint8')
        ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
        ret, thresh2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
        ret, thresh3 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
        ret, thresh4 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)
        ret, thresh5 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)
        titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO',
                  'TOZERO_INV']
        images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
        for i in range(6):
            plt.subplot(2, 3, i + 1)
            plt.imshow(images[i], 'gray', vmin=0, vmax=255)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])

        return PIL.Image.frombytes('L', input.size, bytes(thresh1))
