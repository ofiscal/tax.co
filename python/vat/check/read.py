# exec( open( "python/vat/check/read.py" ) . read() )

import sys
import numpy as np
import pandas as pd

import python.util as util
import python.build.legends as legends
import python.build.common as common


enph_subsample = "data/enph-2017/recip-" + str( common.subsample ) + "/"

common_dict = {"DIRECTORIO" : "household", "ORDEN":"member", "FEX_C":"weight"}
inv_common_dict = {v:k for k,v in common_dict.items()}

def myReadCsv( filename, col_dict ):
  inv_col_dict = {v:k for k,v in col_dict.items()}
  return pd.read_csv(
      enph_subsample + filename + ".csv"
    , dtype = { inv_col_dict["coicop"] : 'object'
              , "FEX_C" : 'object' }
    , usecols = list(common_dict.keys()) + list(col_dict.keys())
    ) . rename( columns = {**common_dict, **col_dict} )


if True: # read files
  rur_pers = myReadCsv( "Gastos_personales_Rural"
                      , { "NC2R_CE_P2" : "coicop"
                        , "NC2R_CE_P7" : "value"
                        , "NC2R_CE_P8" : "freq" } )

  rur_pers_fue = myReadCsv(
    "Gastos_personales_Rural_-_Comidas_preparadas_fuera_del_Hogar"
    ,  { "NC2R_CA_P3" : "coicop"
        , "NC2R_CA_P7_S1" : "value"
        , "NC2R_CA_P8_S1" : "freq" } )

  rur_sem = myReadCsv( "Gastos_semanales_Rurales"
                      , { "NC2R_CA_P3" : "coicop"
                        , "NC2R_CA_P7_S1" : "value"
                        , "NC2R_CA_P8_S1" : "freq" } )

  rur_sem_fue = myReadCsv(
    "Gastos_semanales_Rural_-_Comidas_preparadas_fuera_del_hogar"
    , { "NH_CGPRCFH_P1S1" : "coicop"
      , "NH_CGPRCFH_P5" : "value"
      , "NH_CGPRCFH_P6" : "freq" } )

  urb_dia = myReadCsv( "Gastos_diarios_Urbanos"
                    , { "P10250S1A1" : "within-household transfer"
                      , "NH_CGDU_P1" : "coicop"
                      , "NH_CGDU_P8" : "value"
                      , "NH_CGDU_P9" : "freq" }
            )
  urb_dia = urb_dia[ urb_dia["within-household transfer"].isnull()
            ] . drop( columns = ["within-household transfer"] )

  urb_dia_pers = myReadCsv( "Gastos_diarios_personales_Urbano"
                          , { "NC4_CC_P1_1" : "coicop"
                            , "NC4_CC_P5" : "value"
                            , "NC4_CC_P6" : "freq" } )

  urb_pers_fue = myReadCsv(
    "Gastos_personales_Urbano_-_Comidas_preparadas_fuera_del_hogar"
    , { "NH_CGPUCFH_P1_S1" : "coicop"
      , "NH_CGPUCFH_P5" : "value"
      , "NH_CGPUCFH_P6" : "freq" } )

  art = myReadCsv( "Gastos_menos_frecuentes_-_Articulos"
                  , { "P10270" : "coicop"
                    , "VALOR" : "value"
                    , "P10270S3" : "freq" } )

  files_and_names = [ ("rur_pers"     , rur_pers)
                    , ("rur_pers_fue" , rur_pers_fue)
                    , ("rur_sem"      , rur_sem)
                    , ("rur_sem_fue"  , rur_sem_fue)
                    , ("urb_dia"      , urb_dia)
                    , ("urb_dia_pers" , urb_dia_pers)
                    , ("urb_pers_fue" , urb_pers_fue)
                    , ("art"          , art ) ]


if True: # collect
  for name, df in files_and_names: df["file"] = name

  purchases = pd.concat( map( lambda pair: pair[1]
                            , files_and_names ) )


if True: # clean
  purchases.loc[ purchases["coicop"] . str.contains( "( |inv)" )
               , "coicop" ] = np.nan

  purchases["weight"] = purchases["weight"] . str.replace( ",", "." )
  purchases["weight"] = pd.to_numeric( purchases["weight"] )

  purchases["value"] = purchases["value"] . map( str )
  purchases.loc[ purchases["value"].str.contains( "[^0-9\.]")
              , "value" ] = np.nan
  purchases["value"] = pd.to_numeric( purchases["value"] )

  purchases["freq"] = purchases["freq"] . map( str )
  purchases.loc[ purchases["freq"].str.contains( "[^0-9\.]")
              , "freq" ] = np.nan
  purchases["freq"] = pd.to_numeric( purchases["freq"] )


if True: # replace value with montly spending on that item
  purchases["freq"] = purchases["freq"] . replace( legends.freq )
  purchases["value"] = purchases["value"] * purchases["freq"]
