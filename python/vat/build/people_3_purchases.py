import sys
import pandas as pd
import python.vat.build.output_io as oio


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.


if True: # input files
  people = oio.readStage( subsample, "people_2_buildings" )
  purchase_sums = oio.readStage( subsample, "purchase_sums" )


if True: # merge purchase sums into people
  people = pd.merge( people, purchase_sums
                   , how = "left"
                   , on=["household","household-member"] )

  people["vat/value, min" ] = people["vat paid, min"] / people["value" ]
  people["vat/value, max" ] = people["vat paid, max"] / people["value" ]
  people["vat/income, min"] = people["vat paid, min"] / people["income"]
  people["vat/income, max"] = people["vat paid, max"] / people["income"]
  people["value/income"   ] = people["value"]         / people["income"]

  people["age-decile"] = pd.qcut(
    people["age"], 10, labels = False, duplicates='drop')
  people["income-decile"] = pd.qcut(
    people["income"], 10, labels = False, duplicates='drop')


oio.saveStage(subsample, people, 'people_3_purchases')
