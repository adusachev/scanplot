from enum import Enum

import numpy as np

from scanplot.types import ArrayN, ConverterParameters


class AxisType(Enum):
    LINEAR = "linear"
    LOGSCALE = "logscale"


class CoordinatesConverter:
    def __init__(self, params: ConverterParameters):
        self.x_min_px: int = params.x_min_px
        self.x_max_px: int = params.x_max_px
        self.y_min_px: int = params.y_min_px
        self.y_max_px: int = params.y_max_px

        self.x_min_factual: float = params.x_min_factual
        self.x_max_factual: float = params.x_max_factual
        self.y_min_factual: float = params.y_min_factual
        self.y_max_factual: float = params.y_max_factual

        self.x_axis_type = AxisType(params.x_axis_type)
        self.y_axis_type = AxisType(params.y_axis_type)

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
