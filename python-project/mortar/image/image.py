"""
This module provides several common image filters.
"""

from typing import Any

from PIL import ImageChops
import PIL.Image


class Image:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.pil_image = PIL.Image.Image()

    def convert(self, *args: Any, **kwargs: Any) -> 'Image':
        self.pil_image = self.pil_image.convert(*args, **kwargs)

        return self

    def copy(self) -> 'Image':
        self.pil_image = self.pil_image.copy()

        return self

    def crop(self, *args: Any, **kwargs: Any) -> 'Image':
        self.pil_image = self.pil_image.crop(*args, **kwargs)

        return self

    def getdata(self, *args: Any, **kwargs: Any) -> Any:
        return self.pil_image.getdata(*args, **kwargs)

    def getpixel(self, xy: tuple[int, int]) -> Any:
        return self.pil_image.getpixel(xy)

    def paste(self, image: 'Image', *args: Any, **kwargs: Any) -> None:
        self.pil_image.paste(image.pil_image, *args, **kwargs)

    def resize(self, *args: Any, **kwargs: Any) -> 'Image':
        self.pil_image = self.pil_image.resize(*args, **kwargs)

        return self

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.pil_image.save(*args, **kwargs)

    def show(self, *args: Any, **kwargs: Any) -> None:
        self.pil_image.show(*args, **kwargs)

    def tobytes(self, *args: Any, **kwargs: Any) -> bytes:
        return self.pil_image.tobytes(*args, **kwargs)

    @property
    def mode(self) -> str:
        return self.pil_image.mode

    @property
    def size(self) -> tuple[int, int]:
        return self.pil_image.size

    @classmethod
    def effect_mandelbrot(cls, *args: Any, **kwargs: Any) -> 'Image':
        return cls.from_pil_image(PIL.Image.effect_mandelbrot(*args, **kwargs))

    @classmethod
    def fromarray(cls, *args: Any, **kwargs: Any) -> 'Image':
        return cls.from_pil_image(PIL.Image.fromarray(*args, **kwargs))

    @classmethod
    def frombytes(cls, *args: Any, **kwargs: Any) -> 'Image':
        return cls.from_pil_image(PIL.Image.frombytes(*args, **kwargs))

    @classmethod
    def linear_gradient(cls, *args: Any, **kwargs: Any) -> 'Image':
        return cls.from_pil_image(PIL.Image.linear_gradient(*args, **kwargs))

    @classmethod
    def invert(cls, image: 'Image') -> 'Image':
        return cls.from_pil_image(ImageChops.invert(image.pil_image))

    @classmethod
    def new(cls, *args: Any, **kwargs: Any) -> 'Image':
        return cls.from_pil_image(PIL.Image.new(*args, **kwargs))

    @classmethod
    def open(cls, *args: Any, **kwargs: Any) -> 'Image':
        return cls.from_pil_image(PIL.Image.open(*args, **kwargs))

    @classmethod
    def from_pil_image(cls, pil_image: PIL.Image.Image) -> 'Image':
        instance = cls()

        instance.pil_image = pil_image

        return instance
