# PITFALL: If a subsample is used, some of these statistics will be NaN or Inf when they otherwise would not

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

import python.util as util
import python.datafiles as datafiles
import python.vat.files as vatfiles
import python.vat.output_io as oio
import python.draw.util as draw
import sys
import os


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.

if True: # input the data. copied from output_io.py.
  purchases = \
    oio.readStage( subsample, '/2.purchases,prices,taxes') # memory hog
  people = \
    oio.readStage( subsample, '/5.person-demog-expenditures')
  households = \
    oio.readStage( subsample, '/6.households')
  households_w_income = \
    oio.readStage( subsample, '/7.households_w_income')
  households_w_income_decile_summary = \
    oio.readStage( subsample, '/8.households_w_income_decile_summary')
  households_decile_summary = \
    oio.readStage( subsample, '/9.households_decile_summary')
