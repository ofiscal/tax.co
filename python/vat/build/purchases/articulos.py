import pandas as pd
import python.vat.build.classes as classes
import python.vat.build.common as common

files = [
  classes.File( "articulos"
    , "Gastos_menos_frecuentes_-_Articulos.csv"
    , { **common.variables
      , "P10270" : "coicop"
      , "FORMA" : "how-got"
      , "VALOR" : "value"
      , "P10270S2" : "where-got"
      , "P10270S3" : "freq"
    }, common.corrections
      + common.purchase_corrections
      + [ classes.Correction.Create_Constant_Column( "quantity", 1 )
] ) ]
