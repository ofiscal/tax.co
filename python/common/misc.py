from python.build.classes import Correction
import numpy as np
import pandas as pd
import python.build.classes as cla


min_wage = 713585.5 # This is an average, because the ENPH spans two years.
                    # Minimum Wage 2016: COP$ 689,454
                    # Minimum Wage 2017: COP$ 737,717

uvt = (29753 + 31859) / 2 # This is the average of the UVTs from 2016 and 2017
muvt = uvt / 12 # monthly UVT, to harmonize with montly income


gmf_threshold = (11150650 + 10413550) / 2
  # 2018 = $11,604,600
  # 2017 = $11,150,650
  # 2016 = $10,413,550


variables = [ # in some purchase files, all three common variables are numbers
    ( "DIRECTORIO", {cla.VarContent.NotAString}, "household", 0 )
  , ( "ORDEN", {cla.VarContent.NotAString}, "household-member", 0 )
  , ( "FEX_C", {cla.VarContent.NotAString}, "weight", 0 )
  ]
variables_with_comma_weight = [
    # in others they are strings with commas instead of periods
    ( "DIRECTORIO", {cla.VarContent.NotAString}, "household", 0 )
  , ( "ORDEN", {cla.VarContent.NotAString}, "household-member", 0 )
  , ( "FEX_C", {cla.VarContent.Comma, cla.VarContent.Digits}, "weight", 0 )
  ]


def to_numbers(df, skip_columns=[]):
  for c in df.columns:
    if df[c].dtype == 'O' and not c in skip_columns:
      df[c] = df[c].str.strip()
      df[c] = df[c].replace("", np.nan)
      df[c] = pd.to_numeric(
          df[c]
        , errors='ignore' ) # leave entire column unchanged if any cell won't convert
  return df

# These apply to every file, be it purchases or people
corrections = [
  Correction.Replace_Substring_In_Column( "weight", ",", "." )
]
