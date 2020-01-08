# MX5P-Temporal-Downscaling

# Requirements
The Scikit-Learn Python library (version 0.20.3) implementations of random forest and gradient boosting machine learning regressions are used for this script. Additional required libraries are: Statsmodels (version 0.10.1), Pandas (version 0.25.3), and Numpy (version 1.17.4). The script uses Python 3.7.

# Usage
This script uses machine learning regressions, random forest and gradient boosting, to temporally downscale a precipitation intensity factor used by CLIGEN, a stochastic weather generator for simulation of long-duration stationary climate records that can be integrated with soil erosion models. The script downscales the intensity factor from precipitation datasets with either 60, 180 or 1440-min resolution to estimate values that would be found from breakpoint precipitation data. This solves the problem of underestimation due to the assumption that intensity may be time-averaged for the stated resolutions, such that it is equivalent to accumulation divided by the interval duration (i.e. accumulation divided by resolution).

Definitions for the predictor variables used by the regressions are given in the table below, including the definition of the precipitation intensity factor. The precipitation factor is known as MX.5P (mean monthly maximum 30-minute precipitation intensity). A short example calculation of MX.5P is given in *Adjustment of CLIGEN Parameters to Generate Precipitation Change Scenarios in Southeastern Australia* by Bofu Yu (2005) in the Catena Journal, doi: 10.1016/j.catena.2005.03.004.

Determination of MX.5P requires that the maximum 30-min intensity of each precipitation event (I30) is known. The I30 time window corresponds to the window of maximum 30-min accumulation. 30-min accumulations are given by dividing the interval accumulation by the fraction that the resolution is coarser than 30-min. For example, to determine 30-min accumulation from hourly data, hourly accumulation is divided by two, whereas for daily data, accumulations are divided by 48. This gives the following equation:

I30=2 x *d*

where *d* is the maximum 30-min accumulation and I30 has units of mm/hr. Note that storm events are defined as being separated by periods of <6 hours of no accumulation, and maximum 30-min accumulations were found by moving a 30-min window by 1-min steps.

In order for downscaled MX.5P to be determined, the user must calculate MX.5P using the time-averaging approach at the resolution of their data (60, 180 or 1440-min) and all of the additional predictor variables given in the table below, which are a combination of statistics derived from daily accumulations and information from the spatial location of the station.

| Variable | Label | Unit | Values Per Station |
| ------ | ------ | ------ | ------ |
| Monthly mean maximum 30-min intensity | MX.5P | mm/hr | 12 |
| Modified Fournier index | Fournier Coeff | mm | 1 |
| Average daily rainfall for wet days in the month | MEAN P | mm | 12 |
| Standard deviation for daily rainfall for wet days in the month | S DEV P | mm | 12 |
| Skewness for daily rainfall for wet days in the month | SKEW P | - | 12 |
| Monthly transition probability of a wet day given a wet day | P(W/W) | - | 12 |
| Monthly transition probability of a wet day given a dry day | P(W/D) | - | 12 |
| Station elevation | Elev | m | 1 |
| Station latitude | Lat | deg. | 1 |
| Station coastal proximity | Coastal Prox | km | 1 |
| Calendar month (categorical variable) | Month | - | 12 |

The definition of the Modified Fournier index is given in Renard and Freimund (1994) *Using Monthly Precipitation Data to Estimate the R-factor in the Revised USLE* in the Journal of Hydrology.

The predictor variables should be put into a comma separated *.csv file with the same formatting as the placeholder files (e.g. MX5P_X_60min_Placeholder.csv). The placeholder files allow the code to be run successfully but should be replaced with the user’s own file. The XY files (e.g. MX5P_XY_60min.csv) contain both the predicted and predictor variables and are used for fitting the models prior to making predictions of downscaled MX.5P based on the user’s predictor variables. 

The script produces a text file in the working directory with the downscaled MX.5P values listed in the order corresponding to the order of values in the file supplied by the user. Some user input is required to specify: the working directory, file paths, the resolution of the precipitation data, and the desired machine learning model. This requires the user to manually edit the script.

The gradient boosting models yield less error. Values of RMSE for the 60, 180 and 1440-min were 2.24, 2.74 and 3.76 mm/hr, respectively. For random forest, the values were 2.81, 3.39 and 4.67, respectively.

