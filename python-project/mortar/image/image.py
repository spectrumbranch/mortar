from typing import Optional

from PIL import ImageChops
from PIL.Image import Image as PILImage

from .filter import Filter
from .threshold import Threshold

__all__ = ['Crop', 'Gray', 'Invert', 'Threshold']


class Crop(Filter):
    name = 'Crop'

    def __init__(self, coords: tuple[int, int, int, int]) -> None:
        self._coords = coords

    def info(self) -> str:
        return f'{self.name} box={self._coords}'

    def run(self, input: PILImage) -> Optional[PILImage]:
        return input.crop(self._coords)


class Gray(Filter):
    name = 'Gray'

    def run(self, input: PILImage) -> Optional[PILImage]:
        return input.convert("L")


class Invert(Filter):
    name = 'Invert'

    def run(self, input: PILImage) -> Optional[PILImage]:
        return ImageChops.invert(input)
