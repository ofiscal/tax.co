import pandas as pd

# Fields not formatted like English numbers don't get interpreted as numbers
numish = pd.read_csv("toy-data/number-ish.csv")
print(numish)
print(numish.describe()) # pd.describe() only describes numeric columns
# The exception is a field containing integers with only one period;
# these are indistinguishable from decimal values.
# One kind of test for that is this:
# (purchases["value"] - np.floor(purchases["value"]) ).describe()
# which indicates a problem if it's not all zeros.
# That could still give a false negative.
# Another test is to read the field as text, and search for terms
# ending in ".000". That indicates a problem.
# That test is performed in test-real-data.py

print("\nA missing column (i.e. one too few commas) throws no error; it just leads to a NaN value: \n")
missingCol = pd.read_csv("toy-data/too-few-columns-in-row-2.csv")

print("\nAn extra column (i.e. one too many commas) throws an error: \n")
extra = pd.read_csv("toy-data/extra-column-in-row-2.csv")
