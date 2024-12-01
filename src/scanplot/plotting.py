import logging
from typing import Tuple

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

logger = logging.getLogger("base_logger")


def draw_image(image: np.ndarray) -> None:
    plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))


def draw_points_on_canvas(points: np.ndarray, image: np.ndarray) -> None:
    x = points[:, 0]
    y = points[:, 1]

    clear_canvas = image.copy()
    clear_canvas[:, :] = 255
    plt.scatter(x, y, alpha=0.5, s=20)
    plt.imshow(cv.cvtColor(clear_canvas, cv.COLOR_BGR2RGB))


# def draw_points_on_image(
#     points: np.ndarray,
#     image: np.ndarray,
#     w: int,
#     h: int,
#     markersize=20,
#     alpha=0.5,
#     color="C0",
# ) -> None:
#     x = np.copy(points[:, 0])
#     y = np.copy(points[:, 1])
#     x += w // 2 - 1
#     y += h // 2 - 1
#     plt.scatter(x, y, alpha=alpha, s=markersize, color=color)
#     plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))


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
    plt.title(f"Number of Points: {points_number}")


def draw_bbox(x_min, x_max, y_min, y_max, bbox_center=None) -> None:
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