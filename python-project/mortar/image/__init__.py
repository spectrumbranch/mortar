"""
This package provides tools for working with images.
"""

from PIL import ImageShow
from PIL import Image

from .text import create_text
from .viewer import Viewer

__all__ = ['Image', 'create_text']

ImageShow.register(Viewer(), 0)
