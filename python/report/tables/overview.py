# exec( open( "python/report/tables/overview.py" ) . read() )

import os
import sys
import pandas as pd

import python.util as util
import python.draw.util as draw
import python.build.output_io as oio
import python.build.common as c


output_dir = "output/vat/tables/recip-" + str(c.subsample) + "/"
if not os.path.exists(output_dir): os.makedirs(output_dir)


if True: # Get, prepare the data
  households = oio.readStage( c.subsample, "households."        + c.vat_strategy_suffix
               ) . rename( columns = {"income, capital, dividends" : "income, dividends"} )

  households["income, labor + cesantia"] = households["income, labor"] + households["income, cesantia"]
 
  households["income-percentile-in[90,97]"] = (
      (households["income-percentile"] >= 90)
    & (households["income-percentile"] <= 97) )


if True: # create a summary dataframe
  householdVars = [ "income"
         , "income, labor + cesantia"
         , "income, capital w/o dividends"
         , "income, dividends"
         , "income, pension"
         , "income, govt"
         , "income, private"
         , "income, infrequent"
         , "income, rank 1"
         , "income, rank 2"
         , "income, rank 3"
         , "income, rank 4"
         , "income, rank 5"
         , "income, labor, rank 1"
         , "income, labor, rank 2"
         , "income, labor, rank 3"
         , "income, labor, rank 4"
         , "income, labor, rank 5"
         , "members"
         , "female head"
         , "value"
         , "value/income"
         , "vat paid, min"
         , "vat paid, max"
         , "vat/income, min"
         , "vat/income, max"
         , "vat/value, min"
         , "vat/value, max"
         , "predial"
         ]

  householdGroupVars = [ "one"
                      , "female head"
                      , "income-decile"
                      , "income-percentile"
                      , "income-percentile-in[90,97]"
                      , "region-2" ]

  # PITFALL: Earlier, this looped over two data sets, households and people.
  # Now its outermost loop is unnecessary.
  summaryDict = {}
  for (unit, df, vs, gvs) in [
      ( "households", households, householdVars, householdGroupVars ) ]:

    groupSummaries = []
    for gv in gvs:
      varSummaries = []
      for v in vs:
        t = util.tabulate_stats_by_group( df, gv, v, "weight" )
        t = t.rename(
          columns = dict( zip( t.columns
                              , map( lambda x: v + ": " + x
                                   , t.columns ) ) )
          , index    = dict( zip( t.index
                                , map( lambda x: str(gv) + ": " + str(x)
                                     , t.index ) ) )
                    )
        varSummaries . append( t )
      groupSummaries . append( pd.concat( varSummaries, axis = 1 ) )
    summaryDict[unit] = pd.concat( groupSummaries, axis = 0 )

  df_tmi = pd.concat( list( summaryDict.values() ), axis = 0
                    ) . transpose()


if True: # save
  df_tmi.to_csv( output_dir      + "overview, tmi." + c.vat_strategy_suffix + ".csv" )
  draw.to_latex( df_tmi, output_dir, "overview, tmi." + c.vat_strategy_suffix )


if True: # do the same thing to a subset of that data
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
    , "income, rank 1: mean"
    , "income, rank 1: mean_nonzero"
    , "income, rank 2: mean"
    , "income, rank 2: mean_nonzero"
    , "income, rank 3: mean"
    , "income, rank 3: mean_nonzero"
    , "income, rank 4: mean"
    , "income, rank 4: mean_nonzero"
    , "income, rank 5: mean"
    , "income, rank 5: mean_nonzero"
    , "income, labor, rank 1: mean"
    , "income, labor, rank 1: mean_nonzero"
    , "income, labor, rank 2: mean"
    , "income, labor, rank 2: mean_nonzero"
    , "income, labor, rank 3: mean"
    , "income, labor, rank 3: mean_nonzero"
    , "income, labor, rank 4: mean"
    , "income, labor, rank 4: mean_nonzero"
    , "income, labor, rank 5: mean"
    , "income, labor, rank 5: mean_nonzero"
    , "members: mean"
    , "female head: mean"
    , "value: median"
    , "value: mean"
    , "vat paid, min: mean"
    , "vat paid, max: mean"
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
    , "predial: median"
    , "predial: mean"
  ]]

  df.to_csv(         output_dir + "overview." + c.vat_strategy_suffix + ".csv" )
  draw.to_latex( df, output_dir, "overview." + c.vat_strategy_suffix )
