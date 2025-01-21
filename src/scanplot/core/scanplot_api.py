import numpy as np

from scanplot.io import load_image
from scanplot.plotting import draw_image
from scanplot.types import ImageLike, PathLike

from .preprocess import _apply_roi, bboxes_to_roi
from .process_template import extract_markers_from_image


def _restructure_bboxes(bboxes: list[dict]) -> dict[str, list]:
    """
    :param bboxes: list of bboxes, bbox = {'x': 424, 'y': 494, 'width': 52, 'height': 69, 'label': 'marker1'}
    :return: ...
    """
    bboxes_by_label = dict()

    for bbox in bboxes:
        bbox_label = bbox["label"]
        del bbox["label"]
        if bbox_label not in bboxes_by_label:
            bboxes_by_label[bbox_label] = [bbox]
        else:
            bboxes_by_label[bbox_label].append(bbox)
    return bboxes_by_label


class Plot:
    def __init__(self, filepath: PathLike):
        self.filepath = filepath
        self.data: ImageLike = load_image(self.filepath)
        markers_number: int = 1

        markers: list[ImageLike] = []
        _plot_images_list_algorighm_input: list[ImageLike] = []

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

    def apply_roi(self, roi_bboxes: list[dict]) -> None:

        roi_bboxes_by_label = _restructure_bboxes(roi_bboxes)
        plot_images_with_roi_applied = []

        for label in roi_bboxes_by_label.keys():
            bboxes_list = roi_bboxes_by_label[label]
            roi_bitmap = bboxes_to_roi(image=self.data, roi_bboxes=bboxes_list)
            plot_image_roi_applied = _apply_roi(image=self.data, roi=roi_bitmap)
            plot_images_with_roi_applied.append(plot_image_roi_applied)

        self._plot_images_list_algorighm_input = plot_images_with_roi_applied

    def run_matching(self):
        for marker in self.markers:
            self._match_single_marker()

    def _match_single_marker(self):
        # template_mask_initial = get_template_mask(source_template_image)

        # template_image, template_mask = center_object_on_template_image(
        #     source_template_image, template_mask_initial
        # )

        # plot_image = replace_black_pixels(plot_image, value=10)
        # template_image = replace_black_pixels(template_image, value=10)

        # correlation_map, _ = template_match(
        #     plot_image, template_image, template_mask, norm_result=True
        # )

        # accumulator = generalized_hough_transform(
        #     plot_image, template_image, norm_result=True, crop_result=True
        # )

        # assert correlation_map.shape == accumulator.shape

        # correlation_map_with_hough = correlation_map + 0.6 * accumulator
        # correlation_map_with_hough = normalize_map(correlation_map_with_hough)
        pass

    def draw(self):
        draw_image(self.data)
