import pandas as pd

import python.vat.raw_enph_input.config as raw_enph

# input files
import python.vat.raw_enph_input.files.nice_purchases as nice_purchases
import python.vat.raw_enph_input.files.medios as medios
import python.vat.raw_enph_input.files.articulos as articulos
import python.vat.raw_enph_input.files.capitulo_c as capitulo_c


def collect_files( file_structs ):
  acc = pd.DataFrame()
  for f in file_structs:
    shuttle = (
      pd.read_csv(
        raw_enph.folder + f.filename
        , usecols = list( f.col_dict.keys() ) )
      . rename( columns = f.col_dict        )
    )
    shuttle["file-origin"] = f.name
    for c in f.corrections:
      shuttle = c.correct( shuttle )
    acc = acc.append(shuttle)
  return acc

purchases = collect_files(
  articulos.files
  + medios.files
  + capitulo_c.files
  + nice_purchases.files
)
