import logging
import re
from typing import Literal

import numpy as np

from scanplot.plotting import draw_image, draw_ROI
from scanplot.types import ArrayNxM, ImageLike

from .color_filter import filter_by_colors, get_dominant_marker_colors
from .corr_map_operations import normalize_map
from .hough_transform import generalized_hough_transform
from .preprocess import (
    _apply_roi,
    _restructure_bboxes,
    bboxes_to_roi,
    replace_black_pixels,
)
from .process_template import (
    center_object_on_template_image,
    extract_markers_from_image,
    get_template_mask,
    image_tresholding,
)
from .template_match import template_match

logger = logging.getLogger(__name__)


class Plot:
    def __init__(self, image: ImageLike):
        self.data: ImageLike = image
        self.markers_number: int = 1
        self.markers: dict[str, ImageLike] = dict()

        self._marker_masks: dict[str, ArrayNxM] = dict()
        self._treshold_values: dict[str, float] = dict()
        self._roi: dict[str, ArrayNxM] = dict()
        self._images_roi_applied: dict[str, ImageLike] = dict()
        self._images_algorithm_input: dict[str, ImageLike] = dict()
        self._correlation_maps: dict[str, ArrayNxM] = dict()
        # self._correlation_maps_adjusted: dict[str, ArrayNxM] = dict()

    @property
    def n_channels(self) -> int:
        if len(self.data.shape) == 2:
            return 2
        elif len(self.data.shape) == 3 and self.data.shape[2] == 3:
            return 3

    def set_markers_number(self, n_markers: int) -> None:
        self.markers_number = n_markers

    def extract_markers(self, marker_bboxes: list[dict]) -> None:
        """
        :param marker_bboxes: list of bboxes
         bbox = {'x': 424, 'y': 494, 'width': 52, 'height': 69, 'label': 'marker1'}
        """
        marker_images, marker_labels = extract_markers_from_image(
            plot_image=self.data, marker_bboxes=marker_bboxes
        )
        self.markers = dict(zip(marker_labels, marker_images))
        if not self.markers:
            raise ValueError(f"You have not selected any markers")

        self._init_roi()

        logger.info(f"Marker templates successfully extracted from plot image")

    def apply_roi(self, roi_bboxes: list[dict]) -> None:

        roi_bboxes_by_label = _restructure_bboxes(roi_bboxes)

        for roi_label in roi_bboxes_by_label.keys():
            bboxes_list = roi_bboxes_by_label[roi_label]
            roi_bitmap = bboxes_to_roi(image=self.data, roi_bboxes=bboxes_list)

            res = re.search("marker\d+", roi_label)  # TODO: rework this in future
            marker_label = res.group(0)

            self._roi[marker_label] = roi_bitmap

        for marker_label, roi_bitmap in self._roi.items():
            plot_image_roi_applied = _apply_roi(image=self.data, roi=roi_bitmap)
            self._images_roi_applied[marker_label] = plot_image_roi_applied
            # self._images_algorithm_input[marker_label] = plot_image_roi_applied

        logger.info(f"ROI successfully applied")

    def run_matching(
        self,
        mode: Literal["basic", "color", "binary"] = "color",
        color_delta: int = 100,
        shape_factor: float = 0.6,
    ) -> dict[str, ArrayNxM]:
        """
        Computes correlation map for each marker.

        :param mode: string, one of {'basic', 'color', 'binary'}
            Matching operation mode.
             'basic' - basic matching (template matching and hough transform)
             'color' - perform image filtration by marker colors and then run basic matching
             'binary' - perform image and marker binarization and then run basic matching
                (useful for black and white images with dense areas of overlapping markers)
        :param color_delta: color sensitivity, used only in in mode='color'
        :param shape_factor: weight coefficient from 0 to inf, higher values give more preference to the shape of the marker than the color
        """
        if not self.markers:
            raise ValueError(f"You have not selected any markers")
        if mode not in {"basic", "color", "binary"}:
            raise ValueError("`mode` must be either 'basic' or 'color' or 'binary'")

        for marker_label, marker_image in self.markers.items():

            # plot_image_to_process = self._images_algorithm_input[marker_label]
            plot_image_to_process = self._images_roi_applied[marker_label]
            plot_image_to_process = self._preprocess_plot_image(plot_image_to_process)
            self._images_algorithm_input[marker_label] = plot_image_to_process

            template_image, template_mask, treshold_value = self._preprocess_template(marker_image)  # fmt: skip
            self.markers[marker_label] = template_image
            self._marker_masks[marker_label] = template_mask
            self._treshold_values[marker_label] = treshold_value

            if mode == "color":
                marker_dominant_colors = get_dominant_marker_colors(
                    self.markers[marker_label],
                    n_colors=3,
                )
                image_filtered = filter_by_colors(
                    image=self._images_algorithm_input[marker_label],
                    colors=marker_dominant_colors,
                    color_delta=color_delta,
                )
                self._images_algorithm_input[marker_label] = image_filtered

            if mode == "binary":
                template_image, _ = image_tresholding(
                    image=self.markers[marker_label],
                    treshold=self._treshold_values[marker_label],
                    mask_value=255,
                    object_value=10,
                )
                plot_image_binary, _ = image_tresholding(
                    image=self._images_algorithm_input[marker_label],
                    treshold=self._treshold_values[marker_label],
                    mask_value=255,
                    object_value=10,
                )
                self._images_algorithm_input[marker_label] = plot_image_binary

            # pass plot image with applied ROI
            corr_map = self._match_single_marker(
                plot_image=self._images_algorithm_input[marker_label],
                marker_template_image=template_image,
                marker_template_mask=template_mask,
                shape_factor=shape_factor,
            )
            self._correlation_maps[marker_label] = corr_map

        # postprocess correlation maps
        for marker_label, marker_image in self.markers.items():

            corr_map_adjusted = self._postprocess_correlation_map(
                correlation_map=self._correlation_maps[marker_label],
                marker_treshold_value=self._treshold_values[marker_label],
                plot_image_to_process=self._images_algorithm_input[marker_label],
                marker_mask=self._marker_masks[marker_label],
            )
            # self._correlation_maps_adjusted[marker_label] = corr_map_adjusted
            self._correlation_maps[marker_label] = corr_map_adjusted

        return self._correlation_maps

    def draw(self):
        draw_image(self.data)

    def draw_region_of_interest(self, marker: str) -> None:
        draw_image(self.data)
        draw_ROI(self._roi[marker])

    def _init_roi(self) -> None:

        if self.n_channels == 3:
            roi_array = np.zeros_like(self.data[:, :, 0]) + 1
        elif self.n_channels == 2:
            roi_array = np.zeros_like(self.data) + 1

        for marker_label in self.markers.keys():
            self._roi[marker_label] = np.copy(roi_array)
            self._images_algorithm_input[marker_label] = np.copy(self.data)

    @staticmethod
    def _match_single_marker(
        plot_image: ImageLike,
        marker_template_image: ImageLike,
        marker_template_mask: ArrayNxM,
        shape_factor: float,
    ) -> ArrayNxM:
        """
        Returns a correlation map
        """
        correlation_map, _ = template_match(
            plot_image, marker_template_image, marker_template_mask, norm_result=True
        )

        accumulator = generalized_hough_transform(
            plot_image, marker_template_image, norm_result=True, crop_result=True
        )

        assert correlation_map.shape == accumulator.shape

        correlation_map_with_hough = correlation_map + shape_factor * accumulator
        correlation_map_with_hough = normalize_map(correlation_map_with_hough)
        return correlation_map_with_hough

    @staticmethod
    def _preprocess_template(
        template_image: ImageLike,
    ) -> tuple[ImageLike, ArrayNxM, float]:
        template_mask_initial, treshold_value = get_template_mask(template_image)

        template_image, template_mask = center_object_on_template_image(
            template_image, template_mask_initial
        )

        template_image = replace_black_pixels(template_image, value=10)

        return template_image, template_mask, treshold_value

    @staticmethod
    def _preprocess_plot_image(plot_image: ImageLike) -> ImageLike:
        plot_image = replace_black_pixels(plot_image, value=10)
        return plot_image

    @staticmethod
    def _postprocess_correlation_map(
        correlation_map: ArrayNxM,
        marker_treshold_value: float | int,
        plot_image_to_process: ImageLike,
        marker_mask: ArrayNxM,
    ) -> ArrayNxM:
        """
        Step to prevent detections in the area of the white background of the image.
        Turns to zero corr map values on image background positions.

        Background area on image is computed using tresholding with the same treshold value
         that was used in template tresholding.

        :param correlation_map: initial corr map
        :param marker_treshold_value: treshold value from which template mask was calculated
        :param plot_image_to_process: plot image after preprocessing steps
        :param marker_mask: bitmap image with template mask
        """
        plot_image_mask, _ = image_tresholding(
            image=plot_image_to_process, treshold=marker_treshold_value
        )

        assert np.all(np.unique(marker_mask) == [0, 255]), "Marker Mask is not correct bitmap"  # fmt: skip
        assert np.all(np.unique(plot_image_mask) == [0, 255]), "Image Mask is not correct bitmap"  # fmt: skip

        marker_mask = marker_mask / 255
        plot_image_mask = plot_image_mask / 255
        marker_mask = marker_mask.astype(np.uint8)
        plot_image_mask = plot_image_mask.astype(np.uint8)

        masks_correlation_map, _ = template_match(
            image=plot_image_mask,
            template=marker_mask,
            method_name="cv.TM_CCORR",
            norm_result=False,
        )
        masks_correlation_map_bitmap = (masks_correlation_map > 0.1).astype(np.float64)

        correlation_map_adjusted = correlation_map * masks_correlation_map_bitmap
        return correlation_map_adjusted
