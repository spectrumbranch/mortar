from typing import Optional

from PIL import ImageChops
from PIL.Image import Image as PILImage

__all__ = ['Crop', 'Filter', 'Gray', 'Invert']


class Filter:
    name = 'Filter'
    enabled = True

    def __init__(self) -> None:
        self.enabled = True

    def info(self) -> str:
        return self.name

    def run(self, input: Image) -> Optional[Image]:
        return None


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
