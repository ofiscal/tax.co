if True:
  import numpy                   as np
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

    df["income-percentile-in[90,98]"] = (
        (df["income-percentile"] >= 90)
      & (df["income-percentile"] <= 98) )

    df["income-millile-in[990,997]"] = (
        (df["income-millile"] >= 990)
      & (df["income-millile"] <= 997) )

    df["income-millile-in[990,998]"] = (
        (df["income-millile"] >= 990)
      & (df["income-millile"] <= 998) )

    df["income < min wage"] = (
      df["income"] < c.min_wage )

def make_summary_frame (
    unit           : str, # unit of observation: households or earners
    df             : pd.DataFrame,
    groupVars      : List[str], # gruops              to summarize
    variables      : List[str], # aspects (of groups) to summarize
      # PITFALL: Long name because "vars" is an occupied keyword.
    restrictedVars : List[str]  # a subset of those things to summarize
) -> Tuple [ pd.DataFrame,   # The restricted (subset of) results.
             pd.DataFrame ]: # The unrestricted results.
  summaryDict = {} # TODO: Don't use this. It's no longer necessary --
                   # maybe it never was -- and it's confusing.
  groupSummaries = []
  for (gv, gRange) in groupVars:
    varSummaries = []
    for v in variables:
      t = desc.tabulate_stats_by_group (
        df0         = df,
        group_name  = gv,
        group_range = gRange,
        param_name  = v,
        weight_name = "weight" )
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

  ret_tmi . reset_index ( inplace = True )
  ret_tmi = ret_tmi . rename ( columns = {"index" : "measure"} )

  if True: # Compute "income tax sums / total income sums"
    # PITFALL: As a ratio of two rows, this has to be calculated
    # differently from (so far) all of the other rows.
    if True: # compute some intermediate things
      def tail_of_row ( measure_name : str ) -> pd.Series:
        """
        From (ret_tmi : pd.DataFrame),
        returns the row with the measure equal to measure_name,
        minus the "measure" column, as a Series of floats.
        """
        return ( ret_tmi.loc[ ret_tmi["measure"]
                              == measure_name ]
                 . drop ( columns = "measure" )
                 . astype ( float ) # before dropping "measure" it was an Object
                 . iloc[0] ) # reduce a one-row Frame to a Series
      total_income_tax_over_total_income : pd.Series = pd.concat (
        [ pd.Series ( {"measure" : "income tax sums / total income sums" } ),
          ( ( tail_of_row ( "tax, income: sums" ) /
              tail_of_row ( "income: sums" ) )
            . replace ( [np.nan, np.inf], 0 ) ) ] )
    ret_tmi : pd.DataFrame = pd.concat (
      [ pd.DataFrame ( total_income_tax_over_total_income ) . transpose(),
        ret_tmi ],
      ignore_index = True )

  return ( ( ret_tmi # a subset of the rows in `ret_tmi`
             . loc [ ret_tmi ["measure"]
                     . isin( defs.ofMostInterestLately ) ] ),
           ret_tmi )

for (unit, df, groupVars, variables, restrictedVars) in [
    ( "earners",
      earners,
      defs.earnerGroupVars,
      defs.earnerVars,
      defs.earnerRestrictedVars ),
    ( "households",
      households,
      defs.householdGroupVars,
      defs.householdVars,
      defs.householdRestrictedVars )
  ]:
  (ret, ret_tmi) = make_summary_frame (
    unit           = unit,
    df             = df,
    groupVars      = groupVars,
    variables      = variables,
    restrictedVars = restrictedVars )

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
