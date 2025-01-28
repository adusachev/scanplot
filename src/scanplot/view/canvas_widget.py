from pathlib import Path
from io import BytesIO
import base64
from PIL import Image

import anywidget
import traitlets
import numpy as np

import matplotlib.cm as cm

import cv2 as cv


class CanvasWidget(anywidget.AnyWidget):
    # js code
    _esm = Path(__file__).parent / 'canvas_simple.js'

    # image
    _image_data = traitlets.Unicode().tag(sync=True)

    # figsize
    _figsize = traitlets.Float(1).tag(sync=True)

    # line_width
    _line_width = traitlets.Float(1).tag(sync=True)

    # line_color
    _line_color = traitlets.Unicode().tag(sync=True)

    # marker_size
    _line_width = traitlets.Float(1).tag(sync=True)

    # marker_color
    _marker_color = traitlets.Unicode().tag(sync=True)

    vline_left = traitlets.Float().tag(sync=True)
    vline_right = traitlets.Float().tag(sync=True)
    hline_lower = traitlets.Float().tag(sync=True)
    hline_upper = traitlets.Float().tag(sync=True)


    def set_image(self, image: np.ndarray) -> None:
        self._image_data = image_to_base64str(image)

        self._init_lines_positions(image)


    def _init_lines_positions(self, image: np.ndarray) -> None:
        image_height = image.shape[0]
        image_width = image.shape[1]
        gap_size_px = 50
        
        self.vline_left = image_width // 2 - gap_size_px
        self.vline_right = image_width // 2 + gap_size_px

        self.hline_lower = image_height // 2 + gap_size_px
        self.hline_upper = image_height // 2 - gap_size_px
        


    def apply_widget_settings(self, fig_size: float) -> None:
        self._figsize = fig_size


# def str2array(base64_str: str):
#     base64_str = base64_str.split(",")[1] if "," in base64_str else base64_str
#     image_bytes = base64.b64decode(base64_str)
#     return np.array(Image.open(BytesIO(image_bytes)))


# TODO: move to utils    
def image_to_base64str(image: np.ndarray) -> str:

    retval, buffer_img = cv.imencode('.png', image)
    image_base64 = base64.b64encode(buffer_img)

    image_base64_str = "data:image/png;base64," + image_base64.decode()

    return image_base64_str

