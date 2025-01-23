import ipywidgets
import numpy as np
from ipywidgets import VBox, fixed

from scanplot.core.detector import Detector
from scanplot.plotting import draw_points_on_image
from scanplot.types import ArrayNx2



class DetectorWidgetCombined:
    def __init__(self, plot):
        self.plot = plot

        self._marker_labels = self.plot.markers.keys()
        self._detector_widget_objects = [DetectorWidget(self.plot, marker=m) for m in self._marker_labels]

    def apply_widget_settings(
        self,
        fig_size: int = 10,
        marker_size: int = 60,
        marker_color: str = "yellow",
        marker_type: str = "*",
    ) -> None:
        for widget_object in self._detector_widget_objects:
            widget_object.apply_widget_settings(
                fig_size=fig_size,
                marker_size=marker_size,
                marker_color=marker_color,
                marker_type=marker_type,
            )

    def widget(self):
      
        detector_widgets = [widget_object.widget() for widget_object in self._detector_widget_objects]

        combined_detector_widget = ipywidgets.Tab(detector_widgets)
        for i in range(len(self._marker_labels)):
            combined_detector_widget.set_title(i, f"marker{i+1}")
        
        return combined_detector_widget
    

    def get_detections(self) -> dict[str, ArrayNx2]:
        all_detections = dict()
        for marker_label, widget_object in zip(self._marker_labels, self._detector_widget_objects):
            points = widget_object.get_detections()
            all_detections[marker_label] = points
        
        return all_detections



class DetectorWidget:
    def __init__(self, plot, marker: str):
        self.detector = Detector(plot, marker)
        self.image = plot.data
        self.points_num_slider = self._get_points_num_slider()
        self.points_density_slider = self._get_points_density_slider()

        self._fig_size: int = 10
        self._marker_size: int = 60
        self._marker_color: str = "yellow"
        self._marker_type: str = "*"


    def apply_widget_settings(
        self,
        fig_size: int | None = None,
        marker_size: int | None = None,
        marker_color: str | None = None,
        marker_type: str | None = None,
    ) -> None:
        if fig_size:
            self._fig_size = fig_size
        if marker_size:
            self._marker_size = marker_size
        if marker_color:
            self._marker_color = marker_color
        if marker_type:
            self._marker_type = marker_type


    def widget(self) -> ipywidgets.widgets.widget_box:
        widget = ipywidgets.interactive(
            self.detect_and_draw,
            points_num_slider_value=self.points_num_slider,
            points_density_slider_value=self.points_density_slider,
        )
        image_with_points_widget = widget.children[-1]

        box = VBox(
            [
                self.points_num_slider,
                self.points_density_slider,
                image_with_points_widget,
            ],
            layout=ipywidgets.Layout(align_items="stretch"),
        )
        return box

    def get_detections(self) -> ArrayNx2:
        return self.detector.detect_points()

    @staticmethod
    def _get_points_num_slider(start_value: int = 20):
        return ipywidgets.FloatSlider(
            value=start_value,
            min=0,
            max=65,
            step=0.1,
            description="Points Number:",
            disabled=False,
            continuous_update=True,
            orientation="horizontal",
            readout=True,
            readout_format="d",
            layout=ipywidgets.Layout(width="500px"),
            style={"description_width": "initial"},
        )

    @staticmethod
    def _get_points_density_slider(start_value: int = 20):
        return ipywidgets.FloatSlider(
            value=start_value,
            min=0,
            max=100,
            step=1,
            description="Points Density:",
            disabled=False,
            continuous_update=True,
            orientation="horizontal",
            readout=True,
            readout_format="d",
            layout=ipywidgets.Layout(width="500px"),
            style={"description_width": "initial"},
        )

    def detect_and_draw(
        self,
        points_num_slider_value: float,
        points_density_slider_value: float,
    ) -> None:
        
        self.detector.points_num = points_num_slider_value
        self.detector.points_density = points_density_slider_value
        points = self.detector.detect_points()

        draw_points_on_image(
            points=points,
            image=self.image,
            fig_size=self._fig_size,
            marker_size=self._marker_size,
            marker_color=self._marker_color,
            marker_type=self._marker_type,
        )
