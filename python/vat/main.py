# The value-added tax.

import numpy as np
import pandas as pd
import python.util as util
import python.datafiles as datafiles
from python.vat.files import purchase_file_legends

purchases = pd.DataFrame() # accumulator: begins empty, accumulates across files
files = list( purchase_file_legends.keys() )


# build the purchase data
for file in files:
  legend = purchase_file_legends[file]
  shuttle = pd.read_csv( datafiles.yearSubsampleSurveyFolder(2017,100) + file + '.csv'
                      , usecols = list( legend.keys() )
  )

  shuttle = shuttle.rename(columns=legend) # homogenize column names across files
  shuttle["file-origin"] = file

  if False: # print summary stats for `shuttle`, before merging with `purchases`
    print( "\n\nFILE: " + file + "\n" )
    for colname in shuttle.columns.values:
      col = shuttle[colname]
      print("\ncolumn: " + colname)
      print("missing: " + str(len(col.index)-col.count())
            + " / "  + str(len(col.index)))
      print( col.describe() )
  purchases = purchases.append(shuttle)
del(shuttle)

purchases.to_csv( 'purchases.recip_100.csv')

coicop_vat = pd.read_csv( "data/vat/coicop-vat.csv", sep=';' )
purchases = purchases.merge( coicop_vat, on="coicop" )

purchases["price"] = purchases["value"] / purchases["quantity"]
purchases["vat-paid"] = purchases["value"] * purchases["vat-rate"]

if True: # build the person expenditure data
  people = purchases.groupby(
    ['household', 'household-member'])['value','vat-paid'].agg('sum')
  people.describe()

  # PITFALL: Even if using a subsample of purchases, use the complete demographic data sample
  demog = pd.read_csv( datafiles.yearSurveyFolder(2017,1) + file + '.csv'
                      , usecols = list( legend.keys() )
