import sys
from python.build.classes import Correction
import numpy as np
import pandas as pd


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

subsample = int( sys.argv[1] )

if not subsample in [1,10,100,1000]:
  raise ValueError( "invalid subsample reciprocal: " + str(subsample) )

vat_strategy = sys.argv[2]

if not vat_strategy in vat_strategy_names:
  raise ValueError( "invalid vat_strategy: " + vat_strategy )

if vat_strategy in [const, approx, prop_2018_10_31]:
  vat_flat_rate = float(sys.argv[3])  # float: 0.19, 0.107, etc.
else:
  vat_flat_rate = ""

vat_strategy_suffix = vat_strategy + "_" + str(vat_flat_rate)

# PITFALL: In purchases_2_1_del_rosario, there are 4 command line arguments rather than 3,
# and the third is not `vat_flat_rate`.
if vat_strategy == del_rosario:
  del_rosario_exemption_source = sys.argv[3]
  del_rosario_exemption_count = int( sys.argv[4] )

variables = { "DIRECTORIO" : "household"
            , "ORDEN" : "household-member"
            , "FEX_C" : "weight"
}

# These apply to every file, be it purchases or people
corrections = [
  Correction.Replace_Substring_In_Column( "weight", ",", "." )
]

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

def to_numbers(df, skip_columns=[]):
  for c in df.columns:
    if df[c].dtype == 'O' and not c in skip_columns:
      df[c] = df[c].str.strip()
      df[c] = df[c].replace("", np.nan)
      df[c] = pd.to_numeric( df[c]
                           , errors='ignore' ) # leave entire column unchanged if any row in it won't convert
  return df
