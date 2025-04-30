import os
from collections.abc import Sequence
from shutil import rmtree
from tempfile import mkdtemp

from mktech.validate import ensure_type

from mortar.pipeline import (
    OCR,
    Crop,
    Gray,
    Image,
    Invert,
    Output,
    Pipeline,
    Threshold,
)

data = f'{os.getcwd()}/tests/data'

_debug = False


def _check_output_stages(
    output: Output, expected_stage_info: Sequence[Sequence[str]]
) -> None:
    stages = output.stages

    assert len(stages) == len(expected_stage_info)

    actual_stage_info = [stage.info for stage in stages]

    for expected, actual in zip(actual_stage_info, expected_stage_info):
        assert actual == expected


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


def test_pipeline_modify() -> None:
    def make_pipeline_0() -> Pipeline:
        pipeline = Pipeline()
        pipeline.add(Crop(bottom_left))
        pipeline.add(Gray())
        pipeline.add(Invert())
        pipeline.add(OCR())

        return pipeline

    def make_pipeline_1() -> Pipeline:
        pipeline = Pipeline()
        pipeline.add(Gray())
        pipeline.add(OCR())

        return pipeline

    def make_pipeline_2() -> Pipeline:
        pipeline = Pipeline()
        pipeline.add(Crop(top_left))
        pipeline.add(Gray())
        pipeline.add(Invert())
        pipeline.add(OCR())

        return pipeline

    size = (1000, 1000)

    image = Image.new('RGB', size, color=(255, 255, 255))

    bottom_left = (124, 1263, 633, 1717)
    top_left = (114, 232, 650, 1232)

    # Create a typical pipeline, run it, and check.

    pipeline = make_pipeline_0()

    output = pipeline.run(image)

    assert pipeline == make_pipeline_0()

    _check_output_stages(
        output,
        [
            ['Start', 'RGB (1000, 1000)'],
            ['Crop box=(124, 1263, 633, 1717)', 'RGB (1000, 1000)'],
            ['Gray', 'RGB (509, 454)'],
            ['Invert', 'L (509, 454)'],
            ['OCR', 'L (509, 454)'],
        ]
    )

    # Remove stages, run modified pipeline, and check.

    _ = pipeline.pop(2)
    _ = pipeline.pop(0)

    output = pipeline.run(image)

    assert pipeline == make_pipeline_1()

    _check_output_stages(
        output,
        [
            ['Start', 'RGB (1000, 1000)'],
            ['Gray', 'RGB (1000, 1000)'],
            ['OCR', 'L (1000, 1000)'],
        ]
    )

    # Insert stages, run modified pipeline, and check.

    pipeline.insert(1, Invert())
    pipeline.insert(0, Crop(top_left))

    output = pipeline.run(image)

    assert pipeline == make_pipeline_2()

    _check_output_stages(
        output,
        [
            ['Start', 'RGB (1000, 1000)'],
            ['Crop box=(114, 232, 650, 1232)', 'RGB (1000, 1000)'],
            ['Gray', 'RGB (536, 1000)'],
            ['Invert', 'L (536, 1000)'],
            ['OCR', 'L (536, 1000)'],
        ]
    )


def test_pipeline_equality() -> None:
    def make_pipeline_0() -> Pipeline:
        pipeline = Pipeline()
        pipeline.add(Crop((124, 1263, 633, 1717)))
        pipeline.add(Gray())
        pipeline.add(Invert())
        pipeline.add(OCR())

        return pipeline

    def make_pipeline_1() -> Pipeline:
        pipeline = Pipeline()
        pipeline.add(Crop((114, 232, 650, 1232)))
        pipeline.add(Gray())
        pipeline.add(Invert())
        pipeline.add(OCR())

        return pipeline

    pipeline_0_0 = make_pipeline_0()
    pipeline_0_1 = make_pipeline_0()

    assert pipeline_0_1 == pipeline_0_0

    pipeline_1_0 = make_pipeline_1()

    assert pipeline_0_0 != pipeline_1_0


def test_pipeline_copy() -> None:
    bottom_left = (124, 1263, 633, 1717)
    top_left = (114, 232, 650, 1232)
    top_right = (770, 242, 1174, 1230)

    def make_pipeline_0() -> Pipeline:
        pipeline = Pipeline()
        pipeline.add(Crop(bottom_left))
        pipeline.add(Gray())
        pipeline.add(Invert())
        pipeline.add(OCR())

        return pipeline

    def make_pipeline_1() -> Pipeline:
        pipeline = Pipeline()
        pipeline.name = 'Pipeline original with crop mod'

        pipeline.add(Crop(top_right))
        pipeline.add(Gray())
        pipeline.add(Invert())
        pipeline.add(OCR())

        return pipeline

    def make_pipeline_copy() -> Pipeline:
        pipeline = Pipeline()
        pipeline.name = 'Pipeline copy'

        pipeline.add(Crop(top_left))
        pipeline.add(Crop(bottom_left))
        pipeline.add(Gray())
        pipeline.add(Invert())
        pipeline.add(OCR())

        return pipeline

    # Make a typical pipeline and copy it. Ensure that the two objects are
    # equal in effect.

    pipeline = make_pipeline_0()
    pipeline_copy = pipeline.copy()

    assert pipeline == make_pipeline_0()
    assert pipeline_copy == make_pipeline_0()
    assert pipeline_copy == pipeline

    # Modify the original pipeline. Ensure that the copy is not affected when
    # the original is modified.

    _ = pipeline.pop(0)
    pipeline.name = 'Pipeline original with crop mod'
    pipeline.insert(0, Crop(top_right))

    assert pipeline == make_pipeline_1()
    assert pipeline_copy == make_pipeline_0()

    # Modify the copy. Ensure that the original is not affected when the copy
    # is modified.

    pipeline_copy.name = 'Pipeline copy'
    pipeline_copy.insert(0, Crop(top_left))

    assert pipeline_copy == make_pipeline_copy()
    assert pipeline == make_pipeline_1()
