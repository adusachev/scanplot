import os
import pathlib

import cv2 as cv
import numpy as np


def load_image(img_path: str | os.PathLike[str], grayscale: bool = False) -> np.ndarray:
    if grayscale:
        img = cv.imread(str(img_path), cv.IMREAD_GRAYSCALE)
    else:
        img = cv.imread(str(img_path))

    if img is None:
        raise FileNotFoundError(f"No such image: {str(img_path)}")
    return img
