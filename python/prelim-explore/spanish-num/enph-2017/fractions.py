import numpy as np
import pandas as pd
import python.util as util
import python.build.datafiles as datafiles
import python.vat.files as vatfiles


# build the purchase data
purchases = pd.DataFrame()
  # accumulator: begins empty, accumulates across files
files = list( vatfiles.purchase_file_legends.keys() )
for file in files:
  legend = vatfiles.purchase_file_legends[file]
  shuttle = pd.read_csv( datafiles.yearSurveyFolder(2017) + "recip-10/" + file + '.csv'
                    , usecols = legend.keys()
                    )
  shuttle = shuttle.rename(columns=legend) # homogenize column names across files
  shuttle["file-origin"] = file
  purchases = purchases.append(shuttle)
del(shuttle,file)


# This paragraph detects a problem:
# Some peso-denominated columns have a minimum value less than 50,
# the minimum unit of currency in circulation.
for colname in list( purchases.columns.values ):
  # ignore object(string)-valued columns
  if purchases[colname].dtype != 'object':
    print( colname + "'s minimum positive value: ")
    print( min ( purchases
                  [ colname ]
                  [ purchases[colname] > 0 ]
    ) )


# The summary statistics printed at the end of this demonstrate
# that the only column with fractional values is quanity,
# which seems acceptable. (Fractions of pesos would be unreasonable.)
remainder_columns = []
for colname in list( purchases.columns.values ):
  # ignore object(string)-valued columns
  if purchases[colname].dtype != 'object':
    new_colname = colname + "-frac"
    remainder_columns.append( new_colname )
    purchases[new_colname] = purchases[colname] - np.floor( purchases[colname] )
print( purchases[remainder_columns].describe() )
