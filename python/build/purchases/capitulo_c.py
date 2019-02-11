import pandas as pd
from numpy import nan
import python.build.classes as classes
import python.common.misc as c


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
    , { **c.variables
      , "NC2_CC_P1"    : "25-broad-categs"
      , "NC2_CC_P2"    : "freq"
      , "NC2_CC_P3_S1" : "value"
      , "NC2_CC_P3_S2" : "duplicated"
    },  capitulo_c_corrections
      + c.corrections
        # TODO (#right) "where-got": assume purchase
  )

  , classes.File( "rural capitulo c"
    , "Gastos_semanales_Rural_-_Capitulo_C.csv"
    , { **c.variables
      , "NC2_CC_P1"    : "25-broad-categs"
      , "NC2_CC_P2"    : "freq"
      , "NC2_CC_P3_S1" : "value"
      , "NC2_CC_P3_S2" : "duplicated"
    }, [ classes.Correction.Replace_In_Column( "duplicated"
                                              , { ' ' : nan
                                                , "nan" : nan
                                                , '1' : 1
                                                , '2' : 2} )
      ] + capitulo_c_corrections
        + c.corrections
        # TODO (#right) : "where-got"
) ]
