"""
This package provides tools for working with images.
"""

from PIL import ImageShow

from .detector import Detector
from .image import Image
from .text import create_text
from .viewer import Viewer

__all__ = ['Image', 'create_text', 'Detector']

ImageShow.register(Viewer(), 0)
