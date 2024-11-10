import numpy as np
import cv2 as cv
import numpy_indexed as npi


def get_image_part(y: int, x: int, image: np.ndarray, w: int, h: int):
    return image[y : y+h, x : x+w]

def sqdiff(image_part: np.ndarray, template: np.ndarray):
    sqdiff_sum = np.sum((image_part.astype(np.float64) - template.astype(np.float64))**2)
    return sqdiff_sum


def compute_mask_pixel_ratio(image_part: np.ndarray, template_mask: np.ndarray, image_mask_value: float):
    
    image_mask_indexes = np.where((image_part[:, :, 0] == image_mask_value) & (image_part[:, :, 1] == image_mask_value) & (image_part[:, :, 2] == image_mask_value))
    template_non_mask_indexes = np.where(template_mask != 0)

    x, y = image_mask_indexes
    image_part_mask_pixel_coords = np.stack((x, y)).T

    x1, y1 = template_non_mask_indexes
    template_non_mask_pixel_coords = np.stack((x1, y1)).T

    true_mask_pixel_coords = npi.intersection(
        image_part_mask_pixel_coords,
        template_non_mask_pixel_coords
    )

    mask_pixel_ratio = len(true_mask_pixel_coords) / len(template_non_mask_pixel_coords)
    
    return mask_pixel_ratio


def compute_mask_pixel_ratio_v2(
    image_mask_part_binary: np.ndarray,
    template_mask_binary: np.ndarray,
    template_non_mask_pixels_count: int
) -> float:
    """
    Return count of non mask pixels of 
    """
    return np.sum(image_mask_part_binary * template_mask_binary) / template_non_mask_pixels_count



def sqdiff_normed_modification(
    image_part: np.ndarray,
    template: np.ndarray, 
    template_mask_rgb: np.ndarray,
    image_mask_part_binary: np.ndarray,
    template_mask_binary: np.ndarray,
    template_non_mask_pixels_count: int,
    ratio_treshold: float = 0.5
) -> float:
    """
    SQDIFF_NORMED modification
    """
    mask_pixel_ratio = compute_mask_pixel_ratio_v2(
        image_mask_part_binary, 
        template_mask_binary,
        template_non_mask_pixels_count
    )
    if mask_pixel_ratio < ratio_treshold:
        return np.nan

    sqdiff = np.sum( ((template - image_part) * template_mask_rgb)**2 )
    norm1 = np.sum( (template * template_mask_rgb)**2 )
    norm2 = np.sum( (image_part * template_mask_rgb)**2 )

    sqdiff_normed = sqdiff / np.sqrt(norm1 * norm2)

    return sqdiff_normed


def sqdiff_normed(image_part: np.ndarray, template: np.ndarray, template_mask: np.ndarray) -> float:
    """
    OpenCV SQDIFF_NORMED implementation
    """
    # image_part = image_part.astype(np.float64)
    # template = template.astype(np.float64)
    # mask = mask.astype(np.float64)

    sqdiff = np.sum( ((template - image_part) * template_mask)**2 )
    norm1 = np.sum( (template * template_mask)**2 )
    norm2 = np.sum( (image_part * template_mask)**2 )

    sqdiff_normed = sqdiff / np.sqrt(norm1 * norm2)

    return sqdiff_normed


def cv_sqdiff_normed(image_part: np.ndarray, template: np.ndarray, mask: np.ndarray):

    sqdiff = cv.matchTemplate(image_part, template, cv.TM_SQDIFF_NORMED, mask=mask)
    return sqdiff
