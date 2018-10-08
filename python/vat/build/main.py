import pandas as pd
import numpy as np

import python.vat.build.common as common

# input files
import python.vat.build.buildings.files as bldg
from python.vat.build.people.main import people
from python.vat.build.purchases.main import purchases


if True: # buildings
  buildings = common.collect_files( bldg.files )
  buildings["estrato"] = buildings["estrato"].replace(' ', np.nan)
  buildings = buildings.drop( columns = ["file-origin"] )


if True: # VAT dictionaries
  vat_cap_c = pd.read_csv( "data/vat/" + "vat-for-capitulo-c.csv"
                         , encoding = "latin1"
              ) . rename( columns = { "CODE" : "25-broad-categs"
                                    , "DESCRIPTION" : "description"
              } )
  vat_coicop = pd.read_csv( "data/vat/" + "vat-by-coicop.csv"
                          , sep = ";"
                          , encoding = "latin1" )


if True: # add VAT to purchases
  purchases = purchases.merge( vat_coicop, how = "left", on="coicop" )
  purchases = purchases.merge( vat_cap_c, how = "left", on="25-broad-categs" )
