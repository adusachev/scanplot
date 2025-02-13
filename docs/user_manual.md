
# User documentation


## Contents


 - [Installation](#installation)
   - [Way 1: Running in Docker (recommended for quickstart)](#way-1:-running-in-docker-(recommended-for-quickstart))
   - [Way 2: Running locally](#way-2:-running-locally)
 - [Usage](#usage)
   - [Marker selection](#marker-selection)
   - [ROI selection](#roi-selection)
   - [Detector](#detector)
   - [Mapping coordinates](#mapping-coordinates)
 - [Notes](#notes)
   - [Images with black background](#images-with-black-background)



## Installation


At the moment, the algorithm does not have a graphical interface, it can be tested in Jupyter Notebook.


### Way 1: Running in Docker (recommended for quickstart)

**Step 1:** Clone repository
```sh
git clone https://github.com/adusachev/scanplot.git <REPO>
cd <REPO>
```

Add your data (plot images) to `<REPO>/datasets/`, so that images can be accessed from inside the Docker container.


**Step 2:** Start Docker container
```sh
docker compose up -d
```

This container runs a jupyter server with all application dependencies installed.
A local directory `<REPO>/datasets/` is mounted into a container.


**Step 3:** Go to http://localhost:8888 and run notebook `main.ipynb`

<br/><br/>

**Other commands**

Stop Docker container:
```sh
docker compose down
```

Rebuild Docker image and start container
```sh
docker compose up -d --build
```

Remove Docker image:
```sh
docker rmi scanplot-jupyter:latest
```

---

### Way 2: Running locally


**Step 0:** Make sure that you have a required python version (> 3.11, < 3.12):
```sh
python3 --version
```

If you don't have the required python version, you can install it using [pyenv](https://github.com/pyenv/pyenv).


**Step 1:** Clone repository
```sh
git clone https://github.com/adusachev/scanplot.git <REPO>
cd <REPO>
```

**Step 2:** Create virtual environment and install dependencies

with `pip`:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
with `poetry`:
```sh
poetry env use python3
poetry shell
poetry install
```

**Step 3:** Open Jupyter Notebook in created virtual environment

**Step 4:** Run notebook `<REPO>/examples/main.ipynb`


---

## Usage


### Marker selection

You need to interactively select the markers that you want to detect on the plot image.



![](./images/markers_selection.gif)



---


### ROI selection

For each choosen marker you can select its own region of interest (ROI) – the area of the image where detections are allowed.

This step is optional, but selecting ROI for each marker can significantly improve the final detection result.

Selecting ROI is also useful to avoid detections in the area of legend.



![](./images/roi_selection_merged.gif)

When a plot image has multiple markers, the ROI for each marker is selected on a separate tab:

![](./images/roi_selection_multiple_markers.gif)

---


### Detector


The detector operates in semi-automatic mode.
You need to vary the detector parameters and choose the best result.

![](./images/detector_interaction.gif)



The detector has **2 parameters**:
- Points Number
- Points Density


The impact of these parameters on the final result is shown below:

![](./images/parameter_search_1.png)

![](./images/parameter_search_2.png)


---

### Mapping coordinates

After applying the detector, you obtain the marker coordinates in **pixels**.

So the last step is to map pixel coordinates to factual chart coordinates.


![](./images/mapper_new_with_anywidget.gif)




---

## Notes


### Images with black background

Images with a black background must be inverted before running algorithm steps.


This can be done using the function `invert_image`:
```python
from scanplot.io import load_image
from scanplot.core import Plot, invert_image

image = load_image(plot_image_filepath)

image_inv = invert_image(image)
plot = Plot(image_inv)
```

Example:
![](./images/invert_image.png)


---
