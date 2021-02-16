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