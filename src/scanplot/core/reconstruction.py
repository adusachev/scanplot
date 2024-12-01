from typing import List, Tuple

import numpy as np


def insert_template_into_image(
    image: np.ndarray,
    template: np.ndarray,
    bbox: Tuple[int, int, int, int],
    template_mask: np.ndarray | None = None,
) -> np.ndarray:
    """
    Вставляет изображение template в изображение image на позицию bbox.
    Если у шаблона есть маска, пиксели маски игнорируются и не вставляются.
    """
    x_min, x_max, y_min, y_max = bbox

    # assert image_part.shape == bbox.shape  # TODO
    # assert channels  # TODO

    if template_mask is None:
        image[y_min : y_max + 1, x_min : x_max + 1] = template
        return image

    template_non_mask_indexes = np.where(template_mask != 0)  # TODO: передвать как аргумент    # fmt: skip
    x_indexes_template, y_indexes_template = template_non_mask_indexes
    x_indexes_image = x_indexes_template + x_min
    y_indexes_image = y_indexes_template + y_min

    image[y_indexes_image, x_indexes_image] = template[y_indexes_template, x_indexes_template]  # fmt: skip

    # for x, y in zip(x_indexes_template, y_indexes_template):
    # image[y + y_min, x + x_min] = template[y, x]
    return image


def add_template_layer(
    layers_image: np.ndarray,
    bbox: Tuple[int, int, int, int],
    binary_template_mask: np.ndarray,
) -> np.ndarray:
    """ """
    x_min, x_max, y_min, y_max = bbox

    # assert image_part.shape == bbox.shape  # TODO
    # assert channels  # TODO

    template_non_mask_indexes = np.where(binary_template_mask != 0)  # TODO: передвать как аргумент    # fmt: skip
    x_indexes_template, y_indexes_template = template_non_mask_indexes
    x_indexes_image = x_indexes_template + x_min
    y_indexes_image = y_indexes_template + y_min

    layers_image[y_indexes_image, x_indexes_image] += binary_template_mask[y_indexes_template, x_indexes_template]  # fmt: skip
    return layers_image


def add_template_layer_light(
    layers_image: np.ndarray,
    bbox: Tuple[int, int, int, int],
    binary_template_mask: np.ndarray,
) -> np.ndarray:
    """
    Does not accumulate template mask values
    """
    x_min, x_max, y_min, y_max = bbox

    # assert image_part.shape == bbox.shape  # TODO
    # assert channels  # TODO

    template_non_mask_indexes = np.where(
        binary_template_mask != 0
    )  # TODO: передвать как аргумент
    x_indexes_template, y_indexes_template = template_non_mask_indexes
    x_indexes_image = x_indexes_template + x_min
    y_indexes_image = y_indexes_template + y_min

    ## difference from add_template_layer here (= instead of +=)
    layers_image[y_indexes_image, x_indexes_image] = binary_template_mask[y_indexes_template, x_indexes_template]  # fmt: skip
    return layers_image
