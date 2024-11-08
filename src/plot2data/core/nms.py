import numpy as np
from typing import Tuple, List
from lsnms import nms

from .template_match import get_bbox_from_point, get_bbox_center

def simplify_points_NMS(
        points: np.ndarray, 
        w_template: int,
        h_template: int,
        convolution_map: np.ndarray,
        treshold: float
) -> Tuple[np.ndarray, np.ndarray]:
    bboxes, scores = get_bbox_from_point(points, w_template, h_template, convolution_map)
    keep = nms(bboxes, scores, iou_threshold=treshold)
    bboxes_nms = bboxes[keep]
    x_center, y_center = get_bbox_center(bboxes_nms)
    return x_center, y_center

