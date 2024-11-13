import ipywidgets


def init_points_num_slider():
    return ipywidgets.FloatSlider(
        value=20,
        min=0,
        max=100,
        step=0.1,
        description='Points Number:',
        disabled=False,
        continuous_update=True,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        layout=ipywidgets.Layout(width='500px'),
        style={'description_width': 'initial'}
    )


def init_points_density_slider():
    return ipywidgets.FloatSlider(
        value=20,
        min=0,
        max=100,
        step=1,
        description='Points Density:',
        disabled=False,
        continuous_update=True,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        layout=ipywidgets.Layout(width='500px'),
        style={'description_width': 'initial'}
    )
