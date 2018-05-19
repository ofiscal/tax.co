# PITFALL: If a subsample is used, some of these statistics will be NaN or Inf when they otherwise would not

import numpy as np
import pandas as pd
import os

import python.util as util
import python.datafiles as datafiles
import python.vat.files as vatfiles
import python.vat.output_io as oio


if True: # input the data. copied from output_io.py.
  subsample = 1
  purchases = oio.readStage( subsample, '/2.purchases,prices,taxes') # memory hog
  people = oio.readStage( subsample, '/5.person-demog-expenditures')
  households = oio.readStage( subsample, '/6.households')


# Overview of the three data sets
util.compareDescriptives( {'purchases' : purchases} )

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    util.describeWithMissing(people)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    util.describeWithMissing(households)


# Education quantiles
  # see "qcut" below for a better way to do this kind of thing
for i in range(20):                                 
  pd.DataFrame( people["education"] ).quantile(i/20)


# Household spending and taxes
util.describeWithMissing( households [["value/inc"]] )
util.describeWithMissing( households [["vat/inc"]] )
util.describeWithMissing(
  households [ households["value/inc"] !=  np.inf ] [["value/inc"]]
)

households["has-child"] = households["age-min"] < 18
util.dwmParamByGroup("vat/inc", "has-child",households).round(3)
util.dwmParamByGroup("vat/inc", "has-child",
                     households [ households["vat/inc"] < np.inf ] ).round(3)
util.dwmParamByGroup("vat/inc", "has-child",
                     households [ households["income"] > 0 ] ).round(3)

util.dwmParamByGroup("vat/inc", "has-student", households)
util.dwmParamByGroup("vat/inc", "has-child",
                     households [ households["income"] > 0 ] ).round(3)

households["has-elderly"] = households["age-max"] > 65
util.dwmParamByGroup("vat/inc","has-elderly",households)
util.dwmParamByGroup("vat/inc", "has-elderly",
                     households [ households["income"] > 0 ] ).round(3)

util.dwmParamByGroup("vat/inc","edu-max",households)
util.dwmParamByGroup("vat/inc","edu-max",
                     households [ households["income"] > 0 ] ).round(3)

# Individual spending and taxes
people["age-decile"] = pd.qcut(people["age"], 10, labels = False)
  # here's a way to show what that did
    # pd.crosstab(index = people["age"], columns = people["age-decile"])
util.dwmParamByGroup("vat/inc","age-decile",people)
util.dwmParamByGroup("vat/inc","age-decile",
                     people[ people["income"] > 0 ] )
util.dwmParamByGroup("value/inc","age-decile",
                     people[ people["income"] > 0 ] )

pd.qcut(people["income"], 10)
people["inc-decile"] = pd.qcut(people["income"], 10, labels = False)
util.dwmParamByGroup("vat/inc","inc-decile",people)
util.dwmParamByGroup("vat/inc","inc-decile",
                     people[ people["vat/inc"] < np.inf ] )

util.dwmParamByGroup("vat/inc","race",
                     people[ people["income"] > 0 ] )

util.dwmParamByGroup("vat/inc","female",
                     people[ people["income"] > 0 ] )
