# This file is relevant only to the extent that it records house purchases.

import pandas as pd
import python.vat.build.classes as classes


files = [
  classes.File( "medios"
    , "Gastos_menos_frecuentes_-_Medio_de_pago.csv"
    , { "P10305"   : "new-or-old-house"
      , "P10305S1" : "value"
    }
    , [ classes.Correction.Create_Constant_Column( "quantity", 1 )
        # TODO : "coicop"
        # TODO : "how-got"
        # TODO : "where-got"
        # TODO : "freq" = in the last year
] ) ]
