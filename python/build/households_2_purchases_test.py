if True:
  import pandas as pd
  import numpy as np
  #
  import python.build.classes   as cl
  import python.build.output_io as oio
  import python.common.common   as com
  import python.common.util     as util


if True:
  hh_cols = oio.readUserData(
      com.subsample,
      "households_1_agg_plus." + com.strategy_year_suffix,
      nrows = 1 )
  hh_rows = oio.readUserData(
    com.subsample,
    "households_1_agg_plus." + com.strategy_year_suffix,
    usecols = ["household"] )
  pur = oio.readUserData(
    com.subsample,
    "purchase_sums." + com.strategy_suffix )
  merge = oio.readUserData(
    com.subsample,
    "households_2_purchases." + com.strategy_year_suffix )

if True: # See people_2_buildings_test for how to use these definitions.
  assert util.unique( merge.columns )
  new_cols = [ "vat / purchase value",
               "vat / income",
               "vat / IT",
               "purchase value / income",
               "purchase value / IT",
               "tax", ]
  assert ( len( merge.columns ) ==
           len( new_cols ) +
           len( hh_cols.columns ) +
           len( pur.columns )
           - 1 ) # omit the key that was merged on
  assert len( merge ) == len( hh_rows )

if True:
    assert         (merge["region-1"] == "SAN ANDRÉS") . any()
    assert ( merge[ merge["region-1"] == "SAN ANDRÉS" ]
             ["vat paid"].max() == 0 )

if True:
  # PITFALL: The reuse of the name `v` below generates harmless mypy errors,
  # because it expects `v` to always have the same type.
  for k,v in {
      "vat / purchase value"      : cl.InRange( 0, 0.3 ),
        # The special motorcycle tax, abusivelyed lump into the VAT table,
        # means the max "vat" is 0.27 rather than 0.19.
      "vat / income"              : cl.InRange( 0, np.inf ),
      "purchase value / income"   : cl.InRange( 0, np.inf )
      }.items():
    assert v.test( merge[k] )
  for k,v in {
      # These bounds could be tighter,
      # but the 1/1000 subsample has a small range.
      # PITFALL: If it weren't for the fuzzing on income,
      # the max on the fractions with income in the denominator
      # could be even bigger.
      "vat / purchase value"       : cl.CoversRange( 0,      0.1 ),
      "vat / income"               : cl.CoversRange( 0,      1e3 ),
      "purchase value / income"    : cl.CoversRange( 0.2,    1e3 ),
      }.items():
    assert v.test( merge[k] )
  for k,v in {
      "vat / purchase value"       : cl.MeanBounds( 2-2, 8e-2 ),
      "vat / income"               : cl.MeanBounds( 100, np.inf ),
      "purchase value / income"    : cl.MeanBounds( 1000, np.inf )
      }.items():
    assert v.test ( merge[k] )
  for c in new_cols:
    assert cl.MissingAtMost( 0.01 ) . test( merge[c] )

oio.test_write(
    com.subsample,
    "households_2_purchases",
    "It worked." )
