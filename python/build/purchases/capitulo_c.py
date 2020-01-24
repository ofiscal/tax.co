import pandas as pd
from numpy import nan
from python.build.classes import File, Correction, StringProperty
import python.common.misc as c


capitulo_c_corrections = [
    Correction.Create_Constant_Column( "quantity", 1 )
  , Correction.Create_Constant_Column( "how-got", 1 )
  , Correction.Create_Constant_Column( "coicop", nan )
  , Correction.Drop_Row_If_Column_Equals( "duplicated", 1 )
  , Correction.Drop_Column( "duplicated" )
]

files = [
  File( "urban capitulo c"
    , "Gastos_diarios_Urbano_-_Capitulo_C.csv"
    , c.variables +
      [ ( "NC2_CC_P1"   , {StringProperty.NotAString}, "25-broad-categs", 0 )
      , ( "NC2_CC_P2"   , {StringProperty.NotAString}, "per month", 0 )
      , ( "NC2_CC_P3_S1", {StringProperty.NotAString}, "value", 0 )
      , ( "NC2_CC_P3_S2", {StringProperty.NotAString}, "duplicated", 0 ) ]
    , capitulo_c_corrections +
      c.corrections
       # TODO (#right) "where-got": assume purchase
  )

  , File( "rural capitulo c"
    , "Gastos_semanales_Rural_-_Capitulo_C.csv"
    , # This first list is unlike c.variables in that FEX_C is not a number
      [ ( "DIRECTORIO", {StringProperty.NotAString}
          , "household", 0 )
      , ( "ORDEN", {StringProperty.NotAString}
          , "household-member", 0 )
      , ( "FEX_C", {StringProperty.Comma, StringProperty.Digits}
          , "weight", 0 )
      ] +
      [ ( "NC2_CC_P1"   , {StringProperty.NotAString}
          , "25-broad-categs", 0 )
      , ( "NC2_CC_P2"   , {StringProperty.NotAString}
          , "per month", 0 )
      , ( "NC2_CC_P3_S1", {StringProperty.NotAString}
          , "value", 0 )
      , ( "NC2_CC_P3_S2", {StringProperty.NotAString}
          , "duplicated", 0 ) ]
    , capitulo_c_corrections +
      c.corrections
      # TODO (#right) : "where-got"
) ]
