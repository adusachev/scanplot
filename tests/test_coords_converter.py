import pytest

from scanplot.core.coords_converter import AxisType, CoordinatesConverter
from scanplot.types import ConverterParameters


@pytest.mark.parametrize(
    "x_px, y_px, x_factual, y_factual, tolerance",
    [(90, 164, 0.1, 0.2, 1e-3), (335, 74, 0.7, 0.6, 1e-3)],
)
def test_from_pixel_linear(x_px, y_px, x_factual, y_factual, tolerance):

    # plot 59
    converter_params = ConverterParameters(
        x_min_px=49,
        x_max_px=294,
        y_min_px=209,
        y_max_px=29,
        x_min_factual=0,
        x_max_factual=0.6,
        y_min_factual=0,
        y_max_factual=0.8,
        x_axis_type="linear",
        y_axis_type="linear",
    )

    converter = CoordinatesConverter(converter_params)

    x_result, y_result = converter.from_pixel(x_pixel=x_px, y_pixel=y_px)
    assert abs(x_result - x_factual) < tolerance
    assert abs(y_result - y_factual) < tolerance


@pytest.mark.parametrize(
    "x_px, y_px, x_factual, y_factual, tolerance",
    [(80.5, 364, 24669, 80872, 1), (280.5, 217, 10151633, 9838022, 1)],
)
def test_from_pixel_logscale(x_px, y_px, x_factual, y_factual, tolerance):

    converter_params = ConverterParameters(
        x_min_px=127,
        x_max_px=433,
        y_min_px=428,
        y_max_px=146,
        x_min_factual=1e5,
        x_max_factual=1e9,
        y_min_factual=1e4,
        y_max_factual=1e8,
        x_axis_type="logscale",
        y_axis_type="logscale",
    )

    converter = CoordinatesConverter(converter_params)

    x_result, y_result = converter.from_pixel(x_pixel=x_px, y_pixel=y_px)
    assert abs(x_result - x_factual) < tolerance
    assert abs(y_result - y_factual) < tolerance
