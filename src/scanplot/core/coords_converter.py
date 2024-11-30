from enum import Enum

import numpy as np

from scanplot.view.coords_mapper_widget import CoordinatesMapper


class AxisType(Enum):
    LINEAR = "linear"
    LOGSCALE = "logscale"


class CoordinatesConverter:
    def __init__(self):
        self.x_min_px: int = None
        self.x_max_px: int = None
        self.y_min_px: int = None
        self.y_max_px: int = None

        self.x_min_factual: float = None
        self.x_max_factual: float = None
        self.y_min_factual: float = None
        self.y_max_factual: float = None

        self.x_axis_type: AxisType = None
        self.y_axis_type: AxisType = None

    def from_pixel(
        self, x_pixel: int | np.ndarray, y_pixel: int | np.ndarray
    ) -> tuple[float, float] | tuple[np.ndarray, np.ndarray]:

        if self.x_axis_type == AxisType.LINEAR:
            x_factual = self._convert_x_axis_linear(x_pixel)
        elif self.x_axis_type == AxisType.LOGSCALE:
            x_factual = self._convert_x_axis_logscale(x_pixel)

        if self.y_axis_type == AxisType.LINEAR:
            y_factual = self._convert_y_axis_linear(y_pixel)
        elif self.y_axis_type == AxisType.LOGSCALE:
            y_factual = self._convert_y_axis_logscale(y_pixel)

        return x_factual, y_factual

    def set_parameters(
        self,
        x_min_px: int,
        x_max_px: int,
        y_min_px: int,
        y_max_px: int,
        x_min_factual: float,
        x_max_factual: float,
        y_min_factual: float,
        y_max_factual: float,
        x_axis_type: str,
        y_axis_type: str,
    ) -> None:
        self.x_min_px = x_min_px
        self.x_max_px = x_max_px
        self.y_min_px = y_min_px
        self.y_max_px = y_max_px

        self.x_min_factual = x_min_factual
        self.x_max_factual = x_max_factual
        self.y_min_factual = y_min_factual
        self.y_max_factual = y_max_factual

        self.x_axis_type = AxisType(x_axis_type)
        self.y_axis_type = AxisType(y_axis_type)

    def import_parameters_from_mapper(self, mapper: CoordinatesMapper) -> None:
        if not mapper._is_valid:
            raise ValueError("Mapper is not valid, check X_min, X_max, Y_min, Y_max")
        self.x_min_px = mapper.x_slider.value[0]
        self.x_max_px = mapper.x_slider.value[1]
        self.y_min_px = mapper.image_height - mapper.y_slider.value[0]
        self.y_max_px = mapper.image_height - mapper.y_slider.value[1]

        self.x_min_factual = mapper.x_min_widget.value
        self.x_max_factual = mapper.x_max_widget.value
        self.y_min_factual = mapper.y_min_widget.value
        self.y_max_factual = mapper.y_max_widget.value

        self.x_axis_type = AxisType(mapper.x_axis_type_dropdown.value)
        self.y_axis_type = AxisType(mapper.y_axis_type_dropdown.value)

    def _convert_x_axis_linear(self, x_pixel: int) -> float:
        """
        Converts x-axis pixel value into real value
        """
        alpha_x = (self.x_max_factual - self.x_min_factual) / (self.x_max_px - self.x_min_px)  # fmt: skip

        if np.all(x_pixel >= self.x_min_px):
            x_factual = alpha_x * (x_pixel - self.x_min_px) + self.x_min_factual
        else:
            x_factual = self.x_min_factual - alpha_x * (self.x_min_px - x_pixel)

        return x_factual

    def _convert_y_axis_linear(self, y_pixel: int) -> float:
        """
        Converts y-axis pixel value into real value
         (assumed that Y pixels coords grow from top to bottom)
        """
        assert self.y_min_px > self.y_max_px, "Y pixels coords grow from top to bottom"

        alpha_y = (self.y_max_factual - self.y_min_factual) / (self.y_min_px - self.y_max_px)  # fmt: skip

        if np.all(y_pixel >= self.y_min_px):
            y_factual = self.y_min_factual + alpha_y * (self.y_min_px - y_pixel)
        else:
            y_factual = self.y_min_factual - alpha_y * (y_pixel - self.y_min_px)

        return y_factual

    def _convert_x_axis_logscale(self, x_pixel: int) -> float:
        log_x_min_factual = np.log10(self.x_min_factual)
        log_x_max_factual = np.log10(self.x_max_factual)

        alpha_x = (log_x_max_factual - log_x_min_factual) / (self.x_max_px - self.x_min_px)  # fmt: skip

        if np.all(x_pixel >= self.x_min_px):
            log_x_factual = alpha_x * (x_pixel - self.x_min_px) + log_x_min_factual
        else:
            log_x_factual = log_x_min_factual - alpha_x * (self.x_min_px - x_pixel)

        x_factual = 10**log_x_factual
        return x_factual

    def _convert_y_axis_logscale(self, y_pixel: int) -> float:
        log_y_min_factual = np.log10(self.y_min_factual)
        log_y_max_factual = np.log10(self.y_max_factual)

        assert self.y_min_px > self.y_max_px, "Y pixels coords grow from top to bottom"

        alpha_y = (log_y_max_factual - log_y_min_factual) / (self.y_min_px - self.y_max_px)  # fmt: skip

        if np.all(y_pixel >= self.y_min_px):
            log_y_factual = log_y_min_factual + alpha_y * (self.y_min_px - y_pixel)
        else:
            log_y_factual = log_y_min_factual - alpha_y * (y_pixel - self.y_min_px)

        y_factual = 10**log_y_factual
        return y_factual
