import cv2 as cv
from jupyter_bbox_widget import BBoxWidget

from scanplot.types import ImageLike


class ROISelectorBBoxWidget(BBoxWidget):
    def __init__(self, image_data: ImageLike, markers_number: int):
        assert markers_number >= 1, "Number of markers should be >= 1"
        self.image_data = image_data
        self.markers_number = markers_number

        super().__init__(
            hide_buttons=True,
            classes=[f"ROI for marker{i+1}" for i in range(self.markers_number)],
            image_bytes=cv.imencode(".png", self.image_data)[1].tobytes(),
        )
