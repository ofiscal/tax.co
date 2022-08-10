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
  100, # TODO: Should be 1
  "report_earners_tmi." + terms.detail + ".2019" )
user_households     = oio.readUserData (
  com.subsample,
  "report_households_tmi." + com.strategy_year_suffix )
baseline_households = oio.readBaselineData (
  100, # TODO: Should be 1
  "report_households_tmi." + terms.detail + ".2019" )

def sanitize_name_for_makefile (s : str) -> str:
  """Because Makefiles cannot handle spaces, and maybe colons, in filenames."""
  return re.sub (
    ":", "",
    re.sub ( " ", "-", s ) )

def make_one_difference_table ( unit      : str,
                                user      : pd.DataFrame,
                                baseline  : pd.DataFrame ):
  df = pd.concat ( [
    pd.DataFrame ( user["measure"] ),
    ( user       . drop ( columns = "measure" ) . astype ( float )
      - baseline . drop ( columns = "measure" ) . astype ( float ) ) ] )
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

def draw_one_comparison (
    measure  : str,
    unit     : str,
    user     : pd.DataFrame,
    baseline : pd.DataFrame ):

  user_deciles     = user     [ list ( defs.decile_names.values() ) ]
  baseline_deciles = baseline [ list ( defs.decile_names.values() ) ]

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
    xlabel = unit + " by income percentile",
    ylabel = "COP",
    labels = defs.decile_names.values(),
    levels = baseline_levels,
    changes = user_levels - baseline_levels,
    save_path = path.join (
      oio.get_user_data_folder ( com.subsample ),
      sanitize_name_for_makefile (
        "change in." + measure + ".by " + unit + "."
        + com.strategy_year_suffix ) ) )

for (unit, user, baseline) in [
    ("households", user_households, baseline_households),
    ("earners",    user_earners,    baseline_earners) ]:
  measure = "tax: mean"
    # TODO : Will probably want to loop over
    # different values of this, too.
  make_one_difference_table (
    unit     = unit,
    user     = user     [ user     ["measure"] . isin (
      defs.ofMostInterestLately ) ],
    baseline = baseline [ baseline ["measure"] . isin (
      defs.ofMostInterestLately ) ] )
  draw_one_comparison (
    measure   = measure,
    unit      = unit,
    user      = user,
    baseline  = baseline )
