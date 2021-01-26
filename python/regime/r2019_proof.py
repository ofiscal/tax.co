# This program demonstrates that r2019 gives the same results
# with csv_dynamic set to True or False.
# Therefore it is safe to delete the non-dynamic section of the code.
#
# How to use this:
# First run the model with r2019.csv_dynamic set to True and False.
# For True, save a copy of households_1.csv as h_new.csv.
# For False, save a copy of households_1.csv as h_old.csv.
# Then run the below.
# The result is that the two data sets are equal --
# with the exception of income quantiles, but that's because those are
# generated stochastically.

if True:
  import pandas as pd
  import numpy as np


pd.options.display.min_rows = 100
pd.options.display.max_rows = 100

old = pd.read_csv( "output/vat/data/recip-10/h_old.csv" )
new = pd.read_csv( "output/vat/data/recip-10/h_new.csv" )

means = ((old == new) | (old.isnull() & new.isnull() )) .mean()
means[ means < 1 ]
