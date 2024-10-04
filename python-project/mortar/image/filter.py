from typing import Optional

from PIL.Image import Image as PILImage


class Filter:
    name = 'Filter'
    enabled = True

    def __init__(self) -> None:
        self.enabled = True

    def info(self) -> str:
        return self.name

    def run(self, input: PILImage) -> Optional[PILImage]:
        return None
