# exec( open( "python/report/households.py" ) . read() )

if True:
  import os
  import sys
  import pandas                  as pd
  #
  import python.build.output_io  as oio
  import python.common.common    as com
  import python.common.describe  as desc
  import python.common.misc      as c
  import python.draw.util        as draw
  import python.report.defs      as defs


if True: # load data
  households = oio.readStage(
      com.subsample,
      "households_2_purchases." + com.strategy_year_suffix )

  earners = oio.readStage(
      com.subsample,
      "people_4_post_households." + com.strategy_year_suffix )

if True: # Create a few columns missing in the input data.
         # TODO ? Move upstream.
  for df in [households, earners]:
    df["income, labor + cesantia"] = (
        df["income, labor"]
        + df["income, cesantia"] )

    df["income-percentile-in[90,97]"] = (
        (df["income-percentile"] >= 90)
      & (df["income-percentile"] <= 97) )

    df["income < min wage"] = (
      df["income"] < c.min_wage )

if True: # Create a summary dataframe.
  summaryDict = {}
  for ( unit,         df,         vs,           ) in [
      ( "households", households, defs.householdVars ) ]:

    groupSummaries = []
    for gv in defs.groupVars:
      varSummaries = []
      for v in vs:
        t = desc.tabulate_stats_by_group( df, gv, v, "weight" )
        t = t.rename (
          columns = dict(
                zip( t.columns
                   , map( lambda x: v + ": " + x
                        , t.columns ) ) )
          , index = dict(
                zip( t.index
                   , map( lambda x: str(gv) + ": "
                          + defs.maybeFill( gv, str(x) )
                        , t.index ) ) ) )
        varSummaries . append( t )
      groupSummaries . append( pd.concat( varSummaries, axis = 1 ) )
    summaryDict[unit] = pd.concat( groupSummaries, axis = 0 )

  df_tmi = pd.concat( list( summaryDict.values() ), axis = 0
                    ) . transpose()

if True: # do the same thing to a subset of that data
  df = df_tmi.loc [ defs.householdRestrictedVars ]

df_tmi . reset_index ( inplace = True )
df_tmi = df_tmi . rename ( columns = {"index" : "measure"} )
df     . reset_index ( inplace = True )
df     = df . rename ( columns = {"index" : "measure"} )

if True: # save
  oio.saveStage(
      com.subsample,
      df_tmi,
      "report_households_tmi." + com.strategy_year_suffix )
  oio.saveStage_excel(
      com.subsample,
      df_tmi,
      "report_households_tmi." + com.strategy_year_suffix )
  oio.saveStage(
      com.subsample,
      df,
      "report_households." + com.strategy_year_suffix )
  oio.saveStage_excel(
      com.subsample,
      df,
      "report_households." + com.strategy_year_suffix )
