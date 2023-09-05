if True:
  from   os import path
  import pandas as pd
  import re
  #
  import python.build.output_io  as oio
  import python.common.common    as com
  import python.common.terms     as terms
  import python.draw.util        as draw
  import python.report.defs      as defs


# Read data.
user_earners        = oio.readUserData (
  com.subsample,
  "report_earners_tmi." + com.strategy_year_suffix )
baseline_earners    = oio.readBaselineData (
  com.subsample,
  "report_earners_tmi." + terms.detail + ".2019" )
user_households     = oio.readUserData (
  com.subsample,
  "report_households_tmi." + com.strategy_year_suffix )
baseline_households = oio.readBaselineData (
  com.subsample,
  "report_households_tmi." + terms.detail + ".2019" )
user_nonzero_earners_by_labor_income        = oio.readUserData (
  com.subsample,
  "report_nonzero_earners_by_labor_income_tmi." + com.strategy_year_suffix )
baseline_nonzero_earners_by_labor_income    = oio.readBaselineData (
  com.subsample,
  "report_nonzero_earners_by_labor_income_tmi." + terms.detail + ".2019" )

def sanitize_name_for_makefile (s : str) -> str:
  """Because Makefiles cannot handle spaces, and maybe colons, in filenames."""
  return re.sub (
    ":", "",
    re.sub ( " ", "-", s ) )

def make_one_difference_table (
    unit      : str,
    user      : pd.DataFrame,
    baseline  : pd.DataFrame ):
  df = pd.concat (
    [ pd.DataFrame ( user["measure"] ),
      ( user       . drop ( columns = "measure" ) . astype ( float )
        - baseline . drop ( columns = "measure" ) . astype ( float ) ) ],
    axis = "columns" )
  df . to_csv (
    path_or_buf = path.join (
      oio.get_user_data_folder ( com.subsample ),
      "changes_" + unit + ".csv" ),
    index = False )
  df . to_excel (
    path.join (
      oio.get_user_data_folder ( com.subsample ),
      "changes_" + unit + ".xlsx" ),
    index = False )

# Compares the user-generated data to the baseline,
# across deciles, for the variable `measure`.
def draw_one_comparison (
    quantile_defining_var : str,
    measure               : str,
    unit                  : str, # unit of observation, e.g. "households"
    user                  : pd.DataFrame,
    baseline              : pd.DataFrame ): # Writes a file.
  decile_columns = list ( defs.decile_names (quantile_defining_var )
                          . values() )
  user_deciles     = user     [ decile_columns ]
  baseline_deciles = baseline [ decile_columns ]
  user_levels : pd.Series = (
    user_deciles [
      user [ "measure" ] == measure ]
    . transpose()
    . iloc[:,0]
    . astype ( float ) )
  baseline_levels : pd.Series = (
    baseline_deciles [
      baseline [ "measure" ] == measure ]
    . transpose()
    . iloc[:,0]
    . astype ( float ) )
  draw.bar_chart_with_changes (
    title  = "Resulting change in \"" + measure + "\"",
    xlabel = unit + " by " + quantile_defining_var + " percentile",
    ylabel = "COP",
    labels = decile_columns,
    levels = baseline_levels,
    changes = user_levels - baseline_levels,
    save_path = path.join (
      oio.get_user_data_folder ( com.subsample ),
      sanitize_name_for_makefile (
        "change in." + measure + ".by " + unit + "."
        + com.strategy_year_suffix ) ) )

for (unit, quantile_defining_var, user, baseline) in [
    ("households",   "IT",        user_households,    baseline_households),
    ("earners",      "income",    user_earners,       baseline_earners),
    ("nonzero_earners_by_labor_income",
     "income",
     user_nonzero_earners_by_labor_income,
     baseline_nonzero_earners_by_labor_income) ]:
  for measure in ["tax: mean", "income - tax: mean"]:
    make_one_difference_table (
      unit     = unit,
      user     = user     [ user     ["measure"] # the quotes are not a typo
                        . isin ( defs.ofMostInterestLately ) ],
      baseline = baseline [ baseline ["measure"] # the quotes are not a typo
                            . isin ( defs.ofMostInterestLately ) ] )
    draw_one_comparison (
      measure               = measure,
      quantile_defining_var = quantile_defining_var,
      unit                  = unit,
      user                  = user,
      baseline              = baseline )
