from importlib import resources

from mortar.pipeline import *

input_path = str(
    resources.files('mortar.examples.data').joinpath('hiragana_chart.png')
)

image = Image.open(input_path)

size = (1000, 1000)
crop = (124, 1263, 633, 1717)

pipeline = Pipeline()
pipeline.add(Crop(crop))
pipeline.add(Gray())
pipeline.add(Invert())
pipeline.add(OCR())

output = pipeline.run(image)

output.show()
