import os
from tempfile import mkdtemp

from mktech.validate import ensure_type
import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage
import pytest

from mortar.image import Threshold
from mortar.path import Path
from mortar.tesseract import ocr

_debug = True

data = f'{os.getcwd()}/test/data'


def test_threshold() -> None:
    size = (100, 255)
    pixel_count = size[0] * size[1]

    data = np.array([[i] * size[0] for i in range(0, 255)], dtype='uint8')

    image = Image.fromarray(data, mode='L')

    threshold = Threshold()

    output = ensure_type(threshold.run(image), PILImage)

    out_data = list(output.getdata())

    top_pixel_count = int(pixel_count / 2) + 50
    top = out_data[0:top_pixel_count]
    bottom_pixel_count = pixel_count - top_pixel_count
    bottom = out_data[top_pixel_count:]

    expected_top = np.array([0] * top_pixel_count, dtype='uint8')
    expected_bottom = np.array([255] * bottom_pixel_count, dtype='uint8')

    assert len(out_data) == pixel_count
    assert np.all(top == expected_top)
    assert np.all(bottom == expected_bottom)

    if _debug:
        temp = mkdtemp(prefix='test_pipeline')

        print(f'save image output to {temp}')

        output.save(Path(temp, 'image.png'))


def test_threshold_rgb_rejection() -> None:
    imageRGB = Image.new('RGB', (300, 200), (228, 150, 150))
    threshold = Threshold()
    outputRGB = threshold.run(imageRGB)
    assert outputRGB is None


@pytest.mark.parametrize('index', range(0, 9))
def test_ocr(index: int) -> None:
    with open(f'{data}/mort/capture_{index:02}.str') as fi:
        mort_str = fi.read()

    result = ocr(f'{data}/mort/capture_{index:02}.png')

    print(f'mort: {mort_str}')
    print(f'result: {result}')

    assert result == mort_str
