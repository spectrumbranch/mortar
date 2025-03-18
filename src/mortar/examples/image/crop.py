from mortar.pipeline import *

size = (1024, 1024)

image = Image.effect_mandelbrot(size, (-1.5, -1, 0.5, 1), 100)

crop = Crop((size[0] / 4, size[1] / 4, size[0] / 2, size[1] * 0.75))

output = crop.run(image)

output.show()
