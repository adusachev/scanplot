import numpy as np


def get_bbox_by_center_point(center_point, width, height):
    x_c, y_c = center_point
    x_min = x_c - width // 2
    y_min = y_c - height // 2
    x_max = x_c + width // 2
    y_max = y_c + height // 2
    bbox = x_min, x_max, y_min, y_max
    return bbox


def insert_template_into_image(image, template, bbox, template_mask=None):
    """
    Вставляет изображение template в изображение image на позицию bbox.
    Если у шаблона есть маска, пиксели маски игнорируются и не вставляются.
    """
    x_min, x_max, y_min, y_max = bbox
    
    # assert image_part.shape == bbox.shape  # TODO
    # assert channels  # TODO
    
    if template_mask is None:
        image[y_min:y_max+1, x_min:x_max+1] = template
        return image
    
    template_non_mask_indexes = np.where(template_mask != 0)  # TODO: передвать как аргумент
    x_indexes_template, y_indexes_template = template_non_mask_indexes
    x_indexes_image = x_indexes_template + x_min
    y_indexes_image = y_indexes_template + y_min
    
    image[y_indexes_image, x_indexes_image] = template[y_indexes_template, x_indexes_template]

    # for x, y in zip(x_indexes_template, y_indexes_template):
        # image[y + y_min, x + x_min] = template[y, x]
    return image
