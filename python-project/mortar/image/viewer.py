import subprocess
from tempfile import NamedTemporaryFile
from typing import Any

from PIL.Image import Image as PILImage


class Viewer:
    def show(self, image: PILImage, **options: Any) -> bool:
        with NamedTemporaryFile(suffix='.png') as file:
            image.save(file.name)

            return subprocess.run(['feh', file.name]).returncode == 0
