from PIL import ImageShow

from .filter import Filter
from .image import Crop, Gray, Invert
from .ocr import OCR
from .threshold import Threshold
from .viewer import Viewer

__all__ = ['Crop', 'Filter', 'Gray', 'Invert', 'OCR', 'Threshold']

ImageShow.register(Viewer())
