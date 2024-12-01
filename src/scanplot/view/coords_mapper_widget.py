import ipywidgets
import numpy as np
from ipywidgets import HBox, VBox, fixed

from scanplot.plotting import draw_axes_mapping_lines


class CoordinatesMapper:
    def __init__(self, source_image: np.ndarray):
        self.image = source_image
        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]

        self.x_slider = self._get_x_slider()
        self.y_slider = self._get_y_slider()
        self.x_min_widget = self._get_x_min_widget()
        self.x_max_widget = self._get_x_max_widget()
        self.y_min_widget = self._get_y_min_widget()
        self.y_max_widget = self._get_y_max_widget()
        self.x_axis_type_dropdown = self._get_x_axis_type_dropdown()
        self.y_axis_type_dropdown = self._get_y_axis_type_dropdown()

    def interactive_widget(
        self,
        fig_size: int = 10,
        line_color: str = "red",
        key_points_marker: str = "x",
        key_points_marker_color: str = "green",
    ) -> ipywidgets.widgets.widget_box:
        """
        Creates an interactive widget for mapping pixel coords and plot axes coords

        :param fig_size: figure size
        :param line_color: color of horizontal and vertical lines
        :param key_points_marker_color: color of the marker at lines intersection point
        :param key_points_marker: type of the marker at lines intersection point
        """
        widget = ipywidgets.interactive(
            draw_axes_mapping_lines,
            y_pos=self.y_slider,
            x_pos=self.x_slider,
            source_image=fixed(self.image),
            fig_size=fixed(fig_size),
            line_color=fixed(line_color),
            key_points_marker_color=fixed(key_points_marker_color),
            key_points_marker=fixed(key_points_marker),
        )
        image_with_lines_widget = widget.children[-1]

        box1 = HBox(
            [self.y_slider, image_with_lines_widget],
            layout=ipywidgets.Layout(align_items="center"),
        )
        box2 = VBox(
            [self.x_slider, box1], layout=ipywidgets.Layout(align_items="center")
        )
        box3 = VBox(
            [
                self.x_min_widget,
                self.x_max_widget,
                self.y_min_widget,
                self.y_max_widget,
                self.x_axis_type_dropdown,
                self.y_axis_type_dropdown,
            ]
        )
        box_final = HBox([box2, box3])

        return box_final

    def _get_x_slider(self):
        return ipywidgets.IntRangeSlider(
            value=[0, self.image_width],
            min=0,
            max=self.image_width,
            step=1,
            description="X_min, X_max:",
            disabled=False,
            continuous_update=True,
            orientation="horizontal",
            readout=True,
            readout_format="d",
            layout=ipywidgets.Layout(width="500px"),
            style={"description_width": "initial"},
        )

    def _get_y_slider(self):
        return ipywidgets.IntRangeSlider(
            value=[0, self.image_height],
            min=0,
            max=self.image_height,
            step=1,
            description="Y_min, Y_max:",
            disabled=False,
            continuous_update=True,
            orientation="vertical",
            readout=True,
            readout_format="d",
            layout=ipywidgets.Layout(height="300px"),
            style={"description_width": "initial"},
        )

    @property
    def _is_valid(self) -> bool:
        return (self.x_min_widget.value != self.x_max_widget.value) and \
            (self.y_min_widget.value != self.y_max_widget.value)  # fmt: skip

    @staticmethod
    def _get_x_min_widget():
        return ipywidgets.FloatText(
            value=0,
            description="X_min:",
            step=0.01,
            disabled=False,
            layout=ipywidgets.Layout(width="150px"),
        )

    @staticmethod
    def _get_y_min_widget():
        return ipywidgets.FloatText(
            value=0,
            description="Y_min:",
            step=0.01,
            disabled=False,
            layout=ipywidgets.Layout(width="150px"),
        )

    @staticmethod
    def _get_x_max_widget():
        return ipywidgets.FloatText(
            value=1,
            description="X_max:",
            step=0.01,
            disabled=False,
            layout=ipywidgets.Layout(width="150px"),
        )

    @staticmethod
    def _get_y_max_widget():
        return ipywidgets.FloatText(
            value=1,
            description="Y_max:",
            step=0.01,
            disabled=False,
            layout=ipywidgets.Layout(width="150px"),
        )

    @staticmethod
    def _get_x_axis_type_dropdown():
        return ipywidgets.Dropdown(
            options=["linear", "logscale"],
            value="linear",
            description="X axis type:",
            disabled=False,
            layout={"width": "180px"},
        )

    @staticmethod
    def _get_y_axis_type_dropdown():
        return ipywidgets.Dropdown(
            options=["linear", "logscale"],
            value="linear",
            description="Y axis type:",
            disabled=False,
            layout={"width": "180px"},
        )
