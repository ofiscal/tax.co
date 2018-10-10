import numpy as np
import pandas as pd
import python.util as util
import re


#### considering all variables ####
beca_col_map = {
    "P8610S2"  : "grant : edu, beca, in-kind"
  , "P8612S2"  : "grant : edu, non-beca, in-kind"
  , "P8610S1"  : "grant : edu, beca"
  , "P8612S1"  : "grant : edu, non-beca"
  , "P6207M1"  : "beca from same school"
  , "P6207M2"  : "beca from ICETEX"
  , "P6207M3"  : "beca from gov, central"
  , "P6207M4"  : "beca from gov, peripheral"
  , "P6207M5"  : "beca from another public entity"
  , "P6207M6"  : "beca from empresa publica ~familiar"
  , "P6207M7"  : "beca from empresa privada ~familiar"
  , "P6207M8"  : "beca from other private"
  , "P6207M9"  : "beca from organismo internacional"
  , "P6207M10" : "beca from Universidades y ONGs"
  , "P6236"    : "non-beca source" # PITFALL : This is a list, encoded as  a string
}

df = pd.read_csv( "data/enph-2017/recip-1/" + "Caracteristicas_generales_personas.csv"
                , usecols =  beca_col_map.keys()
    ) . replace( ' ', np.nan
    ) . rename( columns = beca_col_map )
should_be_numbers = df.filter( regex = "^((?!beca source).)*$" )
should_be_numbers = should_be_numbers . astype( 'float' )

df.sum()

util.describeWithMissing( df )

len( df["non-beca source"].unique() )
for v in sorted( df["non-beca source"].astype('str').unique() ): print(v)
  # Eyeballing the results of that, 10 of the 24 observations received from maybe* outside the government,
  # while almost all of them received from the government. Therefore I'm calling this government income.
  # * maybe because "from a university" is ambiguous -- the university might be public



#### considering only government sources ####

beca_col_map = {
    "P6207M2" : "beca from ICETEX"
  , "P6207M3" : "beca from gov, central"
  , "P6207M4" : "beca from gov, peripheral"
  , "P6207M5" : "beca from another public entity"
  , "P6207M6" : "beca from empresa publica ~familiar"
}

ddf = pd.read_csv( "data/enph-2017/recip-1/" + "Caracteristicas_generales_personas.csv"
                , usecols =  beca_col_map.keys()
    ) . replace( ' ', np.nan
    ) . rename( columns = beca_col_map )
df = ( df
     ) . astype( 'float' )

df.sum()


## like above somewhere, but only the "where did it come from" boolean columns
beca_col_map = {
    "P6207M1" : "beca from same school"
  , "P6207M2" : "beca from ICETEX"
  , "P6207M3" : "beca from gov, central"
  , "P6207M4" : "beca from gov, peripheral"
  , "P6207M5" : "beca from another public entity"
  , "P6207M6" : "beca from empresa publica ~familiar"
  , "P6207M7" : "beca from empresa privada ~familiar"
  , "P6207M8" : "beca from other private"
  , "P6207M9" : "beca from organismo internacional"
  , "P6207M10" : "beca from Universidades y ONGs"
}

df = pd.read_csv( "data/enph-2017/recip-1/" + "Caracteristicas_generales_personas.csv"
                , usecols =  beca_col_map.keys()
    ) . replace( ' ', np.nan
    ) . rename( columns = beca_col_map )
df = df . astype( 'float' )

df["sources"] = df.sum(axis=1)
len( df[ df["sources"] > 1 ] )
len( df[ df["sources"] > 0 ] )
