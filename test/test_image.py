import os

import numpy as np
from mktech.validate import ensure_type

from mortar.image import Image
from mortar.pipeline import OCR, Threshold

data = f'{os.getcwd()}/test/data'


class TestFilter:
    def test_threshold(self) -> None:
        size = (100, 255)
        pixel_count = size[0] * size[1]

        data = np.array([[i] * size[0] for i in range(0, 255)], dtype='uint8')

        image = Image.fromarray(data, mode='L')

        threshold = Threshold()

        output = ensure_type(threshold.run(image), Image)

        out_data = list(output.getdata())

        top_pixel_count = int(pixel_count / 2) + 50
        top = out_data[0:top_pixel_count]
        bottom_pixel_count = pixel_count - top_pixel_count
        bottom = out_data[top_pixel_count:]

        expected_top = np.array([0] * top_pixel_count, dtype='uint8')
        expected_bottom = np.array([255] * bottom_pixel_count, dtype='uint8')

        assert len(out_data) == pixel_count
        assert np.all(top == expected_top)
        assert np.all(bottom == expected_bottom)

    def test_threshold_rgb_rejection(self) -> None:
        imageRGB = Image.new('RGB', (300, 200), (228, 150, 150))
        threshold = Threshold()
        outputRGB = threshold.run(imageRGB)
        assert outputRGB is None

    def test_ocr(self) -> None:
        image = Image.open(f'{data}/hiragana_ocr.png')

        output = OCR().run(image)

        assert output == '''ご ぞ ど ば ぼ ば ぼ ま
げ ゼ ぜ ゼ ぜ で べ ペ
ぐず づい ぶ い ぶ
ぎじ ぢ びび で び
が ざさ ざ だ ば だ ぱ ば
'''
