"""
This package provides tools for working with images.
"""

from PIL import ImageShow

from .image import Image
from .text import create_text
from .viewer import Viewer
from .detector import Detector

__all__ = ['Image', 'create_text', 'Detector']

ImageShow.register(Viewer(), 0)
