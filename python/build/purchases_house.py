import pandas as pd
import numpy as np

#import python.common


class common:
  subsample = 1


# medios: read, clean
medios = pd.read_csv( "data/enph-2017/recip-" + str(common.subsample)
                    + "/Gastos_menos_frecuentes_-_Medio_de_pago.csv"
                    , usecols = ["DIRECTORIO", "P10305", "P10305S1"]
) . rename ( columns = { "DIRECTORIO" : "household"
                     # , "ORDEN" : "household-member" # PITFALL: Always 1.
                       , "P10305" : "house,new"
                       , "P10305S1" : "house,value" }
) . replace( " ", np.nan )
medios["house,value"] = medios["house,value"].astype('float')
medios = medios[ (medios["house,new"] < 3) # code 3 = did not purchase
               & (medios["house,value"] > 100) # avoids error codes 98 and 99
               ]
medios["house,new"] = 2 - medios["house,new"] # now it's a 0-1 variable
medios["house,newness-unknown"] = 0


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

buildings["house,new"] = 0
buildings["house,newness-unknown"] = 1


house_purchases = buildings.append(medios)


# compute VAT on houses

#if True: # TODO: replace with common.vat_strategy=="prop_2018_11_29":
#  medios["house,above-vat-threshold"] = (
#    medios["house,above-vat-threshold"] > (888.5 + 853.8 mil / 2) )
