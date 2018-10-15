import pandas as pd
import numpy as np

import python.vat.build.classes as classes
import python.vat.build.common as common
import python.vat.build.output_io as oio


subsample = 1 # use the full sample always, because it's a small file, and merged with others
  # If it was subsampled at 1/n, and the other one was as well,
  # then their merge would be subsampled at 1/n^2.

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
