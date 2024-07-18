from typing import cast, Optional

from PIL.Image import Image
from PIL import ImageDraw, ImageFont
import PIL

from mortar.config import config
from .path import Path, PathInput


class Stage:
    enabled = True

    def __init__(self) -> None:
        self.enabled = True

    def run(self, input: Image) -> Optional[Image]:
        return None


class Pipeline:
    def __init__(self) -> None:
        self.stages: list[Stage] = []

    def add(self, stage: Stage) -> None:
        self.stages.append(stage)

    def run(self, input: Image | str) -> 'Output':
        output = Output(self)

        if isinstance(input, Image):
            image = input
        elif isinstance(input, str):
            image = PIL.Image.open(input)

        output.add(image)

        for i in self.stages:
            if i.enabled:
                image = cast(Image, i.run(image.copy()))

                output.add(image)

        return output


class Output:
    def __init__(self, pipeline: Pipeline) -> None:
        self.pipeline = pipeline
        self.stages: list[Image] = []

    def add(self, stage: Image | str) -> None:
        if isinstance(stage, Image):
            self.stages.append(stage)
        elif isinstance(stage, str):
            image = PIL.Image.new('RGB', (800, 100))

            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(f'{config.font}/reiko.ttf', size=28)

            (x, y) = (0, 0)
            text_color = 'rgb(235, 235, 235)'

            draw.text((x, y), stage, fill=text_color, font=font)

            self.stages.append(image)

    def save(self, path: PathInput) -> None:
        for idx, it in enumerate(self.stages):
            file_path = Path(path, f'{idx}.png')

            it.save(file_path)
