from python.vat.build.classes import Correction
import numpy as np
import pandas as pd


subsample = 100

folder = "data/enph-2017/recip-" + str(subsample) + "/"

variables = { "DIRECTORIO" : "household"
              , "ORDEN" : "household-member"
              , "FEX_C" : "weight"
}

# These apply to every file, be it purchases or people
corrections = [
  Correction.Replace_Substring_In_Column( "weight", ",", "." )
]

def collect_files( file_structs ):
  acc = pd.DataFrame()
  for f in file_structs:
    shuttle = (
      pd.read_csv(
        folder + f.filename
        , usecols = list( f.col_dict.keys() ) )
      . rename( columns = f.col_dict        )
    )
    shuttle["file-origin"] = f.name
    for c in f.corrections:
      shuttle = c.correct( shuttle )
    acc = acc.append(shuttle)
  return acc

def to_numbers(df):
  for c in df.columns:
    if df[c].dtype == 'O':
      df[c] = df[c].str.strip()
      df[c] = df[c].replace("", np.nan)
      df[c] = pd.to_numeric( df[c]
                           , errors='ignore' ) # ignore operation if any value won't convert
  return df
