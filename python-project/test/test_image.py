import os
from tempfile import mkdtemp

import numpy as np
from PIL import Image
import pytest

from mortar.image import Crop, Gray, Invert, Threshold
from mortar.path import Path
from mortar.tesseract import ocr

_debug = True

data = f'{os.getcwd()}/test/data'


def test_threshold() -> None:
    size = (100, 255)
    pixel_count = size[0] * size[1]

    # image = Image.new('L', size, color=255)

    data = np.array([[i] * size[0] for i in range(0, 255)], dtype='uint8')

    #image = Image.frombytes('L', size, data)
    image = Image.fromarray(data, mode='L')
    #breakpoint()
    #image.show()

    # image = image.convert("L")

    threshold = Threshold()

    output = threshold.run(image)

    out_data = list(output.getdata())

    top_pixel_count = int(pixel_count / 2) + 50
    top = out_data[0:top_pixel_count]
    bottom_pixel_count = pixel_count - top_pixel_count
    bottom = out_data[top_pixel_count:]

    expected_top = np.array([0] * top_pixel_count, dtype='uint8')
    expected_bottom = np.array([255] * bottom_pixel_count, dtype='uint8')

    assert len(out_data) == pixel_count
    assert (top == expected_top).all()
    assert (bottom == expected_bottom).all()

    if _debug:
        temp = mkdtemp(prefix='test_pipeline')

        print(f'save image output to {temp}')

        output.save(Path(temp, 'image.png'))


@pytest.mark.parametrize('index', range(0, 9))
def test_ocr(index: int) -> None:
    """ Run test data previously gathered from MORT through tesseract,
        confirming that OCR results are the same. """

    with open(f'{data}/mort/capture_{index:02}.str') as fi:
        mort_str = fi.read()

    result = ocr(f'{data}/mort/capture_{index:02}.png')

    print(f'mort: {mort_str}')
    print(f'result: {result}')

    assert result == mort_str
