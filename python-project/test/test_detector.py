"""
Test that we get expected coordinate
results of rectangles from known images
"""
import os

from mortar.image import Detector

data = f'{os.getcwd()}/test/data/detector'


def iog_jp_charity_detector_fn(x: int, y: int, w: int, h: int) -> bool:
    if (x == 880):
        return h > 100 and w < 700
    return h > 200 and w < 1083


def test_detector_iog_top_big() -> None:
    """
    iog_top_big.png / iog_test_45m-173.png
    """
    detector = Detector()
    rects = detector.detect_rects(
        f'{os.getcwd()}/test/data/detector/iog_top_big.png',
        iog_jp_charity_detector_fn)

    assert len(rects) == 1
    x, y, w, h = rects[0]
    assert (x == 685)
    assert (y == 270)
    assert (w == 1056)
    assert (h == 343)


def test_detector_iog_top_small() -> None:
    """
    iog_top_small.png / iog_test_45m-169.png
    """
    detector = Detector()
    rects = detector.detect_rects(
        f'{os.getcwd()}/test/data/detector/iog_top_small.png',
        iog_jp_charity_detector_fn)

    assert len(rects) == 1
    x, y, w, h = rects[0]
    assert (x == 685)
    assert (y == 270)
    assert (w == 1056)
    assert (h == 275)


def test_detector_iog_bottom() -> None:
    """
    iog_bottom.png / iog_test_45m-120.png
    """
    detector = Detector()
    rects = detector.detect_rects(
        f'{os.getcwd()}/test/data/detector/iog_bottom.png',
        iog_jp_charity_detector_fn)

    assert len(rects) == 1
    x, y, w, h = rects[0]
    assert (x == 685)
    assert (y == 646)
    assert (w == 1056)
    assert (h == 342)


def test_detector_iog_area_label() -> None:
    """
    iog_area_label.png / iog_test_45m-1842.png
    """
    detector = Detector()
    rects = detector.detect_rects(
        f'{os.getcwd()}/test/data/detector/iog_area_label.png',
        iog_jp_charity_detector_fn)

    assert len(rects) == 1
    x, y, w, h = rects[0]
    assert (x == 880)
    assert (y == 304)
    assert (w == 666)
    assert (h == 104)


def test_detector_iog_pause_menu() -> None:
    """
    iog_pause_menu.png / iog_test_45m-2298.png

    pause menu small position [ w: 285, h: 233, (681,756) ]
    pause menu large position [ w: 753, h: 233, (993,756) ]
    """
    detector = Detector()
    rects = detector.detect_rects(
        f'{os.getcwd()}/test/data/detector/iog_pause_menu.png',
        iog_jp_charity_detector_fn)

    assert len(rects) == 2
    x, y, w, h = rects[0]
    assert (x == 993)
    assert (y == 756)
    assert (w == 753)
    assert (h == 233)

    x1, y1, w1, h1 = rects[1]
    assert (x1 == 681)
    assert (y1 == 756)
    assert (w1 == 285)
    assert (h1 == 233)
