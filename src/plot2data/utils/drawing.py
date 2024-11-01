import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cv2 as cv
import numpy as np

def draw_image(image: np.ndarray) -> None:
    plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))


def draw_points_on_canvas(points: np.ndarray, image: np.ndarray) -> None:
    x = points[:, 0]
    y = points[:, 1]
    
    clear_canvas = image.copy()
    clear_canvas[:, :] = 255
    plt.scatter(x, y, alpha=0.5, s=20)
    plt.imshow(cv.cvtColor(clear_canvas, cv.COLOR_BGR2RGB))


def draw_points_on_image(
        points: np.ndarray, image: np.ndarray, w: int, h: int,
        markersize=20, alpha=0.5, color="C0"
) -> None:
    x = np.copy(points[:, 0])
    y = np.copy(points[:, 1])
    x += w // 2 - 1
    y += h // 2 - 1
    plt.scatter(x, y, alpha=alpha, s=markersize, color=color)
    plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))


def draw_bbox(x_min, x_max, y_min, y_max, bbox_center=None) -> None:
    height = y_max - y_min
    width = x_max - x_min
    rect = Rectangle((x_min, y_min), width, height, edgecolor='r', facecolor='none')
    ax = plt.gca()
    ax.add_patch(rect)

    if bbox_center:
        bbox_center_x, bbox_center_y = bbox_center
        plt.scatter([bbox_center_x], [bbox_center_y], marker="*")
