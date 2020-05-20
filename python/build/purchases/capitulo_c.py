# This describes how to reformat some of the raw ENPH files.

import pandas as pd
from numpy import nan
from python.build.classes import File, Correction, StringCellProperty
import python.common.misc as c


capitulo_c_corrections = [
    Correction.Create_Constant_Column( "quantity", 1 )
  , Correction.Create_Constant_Column( "how-got", 1 )
  , Correction.Create_Constant_Column( "where-got", 1 )
  , Correction.Create_Constant_Column( "coicop", nan )

  # TODO ? Recover and document the logic behind the following corrections.
    , Correction.Drop_Row_If_Column_Equals( "duplicated", 1 )
    , Correction.Drop_Column( "duplicated" )
]

files = [
  File( "urban capitulo c"
    , "Gastos_diarios_Urbano_-_Capitulo_C.csv"
    , c.variables +
      [ ( "NC2_CC_P1"   , {StringCellProperty.NotAString}, "25-broad-categs", 0 )
      , ( "NC2_CC_P2"   , {StringCellProperty.NotAString}, "per month", 0 )
      , ( "NC2_CC_P3_S1", {StringCellProperty.NotAString}, "value", 0 )
      , ( "NC2_CC_P3_S2", {StringCellProperty.NotAString}, "duplicated", 0 ) ]
    , capitulo_c_corrections +
      c.corrections
  )

  , File( "rural capitulo c"
    , "Gastos_semanales_Rural_-_Capitulo_C.csv"
    , # This first list is unlike c.variables in that FEX_C is not a number
      [ ( "DIRECTORIO", {StringCellProperty.NotAString}
          , "household", 0 )
      , ( "FEX_C", {StringCellProperty.Comma, StringCellProperty.Digits}
          , "weight", 0 )
      ] +
      [ ( "NC2_CC_P1"   , {StringCellProperty.NotAString}
          , "25-broad-categs", 0 )
      , ( "NC2_CC_P2"   , {StringCellProperty.NotAString}
          , "per month", 0 )
      , ( "NC2_CC_P3_S1", {StringCellProperty.NotAString}
          , "value", 0 )
      , ( "NC2_CC_P3_S2", {StringCellProperty.NotAString}
          , "duplicated", 0 ) ]
    , capitulo_c_corrections +
      c.corrections
) ]
