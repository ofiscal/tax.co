from python.build.classes import Correction
import numpy as np
import pandas as pd
import python.common.cl_fake as cl


min_wage = 713585.5 # This is an average, because the ENPH spans two years.
                    # Minimum Wage 2016: COP$ 689,454
                    # Minimum Wage 2017: COP$ 737,717

uvt = (29753 + 31859) / 2 # This is the average of the UVTs from 2016 and 2017

variables = { "DIRECTORIO" : "household"
            , "ORDEN" : "household-member"
            , "FEX_C" : "weight"
}

def to_numbers(df, skip_columns=[]):
  for c in df.columns:
    if df[c].dtype == 'O' and not c in skip_columns:
      df[c] = df[c].str.strip()
      df[c] = df[c].replace("", np.nan)
      df[c] = pd.to_numeric( df[c]
                           , errors='ignore' ) # leave entire column unchanged if any row in it won't convert
  return df

# These apply to every file, be it purchases or people
corrections = [
  Correction.Replace_Substring_In_Column( "weight", ",", "." )
]

def collect_files( file_structs, subsample=cl.subsample ):
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
