"""
This module provides the base class for an image filter.
"""

from typing import Optional

from PIL.Image import Image as PILImage


class Filter:
    """
    Base class which any image filter inherits.
    """

    name = 'Filter'
    enabled = True

    def __init__(self) -> None:
        self.enabled = True

    def info(self) -> str:
        """ Return the name of the filter. """
        return self.name

    def run(self, input: PILImage) -> Optional[PILImage]:
        """ Run the filter and return the resulting image. """
        return None
