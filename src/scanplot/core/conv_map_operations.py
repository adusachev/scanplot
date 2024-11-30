import logging
from typing import List, Tuple

import numpy as np

logger = logging.getLogger("base_logger")


def remove_nan_inf(map: np.ndarray) -> np.ndarray:
    """
    Replace all NaN and Inf values with zero values

    :param map: 2d array
    """
    map2 = np.copy(map)
    nan_indexes = np.where(np.isnan(map))
    inf_indexes = np.where(np.isinf(map))
    logger.debug(f"Number of NaN values: {len(nan_indexes[0])}")
    logger.debug(f"Number of inf values: {len(inf_indexes[0])}")
    map2[nan_indexes] = 0
    map2[inf_indexes] = 0
    return map2


def invert_correlation_map(correlation_map: np.ndarray) -> np.ndarray:
    """
    Invert 2D array with float values
    """
    inverted_correlation_map = (-correlation_map) + np.nanmax(correlation_map)
    return inverted_correlation_map


def normalize_map(map: np.ndarray) -> np.ndarray:
    return map / np.nanmax(map)


def get_first_N_maximums(
    corr_map: np.ndarray, N: int
) -> List[Tuple[float, Tuple[int, int]]]:
    """
    Return first N max elements values and indices in 2d map

    :param corr_map: 2d array (correlation map or accumulator array)
    :param N: number of maximums
    :return: list of elements (max_value, (max_index_y, max_index_x))
    """
    indices = corr_map.ravel().argsort()[-N:]
    indices = (np.unravel_index(i, corr_map.shape) for i in indices)

    return [(corr_map[i], i) for i in indices]
