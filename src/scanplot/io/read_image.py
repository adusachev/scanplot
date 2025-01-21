import cv2 as cv

from scanplot.types import ImageLike, PathLike


def load_image(img_path: PathLike, grayscale: bool = False) -> ImageLike:
    if grayscale:
        img = cv.imread(str(img_path), cv.IMREAD_GRAYSCALE)
    else:
        img = cv.imread(str(img_path))

    if img is None:
        raise FileNotFoundError(f"No such image: {str(img_path)}")
    return img
