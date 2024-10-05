from importlib import resources

from mortar.pipeline import *

tr = resources.files('mortar.examples.data')
iter = tr.iterdir()

for it in tr.iterdir():
    if it.name == 'hiragana_chart.png':
        with resources.as_file(it) as path:
            image = Image.open(path)

size = (1000, 1000)
bottom_left = (124, 1263, 633, 1717)
top_left = (114, 232, 650, 1232)
top_right = (770, 242, 1174, 1230)

# Create a typical pipeline, run it, and show output.

pipeline = Pipeline()
pipeline.add(Crop(bottom_left))
pipeline.add(Gray())
pipeline.add(Invert())
pipeline.add(OCR())

output = pipeline.run(image)

output.show()

# Remove a stage, run modified pipeline, and show output.

pipeline.pop(0)

output = pipeline.run(image)

output.show()

# Copy the pipeline.

pipeline_copy = pipeline.copy()
pipeline_copy.name = 'Pipeline copy'

# # Insert a new stage into the copy, run it, and show output.

pipeline_copy.insert(0, Crop(top_left))

output = pipeline_copy.run(image)

output.show()

# # Insert a new stage into the original, run it, and show output.

pipeline.name = 'Pipeline original'

pipeline.insert(0, Crop(top_right))

output = pipeline.run(image)

output.show()
