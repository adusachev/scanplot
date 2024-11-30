import numpy as np

from .nms import apply_nms
from .parameters_search import get_corr_map_maximums, linear_parameter_transform


def detect_points_on_correlation_map(
    points_num: float,
    points_density: float,
    correlation_map: np.ndarray,
    image: np.ndarray,
    template: np.ndarray,
) -> np.ndarray | None:

    ## transform parameters
    corr_map_treshold = linear_parameter_transform(points_num, a=-0.01, b=1)
    iou_treshold = linear_parameter_transform(points_density, a=-0.01, b=1)

    ## get max points
    max_points, _ = get_corr_map_maximums(
        correlation_map=correlation_map, treshold=corr_map_treshold
    )

    ## NMS
    template_height = template.shape[0]
    template_width = template.shape[1]

    detected_points = apply_nms(
        points=max_points,
        correlation_map=correlation_map,
        iou_treshold=iou_treshold,
        bbox_width=template_width,
        bbox_height=template_height,
    )
    # x_nms = detected_points[:, 0]
    # y_nms = detected_points[:, 1]

    return detected_points
