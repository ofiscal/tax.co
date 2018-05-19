import numpy as np
import pandas as pd

import python.util as util
import python.vat.draw.util as draw
import python.vat.output_io as oio

# %matplotlib inline
  # enable the previous line if calling from Jupyter
import matplotlib
matplotlib.use('Agg')
  # enable the previous line if calling from the (non-gui) shell
import matplotlib.pyplot as plt


if True:
  subsample = 1
  people = oio.readStage( subsample, '/5.person-demog-expenditures')
  households = oio.readStage( subsample, '/6.households')
