import pandas as pd
from python.build.classes import File, Correction, VarContent
import python.common.misc as c


files = [
  File( "articulos"
    , "Gastos_menos_frecuentes_-_Articulos.csv"
    , c.variables +
      [ ( "P10270", {VarContent.NonNumeric, VarContent.Digits}
          , "coicop", 0 )
      , ( "FORMA", {VarContent.NotAString}
          , "how-got", 0 )
      , ( "VALOR", {VarContent.NotAString}
          , "value", 0 )
      , ( "P10270S2", {VarContent.NotAString}
          , "where-got", 0 )
      , ( "P10270S3", {VarContent.NotAString}
          , "freq", 0 ) ]
    , [ Correction.Create_Constant_Column( "quantity", 1 ) ]
      + c.corrections
) ]
