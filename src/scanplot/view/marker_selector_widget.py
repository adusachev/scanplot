import cv2 as cv
import numpy as np
from jupyter_bbox_widget import BBoxWidget

from scanplot.types import ImageLike


class MarkerSelectorWidget(BBoxWidget):
    def __init__(
        self,
        image_data: ImageLike,
        markers_number: int,
        fig_size: int = 10,
    ):
        assert markers_number >= 1, "Number of markers should be >= 1"
        self.image_data = image_data
        self.markers_number = markers_number

        self._marker_labels: list[str] = [
            f"marker{i+1}" for i in range(self.markers_number)
        ]

        # control widget size
        self._fig_size = fig_size
        self._scaling_factor = fig_size / 10
        h_image, w_image = image_data.shape[0], image_data.shape[1]
        # add 120 to prevent hiding buttons
        self._widget_height_px = int(h_image * self._scaling_factor) + 120
        self._widget_width_px = int(w_image * self._scaling_factor)

        super().__init__(
            hide_buttons=True,
            classes=self._marker_labels,
            image_bytes=cv.imencode(".png", self.image_data)[1].tobytes(),
            layout={
                "width": f"{self._widget_width_px}px",
                "height": f"{self._widget_height_px}px",
            },
        )

    def widget(self):
        return self

    def validate_bboxes(self):
        if len(self.bboxes) < self.markers_number:
            raise Exception(
                f"Need to select {self.markers_number} BBoxes, one BBox for each marker type"
            )

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
