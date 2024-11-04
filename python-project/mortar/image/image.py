"""
This module provides several common image filters.
"""

from typing import Optional

from PIL import ImageChops
from PIL.Image import Image as PILImage

from .filter import Filter
from .threshold import Threshold

__all__ = ['Crop', 'Gray', 'Invert', 'Threshold']


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