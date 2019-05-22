import pandas as pd
from python.build.classes import File, Correction, StringProperty
import python.common.misc as c


files = [
  File( "articulos"
    , "Gastos_menos_frecuentes_-_Articulos.csv"
    , c.variables +
      [ ( "P10270", {StringProperty.NonNumeric, StringProperty.Digits}
          , "coicop", 0 )
      , ( "FORMA", {StringProperty.NotAString}
          , "how-got", 0 )
      , ( "VALOR", {StringProperty.NotAString}
          , "value", 0 )
      , ( "P10270S2", {StringProperty.NotAString}
          , "where-got", 0 )
      , ( "P10270S3", {StringProperty.NotAString}
          , "freq", 0 ) ]
    , [ Correction.Create_Constant_Column( "quantity", 1 ) ]
      + c.corrections
) ]
