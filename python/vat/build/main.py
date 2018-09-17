import pandas as pd
import numpy as np

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

for c in common.coicop_corrections:
  purchases = c.correct( purchases )

purchases = to_numbers(purchases)

# people = to_numbers( collect_files( people.files ) )
