# The only thing to check is the increase in the set of columns.
# (Could check length, but a left merge cannot change that.)

if True:
  import sys
  import pandas as pd
  #
  import python.build.classes   as cl
  import python.build.output_io as oio
  import python.common.common   as com
  import python.common.misc     as misc
  import python.common.util     as util


df1_cols = oio.readStage( com.subsample,
                          "people_1",
                          nrows = 1 )
df1_rows = oio.readStage( com.subsample,
                          "people_1",
                          usecols = ["household"] )
df2 = oio.readStage(com.subsample, 'people_2_buildings')


cols1 = set( df1_cols.columns )
cols2 = set( df2.columns      )
new_cols = {
    "estrato",
    "region-1",
    "region-2",
    "age-decile",
    "income-decile",
    "female head" }

assert util.unique( df2.columns )
assert util.unique( new_cols )

assert set.intersection (cols1, new_cols) == set()
assert set.union        (cols1, new_cols) == cols2
assert set.difference   (cols2, cols1)    == new_cols

assert len(df1_rows) == len(df2)
assert util.near( len(df2),
                  misc.num_people / com.subsample,
                  tol_frac = 1/5 )

per_cell_spec = {
    "age-decile"    : cl.InRange( 0, 9 ),
    "income-decile" : cl.InRange( 0, 9 ),
    "female head"   : cl.InRange( 0, 1 ) }

per_column_spec = {
    "age-decile"    : cl.CoversRange( 0, 9 ),
    "income-decile" : cl.CoversRange( 0, 9 ),
    "female head"   : cl.CoversRange( 0, 1 ) }

for k,v in per_cell_spec.items():
  assert v . test( df2[k] )

for k,v in per_column_spec.items():
  assert v.test( df2[k] )

oio.test_write( com.subsample,
                "people_2_buildings",
                "It worked." )

