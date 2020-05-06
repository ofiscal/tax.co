# This describes how to reformat one of the raw ENPH files.

import pandas as pd
from python.build.classes import File, Correction, StringCellProperty
import python.common.misc as c


files = [
  File( "articulos"
    , "Gastos_menos_frecuentes_-_Articulos.csv"
    , c.variables +
      [ ( "P10270", {StringCellProperty.NonNumeric, StringCellProperty.Digits}
          , "coicop", 0 )
      , ( "FORMA", {StringCellProperty.NotAString}
          , "how-got", 0 )
      , ( "VALOR", {StringCellProperty.NotAString}
          , "value", 0 )
      , ( "P10270S2", {StringCellProperty.NotAString}
          , "where-got", 0 )
      , ( "P10270S3", {StringCellProperty.NotAString}
          , "per month", 0 ) ]
    , [ Correction.Create_Constant_Column( "quantity", 1 ) ]
      + c.corrections
) ]
