import cv2 as cv
import ipywidgets
from jupyter_bbox_widget import BBoxWidget

from scanplot.types import ImageLike


class ROISelectorBaseWidget(BBoxWidget):
    def __init__(self, image_data: ImageLike, markers_number: int):
        assert markers_number >= 1, "Number of markers should be >= 1"
        self.image_data = image_data
        self.markers_number = markers_number

        super().__init__(
            hide_buttons=True,
            classes=[f"ROI for marker{i+1}" for i in range(self.markers_number)],
            image_bytes=cv.imencode(".png", self.image_data)[1].tobytes(),
        )

    def widget(self):
        return self


class ROISelectorCombinedWidget:
    def __init__(
        self,
        image_data: ImageLike,
        markers_number: int,
        fig_size: int = 10,
    ):
        assert markers_number >= 1, "Number of markers should be >= 1"
        self.image_data = image_data
        self.markers_number = markers_number

        self._fig_size: int = fig_size

        self._marker_labels: list[str] = [
            f"marker{i+1}" for i in range(self.markers_number)
        ]
        self._roi_selector_widgets: list[BBoxWidget] = self._init_roi_widgets()

    @property
    def bboxes(self) -> list[dict]:
        """
        Return bboxes from each roi selector widget
        """
        all_bboxes = []
        for roi_selector_widget in self._roi_selector_widgets:
            all_bboxes.extend(roi_selector_widget.bboxes)
        return all_bboxes

    @property
    def _fig_size_px(self) -> int:
        return 50 * self._fig_size

    def widget(self):
        """
        Creates a Tab widget.
        Number of tabs is equal to markers number.
        Each tab contains BBoxWidget.
        """
        combined_roi_selector_widget = ipywidgets.Tab(self._roi_selector_widgets)
        for i, marker_label in enumerate(self._marker_labels):
            combined_roi_selector_widget.set_title(i, marker_label)

        return combined_roi_selector_widget

    def _init_roi_widgets(self) -> list[BBoxWidget]:
        roi_selector_widgets = []

        for marker_label in self._marker_labels:
            widget = BBoxWidget(
                hide_buttons=True,
                classes=[f"ROI for {marker_label}"],
                image_bytes=cv.imencode(".png", self.image_data)[1].tobytes(),
                colors=["green"],
                layout={
                    "width": f"{self._fig_size_px}px",
                    "height": f"{self._fig_size_px}px",
                },
            )
            roi_selector_widgets.append(widget)

        return roi_selector_widgets
