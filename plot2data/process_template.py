from typing import Tuple
import numpy as np
import skimage.measure
import cv2 as cv
from setup_logger import logger



def template_tresholding(template: np.ndarray, treshold: int = 230) -> np.ndarray:
    """
    Tresholding.
    Return template mask.
    """
    try:
        temaplte_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    except Exception as ex:
        temaplte_gray = template
    mask = temaplte_gray.copy()
    indexes_under_tresh = np.where(temaplte_gray < treshold)
    indexes_over_tresh = np.where(temaplte_gray >= treshold)
    mask[indexes_over_tresh] = 0
    mask[indexes_under_tresh] = 255

    assert np.all(np.unique(mask) == [0, 255]), "Image is not bitmap"
    return mask




def extract_largest_component(mask: np.ndarray) -> np.ndarray:
    """
    Remove all connected components from bitmap image except the largest connected component. 
    Only 255 pixels are considered as components.
    """
    assert np.all(np.unique(mask) == np.array([0, 255])), "Mask image is not bitmap"
    
    # convert 3 channel input to 1 channel
    if len(mask.shape) == 3:
            mask = mask[:, :, 0]
    
    label_map = skimage.measure.label(mask, background=0, connectivity=1)
    largest_component_label = get_largest_component_label(label_map)
    
    new_mask = np.copy(label_map)
    unnecessary_labels_indexes = np.where( label_map != largest_component_label )
    new_mask[unnecessary_labels_indexes] = 0
    new_mask[ np.where(new_mask != 0) ] = 255
    new_mask = new_mask.astype(np.uint8)
    
    return new_mask




def get_largest_component_label(label_map: np.ndarray) -> int:
    """
    Return label with largest count.
    Background 0 label is not considered.
    """
    component_labels, component_sizes = np.unique(label_map, return_counts=True)
    # remove label 0 (background), because component_labels is sorted by np.unique
    component_labels = component_labels[1:]
    component_sizes = component_sizes[1:]
    
    max_component_index = np.argmax(component_sizes)
    max_component_label = component_labels[max_component_index]
    return max_component_label



def find_bbox(image: np.ndarray, seg_value: int = 255):
    """
    Find bbox around segmented object with given color/label.
    Return (x_min, x_max, y_min, y_max), (bbox_c_x, bbox_c_y)
    """
    segmentation = np.where(image == seg_value)

    # Bounding Box
    bbox = 0, 0, 0, 0
    x_min = int(np.min(segmentation[1]))
    x_max = int(np.max(segmentation[1]))
    y_min = int(np.min(segmentation[0]))
    y_max = int(np.max(segmentation[0]))
    bbox = x_min, x_max, y_min, y_max
    
    # Bounding Box center
    bbox_center_x = (x_max - x_min) // 2 + x_min
    bbox_center_y = (y_max - y_min) // 2 + y_min
    bbox_center = (bbox_center_x, bbox_center_y)
    
    return bbox, bbox_center



def crop_image(
    image: np.ndarray,
    bbox: Tuple[int, int, int, int]
) -> np.ndarray:
    x_min, x_max, y_min, y_max = bbox

    if is_grayscale(image):
        cropped_image = image[y_min:y_max+1, x_min:x_max+1]
    else:
        cropped_image = image[y_min:y_max+1, x_min:x_max+1, :]
    
    return cropped_image



def is_grayscale(img: np.ndarray) -> bool:
    return len(img.shape) == 2


def frame_image(image: np.ndarray, frame_width: int = 1) -> np.ndarray:
    """
    Add black frame of given pixel width around input image.
    Return framed image.
    """
    image_width = image.shape[1]
    image_height = image.shape[0]

    framed_img_width = image_width + int(frame_width * 2)
    framed_img_height = image_height + int(frame_width * 2)

    if is_grayscale(image):
        framed_img = np.zeros((framed_img_height, framed_img_width), dtype=np.uint8)
        framed_img[frame_width:-frame_width, frame_width:-frame_width] = image
    else:
        framed_img = np.zeros((framed_img_height, framed_img_width, 3), dtype=np.uint8)
        framed_img[frame_width:-frame_width, frame_width:-frame_width, :] = image

    return framed_img


