import ipywidgets


def init_y_range_slider(image_height: int = 0):
    return ipywidgets.IntRangeSlider(
        value=[0, image_height],
        min=0,
        max=image_height,
        step=2,
        description="Y_min, Y_max:",
        disabled=False,
        continuous_update=True,
        orientation="vertical",
        readout=True,
        readout_format="d",
        layout=ipywidgets.Layout(height="300px"),
        style={"description_width": "initial"},
    )


def init_x_range_slider(image_width: int = 0):
    return ipywidgets.IntRangeSlider(
        value=[0, image_width],
        min=0,
        max=image_width,
        step=2,
        description="X_min, X_max:",
        disabled=False,
        continuous_update=True,
        orientation="horizontal",
        readout=True,
        readout_format="d",
        layout=ipywidgets.Layout(width="500px"),
        style={"description_width": "initial"},
    )


def x_min_widget():
    return ipywidgets.FloatText(
        value=0,
        description="X_min:",
        step=0.01,
        disabled=False,
        layout=ipywidgets.Layout(width="150px"),
    )


def y_min_widget():
    return ipywidgets.FloatText(
        value=0,
        description="Y_min:",
        step=0.01,
        disabled=False,
        layout=ipywidgets.Layout(width="150px"),
    )


def x_max_widget():
    return ipywidgets.FloatText(
        value=0,
        description="X_max:",
        step=0.01,
        disabled=False,
        layout=ipywidgets.Layout(width="150px"),
    )


def y_max_widget():
    return ipywidgets.FloatText(
        value=0,
        description="Y_max:",
        step=0.01,
        disabled=False,
        layout=ipywidgets.Layout(width="150px"),
    )


def log_scale_checkbox_x_axis():
    return ipywidgets.Checkbox(
        value=False, description="X axis is log-scale", disabled=False, indent=True
    )


def log_scale_checkbox_y_axis():
    return ipywidgets.Checkbox(
        value=False, description="Y axis is log-scale", disabled=False, indent=True
    )
