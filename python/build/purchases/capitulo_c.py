import pandas as pd
from numpy import nan
import python.build.classes as classes
import python.common.misc as c
import python.build.input_formats as ifo


capitulo_c_corrections = [
    classes.Correction.Create_Constant_Column( "quantity", 1 )
  , classes.Correction.Create_Constant_Column( "how-got", 1 )
  , classes.Correction.Create_Constant_Column( "coicop", nan )
  , classes.Correction.Drop_Row_If_Column_Equals( "duplicated", 1 )
  , classes.Correction.Drop_Column( "duplicated" )
]

files = [
  classes.File( "urban capitulo c"
    , "Gastos_diarios_Urbano_-_Capitulo_C.csv"
    , c.variables +
      [ ( "NC2_CC_P1"   , {ifo.VarContent.NotAString}, "25-broad-categs", 0 )
      , ( "NC2_CC_P2"   , {ifo.VarContent.NotAString}, "freq", 0 )
      , ( "NC2_CC_P3_S1", {ifo.VarContent.NotAString}, "value", 0 )
      , ( "NC2_CC_P3_S2", {ifo.VarContent.NotAString}, "duplicated", 0 ) ]
    , capitulo_c_corrections +
      c.corrections
       # TODO (#right) "where-got": assume purchase
  )

  , classes.File( "rural capitulo c"
    , "Gastos_semanales_Rural_-_Capitulo_C.csv"
    , # This first lis is unlike c.variables in that FEX_C is not a number
      [ ( "DIRECTORIO", {ifo.VarContent.NotAString}
          , "household", 0 )
      , ( "ORDEN", {ifo.VarContent.NotAString}
          , "household-member", 0 )
      , ( "FEX_C", {ifo.VarContent.Comma, ifo.VarContent.Digits}
          , "weight", 0 )
      ] +
      [ ( "NC2_CC_P1"   , {ifo.VarContent.NotAString}
          , "25-broad-categs", 0 )
      , ( "NC2_CC_P2"   , {ifo.VarContent.NotAString}
          , "freq", 0 )
      , ( "NC2_CC_P3_S1", {ifo.VarContent.NotAString}
          , "value", 0 )
      , ( "NC2_CC_P3_S2", {ifo.VarContent.NotAString}
          , "duplicated", 0 ) ]
    , capitulo_c_corrections +
      c.corrections
      # TODO (#right) : "where-got"
) ]
