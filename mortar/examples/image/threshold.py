from mortar.pipeline import *

image = Image.linear_gradient('L')

threshold = Threshold()
thresholdDiffThreshval = Threshold(64)

output = threshold.run(image)
outputDiffThreshval = thresholdDiffThreshval.run(image)

output.show()
outputDiffThreshval.show()
