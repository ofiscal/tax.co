import pandas as pd

# qcut(x,n) always makes n buckets,
# but some (here the first two) are indistinguishable
x = [0,0] + list( range( 1, 98 ) ) + [1000]
y = pd.qcut( x, 100, duplicates = 'drop' )
for i in y: print(i)

# For only 98 buckets to be distinguishable, I believe,
# it would have to be that all first 2 and some of the 3rd percentile
# are at 0 income. But if the 1/10 sample is representative, only 1.1% of
# families have income <= 0.
x = pd.read_csv( "output/vat/data/recip-10/households.const_0.18.csv"
                 , usecols = ["income"] )["income"]
len(x)
len( x[ x <= 0 ] )
pd.qcut( x, 100, duplicates = 'drop' )

