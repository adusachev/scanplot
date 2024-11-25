import ipywidgets


def init_points_num_slider(start_value: int = 20):
    return ipywidgets.FloatSlider(
        value=start_value,
        min=0,
        max=100,
        step=0.1,
        description="Points Number:",
        disabled=False,
        continuous_update=True,
        orientation="horizontal",
        readout=True,
        readout_format="d",
        layout=ipywidgets.Layout(width="500px"),
        style={"description_width": "initial"},
    )


def init_points_density_slider(start_value: int = 20):
    return ipywidgets.FloatSlider(
        value=start_value,
        min=0,
        max=100,
        step=1,
        description="Points Density:",
        disabled=False,
        continuous_update=True,
        orientation="horizontal",
        readout=True,
        readout_format="d",
        layout=ipywidgets.Layout(width="500px"),
        style={"description_width": "initial"},
    )
