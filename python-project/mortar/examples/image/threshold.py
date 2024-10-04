from mortar.pipeline import *

image = Image.linear_gradient('L')

threshold = Threshold()

output = threshold.run(image)

output.show()
