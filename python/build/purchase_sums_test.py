# Beyond the shape of the data, there's nothing to test.

if True:
  import pandas as pd
  #
  import python.common.common as cm
  import python.build.output_io as oio


sums = oio.readStage(
    cm.subsample,
    "purchase_sums." + cm.strategy_suffix )

assert ( list( sorted( sums.columns ) ) ==
         [ "home purchase value",
           "household",
           "household-member",
           "predial",
           "transactions",
           "value",
           "vat paid, max",
           "vat paid, min" ] )

sums["id"] = ( sums["household"].astype(str) +
               "-" +
               sums["household-member"].astype(str) )
assert sums["id"].is_unique

oio.test_write( cm.subsample,
                "build_purchase_sums",
                "It worked." )
