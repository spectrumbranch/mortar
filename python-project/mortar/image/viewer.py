"""
This module configures the default image viewer for the Pillow library.
"""

import os
import subprocess
from tempfile import NamedTemporaryFile
from typing import Any

from PIL.Image import Image as PILImage

if 'MORTAR_VIEWER' in os.environ:
    _viewer = os.environ['MORTAR_VIEWER']
else:
    _viewer = 'feh'


class Viewer:
    """
    Default image viewer for systems that don't have the existing PIL defaults
    available.
    """

    def show(self, image: PILImage, **options: Any) -> bool:
        """
        Implements PIL.ImageShow.show for the viewer.

        Save the image to a temporary file. Open the image file in the viewer
        and return the status.
        """

        with NamedTemporaryFile(suffix='.png') as file:
            image.save(file.name)

            return subprocess.run([_viewer, file.name]).returncode == 0
