import os
from tempfile import mkdtemp

from mktech.validate import ensure_type

from mortar.pipeline import Crop, Gray, Image, Invert, Pipeline

data = f'{os.getcwd()}/test/data'

_debug = False


def test_image() -> None:
    size = (1000, 1000)
    crop = (500, 500, 999, 999)

    image = Image.new('RGB', size, color=(255, 255, 255))

    image = image.crop(crop)

    image = image.convert("L")

    image = Image.invert(image)


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
    i1 = ensure_type(stages[1].image, Image)
    i2 = ensure_type(stages[2].image, Image)
    i3 = ensure_type(stages[3].image, Image)

    if _debug:
        temp = mkdtemp(prefix='test_pipeline')

        print(f'save pipeline output to {temp}')

        output.save(temp)

    assert i1.size == (500, 500)
    assert i2.mode == "L"
    assert i2.getpixel((0, 0)) == 255
    assert i2.getpixel((499, 499)) == 255
    assert i3.getpixel((0, 0)) == 0
    assert i3.getpixel((499, 499)) == 0
