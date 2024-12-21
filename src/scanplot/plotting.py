import logging
from typing import Tuple

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch, Rectangle

logger = logging.getLogger(__name__)


def draw_image(image: np.ndarray, alpha: float = 1) -> None:
    plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB), alpha=alpha)
    plt.xticks([])
    plt.yticks([])


def draw_points_on_canvas(points: np.ndarray, image: np.ndarray) -> None:
    x = points[:, 0]
    y = points[:, 1]

    clear_canvas = image.copy()
    clear_canvas[:, :] = 255
    plt.scatter(x, y, alpha=0.5, s=20)
    plt.imshow(cv.cvtColor(clear_canvas, cv.COLOR_BGR2RGB))


def draw_points_on_image(
    points: np.ndarray,
    image: np.ndarray,
    fig_size: int = 10,
    marker_size: int = 60,
    marker_color: str = "yellow",
    marker_type: str = "*",
) -> None:
    plt.figure(figsize=(fig_size, fig_size))

    draw_image(image)

    x = points[:, 0]
    y = points[:, 1]
    points_number = len(points)
    plt.scatter(
        x,
        y,
        s=marker_size,
        c=marker_color,
        marker=marker_type,
        edgecolors="black",
        linewidths=0.2,
    )
    plt.xticks([])
    plt.yticks([])
    plt.title(f"Number of detections: {points_number}")


def draw_bbox(
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    bbox_center: Tuple[int, int] | None = None,
) -> None:
    """
    Draws a rectangle.
    If bbox_center specified, draws rectangle center point
    """
    height = y_max - y_min
    width = x_max - x_min
    rect = Rectangle((x_min, y_min), width, height, edgecolor="r", facecolor="none")
    ax = plt.gca()
    ax.add_patch(rect)

    if bbox_center:
        bbox_center_x, bbox_center_y = bbox_center
        plt.scatter([bbox_center_x], [bbox_center_y], marker="*")


def draw_axes_mapping_lines(
    y_pos: Tuple[int, int],
    x_pos: Tuple[int, int],
    source_image: np.ndarray,
    fig_size: int = 10,
    line_color: str = "red",
    key_points_marker_color: str = "green",
    key_points_marker: str = "x",
) -> None:
    """
    Draw single (static) position of calibration lines on source image

    :param y_pos: tuple with y-positions of horizontal lines
    :param x_pos: tuple with x-positions of vertical lines
    :param fig_size: matplotlib figure size
    :param line_color: color of horizontal and vertical lines
    :param key_points_marker_color: color of the marker at lines intersection point
    :param key_points_marker: type of the marker at lines intersection point
    """
    plt.figure(figsize=(fig_size, fig_size))

    # draw source image
    draw_image(source_image)

    # draw calibration lines
    h_image, w_image = source_image.shape[0], source_image.shape[1]
    y_pos = h_image - np.array(y_pos)
    plt.hlines(
        y=y_pos, xmin=0, xmax=w_image, linestyles="--", color=line_color, alpha=0.3
    )
    plt.vlines(
        x=x_pos, ymin=0, ymax=h_image, linestyles="--", color=line_color, alpha=0.3
    )

    # draw calibration points
    x_min, x_max = x_pos
    y_min, y_max = y_pos
    plt.scatter(
        [x_min, x_min, x_max],
        [y_min, y_max, y_min],
        marker=key_points_marker,
        color=key_points_marker_color,
    )
    plt.xticks([])
    plt.yticks([])


def draw_ROI(roi: np.ndarray) -> None:
    """
    Draws a region of intrest.
    Converts bitmap array with ROI to RGB image where green color refers to ROI.

    :param roi: 2D array with values (0, 1) where 1 refers to ROI, 0 refers to restricted area
    """
    allowed_area_indexes = np.where(roi == 1)
    restricted_area_indexes = np.where(roi == 0)

    roi_rgb = np.zeros((roi.shape[0], roi.shape[1], 3), dtype=np.uint8)
    roi_G_channel = roi_rgb[:, :, 1]
    roi_R_channel = roi_rgb[:, :, 2]

    roi_G_channel[allowed_area_indexes] = 120
    roi_R_channel[restricted_area_indexes] = 220

    draw_image(roi_rgb, alpha=0.3)
    colors = ["green", "red"]
    labels = ["Detections allowed", "Detections prohibited"]
    patches = [Patch(color=c, label=l, alpha=0.3) for c, l in zip(colors, labels)]
    plt.legend(handles=patches, loc="upper center", bbox_to_anchor=(0.5, 1.17))
