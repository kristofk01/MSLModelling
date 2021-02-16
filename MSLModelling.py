import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

(DATE, MSL, MISSING) = (0, 1, 2)

def get_clean_data(station):
    """
    Prepares and cleans the raw data - removes missing months and months with 6 or more missing days.

    Args:
        station (str):  Path to the raw data file.

    Returns:
        numpy.array (n x 2):    First and second column being months and mean sea levels
                                respectively.
    """
    all_station_data = np.loadtxt(station, delimiter=';', usecols=(DATE, MSL, MISSING))
    mask = (all_station_data[:,MSL] != -99999)
    station_data = all_station_data[mask]
    mask = (station_data[:,MISSING] < 6)
    station_data = station_data[mask]

    return station_data[:,:MISSING] # return DATE and MSL columns only

# predicting the sea level
def predicted_level(historical_data, datetime):
    """
    Used as a prediction for the mean sea level in meters for the specified datetime
    (representing a fraction of a year, e.g. 2030.5 would be 1st June 2030).
    
    Args:
        historical_data (numpy.array, float):   Input data as returned by get_clean_data.
        datetime        (float):                Fractional year.

    Returns:
        float:  Predicted mean sea level.
    """
    (slope, intercept) = linregress(historical_data)[:2]
    return round((slope*datetime + intercept)/1000, 2)

# piecewise linear model
def piecewise_linear(data, segments, conjoin=False, quiet=False, filename=""):
    """
    Takes an array returned by get_clean_data, given n number of segments, produces a 
    piecewise linear model.

    Args:
        data        (numpy.array, float):   Input data as returned by get_clean_data.
        segments    (int):                  The number of segments into which to split the data into.
        conjoin     (bool):                 Model which conjoins the median of each segment (default: False).
        quiet       (bool):                 Show/hide graphical output (default: False).
        filename    (str):                  When given, save the plot on disk (default: do not save).
    
    Returns:
        numpy.array (segments x 2): Parameters for the linear segments where the first and
                                    second columns contain the slopes and intercepts for
                                    each segment respectively.
    """
    piecewise = np.array_split(data, segments)

    piecewise_steps = np.zeros((segments, 2), float)
    for (index, section) in enumerate(piecewise):
        piecewise_steps[index] = linregress(section)[:2]
    
    if not quiet:
        # msl data
        plt.scatter(data[:,DATE], data[:,MSL], label="Sea Levels", alpha=0.5)

        # line of best fit
        (lr_slope, lr_intercept) = linregress(data)[:2]
        plt.plot(data[:,DATE], lr_slope * data[:,DATE] + lr_intercept,
                 label="Line of Best Fit", color="red", linewidth=4)
        
        # piecewise linear model
        for (index, (slope, intercept)) in enumerate(piecewise_steps):
            plt.plot(piecewise[index][:,DATE], slope * piecewise[index][:,DATE] + intercept,
                     color="black", linewidth=3)

        # conjoin segments
        if conjoin:
            median_date = []
            segment_msl = []
            for section in piecewise:
                median_date.append(np.median(section[:,DATE]))
                segment_msl.append(np.mean(section[:,MSL]))
            plt.plot(median_date, segment_msl, label="Median Piecewise Model", color="lime",
                    linewidth=3)

        plt.xlabel("Year")
        plt.ylabel("Mean Sea Level (mm)")
        plt.legend()
        if filename != "":
            plt.savefig(filename, bbox_inches="tight")
        plt.show()
    
    return piecewise_steps