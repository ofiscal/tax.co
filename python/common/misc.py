if True:
  import numpy as np
  import os
  import pandas as pd
  from   typing import Optional
  #
  from python.build.classes import Correction, StringCellProperty


######
###### About Colombia's laws
######

min_wage = 713585.5 # This is an average, because the ENPH spans two years.
                    # Minimum Wage 2016: COP$ 689,454
                    # Minimum Wage 2017: COP$ 737,717

uvt = (29753 + 31859) / 2 # This is the average of the UVTs from 2016 and 2017
muvt = uvt / 12 # monthly UVT, to harmonize with montly income

gmf_threshold = (11150650 + 10413550) / 2
  # 2018 = $11,604,600
  # 2017 = $11,150,650
  # 2016 = $10,413,550


######
###### About the data
######

num_households          = 87201  # number of households in full sample
  # (see explore/data,raw/count-households.py)
num_people              = 291590  # number of people    (full sample)
  # PITFALL: This suggests the 1/1000 sample should have 292 people.
  # The subsampling is based on households, though, not individuals,
  # and the true figure is substantially off from that,
  # requiring a high (20%) tolerance in some tests that count rows, like:
  #   assert near( len(p3),
  #                num_people / com.subsample,
  #                tol_frac = 1/5 )
num_purchases           = 9309621 # number of purchases (full sample)
num_purchases_surviving = 7357003 # number of purchases (full sample) with
  # both a value (in pesos) and a code indicating the kind of expense

variables = [ # in some purchase files, all three common variables are numbers
    ( "DIRECTORIO", {StringCellProperty.NotAString}, "household", 0 )
  , ( "FEX_C",      {StringCellProperty.NotAString}, "weight", 0 )
  ]
variables_with_comma_weight = [
    # in others they are strings with commas instead of periods
    ( "DIRECTORIO", {StringCellProperty.NotAString}, "household", 0 )
  , ( "FEX_C",      {StringCellProperty.Comma
                    ,StringCellProperty.Digits}, "weight", 0 )
  ]

# These apply to every file, be it purchases or people
corrections = [
  Correction.Replace_Substring_In_Column( "weight", ",", "." )
]


######
###### Functions
######

def all_columns_to_numbers(df, skip_columns=[]):
  for c in df.columns:
    if df[c].dtype == 'O' and not c in skip_columns:
      df[c] = df[c].astype(str).str.strip()
      df[c] = df[c].replace( { "":np.nan
                             , "nan":np.nan} )
      df[c] = pd.to_numeric(
          df[c]
        , errors='ignore' ) # leave entire column unchanged if any cell won't convert
  return df

def read_csv_or_xlsx (
    filename : str,
    **kwargs
) -> Optional [ pd.DataFrame ]:
  # TODO : This generates downstream mypy type errors,
  # because usage sites aren't designed to handle the `None` possibility.
  # I suspect that instead of returning None, this should throw an error.
  # but I'd have to think carefully about
  # whether and where the error would be reported --
  # can I log it? What if it's thrown from within an exec() statement?
  # Would I have to litter the call sites with try-catch statements anyway?
  # (That would be just as awkward as handling the None case.)
    """ If filename ends in .csv, this assumes it is .csv-formatted, and similarly for .xlsx. If no file extension is provided, it finds the first file starting with the provided prefix. (If that file does not end in .csv or .xlsx, the result is not defined."""
    _, ext = os . path . splitext( filename )
    if ext == ".csv"    : return pd.read_csv  ( filename, **kwargs )
    elif ext == ".xlsx" : return pd.read_excel( filename, **kwargs )
    else:
      ffsw = find_first_file_starting_with ( filename )
      if ffsw: return read_csv_or_xlsx ( ffsw, **kwargs )
      else:    return None

def find_first_file_starting_with (
    path : str
) -> Optional [ str ]:
  """PITFALL: If multiple files start with the prefix, this might not do what you want."""
  folder, prefix = os . path . split ( path )
  files = os . listdir ( folder )
  with_prefix = [ f for f in files if f.startswith( prefix ) ]
  if with_prefix: return os . path . join (
      folder, with_prefix[0] )
  else: return None
