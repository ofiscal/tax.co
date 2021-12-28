if True:
  import pandas as pd
  import numpy as np
  #
  import python.build.classes   as cl
  import python.build.output_io as oio
  import python.common.common   as com
  import python.common.util     as util


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
  assert util.unique( merge.columns )
  new_cols = [ "vat / purchase value",
               "vat/income",
               "purchase value / income" ]
  assert ( len( merge.columns ) ==
           len( hh_cols.columns ) +
           len( pur.columns ) - 1 + # omit the key that was merged on
           len( new_cols ) )
  assert len( merge ) == len( hh_rows )

if True:
    assert         (merge["region-1"] == "SAN ANDRÉS") . any()
    assert ( merge[ merge["region-1"] == "SAN ANDRÉS" ]
             ["vat paid"].max() == 0 )

if True:
  for k,v in {
      "vat / purchase value"      : cl.InRange( 0, 0.3 ),
        # The special motorcycle tax, abusivelyed lump into the VAT table,
        # means the max "vat" is 0.27 rather than 0.19.
      "vat/income"                : cl.InRange( 0, np.inf ),
      "purchase value / income"   : cl.InRange( 0, np.inf )
      }.items():
    assert v.test( merge[k] )
  for k,v in {
      # These bounds could be tighter,
      # but the 1/1000 subsample has a small range.
      "vat / purchase value"       : cl.CoversRange( 0,      0.1    ),
      "vat/income"                 : cl.CoversRange( 0,      np.inf ),
      "purchase value / income"    : cl.CoversRange( 0.2,    np.inf )
      }.items():
    assert v.test( merge[k] )
  for k,v in {
      "vat / purchase value"       : cl.MeanBounds( 2.5e-2, 6e-2 ),
      "vat/income"                 : cl.MeanBounds( np.inf, np.inf ),
      "purchase value / income"    : cl.MeanBounds( np.inf, np.inf )
      }.items():
    assert v.test( merge[k] )
  for c in new_cols:
    assert cl.MissingAtMost( 0.01 ) . test( merge[c] )

oio.test_write(
    com.subsample,
    "households_2_purchases",
    "It worked." )
