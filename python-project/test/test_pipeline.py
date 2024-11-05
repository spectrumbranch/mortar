import os
from shutil import rmtree
from tempfile import mkdtemp

from mktech.validate import ensure_type

from mortar.pipeline import Crop, Gray, Image, Invert, OCR, Pipeline, Threshold

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
    i1 = ensure_type(stages[1].data, Image)
    i2 = ensure_type(stages[2].data, Image)
    i3 = ensure_type(stages[3].data, Image)

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


def test_pipeline_ocr() -> None:
    image = Image.open(f'{data}/hiragana_ocr.png')

    pipeline = Pipeline()
    pipeline.add(Gray())
    pipeline.add(Threshold())
    pipeline.add(OCR())

    output = pipeline.run(image)

    stages = output.stages
    s3 = ensure_type(stages[3].data, str)

    assert s3 == '''ご ぞ ど ば ぼ ば ぼ ま
げ ゼ ぜ ゼ ぜ で べ ペ
ぐず づい ぶ い ぶ
ぎじ ぢ びび で び
が ざさ ざ だ ば だ ぱ ば
'''

    temp = mkdtemp(prefix='test_pipeline_')

    output.save(temp)

    rmtree(temp)
