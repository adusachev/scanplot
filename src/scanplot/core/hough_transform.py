import logging
from collections import defaultdict
from typing import List, Tuple

import cv2 as cv
import numpy as np
from scipy.ndimage import sobel

from .corr_map_operations import normalize_map
from .process_template import crop_image

logger = logging.getLogger("base_logger")


def generalized_hough_transform(
    image: np.ndarray,
    template: np.ndarray,
    norm_result: bool = True,
    crop_result: bool = True,
) -> np.ndarray:
    hough_model = build_hough_model(template)
    accumulator = fill_accumulator(hough_model, image)

    if norm_result:
        accumulator = normalize_map(accumulator)

    if crop_result:
        template_heihgt, template_width = template.shape[0], template.shape[1]
        accumulator = crop_accumulator(accumulator, template_width, template_heihgt)

    return accumulator


def crop_accumulator(
    accumulator: np.ndarray, template_width: int, template_heihgt: int
) -> np.ndarray:
    x_min = template_width // 2
    y_min = template_heihgt // 2
    if template_width % 2 == 0:
        x_max = accumulator.shape[1] - template_width // 2
    else:
        x_max = accumulator.shape[1] - template_width // 2 - 1

    if template_heihgt % 2 == 0:
        y_max = accumulator.shape[0] - template_heihgt // 2
    else:
        y_max = accumulator.shape[0] - template_heihgt // 2 - 1

    accumulator_cropped = crop_image(accumulator, bbox=(x_min, x_max, y_min, y_max))
    return accumulator_cropped


def calc_gradients_v0(image: np.ndarray) -> np.ndarray:
    """
    Calculate the gradient orientation for edge point in the image

    :param image: binary image of edges (in this work, generally may be any image)
    :return: calculated gradients (image with same shape as input)
    """
    dx = sobel(image, axis=0, mode="constant")
    dy = sobel(image, axis=1, mode="constant")
    gradient = np.arctan2(dy, dx) * 180 / np.pi

    return gradient


def calc_gradients(image: np.ndarray) -> np.ndarray:
    """
    Calculate the gradient orientation for edge point in the image

    :param image: binary image of edges (in this work, generally may be any image)
    :return: calculated gradients (image with same shape as input)
    """
    grad_x = cv.Sobel(
        image, ddepth=cv.CV_64F, dx=1, dy=0, ksize=3, borderType=cv.BORDER_DEFAULT
    )
    grad_y = cv.Sobel(
        image, ddepth=cv.CV_64F, dx=0, dy=1, ksize=3, borderType=cv.BORDER_DEFAULT
    )
    gradient = np.arctan2(grad_y, grad_x) * 180 / np.pi

    return gradient


def build_hough_model(
    template_image: np.ndarray,
    min_canny_treshold: int = 10,
    max_canny_treshold: int = 50,
    reference_point: Tuple[int, int] = None,
) -> defaultdict:
    """
    Build the Hough model (R-table) from the given shape image and a reference point

    :param template_image: source template image
    :param min_canny_treshold: threshold1 in cv.Canny
    :param max_canny_treshold: threshold2 in cv.Canny
    :param origin: reference point (by default center of a template)
    :return: Hough model of the template
    """
    # get reference_point if it is not specified
    if reference_point is None:
        reference_point = (template_image.shape[0] // 2, template_image.shape[1] // 2)

    # calc template gradients
    edges = cv.Canny(
        template_image, threshold1=min_canny_treshold, threshold2=max_canny_treshold
    )
    gradient = calc_gradients(edges)

    # build Hough model
    hough_model = defaultdict(list)
    for (i, j), value in np.ndenumerate(edges):
        if value:
            hough_model[gradient[i, j]].append((reference_point[0] - i, reference_point[1] - j))  # fmt: skip

    return hough_model


def fill_accumulator(
    hough_model: defaultdict,
    source_image: np.ndarray,
    min_canny_treshold: int = 10,
    max_canny_treshold: int = 50,
) -> np.ndarray:
    """
    Perform a General Hough Transform with the given image and R-table (Hough model).

    :param r_table: Hough model of the template
    :param source_image: source image where we try to find template (polt image, can be RGB or single channel)
    :param min_canny_treshold: threshold1 in cv.Canny
    :param max_canny_treshold: threshold2 in cv.Canny
    :return: accumulator (array with same shape as input gray_image)
    """
    # convert to single channel if required
    try:
        source_image_gray = cv.cvtColor(source_image, cv.COLOR_BGR2GRAY)
    except Exception as ex:
        source_image_gray = source_image

    # calc image gradients
    edges = cv.Canny(
        source_image_gray, threshold1=min_canny_treshold, threshold2=max_canny_treshold
    )
    gradient = calc_gradients(edges)

    # create and fill accumulator array
    accumulator = np.zeros(source_image_gray.shape)
    for (i, j), value in np.ndenumerate(edges):
        if value:
            for r in hough_model[gradient[i, j]]:
                accum_i, accum_j = i + r[0], j + r[1]
                if accum_i < accumulator.shape[0] and accum_j < accumulator.shape[1]:
                    accumulator[accum_i, accum_j] += 1

    return accumulator
