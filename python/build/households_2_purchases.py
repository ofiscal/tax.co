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
  import python.common.common as com


if True: # merge purchase data into person data
  # PITFALL: The unit of observation in all these data sets is a household.
  hh = oio.readStage(
    com.subsample,
    "households_1_agg_plus." + com.strategy_year_suffix )
  pur = oio.readStage(
    com.subsample,
    "purchase_sums." + com.strategy_suffix )
  merge = pd.merge( hh, pur,
                    how = "left",
                    on=["household"] )

if True: # In San Andrés there is no VAT.
  for s in ["min", "max"]:
    merge.loc[ merge["region-1"] == "SAN ANDRÉS", "vat paid, " + s ] = 0

if True: # create a few more variables
  merge["vat/value, min" ] = merge["vat paid, min"] / merge["value" ]
  merge["vat/value, max" ] = merge["vat paid, max"] / merge["value" ]
  merge["vat/income, min"] = merge["vat paid, min"] / merge["income"]
  merge["vat/income, max"] = merge["vat paid, max"] / merge["income"]
  merge["value/income"   ] = merge["value"]         / merge["income"]

if True: # save
  oio.saveStage(
      com.subsample,
      merge,
      "households_2_purchases." + com.strategy_year_suffix )

