from functools import reduce
import operator
from typing import Optional

from mktech.validate import ensure_type
from PIL.Image import Image
from PIL import ImageDraw, ImageFont
import PIL

from .config import config
from .image import Crop, Filter, Gray, Invert
from .path import Path, PathInput

__all__ = [
    'Pipeline',
    # image re-exports
    'Crop',
    'Filter',
    'Gray',
    'Invert'
]


def image_info(image: Image) -> str:
    return f'{image.mode} {image.size}'


class Pipeline:
    def __init__(self) -> None:
        self.stages: list[Filter] = []

    def add(self, stage: Filter) -> None:
        self.stages.append(stage)

    def run(self, input: Image | str) -> 'Output':
        output = Output(self)

        if isinstance(input, Image):
            image = input
        elif isinstance(input, str):
            image = PIL.Image.open(input)

        output.add(image, f'0: Start\n{image_info(image)}')

        for idx, it in enumerate(self.stages):
            if it.enabled:
                image = ensure_type(it.run(image.copy()), Image)

                text = f'{idx + 1}: {it.info()}\n{image_info(image)}'

                output.add(image, text)

        return output


class Output:
    class Stage:
        def __init__(
            self,
            image: Optional[Image],
            text: Optional[str] = None
        ) -> None:
            self.image = image
            self.text = text

    _bg_color = 'rgb(25, 25, 25)'
    _margin = 10
    _border_width = 5

    def __init__(self, pipeline: Pipeline) -> None:
        self.pipeline = pipeline
        self.stages: list[Output.Stage] = []
        self._frames: list[Image] = []

    def add(self, stage: Image | str, text: Optional[str] = None) -> None:
        if isinstance(stage, Image):
            self.stages.append(Output.Stage(stage, text))
        elif isinstance(stage, str):
            image = PIL.Image.new('RGB', (800, 100))

            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(f'{config.font}/reiko.ttf', size=28)

            (x, y) = (0, 0)
            text_color = 'rgb(235, 235, 235)'

            draw.text((x, y), stage, fill=text_color, font=font)

            self.stages.append(Output.Stage(None, text))

    def save(self, path: PathInput) -> None:
        for idx, it in enumerate(self.stages):
            file_path = Path(path, f'{idx}.png')

            image = ensure_type(it.image, Image)

            image.save(file_path)

        self._composite().save(Path(path, 'all.png'))

    def show(self) -> None:
        self._composite().show()

    def _composite(self) -> Image:
        self._frame_images()

        width = max([it.size[0] for it in self._frames])
        heights = [it.size[1] for it in self._frames]
        height = (reduce(operator.add, heights, 0) +
                  self._margin *
                  len(self._frames) - 1)

        canvas = PIL.Image.new('RGB', (width, height), color=self._bg_color)

        y = 0

        for it in self._frames:
            frame_height = it.size[1]
            canvas.paste(it, (0, y))

            y += frame_height + self._margin

        return canvas

    def _frame_images(self) -> None:
        font_size = 48
        font = ImageFont.load_default(font_size)
        text_color = 'rgb(200, 200, 200)'
        divider_color = 'rgb(255, 0, 255)'

        text_margin = self._margin * 3

        self._frames = []

        for it in self.stages:
            y = 0

            text_height = font_size * 2 + text_margin
            frame_image = ensure_type(it.image, Image)

            frame_width = frame_image.size[0]
            height = frame_image.size[1] + self._border_width + text_height

            image = PIL.Image.new(
                'RGB',
                (frame_width, height),
                color=self._bg_color
            )

            draw = ImageDraw.Draw(image)

            text = ensure_type(it.text, str)
            length = round(_text_length(text, draw, font)) + self._margin

            width = max(frame_width + self._border_width, length)
            image = image.resize((width, height))
            draw = ImageDraw.Draw(image)

            draw.text((self._margin, 0), text, fill=text_color, font=font)

            y += text_height

            image.paste(frame_image, (0, y))

            draw.rectangle(
                (0, y, frame_width, y + frame_image.size[1]),
                outline=divider_color,
                width=self._border_width
            )

            self._frames.append(image)


def _text_length(
    text: str,
    image_draw: ImageDraw.ImageDraw,
    font: ImageFont.ImageFont
) -> float:
    lines = text.split('\n')
    lengths = [image_draw.textlength(it, font=font) for it in lines]

    return max(lengths)
