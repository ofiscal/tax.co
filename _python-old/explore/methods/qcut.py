# Solved!
  # Problem: many people report identical incomes -- not just at 0 pesos/month,
    # but other levels too.
    # This causes some of the 100 quantiles to be indistinguishable.
  # Solution: Add a tiny bit of random noise to incomes, to create "income+noise".
    # Group on that, then discard it, and report on the original incomes.

import pandas as pd
import numpy as np

# qcut(x,n) always makes n buckets,
# but some (here the first two) are indistinguishable
x = pd.Series( [0,0] + list( range( 1, 98 ) ) + [1000] )
y = pd.qcut( x, 100, duplicates = 'drop' )
# for i in y: print(i)
len(y)
len(y.unique())

# For only 98 buckets to be distinguishable, I believe,
# it would have to be that all first 2 and some of the 3rd percentile
# are at 0 income. But if the 1/10 sample is representative, only 1.1% of
# families have income <= 0.
s = pd.read_csv( "output/vat/data/recip-1/households.const_0.18.csv"
                 , usecols = ["income"] )
len(s)
len( s[ s["income"] <= 0 ] )

# Here's a solution.
epsilon = 1
noise = pd.Series( np.random.uniform( -epsilon, epsilon, len(s) ) )
s["income+noise"] = s["income"] + noise
s["quantile"] = pd.qcut( s["income+noise"], 100, duplicates = 'drop' )
s["count"] = 1 # to be summed
counts = s . groupby( by = "quantile"
         ) . agg( { "count" : np.sum
                  , "income" : [np.min, np.max] } )
