import logging
from typing import Tuple

import cv2 as cv
import numpy as np
import skimage.measure

from scanplot.types import ArrayNxM, ImageLike

logger = logging.getLogger(__name__)


def get_template_mask(template_image: ImageLike) -> Tuple[ArrayNxM, float]:
    """
    Perform tresholding.
    If object of interest is black, recalculate treshold value and repeat tresholding.
    """
    template_mask, treshold_value = image_tresholding(template_image)

    template_black_pixels_proportion = _get_black_pixels_proportion(
        template_image, template_mask, black_pixel_treshold=20
    )

    if template_black_pixels_proportion > 0.4:
        # recalculate treshold value for black objects on template image
        logger.debug(f"Object is black, treshold value reduced from {treshold_value:.2f} to {treshold_value / 2:.2f}")  # fmt: skip
        treshold_value = treshold_value / 2
        template_mask, _ = image_tresholding(template_image, treshold=treshold_value)

    return template_mask, treshold_value


def image_tresholding(
    image: ImageLike,
    treshold: int | None = None,
    mask_value: int = 0,
    object_value: int = 255,
) -> Tuple[ArrayNxM, int]:
    """
    Perform Tresholding.
    Use mean tresholding if treshold value is not specified.
    """
    if treshold is None:
        treshold = int(np.mean(image))
        logger.debug(f"Use Mean tresholding, treshold value = {treshold}")
    try:
        image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    except Exception as ex:
        image_gray = image
    mask = image_gray.copy()
    indexes_under_tresh = np.where(image_gray < treshold)
    indexes_over_tresh = np.where(image_gray >= treshold)
    mask[indexes_over_tresh] = mask_value
    mask[indexes_under_tresh] = object_value

    # assert np.all(np.unique(mask) == [0, 255]), "Image is not bitmap"
    return mask, treshold


def center_object_on_template_image(
    template_image: np.ndarray, template_mask: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Performs object centering on image.

    :param template_image: image, ArrayNxMx3 or ArrayNxM
    :param template_mask: bitmap image, ArrayNxM
    :return: centered_template_image, centered_template_mask
    """
    mask = _extract_largest_component(template_mask)

    template_object_bbox, _ = _get_segmented_object_bbox(mask)
    centered_template_image = crop_image(template_image, template_object_bbox)
    centered_template_mask = crop_image(template_mask, template_object_bbox)

    result_template_image = _frame_image(
        centered_template_image, frame_width=3, frame_color=255
    )
    result_template_mask = _frame_image(
        centered_template_mask, frame_width=3, frame_color=0
    )

    return result_template_image, result_template_mask


def crop_image(image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """
    Return cropped image

    :param bbox: (x_min, x_max, y_min, y_max)
    """
    x_min, x_max, y_min, y_max = bbox

    if _is_grayscale(image):
        cropped_image = image[y_min : y_max + 1, x_min : x_max + 1]
    else:
        cropped_image = image[y_min : y_max + 1, x_min : x_max + 1, :]

    return cropped_image


def _extract_largest_component(mask: np.ndarray) -> np.ndarray:
    """
    Remove all connected components from bitmap image except the largest connected component.
    Only 255 pixels are considered as components.

    :param mask: bitmap image, ArrayNxM
    """
    assert np.all(np.unique(mask) == np.array([0, 255])), "Mask image is not bitmap"

    # convert 3 channel input to 1 channel
    if len(mask.shape) == 3:
        mask = mask[:, :, 0]

    label_map = skimage.measure.label(mask, background=0, connectivity=1)
    largest_component_label = _get_largest_component_label(label_map)

    new_mask = np.copy(label_map)
    unnecessary_labels_indexes = np.where(label_map != largest_component_label)
    new_mask[unnecessary_labels_indexes] = 0
    new_mask[np.where(new_mask != 0)] = 255
    new_mask = new_mask.astype(np.uint8)

    return new_mask


def _get_largest_component_label(label_map: np.ndarray) -> int:
    """
    Return label with largest count.
    Background 0 label is not considered.
    """
    component_labels, component_sizes = np.unique(label_map, return_counts=True)
    # remove label 0 (background), because component_labels is sorted by np.unique
    component_labels = component_labels[1:]
    component_sizes = component_sizes[1:]

    max_component_index = np.argmax(component_sizes)
    max_component_label = component_labels[max_component_index]
    return max_component_label


def _get_segmented_object_bbox(
    mask: np.ndarray, seg_value: int = 255
) -> Tuple[Tuple[int, int, int, int], Tuple[int, int]]:
    """
    Find bbox around segmented object with given color/label.
    Return (x_min, x_max, y_min, y_max), (bbox_c_x, bbox_c_y)

    :param mask: bitmap image, ArrayNxM
    :return: bbox, bbox_center
    """
    segmentation = np.where(mask == seg_value)

    # Bounding Box
    x_min = int(np.min(segmentation[1]))
    x_max = int(np.max(segmentation[1]))
    y_min = int(np.min(segmentation[0]))
    y_max = int(np.max(segmentation[0]))
    bbox = x_min, x_max, y_min, y_max

    # Bounding Box center
    bbox_center_x = (x_max - x_min) // 2 + x_min
    bbox_center_y = (y_max - y_min) // 2 + y_min
    bbox_center = (bbox_center_x, bbox_center_y)

    return bbox, bbox_center


def _is_grayscale(img: np.ndarray) -> bool:
    return len(img.shape) == 2


def _frame_image(
    image: np.ndarray, frame_width: int = 1, frame_color: int = 0
) -> np.ndarray:
    """
    Add frame of given color and pixel width around input image.
    Return framed image.
    """
    image_width = image.shape[1]
    image_height = image.shape[0]

    framed_img_width = image_width + int(frame_width * 2)
    framed_img_height = image_height + int(frame_width * 2)

    if _is_grayscale(image):
        framed_img = np.zeros((framed_img_height, framed_img_width), dtype=np.uint8)
        framed_img += frame_color
        framed_img[frame_width:-frame_width, frame_width:-frame_width] = image
    else:
        framed_img = np.zeros((framed_img_height, framed_img_width, 3), dtype=np.uint8)
        framed_img += frame_color
        framed_img[frame_width:-frame_width, frame_width:-frame_width, :] = image

    return framed_img


def reconstruct_template_mask(mask: np.ndarray) -> np.ndarray:
    """
    Generation of new template mask, where only pixels from external connected component
      are assigned as mask pixels.

    :param mask: bitmap image of template mask
    :return: new_mask - bitmap image of new template mask
    """
    assert np.all(np.unique(mask) == np.array([0, 255])), "Mask image is not bitmap"
    if len(mask.shape) == 3:
        mask = mask[:, :, 0]  # convert 3 channel input to 1 channel

    BACKGROUND_COLOR = 1000  # конкретно здесь нужен любой цвет, которого точно нет на изображении    # fmt: skip
    label_map = skimage.measure.label(mask, background=BACKGROUND_COLOR, connectivity=1)

    # номер внешней связной компоненты равен номеру в левом верхнем углу
    external_connected_component_label = label_map[0, 0]
    if not np.all(label_map[0] == external_connected_component_label):
        logger.warning("Upper horizontal line is not a connected component")

    new_mask = np.zeros_like(mask, dtype=np.uint8) + 255
    external_connected_component_indexes = np.where(
        label_map == external_connected_component_label
    )
    new_mask[external_connected_component_indexes] = 0
    return new_mask


def get_binary_mask(mask: np.ndarray) -> np.ndarray:
    """
    Return binary template mask
    0 - background pixels, 1 - object pixels
    """
    mask_unique_values = np.unique(mask)

    if np.all(mask_unique_values == [0, 255]):
        mask_binary = mask / 255
    elif np.all(mask_unique_values == [0, 1]):
        mask_binary = mask
    else:
        raise Exception("Invalid mask values")
    return mask_binary


def extract_markers_from_image(
    plot_image: np.ndarray, marker_bboxes: list[dict]
) -> tuple[list[np.ndarray], list[str]]:
    """
    :param marker_bboxes: list of bboxes
      bbox = {'x': 424, 'y': 494, 'width': 52, 'height': 69, 'label': 'marker1'}
    """
    marker_images = []
    marker_labels = []
    for bbox in marker_bboxes:
        x_min = bbox["x"]
        x_max = bbox["x"] + bbox["width"]
        y_min = bbox["y"]
        y_max = bbox["y"] + bbox["height"]
        label = bbox["label"]

        marker_image = crop_image(plot_image, bbox=(x_min, x_max, y_min, y_max))
        marker_images.append(marker_image)
        marker_labels.append(label)
    return marker_images, marker_labels


def _get_black_pixels_proportion(
    template_image: ImageLike,
    template_mask: ArrayNxM,
    black_pixel_treshold: int = 20,
) -> float:
    """
    Сalculates the proportion of black pixels in an template image.
    Does not consider template mask pixels.

    :param black_pixel_treshold: the value below which pixels are considered black
    """
    if len(template_image.shape) == 3:
        template_grayscale = cv.cvtColor(template_image, cv.COLOR_BGR2GRAY)
    else:
        template_grayscale = template_image

    assert np.all(np.unique(template_mask) == [0, 255]), "Mask is not valid"
    marker_pixels_indexes = np.where(template_mask == 255)
    marker_pixels_list = np.ravel(template_grayscale[marker_pixels_indexes])

    black_pixels_list = np.where(marker_pixels_list < black_pixel_treshold)[0]

    black_pixels_proportion = len(black_pixels_list) / len(marker_pixels_list)
    logger.debug(f"Black pixels proportion on template image: {black_pixels_proportion}")  # fmt: skip

    return black_pixels_proportion
