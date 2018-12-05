import pandas as pd
import numpy as np

#import common


class common:
  subsample = 1

# medios: read, clean
medios = pd.read_csv( "data/enph-2017/recip-" + str(common.subsample)
                    + "/Gastos_menos_frecuentes_-_Medio_de_pago.csv"
                    , usecols = ["DIRECTORIO", "P10305", "P10305S1"]
) . rename ( columns = { "DIRECTORIO" : "household"
                     # , "ORDEN" : "household-member" # PITFALL: Always 1.
                       , "P10305" : "house,new"
                       , "P10305S1" : "house,value" } )
medios = medios[ medios["house,new"] < 3 ]
medios["house,new"] = 2 - medios["house,new"]


# buildings: read, clean
buildings = pd.read_csv( "data/enph-2017/recip-" + str(common.subsample)
                       + "/Viviendas_y_hogares.csv"
                       , usecols = ["DIRECTORIO", "P5102", "P5103"]
) . rename( columns = { "DIRECTORIO" : "household"
                    # , "ORDEN" : "household-member" # PITFALL: Always 1.
                      , "P5102":"house,recent-bought"
                      , "P5103":"house,value" }
) . replace( " ", np.nan )

buildings = buildings[ (~ buildings["house,recent-bought"] . isnull() )
                     & (~ buildings["house,value" ]        . isnull() )
]
buildings["house,value"] = buildings["house,value"].astype('float')
buildings = buildings[ buildings["house,value"] > 100
                       # avoids error codes 98 and 99
] . drop( columns = "house,recent-bought" ) # at this point it's always 1
