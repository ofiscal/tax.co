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

       # PITFALL: Although the following are peso-denominated, they are constant within household.
       # Along with the other Viviendas_y_hogares data, they are merged into people_2_buildings.
       # That might seem wrong, but fear not,
       # because in households_2_purchases, their within-family max is taken, rather than their sum (which is how the other peso-valued variables are aggregated).
      , ("IT",0,"IT",0)
      , ("ICGU",0,"IC",0)
      , ("ICMUG",0,"ICM",0)
      , ("ICMDUG",0,"ICMD",0) # "ingreso corriente monetario disponisble"
      , ("GTUG",0,"GT",0)
      , ("GCUG",0,"GC",0)
      , ("GCMUG",0,"GCM",0) # "gasto corriente monetario"
    ] ) ]

buildings = cl.collect_files( files
                            , subsample=1 ) # see PITFALL above
for c in [ "IT",
           "IC",
           "ICM",
           "ICMD",
           "GT",
           "GC",
           "GCM" ]:
  buildings = ( cla.Correction.Replace_Substring_In_Column(
                  c, ",", "." )
                . correct( buildings ) )

if True: # estrato is strange
    # It includes undocumented values 0 and 9.
    # 0 might mean "renter":
    # https://www.eltiempo.com/archivo/documento/MAM-1757051
    # I'm assuming 9 is some kind of error code.
    buildings["estrato"] = buildings["estrato"].replace(9, np.nan)

buildings["recently bought this house"] = (
    buildings["recently bought this house"] == 1 )

oio.saveStage(
  1 # see PITFALL above
  , buildings
  , 'buildings' )
