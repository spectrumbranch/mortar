"""
This package provides tools for working with images.
"""

from PIL import ImageShow

from .detector import Detector, ImageNotFoundError
from .image import Image
from .text import create_text
from .viewer import Viewer

__all__ = ['Image', 'create_text', 'Detector', 'ImageNotFoundError']

ImageShow.register(Viewer(), 0)  # pyright: ignore[reportUnknownMemberType]
