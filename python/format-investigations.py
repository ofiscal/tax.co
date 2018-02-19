import pandas as pd

folder = "data/enig-2007/"

## The first file that generated a format warning during subsample.py
  # the warning:
  # now (henceforth) processing: Ig_ml_hogar.txt
  # sys:1: DtypeWarning: Columns (101) have mixed types.
  # Specify dtype option on import or set low_memory=False.
data = pd.read_csv(     folder + "recip-1/" + "Ig_ml_hogar.txt", sep='\t', encoding='latin_1')
bad_column = 101

# Detect that it should be a string:
data.ix[:,bad_column].unique() # eyeball the output; it's mostly strings, plus a Nan that should be ""

# Determine the name of the column that needs format specification:
list(data.columns.values)[bad_column] # eyeball the output: it's called P5185S9A1


## The second such file
  # the warning:
  # now (henceforth) processing: Ig_ml_pblcion_edad_trbjar.txt
  # sys:1: DtypeWarning: Columns (94) have mixed types.
  # Specify dtype option on import or set low_memory=False.
data = pd.read_csv(     folder + "recip-1/" + "Ig_ml_pblcion_edad_trbjar.txt", sep='\t', encoding='latin_1')
bad_column = 94

# Detect that it should be a string:
data.ix[:,bad_column].unique() # eyeball the output; again it's mostly strings, plus a Nan that should be ""

# Determine the name of the column that needs format specification:
list(data.columns.values)[bad_column] # eyeball the output: it's called P7580S1
