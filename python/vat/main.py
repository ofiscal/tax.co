# The value-added tax.

import numpy as np
import pandas as pd
import python.util as util
import python.datafiles as datafiles
from python.vat.files import legends

acc = pd.DataFrame() # accumulator: begins empty, accumulates across files
files = list( legends.keys() )


# build the purchase data
for file in files:
  legend = legends[file]
  data = pd.read_csv( datafiles.yearSubsampleSurveyFolder(2017,100) + file + '.csv'
                      , usecols = list( legend.keys() )
  )

  data = data.rename(columns=legend) # homogenize column names across files
  data["file-origin"] = file

  if False: # print summary stats for `data`, before merging with `acc`
    print( "\n\nFILE: " + file + "\n" )
    for colname in data.columns.values:
      col = data[colname]
      print("\ncolumn: " + colname)
      print("missing: " + str(len(col.index)-col.count())
            + " / "  + str(len(col.index)))
      print( col.describe() )
  acc = acc.append(data)
purchases = acc

purchases.to_csv( 'purchases.recip_100.csv')

coicop_vat = pd.read_csv( "data/vat/coicop-vat.csv", sep=';' )
purchases = purchases.merge( coicop_vat, on="coicop" )

purchases["price"] = purchases["value"] / purchases["quantity"]
purchases["vat-paid"] = purchases["value"] * purchases["vat-rate"]

if True: # build the person expenditure data
  people = purchases.groupby(
    ['household', 'household-member'])['value','vat-paid'].agg('sum')
  people.describe()
