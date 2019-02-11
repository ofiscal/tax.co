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
