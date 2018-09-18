import pandas as pd
import numpy as np

from python.vat.build.classes import Correction
import python.vat.build.common as common

# input files
import python.vat.build.purchases.nice_purchases as nice_purchases
import python.vat.build.purchases.medios as medios
import python.vat.build.purchases.articulos as articulos
import python.vat.build.purchases.capitulo_c as capitulo_c
import python.vat.build.people as people


def collect_files( file_structs ):
  acc = pd.DataFrame()
  for f in file_structs:
    shuttle = (
      pd.read_csv(
        common.folder + f.filename
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

purchases = collect_files(
  articulos.files
  # + medios.files
    # The tax only applies if the purchase is more than 880 million pesos,
    # and the data only records purchases of a second home.
  + capitulo_c.files
  + nice_purchases.files
)

for c in [ # TODO ? This might be easier to understand without the Correction class.
  Correction.Replace_Substring_In_Column( "quantity", ",", "." )
  , Correction.Replace_Missing_Values( "quantity", 1 )

  , Correction.Change_Column_Type( "coicop", str )
  , Correction.Replace_Entirely_If_Substring_Is_In_Column( "coicop", "inv", np.nan )

  # The rest of these variables need the same number-string-cleaning process:
    , Correction.Change_Column_Type( "where-got", str )
      # same as this: purchases["where-got"] = purchases["where-got"] . astype( str )
    , Correction.Replace_In_Column( "where-got"
                                  , { ' ' : np.nan
                                    , "nan" : np.nan } ) # 'nan's are created from the cast to type str
      # same as this: purchases["where-got"] = purchases["where-got"] . replace( <that same dictionary> )

    , Correction.Change_Column_Type( "freq", str )
    , Correction.Replace_In_Column( "freq"
                                  , { ' ' : np.nan
                                    , "nan" : np.nan } )

    , Correction.Change_Column_Type( "how-got", str )
    , Correction.Replace_In_Column( "how-got"
                                  , { ' ' : np.nan
                                    , "nan" : np.nan } )

    , Correction.Change_Column_Type( "value", str )
    , Correction.Replace_In_Column( "value"
                                  , { ' ' : np.nan
                                    , "nan" : np.nan } )
]: purchases = c.correct( purchases )

purchases = to_numbers(purchases)

for c in [
  Correction.Apply_Function_To_Column(
    "how-got"
    , lambda x: 1 if x==1 else
      # HACK: x >= 0 yields true for numbers, false for NaN
      (0 if x >= 0 else np.nan) )
  , Correction.Rename_Column("how-got", "is-purchase")
]: c.correct( purchases )

# people = to_numbers( collect_files( people.files ) )
