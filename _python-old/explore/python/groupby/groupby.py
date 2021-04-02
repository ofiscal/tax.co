import pandas as pd

testGroupBy = pd.read_csv( "data/groupby.csv" )
grouped = testGroupBy.groupby(['team','position'])['money','time'].agg('sum')
