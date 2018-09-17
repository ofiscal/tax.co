# This file is relevant only to the extent that it records house purchases.

import pandas as pd
from numpy import nan
import python.vat.build.classes as classes
import python.vat.build.common as common


files = [
  classes.File( "medios"
    , "Gastos_menos_frecuentes_-_Medio_de_pago.csv"
    , { **common.variables
      , "P10305"   : "new-or-old-house"
      , "P10305S1" : "value"
    }, [ classes.Correction.Create_Constant_Column( "quantity", 1 )
       , classes.Correction.Create_Constant_Column( "coicop", nan ) ]
      + common.corrections
      + common.purchase_corrections
        # TODO : "how-got"
        # TODO : "where-got"
        # TODO : "freq" = in the last year
) ]
