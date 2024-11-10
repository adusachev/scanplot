import ipywidgets


points_num_slider = ipywidgets.FloatSlider(
    value=20,
    min=0,
    max=100,
    step=0.1,
    description='Points Number:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d',
    layout=ipywidgets.Layout(width='500px'),
    style={'description_width': 'initial'}
)

points_density_slider = ipywidgets.FloatSlider(
    value=20,
    min=0,
    max=100,
    step=1,
    description='Points Density:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d',
    layout=ipywidgets.Layout(width='500px'),
    style={'description_width': 'initial'}
)
