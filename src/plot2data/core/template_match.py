import os
import pathlib
from typing import List, Tuple
import numpy as np
import cv2 as cv
# from sklearn.cluster import AgglomerativeClustering, MeanShift, DBSCAN
from dotenv import load_dotenv
import numpy_indexed as npi
from lsnms import nms

import logging
logger = logging.getLogger("base_logger")

from conv_map_operations import invert_convolution_map

# import sys
# import pathlib
# SRC_DIR = str(pathlib.Path(__name__).resolve().parent.parent.parent)
# sys.path.append(SRC_DIR)

# BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
# load_dotenv(BASE_DIR / '.env')
# DATA_PATH = pathlib.Path(os.getenv("DATA_PATH"))

# PLOT_NUMBER = os.getenv("PLOT_NUMBER")
# MARKER_NUMBER = os.getenv("MARKER_NUMBER")

# PLOT_PATH = DATA_PATH / f"plot{PLOT_NUMBER}.png"
# # TEMPLATE_PATH = DATA_PATH / f"plot{PLOT_NUMBER}_marker{MARKER_NUMBER}.png"
# TEMPLATE_PATH = DATA_PATH / "markers_orig" / f"plot{PLOT_NUMBER}_marker{MARKER_NUMBER}.png"




# def read_image_rgb(img_path: pathlib.Path) -> np.ndarray:
#     img = cv.imread(str(img_path))
#     return img

    
# def read_image_gray(img_path: pathlib.Path) -> np.ndarray:
#     img = cv.imread(str(img_path), cv.IMREAD_GRAYSCALE)
#     return img



# def invert_convolution_map(convolution_map: np.ndarray) -> np.ndarray:
#     """
#     Invert 2D array with float values
#     """   
#     inverted_convolution_map = (- convolution_map) + np.nanmax(convolution_map)
#     return inverted_convolution_map


def template_match(
    image: np.ndarray,
    template: np.ndarray,
    template_mask: np.ndarray,
    method_name: str
) -> Tuple[np.ndarray, float]:
    """ 
    Run opencv templateMatch.
    Return convolution map and maximum value on map.
    """
    method = eval(method_name)
    convolution_map = cv.matchTemplate(image, template, method, mask=template_mask)

    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        logger.debug(f"Convolution map bounds: {np.nanmin(convolution_map), np.nanmax(convolution_map)}")
        logger.debug("Convolution map was inverted")
        convolution_map = invert_convolution_map(convolution_map)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(convolution_map)
    return convolution_map, max_val



def detect_points(
    convolution_map: np.ndarray,
    max_value: float,
    tolerance: float
) -> np.ndarray:
    
    max_positions = np.where( np.isclose(convolution_map, max_value, atol=tolerance) )
    y, x = max_positions
    points = np.array([x, y]).T
    
    return points


def detect_points_v1(
    convolution_map: np.ndarray,
    max_value: float,
    tolerance: float,
    convolution_map_ccoef: np.ndarray
) -> np.ndarray:
    """
    Берет convolution_map_ccoef полученную из cv.TM_CCOEFF_NORMED, 
     и делает по ней дополнительную фильтрацию - смотрит, где convolution_map_ccoef не NaN
    """
    max_positions = np.where( np.isclose(convolution_map, max_value, atol=tolerance) )
    y, x = max_positions
    max_points = np.array([x, y]).T
    
    area_of_interest = np.where( np.isnan(convolution_map_ccoef) == False )
    y, x = area_of_interest
    area_of_interest_points = np.array([x, y]).T

    points = npi.intersection(max_points, area_of_interest_points)

    return points



def find_tolerance_limit_v1(
    convolution_map: np.ndarray, 
    convolution_map_ccoef: np.ndarray
) -> float:
    """
    Использует detect_points_v1
    """
    tolerance_range = np.arange(0, 2, 0.001)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(convolution_map)

    for i, tolerance in enumerate(tolerance_range):
        # points = detect_points(convolution_map, max_val, tolerance)
        points = detect_points_v1(convolution_map, max_val, tolerance, convolution_map_ccoef)
        points_number = len(points)
        if points_number > 1000:
            tolerance_limit = tolerance_range[i-1]
            return tolerance_limit
        
    return tolerance_range[-1]


def find_tolerance_limit(convolution_map: np.ndarray) -> float:
    tolerance_range = np.arange(0, 2, 0.001)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(convolution_map)

    for i, tolerance in enumerate(tolerance_range):
        points = detect_points(convolution_map, max_val, tolerance)
        points_number = len(points)
        if points_number > 1000:
            tolerance_limit = tolerance_range[i-1]
            return tolerance_limit
        
    return tolerance_range[-1]



# def agglomerative_clustering(points: np.ndarray, eps: float = 5.5) -> np.ndarray:
#     """
#     Run Agglomerative Clustering with distance treshold.
#     Return array of cluster labels.
#     """
#     if len(points) == 1:
#         labels_pred = np.zeros(1, dtype=np.int64)
#         return labels_pred

#     try:
#         agglomerat = AgglomerativeClustering(n_clusters=None, distance_threshold=eps)
#         labels_pred = agglomerat.fit_predict(points)
#     except MemoryError as ex:
#         logger.error(f"Number of points: {len(points)} too lot for clustering")
#         raise Exception(f"Number of points: {len(points)} too lot for clustering")
    
#     return labels_pred



# def meanshift_clustering(points: np.ndarray, bandwidth: float = 4) -> np.ndarray:
#     """
#     Run Mean-Shift clustering with a given bandwidth.
#     Return array of cluster labels.
#     """
#     mean_shift = MeanShift(bandwidth=bandwidth)
#     labels_pred = mean_shift.fit_predict(points)    
#     return labels_pred


# def dbscan_clustering(points: np.ndarray, eps: float, min_samples: int) -> np.ndarray:
#     """
#     Run DBSCAN clustering.
#     Return array of cluster labels.
#     """
#     dbscan = DBSCAN(eps=eps, min_samples=min_samples)
#     labels_pred = dbscan.fit_predict(points)
#     return labels_pred



# def simplify_points(points: np.ndarray, labels_pred: np.ndarray) -> np.ndarray:
#     """
#     Take clustering result (labeled data) and return array with cluster centers.
#     """
#     unique_labels = np.unique(labels_pred)
#     n = len(unique_labels)
#     cluster_centers = np.zeros((n, 2))

#     for i in range(len(unique_labels)):
#         label = unique_labels[i]
#         cluster_indexes = np.where(labels_pred == label)[0]
#         cluster_points = points[cluster_indexes]
#         cluster_centers[i] = np.mean(cluster_points, axis=0)
    
#     return cluster_centers


def point_to_bbox(y: int, x: int, w: int, h: int, convolution_map: np.ndarray) -> Tuple:
    """
    Map some point on convolution map to bbox on the source image.
    """
    x_min, y_min = x, y
    x_max = x + w - 1
    y_max = y + h - 1

    # # check that indexes are valid
    # convolution_map[y_min, x_min]
    # convolution_map[y_max, x_max]
    
    return x_min, y_min, x_max, y_max
    # return x_min - 0.5, y_min - 0.5, x_max + 0.5, y_max + 0.5  # for drawing





# def replace_black_pixels(image_rgb: np.ndarray, value: int = 10) -> np.ndarray:
#     """
#     Replace all [0, 0, 0] pixels on RGB image with [value, value, value] pixels
#     """
#     image = np.copy(image_rgb)
    
#     if len(image.shape) == 3:
#         zero_indexes = np.where((image[:, :, 0] == 0) & (image[:, :, 1] == 0) & (image[:, :, 2] == 0))
#         y, x = zero_indexes
#         image[y, x, :] = value
#     elif len(image.shape) == 2:
#         logger.warning("Image is 1-channel")
#         zero_indexes = np.where(image == 0)
#         y, x = zero_indexes
#         image[y, x] = value

#     logger.debug(f"Number of black pixels on image: {len(zero_indexes[0])}")
#     return image
    

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



# def simplify_points_NMS(
#     points: np.ndarray, 
#     w_template: int,
#     h_template: int,
#     convolution_map: np.ndarray,
#     treshold: float
# ) -> Tuple[np.ndarray, np.ndarray]:
#     bboxes, scores = get_bbox_from_point(points, w_template, h_template, convolution_map)
#     keep = nms(bboxes, scores, iou_threshold=treshold)
#     bboxes_nms = bboxes[keep]
#     x_center, y_center = get_bbox_center(bboxes_nms)
#     return x_center, y_center


