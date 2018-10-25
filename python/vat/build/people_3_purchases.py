import sys
import pandas as pd
import python.vat.build.output_io as oio
import python.vat.build.common as common


if True: # input files
  people = oio.readStage( common.subsample, "people_2_buildings" )
  purchase_sums = oio.readStage( common.subsample, "purchase_sums." + common.vat_strategy_suffix )


if True: # merge purchase sums into people
  people = pd.merge( people, purchase_sums
                   , how = "left"
                   , on=["household","household-member"] )

  for s in ["min","max"]:
    people.loc[ people["region-1"] == "SAN ANDRÉS", "vat paid, " + s ] = 0


if True: # create a few more variables
  people["vat/value, min" ] = people["vat paid, min"] / people["value" ]
  people["vat/value, max" ] = people["vat paid, max"] / people["value" ]
  people["vat/income, min"] = people["vat paid, min"] / people["income"]
  people["vat/income, max"] = people["vat paid, max"] / people["income"]
  people["value/income"   ] = people["value"]         / people["income"]

  people["age-decile"] = pd.qcut(
    people["age"], 10, labels = False, duplicates='drop')
  people["income-decile"] = pd.qcut(
    people["income"], 10, labels = False, duplicates='drop')

  people["female head"] = people["female"] * (people["household-member"]==1)


oio.saveStage( common.subsample, people, 'people_3_purchases.' + common.vat_strategy_suffix )
