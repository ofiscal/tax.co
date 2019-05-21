import pandas as pd
import sys


strategy_names = [ # There used to be a lot of these.
  "detail"             # They disappeared in the branch "retire-hypotheticals".
]

[detail] = strategy_names

subsample = int( sys.argv[1] )
if not subsample in [1,10,100,1000]:
  raise ValueError( "invalid subsample reciprocal: " + str(subsample) )

strategy = sys.argv[2]
if not strategy in strategy_names:
  raise ValueError( "invalid strategy: " + strategy )

regime_year = int( sys.argv[3] )
if not regime_year in [2016, 2018]:
  raise ValueError( "invalid tax regime year: " + str(regime_year) )

strategy_suffix = strategy
strategy_year_suffix = strategy + "." + str(regime_year)


# Wart: This function is duplicated in cl_fake.py
def retrieve_file( file_struct, subsample=subsample ):
  return pd.read_csv(
      "data/enph-2017/recip-" + str(subsample) + "/" + file_struct.filename
      , usecols = list( file_struct.col_dict.keys() )
    ) . rename( columns = file_struct.col_dict      )

# Wart: This function is duplicated in cl_fake.py
def collect_files( file_structs, subsample=subsample ):
  acc = pd.DataFrame()
  for f in file_structs:
    shuttle = retrieve_file(f)
    shuttle["file-origin"] = f.name
    for c in f.corrections:
      shuttle = c.correct( shuttle )
    acc = acc.append(shuttle)
  return acc
