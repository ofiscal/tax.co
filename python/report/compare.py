if True:
  from   os import path
  import pandas as pd
  import re
  #
  import python.build.output_io  as oio
  import python.common.common    as com
  import python.draw.util        as draw
  import python.common.terms     as terms


def sanitize_name_for_makefile (s : str) -> str:
  """Because Makefiles cannot handle spaces, and maybe colons, in filenames."""
  return re.sub (
    ":", "",
    re.sub ( " ", "-", s ) )

income_deciles = [ "income-decile: " + str(n)
                   for n in range(0,10) ]

income_deciles_shorthand = [
  str(i) + "-" + str(i+9)
  for i in range (0, 100, 10) ]

def draw_one_comparison (
    measure : str,
    unit : str,
    user : pd.DataFrame,
    baseline : pd.DataFrame,
    save_path : str ):

  user_deciles     = user     [ income_deciles ]
  baseline_deciles = baseline [ income_deciles ]

  user_levels : pd.Series = (
    user_deciles [
      user [ "measure" ] == measure ]
    . transpose()
    . iloc[:,0] )

  baseline_levels : pd.Series = (
    baseline_deciles [
      baseline [ "measure" ] == measure ]
    . transpose()
    . iloc[:,0] )

  draw.bar_chart_with_changes (
    title  = "Resulting change in \"" + measure + "\"",
    xlabel = unit + " by income percentile",
    ylabel = "COP",
    labels = income_deciles_shorthand,
    levels = baseline_levels,
    changes = user_levels - baseline_levels,
    save_path = save_path )

for unit in ["households", "earners"]:

  measure = "tax: mean"
    # TODO : Will probably want to loop over
    # different values of this, too.

  draw_one_comparison (
    measure   = measure,
    unit      = unit,
    user      = oio.readUserData (
      com.subsample,
      "report_" + unit + "." + com.strategy_year_suffix ),
    baseline  = oio.readBaselineData (
      1,
      "report_" + unit + "." + terms.detail + ".2019" ),
    save_path = path.join (
      oio.get_user_data_folder ( com.subsample ),
      sanitize_name_for_makefile (
        "change in." + measure + ".by " + unit + "."
        + com.strategy_year_suffix ) ) )
