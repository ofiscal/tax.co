import pandas as pd

f = pd.DataFrame( { 'k' : [1,2,  1, 2, 3,  4]
                  , 'f' : [1,2,  11,22,33,  4] } )
g = pd.DataFrame( { 'k' : [1,2,3,  5]
                  , 'g' : [1,2,3,  5] } )

f.merge(g, how="left", on="k")
f.merge(g, how="right", on="k")
f.merge(g, how="inner", on="k")
