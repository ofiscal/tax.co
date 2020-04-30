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
  prCols = oio.readStage( com.subsample,
                          "purchase_sums." + com.strategy_suffix,
                          nrows = 1 )
  p3 = oio.readStage( com.subsample,
                      'people_3_purchases.' + com.strategy_suffix )

assert near( len(p3),
             num_people / com.subsample,
             tol_frac = 1/5 )

assert len(p2rows) == len(p3)

new_cols = [ "vat/value, min",
             "vat/value, max",
             "vat/income, min",
             "vat/income, max",
             "value/income",
             "age-decile",
             "income-decile",
             "female head"]

if True: # Assert uniqueness of anything new.
         # (Earlier tests do the same for preexisting files.)
  assert( unique( p3.columns ) )
  assert( unique( new_cols ) )

if True: # p3's columns are the union of the other things.
  assert ( set( p3.columns ) ==
           set.union( set( p2cols.columns ),
                      set( prCols.columns ),
                      set( new_cols ) ) )
  # PITFALL: The next assertion looks weaker than the last. It's not.
  # It guards against the possibility that any two sets
  # in the union overlap.
  assert ( len( p3    .columns ) ==
           len( p2cols.columns ) +
           len( prCols.columns ) - 2 + # omit the 2 keys we merged on
           len( new_cols ) )

if True: # some places should be San Andrés, and they should have no IVA.
  assert (p3["region-1"] == "SAN ANDRÉS").any()
  assert p3[ p3["region-1"] == "SAN ANDRÉS" ]["vat paid, min"].max() == 0
  assert p3[ p3["region-1"] == "SAN ANDRÉS" ]["vat paid, max"].max() == 0

per_cell_spec = {
    "vat/value, min"  : { cl.IsNull(), cl.InRange( 0, 0.3 ) },
    "vat/value, max"  : { cl.IsNull(), cl.InRange( 0, 0.3 ) },
    "vat/income, min" : { cl.IsNull(), cl.InRange( 0, np.inf ) },
    "vat/income, max" : { cl.IsNull(), cl.InRange( 0, np.inf ) },
    "value/income"    : { cl.IsNull(), cl.InRange( 0, np.inf ) },
    "age-decile"      : {              cl.InRange( 0, 9 ) },
    "income-decile"   : {              cl.InRange( 0, 9 ) },
    "female head"     : {              cl.InRange( 0, 1 ) } }

per_column_spec = {
    "vat/value, min"  : cl.CoversRange( 0,      0.15   ),
    "vat/value, max"  : cl.CoversRange( 0,      0.15   ),
    "vat/income, min" : cl.CoversRange( 0,      np.inf ),
    "vat/income, max" : cl.CoversRange( 0,      np.inf ),
    "value/income"    : cl.CoversRange( 0.01,   np.inf ),
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

