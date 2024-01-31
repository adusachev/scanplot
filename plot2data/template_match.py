import os
import pathlib
from typing import List, Tuple
import numpy as np
import cv2 as cv
from sklearn.cluster import AgglomerativeClustering
from dotenv import load_dotenv

from setup_logger import logger


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
DATA_PATH = pathlib.Path(os.getenv("DATA_PATH"))

PLOT_NUMBER = os.getenv("PLOT_NUMBER")
MARKER_NUMBER = os.getenv("MARKER_NUMBER")

PLOT_PATH = DATA_PATH / f"plot{PLOT_NUMBER}.png"
# TEMPLATE_PATH = DATA_PATH / f"plot{PLOT_NUMBER}_marker{MARKER_NUMBER}.png"
TEMPLATE_PATH = DATA_PATH / "markers_orig" / f"plot{PLOT_NUMBER}_marker{MARKER_NUMBER}.png"




def read_image_rgb(img_path: pathlib.Path) -> np.ndarray:
    img = cv.imread(str(img_path))
    return img

    
def read_image_gray(img_path: pathlib.Path) -> np.ndarray:
    img = cv.imread(str(img_path), cv.IMREAD_GRAYSCALE)
    return img



def invert_convolution_map(convolution_map: np.ndarray) -> np.ndarray:
    """
    Invert 2D array with float values
    """
    inverted_convolution_map = (- convolution_map) + np.max(convolution_map)
    return inverted_convolution_map


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

    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED, cv.TM_CCORR]:
        logger.debug(f"Convolution map bounds: {np.min(convolution_map), np.max(convolution_map)}")
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



def find_tolerance_limit(convolution_map: np.ndarray) -> float:
    tolerance_range = np.arange(0, 0.4, 0.01)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(convolution_map)

    for i, tolerance in enumerate(tolerance_range):
        points = detect_points(convolution_map, max_val, tolerance)
        points_number = len(points)
        if points_number > 1000:
            tolerance_limit = tolerance_range[i-1]
            return tolerance_limit
        
    return tolerance_range[-1]



def simplify_points(points: np.ndarray, eps: float = 5.5) -> np.ndarray:
    """
    Run Agglomerative Clustering.
    Return coordinates of cluster centers.
    """
    try:
        agglomerat = AgglomerativeClustering(n_clusters=None, distance_threshold=eps)
        labels_pred = agglomerat.fit_predict(points)
        unique_labels = np.unique(labels_pred)
        n = len(unique_labels)
        cluster_centers = np.zeros((n, 2))

        for i in range(len(unique_labels)):
            label = unique_labels[i]
            cluster_indexes = np.where(labels_pred == label)[0]
            cluster_points = points[cluster_indexes]
            cluster_centers[i] = np.mean(cluster_points, axis=0)
    except MemoryError as ex:
        logger.error(f"Number of points: {len(points)} too lot for clustering")
        raise Exception(f"Number of points: {len(points)} too lot for clustering")
    except ValueError:
        logger.warning(f"some message")
        cluster_centers = points
    
    return cluster_centers


