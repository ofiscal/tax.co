import sys
import pandas as pd

import python.util as util
import python.vat.build.output_io as oio
from python.vat.build.people.files import edu_key


# subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.
subsample = 10

households = oio.readStage( subsample, "households" )

vars = [ "income"
       , "income, pension"
       , "income, cesantia"
       , "income, capital, dividends"
       , "income, capital w/o dividends"
       , "income, infrequent"
       , "income, govt"
       , "income, private"
       , "income, labor"
       , "members"
       , "female head"
       , "vat/income, min"
       , "vat/income, max"
       ]

groupVars = [ "one"
            , "female head"
            , "income-decile"
            , "region-2" ]

groupSummaries = []
for gv in groupVars:
  varSummaries = []
  for v in vars:
    t = util.tabulate_stats_by_group( households, gv, v )
    t = t.rename( columns = dict( zip( t.columns
                                      , map( lambda x: v + ": " + x
                                           , t.columns ) ) )
                , index    = dict( zip( t.index
                                      , map( lambda x: gv + ": " + str(x)
                                           , t.index ) ) )
                )
    varSummaries.append( t )
  groupSummaries.append( pd.concat( varSummaries, axis = 1 ) )

pd.concat( groupSummaries, axis = 0
         ) . transpose(
         ) . to_csv( "output/vat/tables/summaries.csv" )
