"""
This package provides the image processing pipeline facility.
"""

import copy
from functools import reduce
import operator
from typing import Any, Optional

from mktech.validate import ensure_type
from PIL import ImageDraw

# from .config import config
from mortar import font
from mortar.font import text_size
from mortar.image import Image, create_text
from mortar.path import Path, PathInput
from .filter import Crop, Filter, Gray, Invert, OCR, Threshold

__all__ = [
    'Image',
    'Pipeline',
    # image re-exports
    'Crop',
    'Gray',
    'Invert',
    'OCR',
    'Output',
    'Threshold'
]

_font = {
    'reiko_48': font.load('reiko.ttf', 48),
    'fira_sans_48': font.load('FiraSans-Regular.otf', 48)
}


def image_info(image: Image) -> str:
    return f'{image.mode} {image.size}'


class Pipeline:
    """
    A Pipeline is a series of stages through which an image is
    processed to create some final result. Each stage of the pipeline is
    implemented by a Filter. The output of each Filter is used as the input of
    the next Filter in the pipeline. The result of running the pipeline is an
    Output object containing the results of each Filter, and thus the overall
    result of the pipeline.
    """

    def __init__(self) -> None:
        self._name = 'Pipeline'

        self.stages: list[Filter] = []

    def add(self, stage: Filter) -> None:
        """ Append a stage to the end of the pipeline. """

        self.stages.append(stage)

    def insert(self, index: int, stage: Filter) -> None:
        """ Insert a stage before index. """

        self.stages.insert(index, stage)

    def pop(self, index: int) -> Filter:
        """ Remove the stage at index and return it. """

        return self.stages.pop(index)

    def run(self, input: Image) -> 'Output':
        """
        Run the pipeline using input as the input image. Return the result.
        """

        output = Output(self)

        output.add(input, f'0: Start\n{image_info(input)}')

        filter_input: Any = input

        for idx, it in enumerate(self.stages):
            if it.enabled:
                filter_output = it.run(filter_input)

                text = f'{idx + 1}: {it.info()}\n{image_info(filter_input)}'

                output.add(filter_output, text)

                filter_input = filter_output

        return output

    @property
    def name(self) -> str:
        """ The name of the pipeline. """

        return self._name

    @name.setter
    def name(self, val: str) -> None:
        self._name = val

    def copy(self) -> 'Pipeline':
        """ Create and return a deep copy of the pipeline. """
        return copy.deepcopy(self)


class Output:
    """
    Contains the results of each stage of a Pipeline, and the overall result of
    the Pipeline.
    """

    class Stage:
        """
        The result of a Pipeline stage.
        """

        def __init__(
            self,
            data: Any,
            text: Optional[str] = None
        ) -> None:
            self.data = data
            self.text = text

    _bg_color = 'rgb(25, 25, 25)'
    _margin = 10
    _border_width = 5

    def __init__(self, pipeline: Pipeline) -> None:
        self.pipeline = pipeline
        self.stages: list[Output.Stage] = []
        self._frames: list[Image] = []

    def add(self, stage: Image | str, text: Optional[str] = None) -> None:
        """
        Add stage to the Output stages.
        """

        self.stages.append(Output.Stage(stage, text))

    def save(self, path: PathInput) -> None:
        """
        Create a composite image showing the results of all stages. Save the
        image to path.
        """

        for idx, it in enumerate(self.stages):
            if isinstance(it.data, Image):
                file_path = Path(path, f'{idx}.png')

                it.data.save(file_path)
            elif isinstance(it.data, str):
                file_path = Path(path, f'{idx}.txt')

                with open(file_path, 'w') as file:
                    file.write(it.data)
            else:
                raise TypeError()

        self._composite().save(Path(path, 'all.png'))

    def show(self) -> None:
        """
        Create a composite image showing the results of all stages. Show the
        image in the default viewer.
        """

        self._composite().show()

    def _composite(self) -> Image:
        self._frame_images()

        width = max([it.size[0] for it in self._frames])
        heights = [it.size[1] for it in self._frames]
        height = (reduce(operator.add, heights, 0) +
                  (self._margin * 2) *
                  len(self._frames) - 1)

        canvas = Image.new('RGB', (width, height), color=self._bg_color)

        y = 0

        draw = ImageDraw.Draw(canvas.pil_image)

        text_color = 'rgb(200, 200, 200)'

        draw.text((0, y), self.pipeline.name, fill=text_color,
                  font=_font['fira_sans_48'])

        y += 48 + self._margin

        for it in self._frames:
            frame_height = it.size[1]
            canvas.paste(it, (0, y))

            y += frame_height + self._margin

        return canvas

    def _frame_images(self) -> None:
        text_color = 'rgb(200, 200, 200)'
        divider_color = 'rgb(255, 0, 255)'

        text_margin = self._margin * 3

        self._frames = []

        for it in self.stages:
            if isinstance(it.data, Image):
                frame_image = it.data

            elif isinstance(it.data, str):
                """
                The OCR result is drawn onto the resulting image, using a font
                that supports the required Japanese glyphs.

                If the OCR operation fails, an error message is drawn onto the
                resulting image.
                """

                frame_image = create_text(it.data, _font['reiko_48'],
                                          'rgb(235, 235, 235)', (10, 10))
            else:
                raise TypeError()

            frame_width = frame_image.size[0]

            text_height = _font['fira_sans_48'].size * 2 + text_margin

            height = frame_image.size[1] + self._border_width + text_height

            text = ensure_type(it.text, str)

            length = (round(text_size(text, _font['fira_sans_48'])[0]) +
                      self._margin)

            width = max(frame_width + self._border_width, length)

            image = Image.new(
                'RGB',
                (width, height),
                color=self._bg_color
            )

            draw = ImageDraw.Draw(image.pil_image)

            draw.text((self._margin, 0), text, fill=text_color,
                      font=_font['fira_sans_48'])

            y = text_height

            image.paste(frame_image, (0, y))

            draw.rectangle(
                (0, y, frame_width, y + frame_image.size[1]),
                outline=divider_color,
                width=self._border_width
            )

            self._frames.append(image)
