from importlib import resources

from mortar.pipeline import *

ocr = OCR()

input_path = str(
    resources.files('mortar.examples.data').joinpath('hiragana_ocr.png')
)

output = ocr.run(Image.open(input_path))

print(f'OCR result: {output}')
