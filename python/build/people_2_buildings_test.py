# The only thing to check is the increase in the set of columns.
# (Could check length, but a left merge cannot change that.)


if True:
  import sys
  import pandas as pd
  #
  import python.build.output_io as oio
  import python.common.misc as c
  import python.common.common as c

df1 = oio.readStage(c.subsample, 'people_1')
df2 = oio.readStage(c.subsample, 'people_2_buildings')

cs1 = set(df1.columns)
new_cols = {'estrato', 'region-1', 'region-2'}
cs2 = set(df2.columns)

assert set.union(cs1,new_cols) == cs2
assert set.difference(cs2,cs1) == new_cols
assert len( df1.columns ) == len( df2.columns ) + len( new_cols )
  # This is useful since column names in Pandas need not be unique.

oio.test_write( cm.subsample,
                "people_2_buildings_test",
                "It worked." )
