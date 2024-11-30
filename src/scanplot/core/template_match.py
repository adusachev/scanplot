import logging
from typing import List, Tuple

import cv2 as cv
import numpy as np
import numpy_indexed as npi

logger = logging.getLogger("base_logger")

from .corr_map_operations import invert_correlation_map, normalize_map


def template_match(
    image: np.ndarray,
    template: np.ndarray,
    template_mask: np.ndarray,
    method_name: str = "cv.TM_SQDIFF_NORMED",
    norm_result: bool = False,
) -> Tuple[np.ndarray, float]:
    """
    Run opencv templateMatch.
    Return correlation map and maximum value on map.
    """
    method = eval(method_name)
    correlation_map = cv.matchTemplate(image, template, method, mask=template_mask)

    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        logger.debug(
            f"Correlation map bounds: {np.nanmin(correlation_map), np.nanmax(correlation_map)}"
        )
        logger.debug("Correlation map was inverted")
        correlation_map = invert_correlation_map(correlation_map)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(correlation_map)

    if norm_result:
        correlation_map = normalize_map(correlation_map)
    return correlation_map, max_val


def detect_points(
    convolution_map: np.ndarray, max_value: float, tolerance: float
) -> np.ndarray:

    max_positions = np.where(np.isclose(convolution_map, max_value, atol=tolerance))
    y, x = max_positions
    points = np.array([x, y]).T

    return points


def find_tolerance_limit(convolution_map: np.ndarray) -> float:
    tolerance_range = np.arange(0, 2, 0.001)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(convolution_map)

    for i, tolerance in enumerate(tolerance_range):
        points = detect_points(convolution_map, max_val, tolerance)
        points_number = len(points)
        if points_number > 1000:
            tolerance_limit = tolerance_range[i - 1]
            return tolerance_limit

    return tolerance_range[-1]


# def detect_points_v1(
#     convolution_map: np.ndarray,
#     max_value: float,
#     tolerance: float,
#     convolution_map_ccoef: np.ndarray
# ) -> np.ndarray:
#     """
#     Берет convolution_map_ccoef полученную из cv.TM_CCOEFF_NORMED,
#      и делает по ней дополнительную фильтрацию - смотрит, где convolution_map_ccoef не NaN
#     """
#     max_positions = np.where( np.isclose(convolution_map, max_value, atol=tolerance) )
#     y, x = max_positions
#     max_points = np.array([x, y]).T

#     area_of_interest = np.where( np.isnan(convolution_map_ccoef) == False )
#     y, x = area_of_interest
#     area_of_interest_points = np.array([x, y]).T

#     points = npi.intersection(max_points, area_of_interest_points)

#     return points


# def find_tolerance_limit_v1(
#     convolution_map: np.ndarray,
#     convolution_map_ccoef: np.ndarray
# ) -> float:
#     """
#     Использует detect_points_v1
#     """
#     tolerance_range = np.arange(0, 2, 0.001)
#     min_val, max_val, min_loc, max_loc = cv.minMaxLoc(convolution_map)

#     for i, tolerance in enumerate(tolerance_range):
#         # points = detect_points(convolution_map, max_val, tolerance)
#         points = detect_points_v1(convolution_map, max_val, tolerance, convolution_map_ccoef)
#         points_number = len(points)
#         if points_number > 1000:
#             tolerance_limit = tolerance_range[i-1]
#             return tolerance_limit

#     return tolerance_range[-1]
