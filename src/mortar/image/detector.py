import os
from typing import Callable

import cv2
from cv2.typing import MatLike


class Detector:
    def __init__(self) -> None:
        self.img: MatLike | None = None

    def detect_rects(
        self,
        img_path: str,
        fn: Callable[[int, int, int, int], bool],
        draw: bool = False
    ) -> list[tuple[int, int, int, int]]:
        """
        Detects all rectangles in the provided image.

        Arg img_path is where the image will be loaded from.

        Arg fn will be called like fn(x,y,w,h) with detected rectangles,
        and is expected to return a bool.
        If it returns True, that rect will be included in the output.

        Arg draw is optional and defaults to False,
        It is used mostly for debugging. Will modify self.img with drawn rects.
        """
        self.img = cv2.imread(img_path)

        # Grayscale and threshold image for easier detecting
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 50, 255, 0)
        # List all contours
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        rects: list[tuple[int, int, int, int]] = []

        for cnt in contours:
            # Compute approximate contour vertex points
            approx = cv2.approxPolyDP(
                cnt, 0.01 * cv2.arcLength(cnt, True), True
            )
            # Rectangles have 4 vertices
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(cnt)
                include_rect = True
                if (fn is not None):
                    # Check against fn predicate to filter out unwanted rects
                    # This is the chance for include_rect to be false
                    include_rect = fn(x, y, w, h)
                if include_rect:
                    print(f"({x},{y}), w: {w}, h: {h}")
                    rects.append((x, y, w, h))

                    # If draw is true, draw over the image to show the rect
                    if draw is True:
                        self.img = cv2.drawContours(
                            self.img, [cnt], -1, (0, 255, 0), 3
                        )
        return rects


def main() -> None:
    detector = Detector()

    def my_condition(_x: int, _y: int, _w: int, h: int) -> bool:
        return h > 200

    rects = detector.detect_rects(
        f'{os.getcwd()}/tests/data/detector/iog_top_big.png',
        my_condition,
        True
    )

    print(rects)

    assert detector.img is not None

    cv2.imshow("Shapes", detector.img)
    _ = cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
