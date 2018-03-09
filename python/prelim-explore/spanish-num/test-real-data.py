# prelim-explore/spanish-num/test-real-data.py
# This builds a data set, purchases.as-text.csv,
# that is easily grepped to find values ending in .000
  # grep "\.000" purchases.as-text.csv | grep -v "\:..\.000"
# If present, those would indicate a Spanish number format error.
# Good news -- there aren't any!

import numpy as np
import pandas as pd
import python.util as util
import python.datafiles as datafiles
import python.vat.files as vatfiles

purchases = pd.DataFrame() # accumulator: begins empty, accumulates across files
files = list( vatfiles.legends.keys() )

# build the purchase data
for file in files:
  legend = vatfiles.legends[file]
  data = pd.read_csv( datafiles.folder(2017) + "recip-100/" + file + '.csv'
    , usecols = legend.keys()
    , dtype =   vatfiles.format_all_fields_as_strings[file] )
  data = data.rename(columns=legend) # homogenize column names across files
  data["file-origin"] = file
  purchases = purchases.append(data)
del(data)

purchases.to_csv( 'purchases.as-text.csv')
