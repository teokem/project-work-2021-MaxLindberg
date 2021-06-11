# Calculation of N14 A𝛽 concentration using N15 labeled A𝛽 and MALDI-MS
This was done as a part of the jupyter course at Lunds university spring 2021.
## Instructions
1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) or [anaconda](https://docs.anaconda.com/anaconda/install/index.html)
2. Clone this project to your computer (e.g. by downloading as zip and extracting or cloning via git)
3. Create and enter a new conda environment with the required python packages by navigating to the local copy (clone) of this repository in a terminal on your computer and type: 
```
conda env create -f environment.yml
conda activate max
```
4. Start a jupyter lab instance by typing (you could also use the older notebook approach by instead typing `jupyter notebook`): 
```
jupyter lab
```
5. Now you can open the Notebook.ipynb and run through the cells to process and plot my example data

6. (Optional) Exchange the "masslist.xlsx" with your own to analyze your own data. This is done by finding peaks in MS spectra in brukers flexAnalysis software and exporting them by the "Export masslist to excel" option.