import sys
import pandas as pd
import numpy as np

import python.vat.build.classes as classes
import python.vat.build.common as common
import python.vat.build.output_io as oio


subsample = int( sys.argv[1] ) # Reciprocal of subsample size. Valid: 1, 10, 100, 1000.

files = [
  classes.File( "buildings"
    , "Viviendas_y_hogares.csv"
    , { "DIRECTORIO" : "household"
      , "REGION" : "region-1"
      , "DOMINIO" : "region-2"
      , "P8520S1A1" : "estrato"
    }
) ]

buildings = common.collect_files( files, subsample=subsample )
buildings["estrato"] = buildings["estrato"].replace(' ', np.nan)
buildings = buildings.drop( columns = ["file-origin"] )

oio.saveStage(subsample, buildings, '/buildings')
