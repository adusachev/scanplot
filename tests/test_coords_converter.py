import pytest

from scanplot.core.coords_converter import AxisType, CoordinatesConverter


@pytest.mark.parametrize(
    "x_px, y_px, x_factual, y_factual, tolerance",
    [(90, 164, 0.1, 0.2, 1e-3), (335, 74, 0.7, 0.6, 1e-3)],
)
def test_from_pixel_linear(x_px, y_px, x_factual, y_factual, tolerance):
    converter = CoordinatesConverter()

    # plot 59
    converter.set_parameters(
        x_min_px=49,
        x_max_px=294,
        y_min_px=209,
        y_max_px=29,
        x_min_factual=0,
        x_max_factual=0.6,
        y_min_factual=0,
        y_max_factual=0.8,
        x_axis_type=AxisType.LINEAR,
        y_axis_type=AxisType.LINEAR,
    )

    x_result, y_result = converter.from_pixel(x_pixel=x_px, y_pixel=y_px)
    assert abs(x_result - x_factual) < tolerance
    assert abs(y_result - y_factual) < tolerance
