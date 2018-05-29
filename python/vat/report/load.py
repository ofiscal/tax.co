# PITFALL: If a subsample is used, some of these statistics will be NaN or Inf when they otherwise would not

import numpy as np
import pandas as pd

import python.util as util
import python.datafiles as datafiles
import python.vat.files as vatfiles
import python.vat.output_io as oio
import python.draw.util as draw


if True: # input the data. copied from output_io.py.
  subsample = 1
  purchases = oio.readStage( subsample, '/2.purchases,prices,taxes') # memory hog
  people = oio.readStage( subsample, '/5.person-demog-expenditures')
  households = oio.readStage( subsample, '/6.households')


if True: # create some new variables
  households["has-child"] = households["age-min"] < 18
  households["has-elderly"] = households["age-max"] > 65

  # here's one way to show what the following decile-creating commands do
      # pd.crosstab(index = people["age"], columns = people["age-decile"])
  people["age-decile"] = pd.qcut(
    people["age"], 10, labels = False, duplicates='drop')
  people["income-decile"] = pd.qcut(
    people["income"], 10, labels = False, duplicates='drop')
  households["income-decile"] = pd.qcut(
    households["income"], 10, labels = False, duplicates='drop')
