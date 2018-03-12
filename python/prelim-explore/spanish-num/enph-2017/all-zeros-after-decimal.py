# prelim-explore/spanish-num/test-enph-2017.py
# This builds a data set, purchases.as-text.csv,
# that is easily grepped to find values ending in ".000".
# The command to do so is:
  # grep "\.000" purchases.as-text.csv | grep -v "\:..\.000"
  # The second clause is to exclude dates, some of which end in ":xy.000"
  # where x and y are digits.
# Such values would, if present, indicate a Spanish number format error.
# Good news -- there aren't any!

import numpy as np
import pandas as pd
import python.util as util
import python.datafiles as datafiles
import python.vat.files as vatfiles


purchases = pd.DataFrame() # accumulator: begins empty, accumulates across files
files = list( vatfiles.purchase_file_legends.keys() )

# build the purchase data, interpreting everything as text
for file in files:
  legend = vatfiles.purchase_file_legends[file]
  data = pd.read_csv( datafiles.yearSurveyFolder(2017) + "recip-10/" + file + '.csv'
    , usecols = legend.keys()
    , dtype =   vatfiles.format_purchase_fields_as_strings[file] )
  data = data.rename(columns=legend) # homogenize column names across files
  data["file-origin"] = file
  purchases = purchases.append(data)
del(data)

purchases.to_csv( 'purchases.as-text.csv')
