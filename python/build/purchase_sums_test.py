# Beyond the shape of the data, there's nothing to test.

if True:
  import pandas as pd
  #
  import python.build.output_io as oio
  import python.common.common as com
  from   python.common.misc import num_people
  from   python.common.util import near


sums = oio.readStage(
    com.subsample,
    "purchase_sums." + com.strategy_suffix )

assert ( list( sorted( sums.columns ) ) ==
         [ "household",
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

print( "len(sums) = ", len(sums) )
print( "num_people = ", num_people )
print( "com.subsample = ", com.subsample )
print( "num_people / com.subsample = ", num_people / com.subsample)
assert near( len(sums),
             num_people / com.subsample,
             tol_frac = 1/5 )

oio.test_write( com.subsample,
                "build_purchase_sums",
                "It worked." )
