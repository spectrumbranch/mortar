from importlib import resources
from mortar.image import Detector
from collections import Counter
from pprint import pprint


def iog_jp_charity_detector_fn(x: int, _y: int, w: int, h: int) -> bool:
    if (x == 880):
        return h > 100 and w < 700
    return h > 200 and w < 1083


detector = Detector()

data_list = []
case_samples = {}

img_directory = resources.files('mortar.examples.data.iog_jp_classifier')

for item in img_directory.iterdir():
    if item.is_file():
        file_name = item.name
        file_path = str(
            img_directory.joinpath(file_name)
        )

        print(f"File: {file_path}")

        rects = detector.detect_rects(file_path, iog_jp_charity_detector_fn)
        representation = (0, 0, 0, 0)
        if len(rects) > 0:
            representation = rects[0]
        data_list.append(representation)
        if representation not in case_samples:
            case_samples[representation] = file_name


print(f"Data: {len(data_list)}")

counter = Counter(data_list)
pprint(f"Counter: {counter}")
pprint(f"Case Samples: {case_samples}")
