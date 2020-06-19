
if True:
  import pandas as pd
  import numpy as np
  #
  import python.build.output_io as oio
  import python.common.common   as com

hh = oio.readStage(
    com.subsample,
    "households_2_purchases." + com.strategy_year_suffix )

if True:
  incomes = ["income", "income, cash"]
  values = [ "value, consumption",
             "value, non-purchase",
             "value, purchase",
             "value, spending" ]
           # "value, tax, predial",
           # "value, tax, purchaselike non-VAT",
           # "value, tax, purchaselike non-predial non-VAT"
  ivars = [ "IT",
            "ICGU",
            "ICMUG",
            "ICMDUG" ]
  gvars = [ "GTUG",
            "GCUG",
            "GCMUG" ]

hh[incomes + ivars] .describe() .transpose()
hh[values  + gvars] .describe() .transpose()

