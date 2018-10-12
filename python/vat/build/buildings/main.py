import pandas as pd
from numpy import nan
import python.vat.build.classes as classes
import python.vat.build.common as common


files = [
  classes.File( "buildings"
    , "Viviendas_y_hogares.csv"
    , { "DIRECTORIO" : "household"
      , "REGION" : "region-1"
      , "DOMINIO" : "region-2"
      , "P8520S1A1" : "estrato"
    }
) ]
