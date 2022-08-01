# TODO : automate these tests

if True:
  import pandas as pd
  from numpy import nan
  import python.common.util as util


df = pd.DataFrame( [  [1,      2  ,      1,       1,         1 ]
                    , [1,      nan,      1,       1,         2 ]
                    , [1,      0  ,      2,       1,         3 ]
                    , [1,      7  ,      2,       1,         4 ]
                    , [1,      8  ,      2,       2,         5 ]
                    , [1,      8  ,      2,       2,         6 ]
  ], columns = ["ignoring","examining","group","group-2", "weight"] )

df

util.tabulate_stats_by_group( df, "group",             None, "examining"           ) . transpose()
util.tabulate_stats_by_group( df, "group",             None, "examining", "weight" ) . transpose()
util.tabulate_stats_by_group( df, ["group","group-2"], None, "examining"           ) . transpose()
util.tabulate_stats_by_group( df, ["group","group-2"], None, "examining", "weight" ) . transpose()
  # If we call this table t, note that t.loc["count",:].sum() == 5,
  # which is the number of rows in t.

df

summarizeQuantiles( "group"
                  , df.rename( columns = {"examining":"income"} ) )

df
