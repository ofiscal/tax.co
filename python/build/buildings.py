import sys
import numpy as np

import python.build.classes as classes
import python.common.misc as c
import python.common.cl_args as cl
import python.build.output_io as oio


# PITFALL: Except for the save at the end, subsample is ignored;
# the program uses the full sample always,
# because it's a small file, and merged with others.
# If it was subsampled at 1/n, and the other one was as well,
# then their merge would be subsampled at roughly 1/n^2.

files = [
  classes.File( "buildings"
    , "Viviendas_y_hogares.csv"
    , [ ("DIRECTORIO", 0, "household", 0)
      , ("REGION", 0, "region-1", 0)
      , ("DOMINIO", 0, "region-2", 0)
      , ("P8520S1A1", 0, "estrato", 0) ]
) ]

buildings = cl.collect_files( files
                            , subsample=1 ) # see PITFALL above
buildings["estrato"] = buildings["estrato"].replace(' ', np.nan)

oio.saveStage(
  cl.subsample # see PITFALL above
  , buildings
  , 'buildings' )
