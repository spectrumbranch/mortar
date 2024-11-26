from mortar.pipeline import *

image = Image.new('RGB', (512, 512), color=(0, 128, 0))

gray = Gray()

output = gray.run(image)

output.show()
