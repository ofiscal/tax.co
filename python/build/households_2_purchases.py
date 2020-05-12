# PURPOSE
#########
# Incorporate sums of purchases into households.
# Compute some more variables.

if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.util as util
  import python.build.output_io as oio
  import python.common.common as c


hh = oio.readStage(
  c.subsample,
  "households." + c.strategy_year_suffix )

pur = oio.readStage(
  c.subsample,
  "purchase_sums." + c.strategy_suffix )

if True: # merge purchase sums into people
  hh = pd.merge( hh, pur
                   , how = "left"
                   , on=["household"] )
  for s in ["min", "max"]:
    hh.loc[ hh["region-1"] == "SAN ANDRÉS", "vat paid, " + s ] = 0

if True: # create a few more variables
  hh["vat/value, min" ] = hh["vat paid, min"] / hh["value" ]
  hh["vat/value, max" ] = hh["vat paid, max"] / hh["value" ]
  hh["vat/income, min"] = hh["vat paid, min"] / hh["income"]
  hh["vat/income, max"] = hh["vat paid, max"] / hh["income"]
  hh["value/income"   ] = hh["value"]         / hh["income"]

if True: # save
  oio.saveStage( c.subsample, hh
               , "households_2_purchases." + c.strategy_year_suffix )

