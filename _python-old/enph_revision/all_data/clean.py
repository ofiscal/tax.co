import pandas as pd
import numpy as np


for df in newEnphsDfs:
  df.columns = map(str.lower, df.columns)

for (df,col) in [  
  (gastos_semanales_rural__comidas_preparadas_fuera, "nh_cgprcfh_p2")
  , (gastos_diarios_urbano__comidas_preparadas_fuera,  "nh_cgducfh_p2")
  , (gastos_personales_urbano__comidas_preparadas_fuera,  "nh_cgpucfh_p2")
  , (gastos_diarios_personales_urbano,"nc4_cc_p2")
]:
  df[col].str.replace( "," , "." )

for df in newEnphsDfs:
  for c in df.columns:
    if df[c].dtype == 'O':
      df[c] = df[c].str.strip()
      df[c] = df[c].replace("", np.nan)
      df[c] = pd.to_numeric( df[c]
                           , errors='ignore' ) # ignore operation if any value won't convert
