import pathlib
import cv2 as cv
import numpy as np



def read_image_rgb(img_path: pathlib.Path) -> np.ndarray:
    img = cv.imread(str(img_path))
    return img

    
def read_image_gray(img_path: pathlib.Path) -> np.ndarray:
    img = cv.imread(str(img_path), cv.IMREAD_GRAYSCALE)
    return img
