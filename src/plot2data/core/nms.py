import numpy as np
from typing import Tuple, List
from lsnms import nms


def apply_nms(
        points: np.ndarray,
        correlation_map: np.ndarray,
        iou_treshold: float,
        bbox_width: int,
        bbox_height: int        
) -> np.ndarray:
    
    bboxes, scores = get_bbox_from_point(points, bbox_width, bbox_height, correlation_map)
    keep = nms(bboxes, scores, iou_threshold=iou_treshold)
    bboxes_nms = bboxes[keep]
    x_nms, y_nms = get_bbox_center(bboxes_nms)
    actual_points = np.stack((x_nms, y_nms)).T
    return actual_points



def point_to_bbox(y: int, x: int, w: int, h: int, correlation_map: np.ndarray) -> Tuple:
    """
    Map some point on convolution map to bbox on the source image.
    """
    x_min, y_min = x, y
    x_max = x + w - 1
    y_max = y + h - 1

    # # check that indexes are valid
    # correlation_map[y_min, x_min]
    # correlation_map[y_max, x_max]
    
    return x_min, y_min, x_max, y_max
    # return x_min - 0.5, y_min - 0.5, x_max + 0.5, y_max + 0.5  # for drawing



def get_bbox_from_point(
    points: np.ndarray,
    box_width: int,
    box_height: int,
    correlation_map: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    :param box_width, box_height: size of bounding box, same as template image size
    :param points: centers of bboxes, array with shape=(n, 2)
    :return: bboxes shape=(n, 4); scores shape=(n,)
    """
    n = len(points)
    scores = np.zeros(n)
    bboxes = np.zeros((n, 4))

    for i, point in enumerate(points):
        y, x = point[1], point[0]
        x_min, y_min, x_max, y_max = point_to_bbox(y, x, box_width, box_height, correlation_map)
        bboxes[i] = np.array([x_min, y_min, x_max, y_max])
        scores[i] = correlation_map[y, x]
    
    return bboxes, scores



def get_bbox_center(bboxes):
    """
    bbox = x_min, y_min, x_max, y_max
    """
    x_min = bboxes[:, 0]
    y_min = bboxes[:, 1]
    x_max = bboxes[:, 2]
    y_max = bboxes[:, 3]

    x_center = x_min + ((x_max - x_min) / 2)
    y_center = y_min + ((y_max - y_min) / 2)

    return x_center, y_center

