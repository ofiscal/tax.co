import numpy as np
import pandas as pd

import python.common.common as cl
import python.common.util as util
import python.build.output_io as oio
import python.build.purchases.nice_purchases as nice_purchases
import python.build.purchases.articulos as articulos
import python.build.purchases.capitulo_c as capitulo_c


ordering_columns = [ "DIRECTORIO"
                   , "SECUENCIA_ENCUESTA"
                   , "SECUENCIA_P"
                   , "ORDEN"]

files = [
    "Caracteristicas_generales_personas.csv"
  , "Gastos_diarios_del_hogar_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv"
  , "Gastos_diarios_personales_Urbano.csv"
  , "Gastos_diarios_Urbano_-_Capitulo_C.csv"
  , "Gastos_diarios_Urbanos.csv"
  , "Gastos_diarios_Urbanos_-_Mercados.csv"
  , "Gastos_menos_frecuentes_-_Articulos.csv"
  , "Gastos_menos_frecuentes_-_Medio_de_pago.csv"
  , "Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar.csv"
  , "Gastos_personales_Rural.csv"
  , "Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar.csv"
  , "Gastos_semanales_Rural_-_Capitulo_C.csv"
  , "Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar.csv"
  , "Gastos_semanales_Rurales.csv"
  , "Gastos_semanales_Rurales_-_Mercados.csv"
  , "Viviendas_y_hogares.csv"
]

dfs = {}
for fn in files:
  dfs[fn] = pd.read_csv(
    "data/enph-2017/recip-1/" + fn
    , usecols = ordering_columns )

ppl = dfs["Caracteristicas_generales_personas.csv"]
len( ppl["DIRECTORIO"].unique() )

for fn in files:
  print( "\nstarting summary of", fn )
  df = dfs[fn]
  # dfs[fn].describe()
  # len(dfs[fn]) # 291590
  for c in ordering_columns:
    print( c, "range: ", df[c].min(), df[c].max() )
  (df["SECUENCIA_ENCUESTA"] != df["ORDEN"]).sum() # always equal
  (df["SECUENCIA_P"] != 1).sum() # always unity
  print( "finishing", fn )

summary = pd.DataFrame()
for fn in files:
  df = dfs[fn]
  for c in set(ordering_columns) - {"DIRECTORIO"}:
#    summary.loc[fn, c + " min"]     = df[c].min() # it's always 1
    summary.loc[fn, c + " max"]     = df[c].max()
#    summary.loc[fn, c + " is constant"] = ( # sometimes true
#      df[c].min() == df[c].max() )
#  summary.loc[fn, "SECUENCIA_ENCUESTA = ORDEN"] = ( # sometimes true
#    (df["SECUENCIA_ENCUESTA"] != df["ORDEN"]).sum() == 0 )

summary.to_csv( "does-household-member-exist.csv" )
