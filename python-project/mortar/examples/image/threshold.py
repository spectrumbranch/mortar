from mortar.pipeline import *

image = Image.linear_gradient('L')

threshold = Threshold()

output = threshold.run(image)
outputDiffThreshval = threshold.run(image, 64)

output.show()
outputDiffThreshval.show()
