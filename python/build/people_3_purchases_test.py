if True:
  import sys
  import pandas as pd
  #
  import python.build.output_io as oio
  import python.common.common as c
  import python.test_utils as t


if True: # read
  p2rows = oio.readStage( c.subsample,
                          "people_2_buildings",
                          usecols = ["household"] )
  p2cols = oio.readStage( c.subsample,
                          "people_2_buildings",
                          nrows = 1 )
  prCols = oio.readStage( c.subsample,
                          "purchase_sums." + c.strategy_suffix,
                          nrows = 1 )
  p3 = oio.readStage( c.subsample,
                      'people_3_purchases.' + c.strategy_suffix )

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
  assert( t.unique( p3.columns ) )
  assert( t.unique( new_cols )

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
           len( prCols.columns ) - 1 + # omit the one we merged on
           len( new_cols ) )

if True: # some places should be San Andrés, and they should have no IVA.
  assert (p3["region-1"] == "SAN ANDRÉS").any()
  assert p3[ p3["region-1"] == "SAN ANDRÉS" ]["vat paid, min"].max() == 0
  assert p3[ p3["region-1"] == "SAN ANDRÉS" ]["vat paid, max"].max() == 0


# ============== ============== ==============
# ============== REMAINING TODO ==============
# ============== ============== ==============

# check that these new variables have reasonable distributions
#   p3[new_cols].describe()
#   pd.options.display.width = 0
#   pd.set_option('display.float_format', '{:.2g}'.format)

# Output.
# Edit the Makefile.
