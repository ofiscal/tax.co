if True:
  import sys
  import pandas as pd
  #
  import python.common.util as util
  import python.build.output_io as oio
  import python.common.common as c


if True: # See people_2_buildings_test for how to use these definitions.
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

