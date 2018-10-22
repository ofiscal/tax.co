import pandas as pd
from numpy import nan
import python.util as util

df = pd.DataFrame( [  [1,2  ,1]
                    , [1,nan,1]
                    , [1,0  ,2]
                    , [1,7  ,2]
                    , [1,8  ,2]
                    , [1,8  ,2]
                   ], columns = ["ignoring","examining","group"] )
util.tabulate_stats_by_group( df, "group", "examining" )
