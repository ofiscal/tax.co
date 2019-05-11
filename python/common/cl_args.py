import pandas as pd
import sys


vat_strategy_names = [ # There used to be a lot of these.
  "detail"             # They disappeared in the branch "retire-hypotheticals".
]

[detail] = vat_strategy_names

subsample = int( sys.argv[1] )
if not subsample in [1,10,100,1000]:
  raise ValueError( "invalid subsample reciprocal: " + str(subsample) )

vat_strategy = sys.argv[2]
if not vat_strategy in vat_strategy_names:
  raise ValueError( "invalid vat_strategy: " + vat_strategy )

vat_strategy_suffix = vat_strategy

regime_year = int( sys.argv[3] )
if not regime_year in [2016, 2018]:
  raise ValueError( "invalid tax regime year: " + str(regime_year) )

# Wart: This function is duplicated in cl_fake.py
def collect_files( file_structs, subsample=subsample ):
  acc = pd.DataFrame()
  for f in file_structs:
    shuttle = (
      pd.read_csv(
        "data/enph-2017/recip-" + str(subsample) + "/" + f.filename
        , usecols = list( f.col_dict.keys() )
      ) . rename( columns = f.col_dict      )
    )
    shuttle["file-origin"] = f.name
    for c in f.corrections:
      shuttle = c.correct( shuttle )
    acc = acc.append(shuttle)
  return acc
