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


if False: # purchases
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


if True: # people
  people = to_numbers( collect_files( people.files ) )

  people["female"] = people["female"] - 1 # originally 1=male, 2=female

  people["student"]         = 2 - people["student"] # originally 1=student, 2=not
  people["beca"]            = 2 - people["beca"] # originally 1=received beca ("en dinero o especie"), 2=not
  people["skipped 3 meals"] = 2 - people["skipped 3 meals"] # originally 1=yes, 2=no
  people["literate"]        = 2 - people["literate"] # originally 1=yes, 2=no
  people["want to work"]    = 2 - people["want to work"] # originally 1=yes, 2=no

  race_key = {
      1 : "Indigena"
    , 2 : "Gitano-Roma"
    , 3 : "Raizal" # "del archipiélago de San Andrés y Providencia"
    , 4 : "Palenquero" # "de San Basilio o descendiente"
    , 5 : "Negro" # "Negro(a), mulato(a), afrocolombiano(a) o afrodescendiente"
    , 6 : "Ninguno" # "Ninguno de los anteriores (mestizo, blanco, etc.)"
    }
  people["race"] = pd.Categorical(
    people["race"].map( race_key )
    , categories = list( race_key.values() )
    , ordered = True # might help for drawing pictures
  )

  edu_key = { 1 : "Ninguno",
      2 : "Preescolar",
      3 : "Basica\n Primaria",
      4 : "Basica\n Secundaria",
      5 : "Media",
      6 : "Superior o\n Universitaria",
      9 : "No sabe,\n no informa" }
  people["education"] = pd.Categorical(
    people["education"].map( edu_key ),
    categories = list( edu_key.values() ),
    ordered = True)

  time_key = { 1 : "work" # Trabajando
             , 2 : "search" # Buscando trabajo
             , 3 : "study" # Estudiando
             , 4 : "household" # Oficios del hogar
             , 5 : "disabled" # Incapacitado permanente para trabajar
             , 6 : "other" # Otra actividad
  }
  people["time use"] = pd.Categorical(
    people["time use"].map( time_key ),
    categories = list( time_key.values() ),
    ordered = True)
