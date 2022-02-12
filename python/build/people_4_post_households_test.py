if True:
  import datetime
  import numpy as np
  import pandas as pd
  #
  import python.build.output_io                     as oio
  import python.build.people_4_post_households_defs as defs
  import python.common.common                       as com
  from   python.common.misc import num_people
  import python.common.tests                        as com_tests


new_columns = [ "in labor force",
                "share",
                "one",
                "income-decile",
                "income-percentile",
                "vat / purchase value",
                "vat/income",
                "purchase value / income",
               ]

log = str( datetime.datetime.now () )

if True: # load data
  hh2 = oio.readStage (
    com.subsample,
    "households_2_purchases." + com.strategy_year_suffix )
  ps3 = oio.readStage (
    com.subsample,
    'people_3_income_taxish.' + com.strategy_year_suffix )
  ps4 = oio.readStage (
    com.subsample,
    'people_4_post_households.' + com.strategy_year_suffix )
  assert (
    set.intersection (
      set ( ps3.columns ),
      set ( defs.columns_to_pull_from_hs ) )
    == set ( ["household"] # PITFALL: If "household" isn't wrapped in a list, the result is a set of letters rather than a set containing a single word.
            ) )


#
# integration tests
#

assert ( set.union ( set ( ps3.columns ),
                     set ( defs.columns_to_pull_from_hs ),
                     set ( new_columns ) )
         == set ( ps4.columns ) )
log = log + "\n" + "Column names look good."

assert ps4["share"].max() <= 1.01
assert ps4["share"].min() >= -0.01
x = ( ps4 [[ "household", "share" ]]
      . groupby ( "household" )
      . agg ( "sum" ) )
assert x["share"].max() <= 1.01
assert x["share"].min() >= 0.99
del(x)
log = log + "\n" + "Share looks reasonable."

assert ( ( (   ( ps4 [ "in labor force" ] == 1 )
             & ( ps4 [ "age" ] >= 18 ) )
         | (     ps4 [ "income" ] > 0 ) ) . all () )
log = log + "\n" + "Rows include only earners."

for c in defs.household_variables_to_allocate_by_income_share:
  assert ps4[c] . mean() < hh2[c].mean()
  assert ps4[c] . mean() > ( hh2[c].mean() / 4 )
log = log + "\n" + "Means of new person-level variables are smaller than corresponding household-level variables, and not extremely so."

same_ratio = [ # Should be pretty similar in hh2 and ps4.
  "vat / purchase value",
  "vat/income",
  "purchase value / income", ]
same_ratio_hh_list = [ x + "-hh" for x in same_ratio ]
same_ratio_hh_dict = { x : x + "-hh" for x in same_ratio }
htemp = ( hh2 [ ["household"] + same_ratio ]
          . rename ( columns = same_ratio_hh_dict ) )
ptemp = ps4.merge ( htemp [ ["household"] + same_ratio_hh_list ],
                    on = "household" )
ptemp = ( # To make sure none of the ratios is infinite.
  ptemp [ ( ptemp [ "income" ] > 0 ) &
          ( ptemp [ "value, purchase" ] > 0 ) ] )
for c in same_ratio:
  assert ( ptemp [ c + "-hh" ] > 0.99 * ptemp [ c ] - 1 ) . all ()
  assert ( ptemp [ c + "-hh" ] < 1.01 * ptemp [ c ] + 1 ) . all ()
  log = log + "\n" + c + "has the same values in ps4 as in hh2."
del ( htemp, ptemp )

com_tests.test_quantiles ( df=ps4 )

oio.test_write ( com.subsample
               , "people_4_post_households"
               , log )
