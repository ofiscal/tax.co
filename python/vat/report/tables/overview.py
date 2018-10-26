import os
import sys
import pandas as pd

import python.util as util
import python.vat.build.output_io as oio
from python.vat.build.people.files import edu_key
import python.vat.build.common as common


households = oio.readStage( common.subsample, "households." + common.vat_strategy_suffix
             ) . rename( columns = {"income, capital, dividends" : "income, dividends"} )

households["income, labor + cesantia"] = households["income, labor"] + households["income, cesantia"]

vars = [ "income"
       , "income, labor + cesantia"
       , "income, capital w/o dividends"
       , "income, dividends"
       , "income, pension"
       , "income, govt"
       , "income, private"
       , "income, infrequent"
       , "members"
       , "female head"
       , "value"
       , "value/income"  
       , "vat/income, min"
       , "vat/income, max"
       , "vat/value, min"
       , "vat/value, max"
       ]

groupVars = [ "one"
            , "female head"
            , "income-decile"
            , "region-2" ]

groupSummaries = []
for gv in groupVars:
  varSummaries = []
  for v in vars:
    t = util.tabulate_stats_by_group( households, gv, v, "weight" )
    t = t.rename( columns = dict( zip( t.columns
                                      , map( lambda x: v + ": " + x
                                           , t.columns ) ) )
                , index    = dict( zip( t.index
                                      , map( lambda x: gv + ": " + str(x)
                                           , t.index ) ) )
                )
    varSummaries.append( t )
  groupSummaries.append( pd.concat( varSummaries, axis = 1 ) )

df_tmi = pd.concat( groupSummaries, axis = 0
                  ) . transpose()

output_dir = "output/vat/tables/recip-" + str(common.subsample) + "/"

if not os.path.exists(output_dir): os.makedirs(output_dir)

df_tmi.to_csv( output_dir + "overview, tmi." + common.vat_strategy_suffix + ".csv" )

df = df_tmi.ix[[
    "income: mean"
  , "income: min"
  , "income: max"
  , "income, labor + cesantia: mean"
  , "income, capital w/o dividends: mean"
  , "income, dividends: mean"
  , "income, pension: mean"
  , "income, govt: mean"
  , "income, private: mean"
  , "income, infrequent: mean"
  , "members: mean"
  , "female head: mean"
  , "value: median"
  , "value: mean"
  , "value/income: median"
  , "value/income: mean"
  , "vat/value, min: median"
  , "vat/value, min: mean"
  , "vat/value, max: median"
  , "vat/value, max: mean"
  , "vat/income, min: median"
  , "vat/income, min: mean"
  , "vat/income, max: median"
  , "vat/income, max: mean"
]]

df.to_csv( output_dir + "overview." + common.vat_strategy_suffix + ".csv" )
