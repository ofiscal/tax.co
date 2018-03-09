import pandas as pd

# Fields not formatted like English numbers don't get interpreted as numbers
numish = pd.read_csv("number-ish.csv")
print(numish)
print(numish.describe()) # it only describes numeric columns

# The exception is a field containing integers with only one period;
# these are indistinguishable from decimal values.
# One kind of test for that is this:
# (purchases["value"] - np.floor(purchases["value"]) ).describe()
# which indicates a problem if it's not all zeros.
# That could still give a false negative.
# Another test is to read the field as text, and search for terms
# ending in ".000". That indicates a problem.
# If both of those tests pass, I think it's probably okay.

# If any row has the wrong number of fields, Python throws an error.
# An extra comma would cause that to happen, if comma is the separator.
extra = pd.read_csv("extra-column-in-one-row.csv")
