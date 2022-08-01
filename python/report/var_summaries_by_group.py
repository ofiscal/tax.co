if True:
  import os
  import pandas                  as pd
  import sys
  from   typing import List, Tuple
  #
  import python.build.output_io  as oio
  import python.common.common    as com
  import python.common.describe  as desc
  import python.common.misc      as c
  import python.draw.util        as draw
  import python.report.defs      as defs


if True: # load data
  households = oio.readUserData(
      com.subsample,
      "households_2_purchases." + com.strategy_year_suffix )

  earners = oio.readUserData(
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

def make_summary_frame (
    unit           : str, # unit of observation: households or earners
    df             : pd.DataFrame,
    variables      : List[str], # things to summarize
    restrictedVars : List[str]  # a subset of those things to summarize
) -> Tuple [ pd.DataFrame,   # The restricted (subset of) results.
             pd.DataFrame ]: # The unrestricted results.
  summaryDict = {} # TODO: Don't use this. It's no longer necessary --
                   # maybe it never was -- and it's confusing.
  groupSummaries = []
  for gv in defs.groupVars:
    varSummaries = []
    for v in variables:
      t = desc.tabulate_stats_by_group ( df, gv, v, "weight" )
      t = t.rename (
        columns = dict (
          zip ( t.columns
              , map ( lambda x: v + ": " + x
                    , t.columns ) ) ),
        index = dict (
          zip ( t.index
              , map ( lambda x: str(gv) + ": "
                      + defs.maybeFill( gv, str(x) )
                    , t.index ) ) ) )
      varSummaries . append ( t )
    groupSummaries . append (
      pd.concat ( varSummaries,
                  axis = 1 ) )
  summaryDict [ unit ] = pd.concat ( groupSummaries, axis = 0 )

  ret_tmi = ( pd.concat ( list ( summaryDict.values() ),
                          axis = 0 )
              . transpose () )

  # TODO ? This passage seems like it could be slightly simplified --
  # rename `index` to `measure` before spawning `ret` from `ret_tmi`,
  # so that it needn't be renamed again in `ret`.
  # The two reset_index calls cannot be combined, though.
  ret = ret_tmi.loc [ restrictedVars ] # a subset of the rows in `ret`
  ret_tmi . reset_index ( inplace = True )
  ret_tmi = ret_tmi . rename ( columns = {"index" : "measure"} )
  ret     . reset_index ( inplace = True )
  ret     = ret . rename ( columns = {"index" : "measure"} )

  return (ret, ret_tmi)

for (unit, df, variables, restrictedVars) in [
    ( "earners",    earners,    defs.earnerVars,    defs.earnerRestrictedVars ),
    ( "households", households, defs.householdVars, defs.householdRestrictedVars ) ]:
  (ret, ret_tmi) = make_summary_frame ( unit, df, variables, restrictedVars )
  oio.saveUserData(
      com.subsample,
      ret_tmi,
      "report_" + unit + "_tmi." + com.strategy_year_suffix )
  oio.saveUserData_excel(
      com.subsample,
      ret_tmi,
      "report_" + unit + "_tmi." + com.strategy_year_suffix )
  oio.saveUserData(
      com.subsample,
      ret,
      "report_" + unit + "."     + com.strategy_year_suffix )
  oio.saveUserData_excel(
      com.subsample,
      ret,
      "report_" + unit + "."     + com.strategy_year_suffix )
