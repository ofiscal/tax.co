# This file could have been called "orden snafu: damage assessmnet"

# In a previous incarnation of tax.co,
# the ORDEN variable was assumed to mean the same thing in the purchase data that it means in the person data:
# a unique-within-household identifier of persons.
# This code explores the effect that has on estimated household spending.


if True:
  import numpy as np
  import pandas as pd
  #
  import python.build.classes as cla
  import python.build.purchases.legends as legends
  import python.build.output_io as oio
  import python.common.common as com
  import python.common.util as util


pur = oio.readStage ( # the last purchases-level data set
    com.subsample,
    "purchases_2_vat." + com.strategy_suffix )

ppl = oio.readStage( # the first person-level data set
    com.subsample,
    'people_1',
    usecols = ["household", "household-member"] )

hh = ( ppl . groupby( "household" )
      . agg( {"household-member" : "max" } )
      . reset_index()
      . rename( columns = {"household-member" : "max member"} ) )

pur["n purchases"] = 1
hh_pur = ( pur . groupby( "household" )
          . agg( {"household-member" : "max",
                  "n purchases" : "sum" } )
          . reset_index()
          . rename( columns = {"household-member" : "max orden"} ) )

pur = pur.merge( hh, on="household" )

lim = pur.copy()
lim = lim[ lim["household-member"] <= lim["max member"] ]
purAgg = ( pur
          . groupby( "household" )
          . agg( {"value" : "sum"} )
          . rename( columns = {"value" : "total"} ) )

limAgg = ( lim
          . groupby( "household" )
          . agg( {"value" : "sum"} )
          . rename( columns = {"value" : "limited"} ) )

aggs = purAgg.merge( limAgg, on="household" )
aggs["frac"] = aggs["limited"] / aggs["total"]
aggs.describe()
