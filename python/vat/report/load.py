# PITFALL: If a subsample is used, some of these statistics will be NaN or Inf when they otherwise would not

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

import python.util as util
import python.datafiles as datafiles
import python.vat.files as vatfiles
import python.vat.output_io as oio
import python.draw.util as draw


if True: # input the data. copied from output_io.py.
  subsample = 1
  purchases = \
    oio.readStage( subsample, '/2.purchases,prices,taxes') # memory hog
  people = \
    oio.readStage( subsample, '/5.person-demog-expenditures')
  households = \
    oio.readStage( subsample, '/6.households')
  households_w_income = \
    oio.readStage( subsample, '/7.households_w_income')
  household_w_income_decile_summary = \
    oio.readStage( subsample, '/8.household_w_income_decile_summary')
  household_decile_summary = \
    oio.readStage( subsample, '/9.household_decile_summary')
