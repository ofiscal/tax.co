# PITFALL: For the buildings file, subsample is ignored;
# the program uses the full sample always.
# It's a small file, so that doesn't hurt.

import numpy as np

import python.build.classes as cla
import python.common.common as cl
import python.build.output_io as oio


files = [
  cla.File( "buildings"
    , "Viviendas_y_hogares.csv"
    , [ ("DIRECTORIO", 0, "household", 0)
      , ("REGION", 0, "region-1", 0)
      , ("DOMINIO", 0, "region-2", 0)
      , ("P8520S1A1", 0, "estrato", 0)
      , ("P5102", 0, "recently bought this house", 0)
         # 1 » Si 2 » No
      , ("IT",0,"IT",0)
      , ("ICGU",0,"ICGU",0)
      , ("ICMUG",0,"ICMUG",0)
      , ("ICMDUG",0,"ICMDUG",0) # "ingreso corriente monetario disponisble"
      , ("GTUG",0,"GTUG",0)
      , ("GCUG",0,"GCUG",0)
      , ("GCMUG",0,"GCMUG",0) # "gasto corriente monetario"
    ] ) ]

buildings = cl.collect_files( files
                            , subsample=1 ) # see PITFALL above
for c in [ "IT",
           "ICGU",
           "ICMUG",
           "ICMDUG",
           "GTUG",
           "GCUG",
           "GCMUG" ]:
  buildings = ( cla.Correction.Replace_Substring_In_Column(
                  c, ",", "." )
                . correct( buildings ) )

buildings["estrato"] = buildings["estrato"].replace(' ', np.nan)
buildings["recently bought this house"] = (
    buildings["recently bought this house"] == 1 )

oio.saveStage(
  1 # see PITFALL above
  , buildings
  , 'buildings' )
