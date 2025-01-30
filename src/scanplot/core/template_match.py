import logging
from typing import List, Tuple

import cv2 as cv
import numpy as np
import numpy_indexed as npi

from scanplot.types import ArrayNx2, ArrayNxM, ImageLike

logger = logging.getLogger(__name__)

from .corr_map_operations import invert_correlation_map, normalize_map


def template_match(
    image: ImageLike,
    template: ImageLike,
    template_mask: ArrayNxM,
    method_name: str = "cv.TM_SQDIFF_NORMED",
    norm_result: bool = False,
) -> Tuple[ArrayNxM, float]:
    """
    Run opencv templateMatch.
    Return correlation map and maximum value on map.
    Normalize output map if required.
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
    convolution_map: ArrayNxM, max_value: float, tolerance: float
) -> ArrayNx2:

    max_positions = np.where(np.isclose(convolution_map, max_value, atol=tolerance))
    y, x = max_positions
    points = np.array([x, y]).T

    return points


def find_tolerance_limit(convolution_map: ArrayNxM) -> float:
    tolerance_range = np.arange(0, 2, 0.001)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(convolution_map)

    for i, tolerance in enumerate(tolerance_range):
        points = detect_points(convolution_map, max_val, tolerance)
        points_number = len(points)
        if points_number > 1000:
            tolerance_limit = tolerance_range[i - 1]
            return tolerance_limit

    return tolerance_range[-1]
