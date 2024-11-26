from argparse import ArgumentParser
from importlib import resources

from mortar.pipeline import *


def parse_tuple_arg(input):
    if input is None:
        result = None
    else:
        coords = [int(it) for it in input.split(',')]

        if len(coords) != 4:
            raise ValueError()

        result = tuple(coords)

    return result


parser = ArgumentParser(prog='OCR pipeline example')

parser.add_argument('-i', '--input-path', help='Path to the input image')
parser.add_argument('-c', '--crop', metavar='x1,y1,x2,y2',
                    help='Crop coordinates')

args = parser.parse_args()

if not args.input_path:
    input_path = str(
        resources.files('mortar.examples.data').joinpath('hiragana_chart.png')
    )
    crop = (124, 1263, 633, 1717)
else:
    input_path = args.input_path

    crop = parse_tuple_arg(args.crop)

image = Image.open(input_path)

pipeline = Pipeline()

if crop is not None:
    pipeline.add(Crop(crop))

pipeline.add(Gray())
pipeline.add(Threshold())
pipeline.add(OCR())

output = pipeline.run(image)

output.show()
