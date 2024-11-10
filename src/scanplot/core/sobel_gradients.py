import numpy as np
import cv2 as cv
from typing import Tuple

import logging
logger = logging.getLogger("base_logger")


# horizontal -- G_x
SOBEL_H = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

# vertical -- G_y
SOBEL_V = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]])


def get_image_part(y: int, x: int, image: np.ndarray, w: int, h: int) -> np.ndarray:
    return image[y : y+h, x : x+w]



def sobel_from_stratch(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    h, w = image.shape[0], image.shape[1]

    conv_map_height = h - 3 + 1
    conv_map_width = w - 3 + 1
    custom_grad_x = np.zeros((conv_map_height, conv_map_width))
    custom_grad_y = np.zeros((conv_map_height, conv_map_width))

    for y in range(conv_map_height):
        for x in range(conv_map_width):
            image_part = get_image_part(y, x, image, 3, 3)
            image_part = image_part.astype(np.float64)
            custom_grad_x[y, x] = np.sum(image_part * SOBEL_H)
            custom_grad_y[y, x] = np.sum(image_part * SOBEL_V)
    
    return custom_grad_x, custom_grad_y


def sobel_opencv(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    grad_x = cv.Sobel(image, ddepth=cv.CV_64F, dx=1, dy=0, ksize=3, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(image, ddepth=cv.CV_64F, dx=0, dy=1, ksize=3, borderType=cv.BORDER_DEFAULT)
    return grad_x, grad_y 



def gradient_orientation(grad_x: np.ndarray, grad_y: np.ndarray) -> np.ndarray:
    return np.arctan2(grad_y, grad_x) * 180 / np.pi

