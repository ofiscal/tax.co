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
  hh = oio.readUserData(
    com.subsample,
    "households_1_agg_plus." + com.strategy_year_suffix )
  pur = oio.readUserData(
    com.subsample,
    "purchase_sums." + com.strategy_suffix )
  merge = pd.merge( hh, pur,
                    how = "left",
                    on=["household"] )

if True: # In San Andrés there is no VAT.
  merge.loc[ merge["region-1"] == "SAN ANDRÉS", "vat paid" ] = 0

if True: # create a few more variables
  merge["vat / purchase value" ] = (
    merge["vat paid"]        / merge["value, purchase" ] )
  merge["vat / income"] = (
    merge["vat paid"]        / merge["income"] )
  merge["purchase value / income" ] = (
    merge["value, purchase"] / merge["income"] )
  merge["tax"] = (
    # PITFALL: This must be computed separately for households and earners,
    # because income and ss taxes vary by earner.
    # (The VAT and other purchaselike taxes are, by contrast,
    # allocated within households based on each earner's income.)
    merge [ [ "tax, income",
              "tax, ss",
              "vat paid",
              "value, tax, purchaselike non-VAT" ] ]
    . sum ( axis = "columns" ) )

if True: # save
  oio.saveUserData(
      com.subsample,
      merge,
      "households_2_purchases." + com.strategy_year_suffix )
