# ABORTED after discovering that only one house out of the 561
# in our sample is above the threshold for paying VAT. See the variable
# "house,above-vat-threshold" (below) for how to reproduce that finding.

import pandas as pd
import numpy as np


import python.common
#class common:
#  subsample = 1
#  vat_strategy = "prop_2018_11_29"


# medios: read, clean
medios = pd.read_csv( "data/enph-2017/recip-" + str(common.subsample)
                    + "/Gastos_menos_frecuentes_-_Medio_de_pago.csv"
                    , usecols = ["DIRECTORIO", "P10305", "P10305S1", "FEX_C"]
) . rename ( columns = { "DIRECTORIO" : "household"
                     # , "ORDEN" : "household-member" # PITFALL: Always 1.
                       , "P10305" : "house,new"
                       , "P10305S1" : "house,value"
                       , "FEX_C" : "weight" }
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
                       , usecols = ["DIRECTORIO", "P5102", "P5103", "FEX_C"]
) . rename( columns = { "DIRECTORIO" : "household"
                    # , "ORDEN" : "household-member" # PITFALL: Always 1.
                      , "P5102":"house,recent-bought"
                      , "P5103":"house,value"
                      , "FEX_C" : "weight" }
) . replace( " ", np.nan )

buildings = buildings[ (~ buildings["house,recent-bought"] . isnull() )
                     & (~ buildings["house,value" ]        . isnull() )
]
buildings["house,value"] = buildings["house,value"].astype('float')
buildings = buildings[ buildings["house,value"] > 100
                       # avoids error codes 98 and 99
] . drop( columns = "house,recent-bought" ) # at this point it's always 1

buildings["house,new"] = 1 # PITFALL: Hack. See how it's used below.
buildings["house,newness-unknown"] = 1


# collect medios and buildings, compute VAT
hps = buildings.append(medios) # house purchases
hps["house,above-vat-threshold"] = (
  hps["house,value"] > (((888.5 + 853.8) * 1e6) / 2)).astype('int')

if common.vat_strategy=="prop_2018_11_29": 
  hps["house,vat-paid"] = (
    0.02 * hps["house,value"] * hps["house,above-vat-threshold"] )
else:
  hps["house,vat-paid"] = (
    0.02 * hps["house,value"] * hps["house,new"] )
