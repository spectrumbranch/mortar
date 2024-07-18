import os
from tempfile import mkdtemp

from PIL import Image, ImageChops
from mortar.pipeline import Pipeline
from mortar.image import Crop, Gray, Invert

data = f'{os.getcwd()}/test/data'

_debug = False


def test_image() -> None:
    size = (1000, 1000)
    crop = (500, 500, 999, 999)

    image = Image.new('RGB', size, color=(255, 255, 255))

    image = image.crop(crop)

    image = image.convert("L")

    image = ImageChops.invert(image)


def test_pipeline() -> None:
    size = (1000, 1000)
    crop = (500, 500, 1000, 1000)

    image = Image.new('RGB', size, color=(255, 255, 255))

    pipeline = Pipeline()
    pipeline.add(Crop(crop))
    pipeline.add(Gray())
    pipeline.add(Invert())

    output = pipeline.run(image)

    stages = output.stages
    s1 = stages[1]
    s2 = stages[2]
    s3 = stages[3]

    if _debug:
        temp = mkdtemp(prefix='test_pipeline')

        print(f'save pipeline output to {temp}')

        output.save(temp)

    assert s1.size == (500, 500)
    assert s2.mode == "L"
    assert s2.getpixel((0, 0)) == 255
    assert s2.getpixel((499, 499)) == 255
    assert s3.getpixel((0, 0)) == 0
    assert s3.getpixel((499, 499)) == 0
