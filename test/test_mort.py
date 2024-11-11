import os

import pytest

from mortar.tesseract import ocr

data = f'{os.getcwd()}/test/data/mort'


@pytest.mark.parametrize('index', range(0, 9))
def test_mort_tess(index):
    """ Run test data previously gathered from MORT through tesseract,
        confirming that OCR results are the same. """

    with open(f'{data}/capture_{index:02}.str') as fi:
        mort_str = fi.read()

    result = ocr(f'{data}/capture_{index:02}.png')

    print(f'mort: {mort_str}')
    print(f'result: {result}')

    assert result == mort_str
