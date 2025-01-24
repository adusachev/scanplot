import re

import logging

import numpy as np

from scanplot.io import load_image
from scanplot.plotting import draw_image, draw_ROI
from scanplot.types import ArrayNxM, ImageLike, PathLike

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
)
from .template_match import template_match


logger = logging.getLogger(__name__)

class Plot:
    def __init__(self, image: ImageLike):
        self.data: ImageLike = image
        
        self.markers_number: int = 1
        self.markers: dict[str, ImageLike] = dict()
        self._marker_masks: dict[str, ArrayNxM] = dict()
        
        self._roi: dict[str, ImageLike] = dict()
        self._images_algorithm_input: dict[str, ImageLike] = dict()

        self._correlation_maps: dict[str, ArrayNxM] = dict()


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
            # plot_image_roi_applied = _apply_roi(image=self.data, roi=roi_bitmap)

            res = re.search("marker\d+", roi_label)  # TODO: rework this in future
            marker_label = res.group(0)
            # self._images_algorithm_input[marker_label] = plot_image_roi_applied
            self._roi[marker_label] = roi_bitmap

        for marker_label, roi_bitmap in self._roi.items():
            plot_image_roi_applied = _apply_roi(image=self.data, roi=roi_bitmap)
            self._images_algorithm_input[marker_label] = plot_image_roi_applied


    def run_matching(self) -> dict[str, ArrayNxM]:
        if not self.markers:
            raise ValueError(f"You have not selected any markers")

        for marker_label, marker_image in self.markers.items():
            
            plot_image_to_process = self._images_algorithm_input[marker_label]
            
            plot_image_to_process = self._preprocess_plot_image(plot_image_to_process)
            template_image, template_mask = self._preprocess_template(marker_image)
            self.markers[marker_label] = template_image
            self._marker_masks[marker_label] = template_mask

            # pass plot image with applied ROI
            corr_map = self._match_single_marker(
                plot_image=plot_image_to_process,
                marker_template_image=template_image,
                marker_template_mask=template_mask,
            )
            self._correlation_maps[marker_label] = corr_map

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

        correlation_map_with_hough = correlation_map + 0.6 * accumulator
        correlation_map_with_hough = normalize_map(correlation_map_with_hough)
        return correlation_map_with_hough

    @staticmethod
    def _preprocess_template(template_image: ImageLike) -> tuple[ImageLike, ArrayNxM]:
        template_mask_initial = get_template_mask(template_image)

        template_image, template_mask = center_object_on_template_image(
            template_image, template_mask_initial
        )

        template_image = replace_black_pixels(template_image, value=10)

        return template_image, template_mask

    @staticmethod
    def _preprocess_plot_image(plot_image: ImageLike) -> ImageLike:
        plot_image = replace_black_pixels(plot_image, value=10)
        return plot_image
