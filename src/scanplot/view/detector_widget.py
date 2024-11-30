import ipywidgets
import numpy as np
from ipywidgets import VBox, fixed

from scanplot.core.detector import detect_points_on_correlation_map
from scanplot.utils.drawing import draw_points_on_image


class DetectorWidget:
    def __init__(
        self,
        source_image: np.ndarray,
        template: np.ndarray,
        correlation_map: np.ndarray,
    ):
        self.source_image = source_image
        self.template = template
        self.correlation_map = correlation_map

        self.points_num_slider = self._get_points_num_slider()
        self.points_density_slider = self._get_points_density_slider()

    def main_widget(
        self,
        fig_size: int = 10,
        marker_size: int = 60,
        marker_color: str = "yellow",
        marker_type: str = "*",
    ) -> ipywidgets.widgets.widget_box:
        widget = ipywidgets.interactive(
            self.detect_and_draw,
            points_num=self.points_num_slider,
            points_density=self.points_density_slider,
            correlation_map=fixed(self.correlation_map),
            source_image=fixed(self.source_image),
            template=fixed(self.template),
            fig_size=fixed(fig_size),
            marker_size=fixed(marker_size),
            marker_color=fixed(marker_color),
            marker_type=fixed(marker_type),
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

    def get_detections(
        self, points_num: float | None = None, points_density: float | None = None
    ) -> np.ndarray:
        if points_num is None:
            points_num = self.points_num_slider.value
        if points_density is None:
            points_density = self.points_density_slider.value

        detected_points = detect_points_on_correlation_map(
            points_num,
            points_density,
            self.correlation_map,
            self.source_image,
            self.template,
        )
        return detected_points

    @staticmethod
    def _get_points_num_slider(start_value: int = 20):
        return ipywidgets.FloatSlider(
            value=start_value,
            min=0,
            max=100,
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

    @staticmethod
    def detect_and_draw(
        points_num: float,
        points_density: float,
        correlation_map: np.ndarray,
        source_image: np.ndarray,
        template: np.ndarray,
        fig_size: int = 10,
        marker_size: int = 60,
        marker_color: str = "yellow",
        marker_type: str = "*",
    ) -> None:
        points = detect_points_on_correlation_map(
            points_num, points_density, correlation_map, source_image, template
        )
        draw_points_on_image(
            points,
            source_image,
            fig_size,
            marker_size,
            marker_color,
            marker_type,
        )
