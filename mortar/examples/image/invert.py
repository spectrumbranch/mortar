from mortar.pipeline import *

image = Image.effect_mandelbrot((1024, 1024), (-1.5, -1, 0.5, 1), 100)

invert = Invert()

output = invert.run(image)

output.show()
