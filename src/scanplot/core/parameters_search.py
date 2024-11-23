from typing import Tuple

import numpy as np


def linear_parameter_transform(
    parameter: float, a: float = -0.01, b: float = 1, round_decimals: int | None = None
) -> float:
    """
    Linear transform y = a * x + b
    """
    parameter_transformed = a * parameter + b
    if round_decimals:
        parameter_transformed = np.round(parameter_transformed, decimals=round_decimals)

    return parameter_transformed


def get_corr_map_maximums(
    correlation_map: np.ndarray, treshold: float
) -> Tuple[np.ndarray, int]:
    """
    Return coordinades of points on 2D correlation map,
     which have value greater than given treshold
    """
    maximums = np.where(correlation_map >= treshold)
    y_points, x_points = maximums
    points = np.stack((x_points, y_points)).T
    number_of_maximums = len(points)

    return points, number_of_maximums
