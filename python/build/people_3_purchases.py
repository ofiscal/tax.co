import sys
import pandas as pd

import python.common.util as util
import python.build.output_io as oio
import python.common.misc as c
import python.common.cl_args as c


if True: # input files
  people = oio.readStage( c.subsample, "people_2_buildings" )
  purchase_sums = oio.readStage( c.subsample, "purchase_sums." + c.strategy_suffix )


if True: # merge purchase sums into people
  people = pd.merge( people, purchase_sums
                   , how = "left"
                   , on=["household", "household-member"] )

  for s in ["min", "max"]:
    people.loc[ people["region-1"] == "SAN ANDRÉS", "vat paid, " + s ] = 0


if True: # create a few more variables
  people["vat/value, min" ] = people["vat paid, min"] / people["value" ]
  people["vat/value, max" ] = people["vat paid, max"] / people["value" ]
  people["vat/income, min"] = people["vat paid, min"] / people["income"]
  people["vat/income, max"] = people["vat paid, max"] / people["income"]
  people["value/income"   ] = people["value"]         / people["income"]

  people["age-decile"] = pd.qcut(
    people["age"], 10, labels = False, duplicates='drop')
  people["income-decile"] = ( # PITFALL: there's a different such variable at the household level
    util.noisyQuantile( 10, 0, 1, people["income"] ) )

  people["female head"] = people["female"] * (people["household-member"]==1)


oio.saveStage( c.subsample, people, 'people_3_purchases.' + c.strategy_suffix )
