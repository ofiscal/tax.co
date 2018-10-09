import numpy as np
import pandas as pd
import python.util as util


beca_col_map = {
#    "P8610S2"    : "grant : edu, beca, in-kind"
#  , "P8612S2"    : "grant : edu, non-beca, in-kind"
#  , "P8610S1"    : "grant : edu, beca"
#  , "P8612S1"    : "grant : edu, non-beca"
  "P6207M1"    : "beca from same school"
  , "P6207M2" : "beca from ICETEX"
  , "P6207M3" : "beca from gov, central"
  , "P6207M4" : "beca from gov, peripheral"
  , "P6207M5" : "beca from another public entity"
  , "P6207M6" : "beca from empresa publica ~familiar"
  , "P6207M7" : "beca from empresa privada ~familiar"
  , "P6207M8" : "beca from other private"
  , "P6207M9" : "beca from organismo internacional"
  , "P6207M10" : "beca from Universidades y ONGs"
  , "P6236" : "non-beca source"
}

df = pd.read_csv( "data/enph-2017/recip-100/" + "Caracteristicas_generales_personas.csv"
                , usecols =  beca_col_map.keys()
    ) . replace( ' ', np.nan
    ) . astype('float'
    ) . rename( columns = beca_col_map )

util.describeWithMissing( df )
