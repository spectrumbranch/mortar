import pytest

from mortar.config import config
from mortar.tesseract import ocr


@pytest.mark.parametrize('index', range(0, 9))
def test_mort_tess(index: int) -> None:
    """ Run test data previously gathered from MORT through tesseract,
        confirming that OCR results are the same. """

    with open(f'{config.data}/ocr/mort/capture_{index:02}.str') as fi:
        mort_str = fi.read()

    result = ocr(f'{config.data}/ocr/mort/capture_{index:02}.png')

    print(f'mort: {mort_str}')
    print(f'result: {result}')

    assert result == mort_str
