"""
This module provides image processing filters.

An image processing filter accepts an input image, performs an operation on it,
and returns the processed image.
"""

from PIL import ImageShow

from .filter import Filter
from .image import Crop, Gray, Invert
from .ocr import OCR
from .text import create_text
from .threshold import Threshold
from .viewer import Viewer

__all__ = ['Crop', 'Filter', 'Gray', 'Invert', 'OCR', 'Threshold',
           'create_text']

ImageShow.register(Viewer(), 0)
