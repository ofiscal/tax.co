import pandas as pd
import python.vat.raw_enph_input.config as raw_enph
import python.vat.raw_enph_input.articulos as articulos
import python.vat.raw_enph_input.nice_purchases as nice_purchases


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
      c.correct( shuttle )
    acc = acc.append(shuttle)
  return acc

purchases = collect_files(
  nice_purchases.files
  + articulos.files )
