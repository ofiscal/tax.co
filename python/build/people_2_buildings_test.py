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


in_cols = oio.readCommonOutput (
  com.subsample,
  "people_1",
  nrows = 1 )
in_rows = oio.readCommonOutput (
  com.subsample,
  "people_1",
  usecols = ["household"] )
out = oio.readCommonOutput (
  com.subsample, 'people_2_buildings' )


cols1 = set( in_cols.columns )
cols2 = set( out.columns      )
new_cols = {
    "estrato",
    'recently bought this house',
    "region-1",
    "region-2",
    "age-decile",
    "IT",
    "IC",
    "ICM",
    "ICMD",
    "GT",
    "GC",
    "GCM",
    "female head" }

assert util.unique( out.columns )

assert set.intersection (cols1, new_cols) == set()
assert set.union        (cols1, new_cols) == cols2
assert set.difference   (cols2, cols1)    == new_cols

assert len(in_rows) == len(out)
assert util.near( len(out),
                  misc.num_people / com.subsample,
                  tol_frac = 1/5 )

per_cell_spec = {
    "age-decile"    : cl.InRange( 0, 9 ),
    "female head"   : cl.InRange( 0, 1 ) }

per_column_spec = {
    "age-decile"    : cl.CoversRange( 0, 9 ),
    "female head"   : cl.CoversRange( 0, 1 ) }

for k,v in per_cell_spec.items():
  assert v . test( out[k] )

# Using kk and vv instead of k and v to avoid a mypy error --
# mypy wants a variable name to always be associated with the same type.
for kk,vv in per_column_spec.items():
  assert vv.test( out[kk] )

oio.test_write( com.subsample,
                "people_2_buildings",
                "It worked." )
