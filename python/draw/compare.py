if True:
  from os import path
  import sys
  import json
  import pandas as pd
  import hashlib
  #
  import python.build.classes    as cla
  import python.common.common    as com
  import python.common.terms     as terms
  import python.build.output_io  as oio
  import python.draw.util        as draw


income_deciles = [ "income-decile: " + str(n)
                   for n in range(0,10) ]
cols_to_keep = [ "measure" ] + income_deciles

user = oio.readUserData (
  com.subsample,
  "report_" + "households" + "." + com.strategy_year_suffix )
user_restricted = user [ income_deciles ]

baseline = oio.readBaselineData (
  com.subsample,
  "report_" + "households" + "." + com.strategy_year_suffix )
baseline_restricted = baseline [ income_deciles ]

user_levels = (
  user_restricted [
    user [ "measure" ] == "tax: mean" ]
  . transpose()
  . iloc[:,0] )

baseline_levels = (
  baseline_restricted [
    baseline [ "measure" ] == "tax: mean" ]
  . transpose()
  . iloc[:,0] )

draw.bar_chart_with_changes (
  labels = [ str(i) + "-" + str(i+9)
             for i in range (0, 100, 10) ],
  levels = baseline_levels,
  changes = user_levels * (1.5) - baseline_levels,
  save_path = "test-diff-chart" )
