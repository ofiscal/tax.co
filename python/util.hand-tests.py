import pandas as pd
from numpy import nan
import python.util as util

df = pd.DataFrame( [  [1,2  ,1]
                    , [3,nan,1]
                    , [5,6  ,2]
                    , [7,8  ,2]
                    , [7,8  ,2]
                   ], columns = ["a","b","g"] )
util.tabulate_count_missing_min_med_max_mean_nonzero_by_group( df, "g", "b" )
