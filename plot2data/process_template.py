from typing import Tuple
import numpy as np
import skimage.measure
import cv2 as cv



def template_tresholding(temaplte_rgb: np.ndarray, treshold: int = 200) -> np.ndarray:
    """
    Tresholding.
    Return template mask.
    """
    temaplte_gray = cv.cvtColor(temaplte_rgb, cv.COLOR_BGR2GRAY)
    mask = temaplte_gray.copy()
    mask[np.where(temaplte_gray >= treshold)] = 0
    mask[np.where(mask != 0)] = 255

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
    bbox_height = y_max - y_min
    bbox_width = x_max - x_min
    cropped_image = image[y_min:y_min+bbox_height+1, x_min:x_min+bbox_width+1]
    return cropped_image



def frame_image(image: np.ndarray, frame_width: int = 1) -> np.ndarray:
    """
    Add black frame of given pixel width around input image.
    Return framed image.
    """
    image_width = image.shape[1]
    image_height = image.shape[0]

    framed_img_width = image_width + int(frame_width * 2)
    framed_img_height = image_height + int(frame_width * 2)

    framed_img = np.zeros((framed_img_height, framed_img_width))
    framed_img[frame_width:-frame_width, frame_width:-frame_width] = image
    
    return framed_img


