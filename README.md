## Automatic Single-cell Tracking and Analysis

This repository contains all the codes required for single-cell tracking and fluorescence signal analysis.

### Background
The raw image sequences with U2OS cells carrying the circadian reporter, REV-ERB-alpha (shown in red), and the cell cycle reporter, Geminin (shown in green), are analyzed. The aim is to quantify the intensities of the two reporters of individual cells and analyze the correlation between circadian parameters and cell cycle phases.

<img src="https://github.com/williams8645/MolMed-Lab-A/blob/main/xy041t010-t020.gif" width="400"/>


### Automatic Single-cell Tracking
This pipline enables automatic single-cell tracking with a large dataset without manually tracking and curation. Automatic single-cell tracking is achieved by ilastik batch mode. Before running the batch processing, we have to train the ilastik files of pixel classification, tracking with learning and object classification with several representative image sequences, as shown below. This workflow is modified by the instruction on the [ilastik](https://www.ilastik.org/documentation/tracking/tracking) website.

<img src="https://user-images.githubusercontent.com/69742955/129479569-ebf04711-8a30-491e-b861-154ee7846df7.png" width="500"/>

The brightness and the contrast of raw image sequences are adjusted by histogram equalization to better visualize cells before importing them into ilastik.
The tracking results and signal intensities are combined by the position of cells in R.


### Data Filtering and analysis
The inapplicable traces due to short lengths in terms of time, incorrect tracking and merging cells are then filtered out by a minimum length, size change of the cell nuclei over time and the rhythmicity of circadian clocks.

![image](https://user-images.githubusercontent.com/69742955/129583425-316507a5-99ba-453c-8402-67b67ebc2450.png)

The circadian parameters are determined by wavelet analysis with pyBOAT ([Mönke et al. 2020](https://www.biorxiv.org/content/10.1101/2020.04.29.067744v2)).

All the results of this project can be found [here](https://github.com/williams8645/MolMed-Lab-A/blob/main/final%20results%20not%20interpolated.pdf).

