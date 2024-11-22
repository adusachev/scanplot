# ScanPlot

## About

This repository presents a methodology for determining the positions of points on raster images of scatter plots.


The proposed methodology is **semi-automatic** and needs user interation on different algorithm stages.


Firstly, user select target marker. Then, in interactive mode, user varies the parameters of the algorithm and choose the best result.
As a result, user receives the coordinates of the points for the selected marker.


![](./docs/images/interaction.gif)



The proposed algorithm considers the digitization of the scatter plot as the task of detecting a pattern in the image.
The technique of marker detection on image is based on Template Matching algorithm, Generalized Hough Transform and Non Maximum Suppression.




---

## Input data requirements


The algorithm supports only 3 channel RGB images.
Scatter plot may have several markers of any shape and color.


Input data that is **not supported**:
- markers with gradient color
- markers with alpha channel
- markers of the same type but with different sizes


![](./docs/images/data_requirements.png)

---

## Usage

At the moment, the algorithm does not have a graphical interface, it can be tested in Jupyter Notebook.

0) Clone repo:
```sh
git clone https://github.com/adusachev/scanplot.git
```

1) Create venv and install dependencies:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2) Open Jupyter Notebook in created virtual environment

3) Run notebook `<PATH_TO_REPO>/src/scanplot/main.ipynb`



---

## Algorithm results examples


![](./docs/images/algorithm_results_examples_1.png)

<br/><br/>

![](./docs/images/algorithm_results_examples_2.png)



---

## Comparsion with other plot digitization tools

 

Proposed algorithm was compared with existing tools for plot digitization:
- WebPlotDigitizer: https://automeris.io/
- DigitizeIt: https://www.digitizeit.xyz/
- PlotDigitizer: https://plotdigitizer.com/


![](./docs/images/comparsion_1.png)

<br/><br/>

![](./docs/images/comparsion_2.png)



---


## Future work

- [ ] **Implementation of the graphical user interface for the algorithm**
- [ ] Mapping the coordinates obtained by the algorithm to tick values on plot image
- [ ] Adding opportunity to select region of interest
- [ ] Improving the accuracy of the algorithm


