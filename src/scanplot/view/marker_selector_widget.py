import cv2 as cv
import numpy as np
from jupyter_bbox_widget import BBoxWidget


class MarkerSelectorBBoxWidget(BBoxWidget):
    def __init__(self, image_data: np.ndarray, markers_number: int):
        assert markers_number >= 1, "Number of markers should be >= 1"
        self.image_data = image_data
        self.markers_number = markers_number

        super().__init__(
            hide_buttons=True,
            classes=[f"marker{i+1}" for i in range(self.markers_number)],
            image_bytes=cv.imencode(".png", self.image_data)[1].tobytes(),
        )

    def widget(self):
        return self

    def validate_bboxes(self):
        if len(self.bboxes) < self.markers_number:
            raise Exception(f"Need to select {self.markers_number} BBoxes")

        bboxes_labels_count = dict()
        for bbox in self.bboxes:
            label = bbox["label"]
            if label not in bboxes_labels_count:
                bboxes_labels_count[label] = 1
            else:
                bboxes_labels_count[label] += 1

        for label, count in bboxes_labels_count.items():
            if count > 1:
                raise Exception(
                    f"More than one BBox with {label=} have been selected, should be only one BBox for each marker"
                )
