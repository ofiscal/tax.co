import sys
import pandas as pd
import numpy as np


df = pd.DataFrame( { 'g' : [1, 1, 1, 2, 2, 2]
                   , 'x' : [1,10, 5, 4, 2, 8]
} )

df . sort_values("x",ascending=False) . groupby("g") . head(2) . sort_values( ["g","x"] )
