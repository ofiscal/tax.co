# Beyond the shape of the data, there's nothing to test.

if True:
  import pandas as pd
  #
  import python.build.output_io as oio
  import python.common.common as com
  from   python.common.misc import num_households
  from   python.common.util import near


sums = oio.readStage(
    com.subsample,
    "purchase_sums." + com.strategy_suffix )

assert ( list( sorted( sums.columns ) ) ==
         [ "home purchase value",
           "household",
           "predial",
           "transactions",
           "value",
           "vat paid, max",
           "vat paid, min" ] )

assert sums["household"].is_unique

assert near( len(sums),
             num_households / com.subsample,
             tol_frac = 1/5 )

oio.test_write( com.subsample,
                "build_purchase_sums",
                "It worked." )
