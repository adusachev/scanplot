# ScanPlot

## About

This repository presents a methodology for determining the positions of points on raster images of scatter plots.


The proposed methodology is **semi-automatic** and needs user interaction on different algorithm stages.


Firstly, user select target marker. Then, in interactive mode, user varies the parameters of the algorithm and choose the best result.
As a result, user receives the coordinates of the points for the selected marker.


![](./docs/images/interaction.gif)



The proposed algorithm considers the digitization of the scatter plot as the task of detecting a pattern in the image.
The technique of marker detection on image is based on Template Matching algorithm, Generalized Hough Transform and Non Maximum Suppression.




---

## Input data requirements


The algorithm supports both grayscale and RGB images.
Scatter plot may have several marker types of any shape and color.


Input data that is **not supported**:
- markers with gradient color
- markers with alpha channel
- markers of the same type but with different sizes


![](./docs/images/data_requirements.png)

---

## Dependencies

scanplot requires:
- Python (> 3.11, < 3.12)


If you don't have the required python version, you can install it using [pyenv](https://github.com/pyenv/pyenv).


---

## Usage

At the moment, the algorithm does not have a graphical interface, it can be tested in Jupyter Notebook.

**Step 1:** Clone repo
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

More detailed information about usage can be found in the [user documentation](https://github.com/adusachev/scanplot/blob/master/docs/user_manual.md).

---

## Algorithm results examples (successful cases)


![](./docs/images/algorithm_results_examples_plot_84.png)
plot image source: [1]

<br/><br/>

![](./docs/images/algorithm_results_examples_plot_67.png)
plot image source: [2]

<br/><br/>

![](./docs/images/algorithm_results_examples_plot_22.png)
plot image source: [3]

<br/><br/>

![](./docs/images/algorithm_results_examples_plot_103.png)
plot image source: [4]

---

## Algorithm results examples (not successful cases)


![](./docs/images/algorithm_results_examples_plot_62.png)


<br/><br/>


![](./docs/images/algorithm_results_examples_plot_96.png)








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

- [x] Adding opportunity to select region of interest
- [ ] Adding opportunity to manually edit detected data points
- [ ] Improving the accuracy of the algorithm on b/w images
- [ ] Implementation of the graphical user interface for the algorithm


---

## References

Plot image sources:


**[1]** &emsp; Meister M, Schall E, Dziak R, Spiesecke S, Thomisch K (2024) A multi-year analysis of acoustic occurrence and habitat use of blue and fin whales in eastern and central Fram Strait. PLoS ONE19(11): e0314369.

**[2]** &emsp; Darcel, C., Davy, P., Le Goc, R., de Dreuzy, J. R., &   Bour, O. (2009). Statistical methodology for discrete fracture model-including fracture size, orientation uncertainty together with intensity uncertainty and variability. 


**[3]** &emsp; Bonnet, E., Bour, O., Odling, N. E., Davy, P., Main, I., Cowie, P., & Berkowitz, B. (2001). Scaling of fracture systems in geological media. Reviews of geophysics, 39(3), 347-383.

**[4]** &emsp; Kim J, Woo HK, Vimalajeewa D, Vidakovic B (2023) Analysis and classification of 1H-NMR spectra by multifractal analysis. PLoS ONE 18(6): e0286205.