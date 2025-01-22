import numpy as np

from .corr_map_operations import get_corr_map_maximums
from .nms import apply_nms

from scanplot.types import ImageLike, ArrayNxM, ArrayNx2

from .scanplot_api import Plot




class Detector:
    def __init__(
        self, 
        plot: Plot,
        marker: str,
        # template: ImageLike,
        # correlation_map: ArrayNxM,
    ):
        self.template = plot.markers[marker]
        self.correlation_map = plot.correlation_maps[marker]
        self.marker_label = marker

        self.points_num: float = 20
        self.points_density: float = 20

    @property
    def corr_map_treshold(self) -> float:
        return linear_parameter_transform(self.points_num, a=-0.01, b=1)
    
    @property
    def iou_treshold(self) -> float:
        return linear_parameter_transform(self.points_density, a=-0.01, b=1)
    
    @property
    def template_height(self) -> int:
        return self.template.shape[0]

    @property
    def template_width(self) -> int:
        return self.template.shape[1]
    
    def detect_points(self) -> ArrayNx2:
        ## get max points
        max_points, _ = get_corr_map_maximums(
            correlation_map=self.correlation_map, treshold=self.corr_map_treshold
        )

        ## NMS
        detected_points = apply_nms(
            points=max_points,
            correlation_map=self.correlation_map,
            iou_treshold=self.iou_treshold,
            bbox_width=self.template_width,
            bbox_height=self.template_height,
        )

        return detected_points



# def detect_points_on_correlation_map(
#     points_num: float,
#     points_density: float,
#     correlation_map: np.ndarray,
#     image: np.ndarray,
#     template: np.ndarray,
# ) -> np.ndarray | None:

#     ## transform parameters
#     corr_map_treshold = linear_parameter_transform(points_num, a=-0.01, b=1)
#     iou_treshold = linear_parameter_transform(points_density, a=-0.01, b=1)

#     ## get max points
#     max_points, _ = get_corr_map_maximums(
#         correlation_map=correlation_map, treshold=corr_map_treshold
#     )

#     ## NMS
#     template_height = template.shape[0]
#     template_width = template.shape[1]

#     detected_points = apply_nms(
#         points=max_points,
#         correlation_map=correlation_map,
#         iou_treshold=iou_treshold,
#         bbox_width=template_width,
#         bbox_height=template_height,
#     )

#     return detected_points


def linear_parameter_transform(
    parameter: float, a: float = -0.01, b: float = 1, round_decimals: int | None = None
) -> float:
    """
    Linear transform y = a * x + b
    """
    parameter_transformed = a * parameter + b
    if round_decimals:
        parameter_transformed = np.round(parameter_transformed, decimals=round_decimals)

    return parameter_transformed
