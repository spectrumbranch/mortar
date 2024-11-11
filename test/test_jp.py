""" Test accuracy of OCR against Japanese game image data. """

from dataclasses import dataclass
import os
from pathlib import Path

import PIL.Image
import pytest

from mortar.tesseract import ocr
from mortar.util import mktemp

data = f'{os.getcwd()}/test/data'

not_yet_implemented = 'test is not yet implemented'


@dataclass
class OCRTest:
    rectangle: tuple[int, int, int, int]
    base_name: str
    count: int


_7thelnard = OCRTest(rectangle=(414, 678, 1489, 967),
                     base_name='7thelnard-01', count=17)
_aretha = OCRTest(rectangle=(328, 754, 1554, 957),
                  base_name='aretha-01', count=18)
_aretha2 = OCRTest(rectangle=(333, 106, 1569, 315),
                   base_name='aretha2-01', count=16)
_bof = OCRTest(rectangle=(412, 711, 1483, 966),
               base_name='bof-01', count=45)
_bof2 = OCRTest(rectangle=(400, 705, 1500, 975),
                base_name='bof2-01', count=19)
_ff4 = OCRTest(rectangle=(408, 144, 1491, 409), base_name='ff4-01', count=18)
_ff6_01 = OCRTest(rectangle=(433, 76, 1459, 370),
                  base_name='ff6-01', count=26)
_ff6_02 = OCRTest(rectangle=(373, 87, 1531, 354),
                  base_name='ff6-02', count=21)
_iog = OCRTest(rectangle=(1173, 408, 1830, 606), base_name='iog-01', count=7)
_rudra = OCRTest(rectangle=(400, 634, 1360, 1030),
                 base_name='rudra-01', count=59)


def dir_mkr(test_case: OCRTest, type: str) -> Path:
    name = test_case.base_name[0:test_case.base_name.find('-')]

    return Path(data, 'jp', name, type)


@pytest.mark.parametrize('index', range(0, _7thelnard.count))
def test_7thelnard(index):
    ocr_test_case(_7thelnard, index)


@pytest.mark.parametrize('index', range(0, _aretha.count))
def test_aretha(index):
    ocr_test_case(_aretha, index)


@pytest.mark.parametrize('index', range(0, _aretha2.count))
def test_aretha2(index):
    ocr_test_case(_aretha2, index)


@pytest.mark.parametrize('index', range(0, _bof.count))
def test_bof(index):
    ocr_test_case(_bof, index)


@pytest.mark.parametrize('index', range(0, _bof2.count))
def test_bof2(index):
    ocr_test_case(_bof2, index)


@pytest.mark.skip(reason=not_yet_implemented)
@pytest.mark.parametrize('index', range(0, _ff4.count))
def test_ff4(index):
    ocr_test_case(_ff4, index)


@pytest.mark.skip(reason=not_yet_implemented)
@pytest.mark.parametrize('index', range(0, _ff6_01.count))
def test_ff6_01(index):
    ocr_test_case(_ff6_01, index)


@pytest.mark.skip(reason=not_yet_implemented)
@pytest.mark.parametrize('index', range(0, _ff6_02.count))
def test_ff6_02(index):
    ocr_test_case(_ff6_02, index)


@pytest.mark.skip(reason=not_yet_implemented)
@pytest.mark.parametrize('index', range(0, _iog.count))
def test_iog(index):
    ocr_test_case(_iog, index)


@pytest.mark.skip(reason=not_yet_implemented)
@pytest.mark.parametrize('index', range(0, _rudra.count))
def test_rudra(index):
    ocr_test_case(_rudra, index)


def ocr_test_case(test_case: OCRTest, index: int) -> None:
    name = f'{test_case.base_name}-{index + 1:02}'
    input_png_path = f'''{dir_mkr(test_case, 'png')}/{name}.png'''
    input_txt_path = f'''{dir_mkr(test_case, 'txt')}/{name}.txt'''
    output_path = mktemp(suffix='.png')

    image = PIL.Image.open(input_png_path)
    expected_text = Path(input_txt_path).read_text()

    crop = image.crop(test_case.rectangle)
    crop.save(output_path)

    result = ocr(output_path)

    os.remove(output_path)

    print(f'{name} {index + 1}/{test_case.count} result: {result}')

    assert result == expected_text
