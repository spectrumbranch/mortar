import os
from mortar.image import Detector
from collections import Counter
from pprint import pprint

from mortar.config import config


# A tested detector fn that inputs x,y,w,h rectangle coords from each image
# returns true if the rect is one we believe contains dialogue, else false.
# A dialogue box in iog-jp may be in more than one position.
def iog_jp_charity_detector_fn(x: int, _y: int, w: int, h: int) -> bool:
    if (x == 880):
        return h > 100 and w < 700
    return h > 200 and w < 1083

# the purpose of this example is to make it easier to feel confident
# throwing away junk frames of the video->screenshot collection
# as well as another way of testing the detector function


detector = Detector()

data_list = []
case_samples = {}

img_directory = f'{config.data}/ocr/examples/images/iog_jp_classifier/'

for file_name in os.listdir(img_directory):
    file_path = os.path.join(img_directory, file_name)
    if os.path.isfile(file_path):
        rects = detector.detect_rects(file_path, iog_jp_charity_detector_fn)
        # default value is (0,0,0,0) when nothing detected
        representation = (0, 0, 0, 0)
        if len(rects) > 0:
            representation = rects[0]
        data_list.append(representation)
        if representation not in case_samples:
            case_samples[representation] = file_name

# length of all data processed
print(f"Data: {len(data_list)}")

counter = Counter(data_list)
# a map of the count of all cases possible [rect: int]
pprint(f"Counter: {counter}")
# a map of [rect: filename] which only tracks the first detected filename for a case
pprint(f"Case Samples: {case_samples}")
