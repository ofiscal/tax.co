import pandas as pd
import python.build.classes as classes
import python.common.misc as c

files = [
  classes.File( "articulos"
    , "Gastos_menos_frecuentes_-_Articulos.csv"
    , c.variables +
      [ ( "P10270", 0, "coicop", 0 )
      , ( "FORMA", 0, "how-got", 0 )
      , ( "VALOR", 0, "value", 0 )
      , ( "P10270S2", 0, "where-got", 0 )
      , ( "P10270S3", 0, "freq", 0 ) ]
    , [ classes.Correction.Create_Constant_Column( "quantity", 1 ) ]
      + c.corrections
) ]
