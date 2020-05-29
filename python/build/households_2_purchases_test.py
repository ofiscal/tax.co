if True:
  import pandas as pd
  import numpy as np
  #
  import python.common.util as util
  import python.build.output_io as oio
  import python.common.common as com


if True:
  hh_cols = oio.readStage(
      com.subsample,
      "households_1_agg_plus." + com.strategy_year_suffix,
      nrows = 1 )
  hh_rows = oio.readStage(
    com.subsample,
    "households_1_agg_plus." + com.strategy_year_suffix,
    usecols = ["household"] )
  pur = oio.readStage(
    com.subsample,
    "purchase_sums." + com.strategy_suffix )
  merge = oio.readStage(
    com.subsample,
    "households_2_purchases." + com.strategy_year_suffix )

if True: # See people_2_buildings_test for how to use these definitions.
  new_cols = [ "vat/value, min",
               "vat/value, max",
               "vat/income, min",
               "vat/income, max",
               "value/income" ]
  assert ( len( merge.columns ) ==
           len( hh_cols.columns ) +
           len( pur.columns ) - 1 + # omit the key that was merged on
           len( new_cols ) )
  assert len( merge ) == len( hh_rows )

if True:
    assert (merge["region-1"] == "SAN ANDRÉS").any()
    for s in ["min","max"]:
      assert ( merge[ merge["region-1"] == "SAN ANDRÉS" ]
                    ["vat paid, " + s].max() == 0 )

# The sum of the columns from the purchase-sum data should be the same
# in both the purchase-sum and the hh data sets.
  # Exception: for "vat paid, min" and "vat paid, max",
  # the sum in the hh data should be the same as the sum in the purchase
  # data excluding San Andres.
  # Such a test would require pulling geo data into the purchase-sum data.
  # However, since those purchase-sum variables are not treated differently
  # from "transactions" or "value" by households_2_purchases.py,
  # it is safe (and faster) to simply omit
  # "vat paid, min" and "vat paid, max" from the test.

# TODO : Add MeanBounds tests for the variables in new_cols.

