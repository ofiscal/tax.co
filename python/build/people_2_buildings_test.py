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


in_cols = oio.readStage( com.subsample,
                          "people_1",
                          nrows = 1 )
in_rows = oio.readStage( com.subsample,
                          "people_1",
                          usecols = ["household"] )
out = oio.readStage(com.subsample, 'people_2_buildings')


cols1 = set( in_cols.columns )
cols2 = set( out.columns      )
new_cols = {
    "estrato",
    'recently bought this house',
    "region-1",
    "region-2",
    "age-decile",
    "income-decile",
    "female head" }

assert util.unique( out.columns )
assert util.unique( new_cols )

assert set.intersection (cols1, new_cols) == set()
assert set.union        (cols1, new_cols) == cols2
assert set.difference   (cols2, cols1)    == new_cols

assert len(in_rows) == len(out)
assert util.near( len(out),
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
  assert v . test( out[k] )

for k,v in per_column_spec.items():
  assert v.test( out[k] )

oio.test_write( com.subsample,
                "people_2_buildings",
                "It worked." )

