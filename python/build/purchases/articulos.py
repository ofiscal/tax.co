import pandas as pd
import python.build.classes as cla
import python.common.misc as c
import python.build.input_formats as ifo


files = [
  cla.File( "articulos"
    , "Gastos_menos_frecuentes_-_Articulos.csv"
    , c.variables +
      [ ( "P10270", {ifo.VarContent.NonNumeric, ifo.VarContent.Digits}
          , "coicop", 0 )
      , ( "FORMA", {ifo.VarContent.NotAString}
          , "how-got", 0 )
      , ( "VALOR", {ifo.VarContent.NotAString}
          , "value", 0 )
      , ( "P10270S2", {ifo.VarContent.NotAString}
          , "where-got", 0 )
      , ( "P10270S3", {ifo.VarContent.NotAString}
          , "freq", 0 ) ]
    , [ cla.Correction.Create_Constant_Column( "quantity", 1 ) ]
      + c.corrections
) ]
