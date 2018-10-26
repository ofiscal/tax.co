# This file would be relevant, because it records house purchases,
# except that the VAT is charged only on sales of new homes, which
# quality is not reported in the ENPH.

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
       , classes.Correction.Create_Constant_Column( "how-got", 1 )
       , classes.Correction.Create_Constant_Column( "coicop", nan ) ]
      + common.corrections
        # todo : "where-got"
        # todo : "freq" = in the last year
) ]
