# This file is relevant only to the extent that it records house purchases.

import pandas as pd
import python.vat.raw_enph_input.classes as classes


files = [
  classes.File( "urban capitulo c"
    , "Gastos_diarios_Urbano_-_Capitulo_C.csv"
    , { "NC2_CC_P1"    : "25-broad-categs"
      , "NC2_CC_P2"    : "freq"
      , "NC2_CC_P3_S1" : "value"
    }
    , [ classes.Correction.Create_Constant_Column( "quantity", 1 )
        # TODO : "how-got"
        # TODO : "where-got"
        # TODO : "freq"
    ] )

  , classes.File( "rural capitulo c"
    , "Gastos_semanales_Rural_-_Capitulo_C.csv"
    , { "NC2_CC_P1"    : "25-broad-categs"
      , "NC2_CC_P2"    : "freq"
      , "NC2_CC_P3_S1" : "value"
    }
    , [ classes.Correction.Create_Constant_Column( "quantity", 1 )
        # TODO : "how-got"
        # TODO : "where-got"
        # TODO : "freq"
] ) ]
