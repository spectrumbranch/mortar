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
    def show(self, image: PILImage, **options: Any) -> bool:
        with NamedTemporaryFile(suffix='.png') as file:
            image.save(file.name)

            return subprocess.run([_viewer, file.name]).returncode == 0
