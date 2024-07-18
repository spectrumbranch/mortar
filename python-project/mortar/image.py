from typing import Optional

from PIL import ImageChops
from PIL.Image import Image

from mortar.pipeline import Stage

__all__ = ['Crop', 'Gray', 'Invert']


class Crop(Stage):
    def __init__(self, coords: tuple[int, int, int, int]) -> None:
        self._coords = coords

    def run(self, input: Image) -> Optional[Image]:
        return input.crop(self._coords)


class Gray(Stage):
    def run(self, input: Image) -> Optional[Image]:
        return input.convert("L")


class Invert(Stage):
    def run(self, input: Image) -> Optional[Image]:
        return ImageChops.invert(input)
