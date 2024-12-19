import logging

import numpy as np

logger = logging.getLogger(__name__)


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


def bboxes_to_roi(image: np.ndarray, roi_bboxes: list[dict]) -> np.ndarray:
    """
    Creates ROI for image based on the list of bboxes.

    :param roi_bboxes: list of bboxes
      Example: bbox = {'x': 424, 'y': 494, 'width': 52, 'height': 69, 'label': 'ROI'}
    :return: 2D array with values (0, 1) where 1 refers to ROI, 0 refers to restricted area
    """
    if len(image.shape) == 3:
        roi = np.zeros_like(image[:, :, 0])
    elif len(image.shape) == 2:
        roi = np.zeros_like(image)

    if len(roi_bboxes) == 0:
        roi += 1
        return roi

    for bbox in roi_bboxes:
        x_min = bbox["x"]
        y_min = bbox["y"]
        width = bbox["width"]
        height = bbox["height"]
        roi[y_min : y_min + height, x_min : x_min + width] = np.ones((height, width))

    return roi


def apply_roi(image: np.ndarray, roi: np.ndarray) -> np.ndarray:
    """ """
    image_roi_applied = np.copy(image)
    restricted_area_indexes = np.where(roi == 0)
    image_roi_applied[restricted_area_indexes] = 255

    return image_roi_applied
