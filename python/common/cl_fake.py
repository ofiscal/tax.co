# Replace import of common.cl_args with this as needed when experimenting.
# PITFALL: Don't forget to undo such replacement before committing.

import pandas as pd
import sys


vat_strategy_names = [
    "const"
  , "detail"
  , "detail_224"
  , "approx"
  , "finance_ministry"
  , "prop_2018_10_31"
  , "prop_2018_11_29"
  , "del_rosario"
]

[const,detail,detail_224,approx,finance_ministry,prop_2018_10_31,prop_2018_11_29,del_rosario] = \
  vat_strategy_names

subsample = 100

vat_strategy = detail
vat_flat_rate = ""

vat_strategy_suffix = vat_strategy + "_" + str(vat_flat_rate)


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
