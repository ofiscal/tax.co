import pandas as pd
import numpy as np


for df in newEnphsDfs:
  df.columns = map(str.lower, df.columns)

coicop_only_files = [ # These files have no verbal accompaniment
  gastos_diarios_personales_urbano
  , gastos_diarios_urbanos
  , gastos_menos_frecuentes__articulos
  , gastos_personales_rural__comidas_preparadas_fuera
  , gastos_personales_rural
  , gastos_semanales_rurales
  ]

for df in coicop_only_files:
  df["verbal"] = np.nan
  df.columns = ["coicop","verbal"]

coicop_and_verbal_files = [ gastos_diarios_urbano__comidas_preparadas_fuera    
                          , gastos_personales_urbano__comidas_preparadas_fuera 
                          , gastos_semanales_rural__comidas_preparadas_fuera
                          ]

for df in coicop_and_verbal_files:
  df.columns = ["coicop","verbal"]

for (file,name) in zip( newEnphsDfs, newEnphsDfNames ):
  file["file"] = name

coicop_data = pd.concat( coicop_and_verbal_files + coicop_only_files,
                         axis = "rows" )
