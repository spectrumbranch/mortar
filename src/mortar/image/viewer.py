"""
This module configures the default image viewer for the Pillow library.

If the environment variable `MORTAR_VIEWER` is set, its contents are used as
the path to the default image viewer.
"""

import os
import subprocess
from tempfile import NamedTemporaryFile

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
    def show(self, image: PILImage, **_options: object) -> bool:
        """
        Implements PIL.ImageShow.show for the viewer.

        Save the image to a temporary file. Open the image file in the viewer
        and return the status.
        """

        with NamedTemporaryFile(suffix='.png') as file:
            image.save(file.name)

            return subprocess.run([_viewer, file.name]).returncode == 0
