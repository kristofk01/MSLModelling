# Modelling Mean Sea Level Data

Using the data obtained from the [Permanent Service for Mean Sea Level (PSMSL)](https://www.psmsl.org/), I investigated the trends regarding the mean sea level in Fremantle, WA. Although, it will work with any other station data provided by PSMSL. This program has proven quite effective at quick and simple analysis of sea level trends - concluding that it is steadily rising.

## Usage

If you'd like to play around with it yourself, here is how...

Firstly, download the ***monthly*** mean sea level data for any station from the PSMSL website [__here__](https://www.psmsl.org/data/obtaining/). Then, create a python script which contains something similar to the example below, and run!

```python
import MSLModelling as model

# Path to the PSMSL data file.
DATA_PATH = "111.rlrdata.txt"

clean_data = model.get_clean_data(DATA_PATH)

# This function uses linear regression to provide the user with an estimate for
# the sea level at a certain point in the future.
print(model.predicted_level(clean_data, 2050), "m")

# Segments the data n times to create a piecewise linear model of the sea level data.
print(model.piecewise_linear(clean_data, 50, quiet=True))

# This shows, if needed, a third model on the data by conjoining each segment
# making trends easier to identify.
model.piecewise_linear(clean_data, 50, conjoin=True, filename="piecewise")
```

Running the code above will produce the following output:

```
6.86 m

[[ 3.63758852e+01 -6.24344692e+04]
 [-9.48599142e+00  2.46395605e+04]
 [ 1.51212317e+01 -2.21582725e+04]...
```

![Image of piecewise model](piecewise.png "Plot returned by piecewise_linear()")