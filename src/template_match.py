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

PLOT_NUMBER = 6
MARKER_NUMBER = 1

PLOT_PATH = DATA_PATH / f"plot{PLOT_NUMBER}.png"
TEMPLATE_PATH = DATA_PATH / f"plot{PLOT_NUMBER}_marker{MARKER_NUMBER}.png"





def process_template(marker_template: np.ndarray) -> np.ndarray:
    """
    Tresholding.
    Return template mask.
    """
    # TODO: implement
    pass



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
    method: str
) -> Tuple[np.ndarray, float]:
    """ 
    Run opencv templateMatch.
    Return convolution map and maximum value on map.
    """
    # TODO: implement
    # <...>
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
    tolerance_list = np.arange(0, 0.4, 0.01)
    for i, tolerance in enumerate(tolerance_list):
        points = detect_points(convolution_map, tolerance)
        points_number = len(points)
        if points_number > 1000:
            tolerance_limit = tolerance_list[i-1]
            return tolerance_limit
        
    return tolerance_list[-1]



def simplify_points(points: np.ndarray, eps: float) -> np.ndarray:
    """
    Run Agglomerative Clustering
    """
    # TODO: implement
    pass





