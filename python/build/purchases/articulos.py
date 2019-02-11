import pandas as pd
import python.build.classes as classes
import python.common.misc as c

files = [
  classes.File( "articulos"
    , "Gastos_menos_frecuentes_-_Articulos.csv"
    , { **c.variables
      , "P10270" : "coicop"
      , "FORMA" : "how-got"
      , "VALOR" : "value"
      , "P10270S2" : "where-got"
      , "P10270S3" : "freq"
    }, [ classes.Correction.Create_Constant_Column( "quantity", 1 ) ]
      + c.corrections
) ]
