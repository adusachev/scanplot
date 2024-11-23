import numpy as np

import logging

logger = logging.getLogger("base_logger")


def replace_black_pixels(image_rgb: np.ndarray, value: int = 10) -> np.ndarray:
    """
    Replace all [0, 0, 0] pixels on RGB image with [value, value, value] pixels
    """
    image = np.copy(image_rgb)

    if len(image.shape) == 3:
        zero_indexes = np.where(
            (image[:, :, 0] == 0) & (image[:, :, 1] == 0) & (image[:, :, 2] == 0)
        )
        y, x = zero_indexes
        image[y, x, :] = value
    elif len(image.shape) == 2:
        logger.warning("Image is 1-channel")
        zero_indexes = np.where(image == 0)
        y, x = zero_indexes
        image[y, x] = value

    logger.debug(f"Number of black pixels on image: {len(zero_indexes[0])}")
    return image
