import ipywidgets
import numpy as np
from ipywidgets import HBox, VBox, fixed

from scanplot.plotting import draw_axes_mapping_lines
from scanplot.types import ConverterParameters, ImageLike

from .mapper_js_widget import MapperCanvasWidget


class CartesianCoordsMapperWidget:
    def __init__(self, plot_image: ImageLike):
        self._image = plot_image
        self._image_height = self._image.shape[0]
        self._image_width = self._image.shape[1]

        self._canvas_mapper_widget = self._init_canvas_mapper_widget()
        self._x1_widget = self._get_x1_widget()
        self._x2_widget = self._get_x2_widget()
        self._y1_widget = self._get_y1_widget()
        self._y2_widget = self._get_y2_widget()
        self._x_axis_type_dropdown = self._get_x_axis_type_dropdown()
        self._y_axis_type_dropdown = self._get_y_axis_type_dropdown()

    @property
    def _x1_pixel_position(self):
        return round(self._canvas_mapper_widget.vline_left)

    @property
    def _x2_pixel_position(self):
        return round(self._canvas_mapper_widget.vline_right)

    @property
    def _y1_pixel_position(self):
        return round(self._canvas_mapper_widget.hline_lower)

    @property
    def _y2_pixel_position(self):
        return round(self._canvas_mapper_widget.hline_upper)

    @property
    def _is_valid(self) -> bool:
        return (self._x1_widget.value != self._x2_widget.value) and \
            (self._y1_widget.value != self._y2_widget.value)  # fmt: skip

    def apply_widget_settings(
        self,
        fig_size: float = 8,
        line_width: float = 1,
        line_color: str = "red",
        marker_size: float = 6,
        marker_color: str = "green",
    ) -> None:
        self._canvas_mapper_widget.apply_widget_settings(
            fig_size=fig_size,
            line_width=line_width,
            line_color=line_color,
            marker_size=marker_size,
            marker_color=marker_color,
        )

    def widget(self) -> ipywidgets.widgets.widget_box:
        """
        Creates an interactive widget for mapping pixel coords and plot axes coords
        """
        box3 = VBox(
            [
                self._x1_widget,
                self._x2_widget,
                self._y1_widget,
                self._y2_widget,
                self._x_axis_type_dropdown,
                self._y_axis_type_dropdown,
            ]
        )
        box_final = HBox([self._canvas_mapper_widget, box3])

        return box_final

    def export_parameters(self) -> ConverterParameters:

        params = ConverterParameters(
            x_min_px=self._x1_pixel_position,
            x_max_px=self._x2_pixel_position,
            y_min_px=self._y1_pixel_position,
            y_max_px=self._y2_pixel_position,
            x_min_factual=self._x1_widget.value,
            x_max_factual=self._x2_widget.value,
            y_min_factual=self._y1_widget.value,
            y_max_factual=self._y2_widget.value,
            x_axis_type=self._x_axis_type_dropdown.value,
            y_axis_type=self._y_axis_type_dropdown.value,
        )
        return params

    def _init_canvas_mapper_widget(self):
        canvas_widget = MapperCanvasWidget()
        canvas_widget.set_image(self._image)
        return canvas_widget

    @staticmethod
    def _get_x1_widget():
        return ipywidgets.FloatText(
            value=0,
            description="X1:",
            step=0.01,
            disabled=False,
            layout=ipywidgets.Layout(width="150px"),
        )

    @staticmethod
    def _get_y1_widget():
        return ipywidgets.FloatText(
            value=0,
            description="Y1:",
            step=0.01,
            disabled=False,
            layout=ipywidgets.Layout(width="150px"),
        )

    @staticmethod
    def _get_x2_widget():
        return ipywidgets.FloatText(
            value=1,
            description="X2:",
            step=0.01,
            disabled=False,
            layout=ipywidgets.Layout(width="150px"),
        )

    @staticmethod
    def _get_y2_widget():
        return ipywidgets.FloatText(
            value=1,
            description="Y2:",
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


class CoordinatesMapperWidget:
    def __init__(self, plot_image: ImageLike):
        self.image = plot_image
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

        self._fig_size: int = 10
        self._line_color: str = "red"
        self._key_points_marker: str = "x"
        self._key_points_marker_color: str = "green"

    def apply_widget_settings(
        self,
        fig_size: int | None = None,
        line_color: str | None = None,
        key_points_marker: str | None = None,
        key_points_marker_color: str | None = None,
    ) -> None:
        """
        :param fig_size: figure size
        :param line_color: color of horizontal and vertical lines
        :param key_points_marker_color: color of the marker at lines intersection point
        :param key_points_marker: type of the marker at lines intersection point
        """
        if fig_size:
            self._fig_size = fig_size
        if line_color:
            self._line_color = line_color
        if key_points_marker:
            self._key_points_marker
        if key_points_marker_color:
            self._key_points_marker_color

    def widget(self) -> ipywidgets.widgets.widget_box:
        """
        Creates an interactive widget for mapping pixel coords and plot axes coords
        """
        widget = ipywidgets.interactive(
            draw_axes_mapping_lines,
            y_pos=self.y_slider,
            x_pos=self.x_slider,
            source_image=fixed(self.image),
            fig_size=fixed(self._fig_size),
            line_color=fixed(self._line_color),
            key_points_marker_color=fixed(self._key_points_marker_color),
            key_points_marker=fixed(self._key_points_marker),
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

    def export_parameters(self) -> ConverterParameters:
        params = ConverterParameters(
            x_min_px=self.x_slider.value[0],
            x_max_px=self.x_slider.value[1],
            y_min_px=self.image_height - self.y_slider.value[0],
            y_max_px=self.image_height - self.y_slider.value[1],
            x_min_factual=self.x_min_widget.value,
            x_max_factual=self.x_max_widget.value,
            y_min_factual=self.y_min_widget.value,
            y_max_factual=self.y_max_widget.value,
            x_axis_type=self.x_axis_type_dropdown.value,
            y_axis_type=self.y_axis_type_dropdown.value,
        )
        return params

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
