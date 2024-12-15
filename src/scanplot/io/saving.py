import logging
import pathlib

import cv2 as cv
import numpy as np

logger = logging.getLogger(__name__)


def dump_coords_csv(x: np.ndarray, y: np.ndarray, savepath: str) -> None:
    points = np.stack((x, y)).T
    np.savetxt(savepath, points, header="x, y")


def save_markers(
    marker_images: list[np.ndarray],
    save_directory: pathlib.Path | str,
    filename_prefix: str,
) -> None:
    save_directory = pathlib.Path(save_directory)

    for i, marker in enumerate(marker_images):
        marker_image_filename = filename_prefix + f"_marker{i+1}.png"
        savepath = save_directory / marker_image_filename
        cv.imwrite(
            filename=str(savepath),
            img=marker,
        )
        logger.debug(f"Marker saved to {str(savepath)}")
