"""
This module provides an Image class to be used for reading, writing, and
manipulating images.
"""

from typing import Any, override

import PIL.Image
from PIL import ImageChops


class Image:
    """
    This class represents an image object. It's a convenience wrapper around
    the pillow library's Image class.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.pil_image: PIL.Image.Image = PIL.Image.Image()
        " The instance of PIL.Image.Image wrapped by the Image object. "

    def convert(self, *args: Any, **kwargs: Any) -> 'Image':
        """
        See [PIL.Image.Image.convert](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.convert)
        """  # noqa: E501
        self.pil_image = self.pil_image.convert(*args, **kwargs)

        return self

    def copy(self) -> 'Image':
        """
        See [PIL.Image.Image.copy](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.copy)
        """  # noqa: E501
        return self.from_pil_image(self.pil_image.copy())

    def crop(self, *args: Any, **kwargs: Any) -> 'Image':
        """
        See [PIL.Image.Image.crop](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.crop)
        """  # noqa: E501
        self.pil_image = self.pil_image.crop(*args, **kwargs)

        return self

    def getdata(self, *args: Any, **kwargs: Any) -> Any:
        """
        See [PIL.Image.Image.getdata](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.getdata)
        """  # noqa: E501
        return self.pil_image.getdata(*args, **kwargs)

    def getpixel(self, xy: tuple[int, int]) -> Any:
        """
        See [PIL.Image.Image.getpixel](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.getpixel)
        """  # noqa: E501
        return self.pil_image.getpixel(xy)

    def paste(self, image: 'Image', *args: Any, **kwargs: Any) -> None:
        """
        See [PIL.Image.Image.paste](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.paste)
        """  # noqa: E501
        self.pil_image.paste(image.pil_image, *args, **kwargs)

    def resize(self, *args: Any, **kwargs: Any) -> 'Image':
        """
        See [PIL.Image.Image.resize](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
        """  # noqa: E501
        self.pil_image = self.pil_image.resize(*args, **kwargs)

        return self

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        See [PIL.Image.Image.save](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save)
        """  # noqa: E501
        self.pil_image.save(*args, **kwargs)

    def show(self, *args: Any, **kwargs: Any) -> None:
        """
        See [PIL.Image.Image.show](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.show)
        """  # noqa: E501
        self.pil_image.show(*args, **kwargs)

    def tobytes(self, *args: Any, **kwargs: Any) -> bytes:
        """
        See [PIL.Image.Image.tobytes](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.tobytes)
        """  # noqa: E501
        return self.pil_image.tobytes(*args, **kwargs)

    @property
    def mode(self) -> str:
        """
        See [PIL.Image.Image.mode](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.mode)
        """  # noqa: E501
        return self.pil_image.mode

    @property
    def size(self) -> tuple[int, int]:
        """
        See [PIL.Image.Image.size](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.size)
        """  # noqa: E501
        return self.pil_image.size

    @classmethod
    def effect_mandelbrot(cls, *args: Any, **kwargs: Any) -> 'Image':
        """
        See [PIL.Image.effect_mandelbrot](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.effect_mandelbrot)
        """  # noqa: E501
        return cls.from_pil_image(PIL.Image.effect_mandelbrot(*args, **kwargs))

    @classmethod
    def fromarray(cls, *args: Any, **kwargs: Any) -> 'Image':
        """
        See [PIL.Image.fromarray](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.fromarray)
        """  # noqa: E501
        return cls.from_pil_image(PIL.Image.fromarray(*args, **kwargs))

    @classmethod
    def frombytes(cls, *args: Any, **kwargs: Any) -> 'Image':
        """
        See [PIL.Image.frombytes](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.frombytes)
        """  # noqa: E501
        return cls.from_pil_image(PIL.Image.frombytes(*args, **kwargs))

    @classmethod
    def linear_gradient(cls, *args: Any, **kwargs: Any) -> 'Image':
        """
        See [PIL.Image.linear_gradient](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.linear_gradient)
        """  # noqa: E501
        return cls.from_pil_image(PIL.Image.linear_gradient(*args, **kwargs))

    @classmethod
    def invert(cls, image: 'Image') -> 'Image':
        """
        See [PIL.ImageChops.invert](https://pillow.readthedocs.io/en/stable/reference/ImageChops.html#PIL.ImageChops.invert)
        """  # noqa: E501
        return cls.from_pil_image(ImageChops.invert(image.pil_image))

    @classmethod
    def new(cls, *args: Any, **kwargs: Any) -> 'Image':
        """
        See [PIL.Image.new](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.new)
        """  # noqa: E501
        return cls.from_pil_image(PIL.Image.new(*args, **kwargs))

    @classmethod
    def open(cls, *args: Any, **kwargs: Any) -> 'Image':
        """
        See [PIL.Image.open](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.open)
        """  # noqa: E501
        return cls.from_pil_image(PIL.Image.open(*args, **kwargs))

    @classmethod
    def from_pil_image(cls, pil_image: PIL.Image.Image) -> 'Image':
        """
        Given an instance of PIL.Image.Image, return a new Image object.
        """

        instance = cls()

        instance.pil_image = pil_image

        return instance

    @override
    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__module__} {self.__class__.__name__}'
            f' mode={self.pil_image.mode} size={self.pil_image.size}'
            f' at 0x{id(self):X}>'
        )
