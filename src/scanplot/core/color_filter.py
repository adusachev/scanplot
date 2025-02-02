import logging
from typing import Tuple

import cv2 as cv
import numpy as np
import skimage

from scanplot.types import ArrayNx3, ArrayNxM, ImageLike

logger = logging.getLogger(__name__)


def k_means(image: ImageLike, n_clusters: int) -> ArrayNxM:
    img = np.copy(image)

    Z = img.reshape((-1, 3))
    Z = np.float32(Z)  # convert to np.float32

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    ret, label, center = cv.kmeans(
        Z, n_clusters, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS
    )

    if len(img.shape) == 3:
        label_map = label.reshape(img[:, :, 0].shape)
    elif len(img.shape) == 2:
        label_map = label.reshape(img.shape)
    else:
        raise ValueError(f"Irregular image shape: {img.shape}")

    return label_map


def average_image_colors(image: ImageLike, label_map: ArrayNxM) -> ImageLike:
    """
    Averages the colors of the image based on the given label map
    """
    image_mean_colors = skimage.color.label2rgb(
        label_map,
        image,
        kind="avg",
        bg_label=None,  # important to pass None explicitly!
    )
    return image_mean_colors


def unique_image_pixels(image: ImageLike) -> ArrayNx3:  # TODO:  | ArrayNx1  # fmt: skip
    """
    Return array of unique pixel colors on image
    """
    # TODO: test on 1-channel image
    unique_pixels = np.unique(image.reshape((-1, 3)), axis=0)
    return unique_pixels


def filtering_bounds(pixels: ArrayNx3, color_delta: int) -> tuple[ArrayNx3, ArrayNx3]:
    """
    For pixel (r, g, b) return two bounds:
     lower bound: (r - color_delta, g - color_delta, b - color_delta)
     upped bound: (r + color_delta, g + color_delta, b + color_delta)

    :pixels: array of pixels, e.g. [[255, 100, 56], [67, 57, 134]]
    """
    # TODO: support for 1-channel image
    if not 0 <= color_delta <= 255:
        raise ValueError(f"Param color_delta must be in range (0, 255)")

    pixels = pixels.astype(np.int64)  # (!)
    lower_bound_pixels = pixels - color_delta
    upper_bound_pixels = pixels + color_delta

    # prevent overflow in uint8 dtype
    lower_bound_pixels[np.where(lower_bound_pixels < 0)] = 0
    upper_bound_pixels[np.where(upper_bound_pixels > 255)] = 255

    lower_bound_pixels = lower_bound_pixels.astype(np.uint8)
    upper_bound_pixels = upper_bound_pixels.astype(np.uint8)
    pixels = pixels.astype(np.uint8)

    return lower_bound_pixels, upper_bound_pixels


def get_filtering_mask(
    image: ImageLike,
    lower_bound_pixels: ArrayNx3,
    upper_bound_pixels: ArrayNx3,
) -> ArrayNxM:
    """
    Finds the pixels of the image that lie within the given boundaries.

    :return: bitmap array
                1 - pixel lie in given bounds
                0 - pixel does NOT lie in given bounds
    """
    if len(image.shape) == 3:
        final_mask = np.zeros_like(image[:, :, 0], dtype=np.int64)
    elif len(image.shape) == 2:
        final_mask = np.zeros_like(image, dtype=np.int64)
    else:
        raise ValueError(f"Irregular image shape: {image.shape}")

    for lower_range, upper_range in zip(lower_bound_pixels, upper_bound_pixels):
        mask = cv.inRange(image, lower_range, upper_range)
        mask.astype(np.int64)
        final_mask += mask

    final_mask = (final_mask > 0).astype(np.uint8)

    return final_mask


def apply_image_mask(
    image: ImageLike,
    mask: ArrayNxM,
    color: int = 255,
) -> ImageLike:

    image_mask_applied = np.copy(image)

    if len(image.shape) == 3:
        image_mask_applied[np.where(mask == 0)] = [color, color, color]
    elif len(image.shape) == 2:
        image_mask_applied[np.where(mask == 0)] = color
    else:
        raise ValueError(f"Irregular image shape: {image.shape}")

    return image_mask_applied
