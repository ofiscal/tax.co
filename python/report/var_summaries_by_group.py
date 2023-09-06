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
  import python.common.util      as util
  import python.report.defs      as defs


##################################
### Load, futz with input data ###
##################################

if True: # load data
  households = oio.readUserData(
      com.subsample,
      "households_2_purchases." + com.strategy_year_suffix )

  earners = oio.readUserData(
      com.subsample,
      "people_4_post_households." + com.strategy_year_suffix )

if True: # generate "income - tax"
  for df, var_name in [ ( households, "IT"     ),
                        ( earners,    "income" ), ]:
    df[ var_name + " - tax"] = df[var_name] - df["tax"]

# PITFALL: The many kinds of quantiles can be confusing. See
#  markdown/multiple-kinds-of-quantiles.md
def copy_with_alternative_quantile_order (
    model : pd.DataFrame,
    ordering_variable : str
) -> pd.DataFrame:
  res = model.copy()
  for label, n in [ (ordering_variable + "-decile"    , 10),
                    (ordering_variable + "-percentile", 100),
                    (ordering_variable + "-millile"   , 1000), ]:
    res[label] = (
      util.myQuantile (
        n_quantiles = n,
        in_col = res [ ordering_variable ] )
      . astype ( int ) )
  return res

nonzero_earners_by_labor_income = \
  copy_with_alternative_quantile_order (
    model = earners [
      # PITFALL: Since a random amount between 0 and 1 peso
      # is added to labor income in `build.people.main`
      # (in order to make the quantiles all the same size),
      # this keeps only people with income greater than 2 pesos,
      # rather than people with any nonzero labor income.
      earners ["income, labor"] > 2 ],
    ordering_variable = "income, labor" )

households_by_IT_per_capita = \
  copy_with_alternative_quantile_order (
    model = households,
    ordering_variable = "IT per capita" )

if True: # Create a few columns missing in the input data.
         # TODO ? Move upstream.
         # TODO : Replace loop with function definition
         # followed by some calls to it,
         # because assigning many variables in a loop is error-prone,
         # whereas one can qualify argument names in function calls.
  for (df, quantileVar, total_income_var) in [
      (households,                      "IT",            "IT"),
      (households_by_IT_per_capita,     "IT per capita", "IT"),
      (earners,                         "income",        "income"),
      (nonzero_earners_by_labor_income, "income, labor", "income"),
  ]:
    df["income, labor + cesantia"] = (
        df["income, labor"]
        + df["income, cesantia"] )

    df[quantileVar + "-percentile-in[90,97]"] = (
        (df[quantileVar + "-percentile"] >= 90)
      & (df[quantileVar + "-percentile"] <= 97) )

    df[quantileVar + "-percentile-in[90,98]"] = (
        (df[quantileVar + "-percentile"] >= 90)
      & (df[quantileVar + "-percentile"] <= 98) )

    df[quantileVar + "-millile-in[990,997]"] = (
        (df[quantileVar + "-millile"] >= 990)
      & (df[quantileVar + "-millile"] <= 997) )

    df[quantileVar + "-millile-in[990,998]"] = (
        (df[quantileVar + "-millile"] >= 990)
      & (df[quantileVar + "-millile"] <= 998) )

    df[total_income_var + " < min wage"] = (
      df[total_income_var] < c.min_wage )

if True: # Make some subsets.
  # PITFALL: All changes to `earners`, `households` should precede this.
  householdsFemale = households[ households["female head"] == 1 ] . copy()
  householdsMale   = households[ households["female head"] == 0 ] . copy()
  earnersFemale = earners[ earners["female"] == 1 ] . copy()
  earnersMale   = earners[ earners["female"] == 0 ] . copy()


###################################
### Build, save the output data ###
###################################

def make_summary_frame (
    unit             : str, # unit of observation: households or earners
    quantileVar      : str, # defines income quantiles, e.g. "IT" or "income"
    total_income_var : str, # often, but not always, equal to `quantileVar`
    df               : pd.DataFrame, # the underlying data   to summarize
    groupVars        : List[ Tuple [ str, List ] ], # gruops to summarize
    variables        : List[str], # aspects (of groups)      to summarize
      # PITFALL: Long name because "vars" is an occupied keyword.
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
                      + defs.fill_if_percentile ( groupVar = gv,
                                                  val      = str(x) )
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
        [ pd.Series ( {"measure" : ( "income tax sums / "
                                     + total_income_var
                                     + " sums" ) } ),
          ( ( tail_of_row ( "tax, income: sums" ) /
              tail_of_row ( total_income_var + ": sums" ) )
            . replace ( [np.nan, np.inf], 0 ) ) ] )
    ret_tmi : pd.DataFrame = (
      pd.concat (
        [ ( pd.DataFrame ( total_income_tax_over_total_income )
            . transpose() ),
          ret_tmi ],
        ignore_index = True )
      . rename ( columns = defs.quantileNames (quantileVar) ) )

  return ( ( ret_tmi # a subset of the rows in `ret_tmi`
             . loc [ ret_tmi ["measure"]
                     . isin (
                       defs.ofMostInterestLately (
                         total_income = quantileVar ) ) ] ),
           ret_tmi )

# TODO: Replace this loop with a series of function calls.
# That will permit qualifying the function argument names.
# (At present, the order of the lists below is delicate --
# the six variables assigned each time the loop runs
# are assigned to a list which, if its order changed,
# would make the results stupid, without looking stupid.)
#
# TODO: Rather than match the definitions of `quantileVar` and `groupVars`,
# it would be safer of `groupVars` were an (unapplied) function,
# which was applied to `quantileVar` by `make_summary_frame`.
for (unit, quantileVar, total_income_var, df, groupVars, variables) in [
    ( "earners",
      "income",
      "income",
      earners,
      defs.earnerGroupVars ("income"),
      defs.earnerVars, ),
    ( "earnersFemale",
      "income",
      "income",
      earnersFemale,
      defs.earnerGroupVars ("income"),
      defs.earnerVars, ),
    ( "earnersMale",
      "income",
      "income",
      earnersMale,
      defs.earnerGroupVars ("income"),
      defs.earnerVars, ),
    ( "nonzero_earners_by_labor_income",
      "income, labor",
      "income",
      nonzero_earners_by_labor_income,
      defs.earnerGroupVars ("income, labor"),
      defs.earnerVars, ),
    ( "households",
      "IT",
      "IT",
      households,
      defs.householdGroupVars ("IT"),
      defs.householdVars, ),
    ( "households_by_IT_per_capita",
      "IT per capita",
      "IT",
      households_by_IT_per_capita,
      defs.householdGroupVars ("IT per capita"),
      defs.householdVars, ),
    ( "householdsFemale",
      "IT",
      "IT",
      householdsFemale,
      defs.householdGroupVars ("IT"),
      defs.householdVars, ),
    ( "householdsMale",
      "IT",
      "IT",
      householdsMale,
      defs.householdGroupVars ("IT"),
      defs.householdVars, ), ]:

  (ret, ret_tmi) = make_summary_frame (
    unit             = unit,
    total_income_var = total_income_var,
    quantileVar      = quantileVar,
    df               = df,
    groupVars        = groupVars,
    variables        = variables, )

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
