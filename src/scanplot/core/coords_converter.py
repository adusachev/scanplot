class CoordinatesConverter:
    def __init__(
        self,
        x_min_px: int,
        x_max_px: int,
        y_min_px: int,
        y_max_px: int,
        x_min_real: float,
        x_max_real: float,
        y_min_real: float,
        y_max_real: float,
        x_logscale: bool,
        y_logscale: bool,
    ):
        self.x_min_px = x_min_px
        self.x_max_px = x_max_px
        self.y_min_px = y_min_px
        self.y_max_px = y_max_px

        self.x_min_real = x_min_real
        self.x_max_real = x_max_real
        self.y_min_real = y_min_real
        self.y_max_real = y_max_real

        self.x_logscale = x_logscale
        self.y_logscale = y_logscale

    def pixel_to_real(self, x_pixel: int, y_pixel: int) -> tuple[float, float]:
        x_real = self._convert_x_axis_linear(x_pixel)
        y_real = self._convert_y_axis_linear(y_pixel)

        return x_real, y_real

    def _convert_x_axis_linear(self, x_pixel: int) -> float:
        """
        Converts x-axis pixel value into real value
        """
        alpha_x = (self.x_max_real - self.x_min_real) / (self.x_max_px - self.x_min_px)

        if x_pixel >= self.x_min_px:
            x_real = alpha_x * (x_pixel - self.x_min_px) + self.x_min_real
        else:
            x_real = self.x_min_real - alpha_x * (self.x_min_px - x_pixel)

        return x_real

    def _convert_y_axis_linear(self, y_pixel: int) -> float:
        """
        Converts y-axis pixel value into real value
         (assumed that Y pixels coords grow from top to bottom)
        """
        assert self.y_min_px > self.y_max_px, "Y pixels coords grow from top to bottom"

        alpha_y = (self.y_max_real - self.y_min_real) / (self.y_min_px - self.y_max_px)

        if y_pixel >= self.y_min_px:
            y_real = self.y_min_real + alpha_y * (self.y_min_px - y_pixel)
        else:
            y_real = self.y_min_real - alpha_y * (y_pixel - self.y_min_px)

        return y_real

    def _convert_x_axis_logscale(self):
        raise NotImplementedError

    def _convert_y_axis_logscale(self):
        raise NotImplementedError
