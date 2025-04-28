from mortar.pipeline import *

size = (1024, 1024)

image = Image.effect_mandelbrot(size, (-1.5, -1, 0.5, 1), 100)

crop = Crop(
    (
        int(size[0] * 0.25),
        int(size[1] * 0.25),
        int(size[0] * 0.5),
        int(size[1] * 0.75)
    )
)

output = crop.run(image)

assert isinstance(output, Image)

output.show()
