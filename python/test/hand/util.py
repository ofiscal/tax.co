import pandas as pd
from numpy import nan
import python.util as util

df = pd.DataFrame( [  [1,2  ,1 ,1 ]
                    , [1,nan,1 ,1 ]
                    , [1,0  ,2 ,1 ]
                    , [1,7  ,2 ,1 ]
                    , [1,8  ,2 ,2 ]
                    , [1,8  ,2 ,2 ]
                   ], columns = ["ignoring","examining","group","group-2"] )

df

util.tabulate_stats_by_group( df, "group", "examining" )
util.tabulate_stats_by_group( df, ["group","group-2"], "examining" )

df

summarizeQuantiles( "group"
                       , df.rename( columns = {"examining":"income"} ) )

df
