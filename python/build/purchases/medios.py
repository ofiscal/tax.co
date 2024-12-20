# OBSOLETE
##########
# This file would be relevant, because it records house purchases,
# but the VAT is levied only on sales of new homes,
# and newness is not reported in the ENPH,
# so we can't use the data to compute VAT for these purchases.

# PURPOSE
#########
# This describes how to reformat some of the raw ENPH files.

import pandas as pd
from numpy import nan
import python.build.classes as classes
import python.common.misc as c


files = [
  classes.File( "medios"
    , "Gastos_menos_frecuentes_-_Medio_de_pago.csv"
    , c.variables +
      [ ("P10305"  , 0, "new-or-old-house", 0)
      , ("P10305S1" , 0, "value", 0) ]
    , [ classes.Correction.Create_Constant_Column( "quantity", 1 )
      , classes.Correction.Create_Constant_Column( "how-got", 1 )
      , classes.Correction.Create_Constant_Column( "coicop", nan ) ]
      + c.corrections
      # PITFALL: Do not act on these TODO items until this file is in use.
      # TODO (#safe) : "where-got"
      # TODO (#safe) : "per month" = in the last year
) ]
