from importlib import resources

from mortar.pipeline import *

tr = resources.files('mortar.examples.data')
iter = tr.iterdir()

for it in tr.iterdir():
    if it.name == 'hiragana_chart.png':
        with resources.as_file(it) as path:
            image = Image.open(path)

size = (1000, 1000)
crop = (124, 1263, 633, 1717)

pipeline = Pipeline()
pipeline.add(Crop(crop))
pipeline.add(Gray())
pipeline.add(Invert())
pipeline.add(OCR())

output = pipeline.run(image)

output.show()
