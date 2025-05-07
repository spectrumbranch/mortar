from importlib import resources
from typing import override

from mortar.image import Detector
from mortar.pipeline import *


def iog_jp_charity_detector_fn(x: int, _y: int, w: int, h: int) -> bool:
    if (x == 880):
        return h > 100 and w < 700
    return h > 200 and w < 1083


def get_macro_crop_rect(rect) -> tuple[int, int, int, int]:
    x, y, w, h = rect
    # convert (x, y, w, h) to (x1, y1, x2, y2)
    x1 = x
    y1 = y
    x2 = x + w
    y2 = y + h
    rect_crop = (x1, y1, x2, y2)
    return rect_crop


class MultiCrop(Filter):
    name = 'MultiCrop'
    _input_type = Image

    def __init__(self, top_padding: int, line_height: int) -> None:
        super().__init__()

        self._top_padding = top_padding
        self._line_height = line_height

    @override
    def run(self, input: Image) -> list[Image]:
        super().run(input)

        crop_width = input.size[0]

        y_top = self._top_padding
        y_bot = y_top + self._line_height
        y_max = input.size[1]

        line_images = []

        while y_bot < y_max:
            line_crop_rect = (0, y_top, crop_width, y_bot)
            line_image = input.copy().crop(line_crop_rect)

            line_images.append(line_image)
            y_top = y_bot
            y_bot = y_top + self._line_height

        return line_images


input_path = str(
    resources.files('mortar.examples.data').joinpath('iog_top_big.png')
)

image = Image.open(input_path)

detector = Detector()

top_padding = 20
line_height = 68

# Detect the rectangle surrounding all the text in the image.

rects = detector.detect_rects(input_path, iog_jp_charity_detector_fn)

assert len(rects) == 1

# Run the original image through a pipeline:
#
# 1. Crop down to the rect surrounding all the text.
# 2. Threshold
# 3. Make multiple crops for each line of text.

rect_crop = get_macro_crop_rect(rects[0])

pipeline = Pipeline()
pipeline.add(Crop(rect_crop))
pipeline.add(Gray())
pipeline.add(Invert())
pipeline.add(MultiCrop(top_padding, line_height))

output = pipeline.run(image)

# Print info on the threshold result.

thresholded_image = output.stages[2].data

print(f':::{thresholded_image.size}')

# Print info on the multi-crop result.

final_stage = output.stages[-1]

print(f':::={final_stage.data}')

# Show each image from the multi-crop result.

# The Output class has a show method which is used, but its implementation
# only knows what to do when the type of the output stage is str or Image. If
# we were to add support for list[Image], we could call output.show() to see
# the results, but since we don't have that yet, we can inspect the results
# in the loop below.

# output.show()

for it in final_stage.data:
    it.show()
