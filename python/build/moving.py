if True:
  import sys
  import pandas as pd
  #
  import python.common.util as util
  import python.build.output_io as oio
  import python.common.common as c


if True: # These tests used to run in people_3_purchases.
         # They must be used instead to test households_2_purchases.
         # See people_3_purchases_test for how to use these definitions.
  new_cols = [ "vat/value, min",
               "vat/value, max",
               "vat/income, min",
               "vat/income, max",
               "value/income" ]

  if True:
    assert (p3["region-1"] == "SAN ANDRÉS").any()
    assert p3[ p3["region-1"] == "SAN ANDRÉS" ]["vat paid, min"].max() == 0
    assert p3[ p3["region-1"] == "SAN ANDRÉS" ]["vat paid, max"].max() == 0

  per_cell_spec = {
      "vat/value, min"  : { cl.IsNull(), cl.InRange( 0, 0.3 ) },
      "vat/value, max"  : { cl.IsNull(), cl.InRange( 0, 0.3 ) },
      "vat/income, min" : { cl.IsNull(), cl.InRange( 0, np.inf ) },
      "vat/income, max" : { cl.IsNull(), cl.InRange( 0, np.inf ) },
      "value/income"    : { cl.IsNull(), cl.InRange( 0, np.inf ) },

  per_column_spec = {
      "vat/value, min"  : cl.CoversRange( 0,      0.15   ),
      "vat/value, max"  : cl.CoversRange( 0,      0.15   ),
      "vat/income, min" : cl.CoversRange( 0,      np.inf ),
      "vat/income, max" : cl.CoversRange( 0,      np.inf ),
      "value/income"    : cl.CoversRange( 0.01,   np.inf ),

  assert ( len( p3    .columns ) ==
           len( p2cols.columns ) +
           len( prCols.columns ) - 2 + # omit the 2 keys we merged on
           len( new_cols ) )
