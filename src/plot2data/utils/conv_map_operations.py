import numpy as np

import logging
logger = logging.getLogger("base_logger")


def remove_nan_inf(map: np.ndarray) -> np.ndarray:
    """
    Replace all NaN and Inf values with zero values

    :param map: 2d array
    """
    map2 = np.copy(map)
    nan_indexes = np.where( np.isnan(map) )
    inf_indexes = np.where( np.isinf(map) )
    logger.debug(f"Number of NaN values: {len(nan_indexes[0])}")
    logger.debug(f"Number of inf values: {len(inf_indexes[0])}")
    map2[nan_indexes] = 0
    map2[inf_indexes] = 0
    return map2

