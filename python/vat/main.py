# The value-added tax.

import numpy as np
import pandas as pd
import python.util as util
import python.datafiles as datafiles
from python.vat.files import legends

acc = pd.DataFrame() # accumulator: begins empty, accumulates across files
files = list( legends.keys() )

for file in files:
  legend = legends[file]
  data = pd.read_csv( datafiles.folder(2017) + "recip-100/" + file + '.csv' )
  data = data[ list(legend.keys()) ] # subset columns
  data = data.rename(columns=legend) # homogenize column names across files
  data["file-origin"] = file

  if True: # print summary stats for `data`, before merging with `acc`
    print( "\n\nFILE: " + file + "\n" )
    for colname in data.columns.values:
      col = data[colname]
      print("\ncolumn: " + colname)
      print("missing: " + str(len(col.index)-col.count())
            + " / "  + str(len(col.index)))
      print( col.describe() )
  acc = acc.append(data)

data = acc
data["price"] = data["value"] / data["quantity"]
uniqueCoicops = data["coicop"].unique()
taxRates = pd.DataFrame( {
  'coicop' : uniqueCoicops
  , 'tax-rate' : np.random.choice( np.array([0.05,0.19])
                                 , size = uniqueCoicops.size )
} )

data = data.merge( taxRates, on="coicop" )
data["tax-paid"] = data["value"] * data["tax-rate"]
