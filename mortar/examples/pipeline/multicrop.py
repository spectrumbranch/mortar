from importlib import resources

from mortar.pipeline import *
from mortar.image import Detector
from tempfile import mkdtemp

input_path = str(
    resources.files('mortar.examples.data').joinpath('iog_top_big.png')
)

image = Image.open(input_path)

detector = Detector()

top_padding = 20
line_height = 68


def iog_jp_charity_detector_fn(x: int, y: int, w: int, h: int) -> bool:
    if (x == 880):
        return h > 100 and w < 700
    return h > 200 and w < 1083


def get_macro_crop_rect(rect) -> tuple:
    x, y, w, h = rect
    # convert (x, y, w, h) to (x1, y1, x2, y2)
    x1 = x
    y1 = y
    x2 = x + w
    y2 = y + h
    rect_crop = (x1, y1, x2, y2)
    return rect_crop


def create_starter_pipeline(rect_crop) -> Image:
    starter_pipeline = Pipeline()
    starter_pipeline.add(Crop(rect_crop))
    starter_pipeline.add(Gray())
    starter_pipeline.add(Invert())
    return starter_pipeline


rects = detector.detect_rects(
    input_path,
    iog_jp_charity_detector_fn)

rect_crop = get_macro_crop_rect(rects[0])

''' step 1: crop the main image and threshold it all at once'''


def get_thresholded_image(image, rect_crop) -> Image:
    starter_pipeline = create_starter_pipeline(rect_crop)

    output = starter_pipeline.run(image)

    thresholded_image = output.stages[-1].data
    print(f':::{thresholded_image.size}')
    return thresholded_image


thresholded_image = get_thresholded_image(image, rect_crop)

''' step 2: crop as many times as needed to get each individual line'''


def get_line_images(thresholded_image, top_padding, line_height) -> list[Image]:
    crop_width = thresholded_image.size[0]

    y_top = top_padding
    y_bot = y_top + line_height
    y_max = thresholded_image.size[1]

    temp = mkdtemp(prefix='test_multicrop')
    print(f'save multicrop prep output to {temp}')
    line_images = []

    while y_bot < y_max:
        line_crop_rect = (0, y_top, crop_width, y_bot)
        line_image = thresholded_image.crop_immutable(line_crop_rect)

        filename = f'{temp}/image_{y_top:04}_{y_bot:04}.png'
        print(f':::>{line_crop_rect} {filename}')
        line_image.save(filename)

        line_images.append(line_image)
        y_top = y_bot
        y_bot = y_top + line_height

    return line_images


line_images = get_line_images(thresholded_image, top_padding, line_height)
print(f':::={line_images}')
