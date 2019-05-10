# Replace import of common.cl_args with this as needed when experimenting.
# PITFALL: Don't forget to undo such replacement before committing.

import pandas as pd
import sys


vat_strategy_names = [ # There used to be a lot of these.
  "detail"             # They disappeared in the branch "retire-hypotheticals".
]

[detail] = vat_strategy_names

subsample = 100

vat_strategy = detail
vat_strategy_suffix = vat_strategy


# Wart: This function is duplicated in cl_args.py
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
