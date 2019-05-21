# Replace import of common.cl_args with this as needed when experimenting.
# PITFALL: Don't forget to undo such replacement before committing.

import pandas as pd
import sys

import python.build.classes as cla


strategy_names = [ # There used to be a lot of these.
  "detail"             # They disappeared in the branch "retire-hypotheticals".
]

[detail] = strategy_names

subsample = 100

strategy = detail
regime_year = 2018

strategy_suffix = strategy
strategy_year_suffix = strategy + "." + str(regime_year)


# Wart: This function is duplicated in cl_args.py
def retrieve_file( file_struct, subsample=subsample ):
  return pd.read_csv(
      "data/enph-2017/recip-" + str(subsample) + "/" + file_struct.filename
      , usecols = list( cla.name_map( file_struct.col_specs )
                      . keys() )
    )

# Wart: This function is duplicated in cl_args.py
def collect_files( file_structs, subsample=subsample ):
  acc = pd.DataFrame()
  for f in file_structs:
    shuttle = ( retrieve_file(f)
              . rename( columns = cla.name_map( f.col_specs ) ) )
    shuttle["file-origin"] = f.name
    for c in f.corrections:
      shuttle = c.correct( shuttle )
    acc = acc.append(shuttle)
  return acc
