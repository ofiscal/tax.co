if True:
  import datetime
  import sys
  import numpy as np
  import pandas as pd
  #
  import python.build.output_io as oio
  import python.common.common as com
  import python.build.classes as cl
  from   python.common.misc import num_people
  from   python.common.util import near, unique


if True: # read
  p2rows = oio.readStage( com.subsample,
                          "people_2_buildings",
                          usecols = ["household"] )
  p2cols = oio.readStage( com.subsample,
                          "people_2_buildings",
                          nrows = 1 )
  p3 = oio.readStage( com.subsample,
                      'people_3_purchases.' + com.strategy_suffix )

assert near( len(p3),
             num_people / com.subsample,
             tol_frac = 1/5 )

assert len(p2rows) == len(p3)

new_cols = [ "age-decile",
             "income-decile",
             "female head"]

if True: # Assert uniqueness of anything new.
         # (Earlier tests do the same for preexisting files.)
  assert( unique( p3.columns ) )
  assert( unique( new_cols ) )

if True: # p3's columns are the union of the other things.
  assert ( set( p3.columns ) ==
           set.union( set( p2cols.columns ),
                      set( new_cols ) ) )
  # PITFALL: The next assertion looks weaker than the last. It's not.
  # It ensures no two sets in the union overlap.
  assert ( len( p3    .columns ) ==
           len( p2cols.columns ) +
           len( new_cols ) )

per_cell_spec = {
    "age-decile"      : {              cl.InRange( 0, 9 ) },
    "income-decile"   : {              cl.InRange( 0, 9 ) },
    "female head"     : {              cl.InRange( 0, 1 ) } }

per_column_spec = {
    "age-decile"      : cl.CoversRange( 0,      9      ),
    "income-decile"   : cl.CoversRange( 0,      9      ),
    "female head"     : cl.CoversRange( 0,      1      ) }

for k,v in per_cell_spec.items():
  assert cl.properties_cover_num_column( v, p3[k] )

for k,v in per_column_spec.items():
  assert v.test( p3[k] )

if True: # IO
  log = str( datetime.datetime.now() )
  oio.test_write( com.subsample
                , "people_3_purchases"
                , log )

